from connection import MiniTCPConnection

def main():
    # 클라이언트가 접속할 서버 주소와 포트
    server_ip = "127.0.0.1"
    server_port = 10001
    conn = MiniTCPConnection(role="client", local_port=0, remote_addr=(server_ip, server_port))
    conn.connect()
    conn.send(b"Hello from client!")
    response = conn.recv()
    print("Received:", response)
    conn.close()

if __name__ == "__main__":
    main()
