import socket, ssl

HOST, PORT = "", 12345
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile="server.crt", keyfile="server.key")  # self-signed

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((HOST, PORT))
lsock.listen(5)
print("Start TLS echo-reverse server", PORT)

while True:
    conn, addr = lsock.accept()
    with ctx.wrap_socket(conn, server_side=True) as ssock:
        data = ssock.recv(1500)
        if not data:
            continue
        ssock.sendall(data[::-1])
