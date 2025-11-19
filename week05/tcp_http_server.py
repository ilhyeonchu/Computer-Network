import os
import socket

HOST = ""
PORT = 8080

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpg",
    ".jpeg": "image/jpeg",
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("Start server")
    while True:
        try:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1500)
                ptr = data.find("\r\n".encode("utf-8"))
                header = data[:ptr]
                left = data[ptr:]
                request = header.decode("utf-8")
                method, path, protocol = request.split(" ")
                print(f"Received: {method} {path} {protocol}")
                if not data:
                    break
                if path == "/":
                    path = "/index.html"
                path = f".{path}"
                if not os.path.exists(path):
                    body = "".encode("utf-8")
                    header = "HTTP/1.1 404 Not Found\r\n"
                    header = f"{header}Server: Our server\r\n"
                    header = f"{header}Connection: close\r\n"
                    header = f"{header}Content-Type: text/html;charset=utf-8\r\n"
                    header = f"{header}Content-Length: {len(body)}\r\n"
                    header = header.encode("utf-8")
                else:
                    ext = os.path.splitext(path)[1].lower()
                    content_type = MIME_TYPES.get(ext, "application/octet-stream")
                    with open(path, "rb") as f:
                        body = f.read()
                    header = "HTTP/1.1 200 OK\r\n"
                    header = f"{header}Server: Our server\r\n"
                    header = f"{header}Connection: close\r\n"
                    header = f"{header}Content-Type: {content_type}\r\n"
                    header = f"{header}Content-Length: {len(body)}\r\n"
                    header = f"{header}\r\n"
                    header = header.encode("utf-8")
                response = header + body
                conn.sendall(response)
        except KeyboardInterrupt:
            print("shutdown server")
            break
