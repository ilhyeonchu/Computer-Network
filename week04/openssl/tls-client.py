import argparse
import socket
import ssl

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server", required=True)
ap.add_argument("-p", "--port", type=int, default=12345)
args = ap.parse_args()

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
with ctx.wrap_socket(
    socket.create_connection((args.server, args.port)), server_hostname=args.server
) as ssock:
    print("cipher:", ssock.cipher())  # TLS 성립 확인
    ssock.sendall(b"hello")
    print(ssock.recv(1500))
