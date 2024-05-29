# import asyncio
# from aioquic.asyncio.protocol import QuicConnectionProtocol, QuicServerProtocol
# from aioquic.asyncio import connect, serve
# from aioquic.quic.configuration import QuicConfiguration
# from aioquic.quic.events import HandshakeCompleted, StreamDataReceived
# from aioquic.quic.logger import QuicFileLogger
# from aioquic.tls import SessionTicketFetcher, SessionTicketStore
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # QUIC client protocol
# class EchoClientProtocol(QuicConnectionProtocol):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.response = None

#     def quic_event_received(self, event):
#         if isinstance(event, StreamDataReceived):
#             self.response = event.data

# # QUIC server protocol
# class EchoServerProtocol(QuicServerProtocol):
#     def quic_event_received(self, event):
#         if isinstance(event, HandshakeCompleted):
#             logger.info("Handshake completed with %s", self._quic._peer_addr)
#         elif isinstance(event, StreamDataReceived):
#             self._quic.send_stream_data(event.stream_id, event.data)

# # Build client QUIC configuration
# def build_client_quic_config(cert_file):
#     configuration = QuicConfiguration(is_client=True)
#     configuration.load_verify_locations(cert_file)
#     return configuration

# # Build server QUIC configuration
# def build_server_quic_config(cert_file, key_file):
#     configuration = QuicConfiguration(is_client=False)
#     configuration.load_cert_chain(cert_file, key_file)
#     return configuration

# # Run the QUIC client
# async def run_client(server_address, server_port, config):
#     async with connect(server_address, server_port, configuration=config, create_protocol=EchoClientProtocol) as protocol:
#         await asyncio.sleep(1)  # give some time for connection setup
#         logger.info("Connected to the server")
#         return protocol

# # Run the QUIC server
# async def run_server(listen_address, listen_port, config):
#     await serve(
#         listen_address,
#         listen_port,
#         configuration=config,
#         create_protocol=EchoServerProtocol,
#     )

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser(description="Run QUIC client/server")
#     subparsers = parser.add_subparsers(dest="mode", help="Mode to run the application in", required=True)

#     client_parser = subparsers.add_parser("client")
#     client_parser.add_argument("-s", "--server", default="localhost", help="Host to connect to")
#     client_parser.add_argument("-p", "--port", type=int, default=4433, help="Port to connect to")
#     client_parser.add_argument("-c", "--cert-file", default="./cert/cert.prem", help="Certificate file (for self signed certs)")

#     server_parser = subparsers.add_parser("server")
#     server_parser.add_argument("-c", "--cert-file", default="./cert/cert.pem", help="Certificate file (for self signed certs)")
#     server_parser.add_argument("-k", "--key-file", default="./cert/key.pem", help="Key file (for self signed certs)")
#     server_parser.add_argument("-l", "--listen", default="localhost", help="Address to listen on")
#     server_parser.add_argument("-p", "--port", type=int, default=4433, help="Port to listen on")

#     args = parser.parse_args()

#     if args.mode == "client":
#         config = build_client_quic_config(args.cert_file)
#         asyncio.run(run_client(args.server, args.port, config))
#     elif args.mode == "server":
#         config = build_server_quic_config(args.cert_file, args.key_file)
#         asyncio.run(run_server(args.listen, args.port, config))


from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio import connect

def build_server_quic_config(cert_file, key_file):
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(cert_file, key_file)
    return configuration

def build_client_quic_config(cert_file):
    configuration = QuicConfiguration(is_client=True)
    configuration.load_verify_locations(cert_file)
    return configuration

async def run_client(server_address, server_port, configuration):
    async with connect(server_address, server_port, configuration=configuration) as protocol:
        await protocol.wait_connected()

async def run_server(listen_address, listen_port, configuration):
    from aioquic.asyncio import serve
    await serve(listen_address, listen_port, configuration=configuration, create_protocol=QuicConnectionProtocol)
