from connection import MiniTCPConnection

def main():
    # 서버 측 포트 설정
    listen_port = 10001
    conn = MiniTCPConnection(role="server", local_port=listen_port)
    conn.accept()
    data = conn.recv()
    print("Received:", data)
    conn.send(b"Hello from server!")
    conn.close()

if __name__ == "__main__":
    main()
