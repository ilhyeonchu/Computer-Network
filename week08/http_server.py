import socket, os

HOST, PORT = "", 8888

def send_response(conn, status, ctype, body_bytes):
    reason = "OK" if status == 200 else "Not Found"
    header = (
        f"HTTP/1.1 {status} {reason}\r\n"
        f"Server: tiny-server\r\n"
        f"Connection: close\r\n"
        f"Content-Type: {ctype}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"\r\n"
    ).encode("utf-8")
    conn.sendall(header + body_bytes)

def read_file_bytes(path):
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as f:
        return f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Start server: http://127.0.0.1:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(2048)
            if not data:
                continue

            line = data.split(b"\r\n", 1)[0].decode("utf-8", "replace")
            parts = line.split(" ")
            if len(parts) < 2:
                continue
            method, path = parts[0], parts[1]
            print("REQ:", method, path, "from", addr)

            if path == "/":
                body = read_file_bytes("index.html") or b"<h1>index.html is missing</h1>"
                send_response(conn, 200, "text/html; charset=utf-8", body)

            elif path == "/style.css":
                body = read_file_bytes("style.css") or b"/* style.css is missing */"
                send_response(conn, 200, "text/css; charset=utf-8", body)

            elif path == "/main.js":
                body = read_file_bytes("main.js") or b"// main.js is missing"
                send_response(conn, 200, "text/javascript; charset=utf-8", body)

            elif path == "/image.jpg":
                body = read_file_bytes("image.jpg") or b""
                if body:
                    send_response(conn, 200, "image/jpeg", body)
                else:
                    send_response(conn, 404, "text/html; charset=utf-8", b"<h1>404</h1>")

            else:
                send_response(conn, 404, "text/html; charset=utf-8", b"<h1>404</h1>")
