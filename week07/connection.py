import socket
import time

from packet import MiniTCPPacket, SYN, ACK, FIN
from congestion import CongestionControl
from graph import plot_cwnd

# 타임아웃 설정 (초 단위)
TIMEOUT = 1.0

class MiniTCPConnection:
    def __init__(self, role="client", local_port=10000, remote_addr=("127.0.0.1", 10001)):
        self.role = role
        self.local_port = local_port
        self.peer = remote_addr  # (ip, port)
        self.seq = 0
        self.ack = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bind_addr = ("", self.local_port if role == "server" else 0)
        self.sock.bind(bind_addr)
        self.sock.settimeout(TIMEOUT)
        # 혼잡 제어 객체
        self.cc = CongestionControl()
        # cwnd 기록 (RTT, cwnd)
        self.cwnd_history = []
        self.start_time = time.time()

    def send_packet(self, flags, payload=b""):
        pkt = MiniTCPPacket(
            src_port=self.sock.getsockname()[1],
            dst_port=self.peer[1],
            seq_num=self.seq,
            ack_num=self.ack,
            flags=flags,
            window=1024,
            payload=payload
        )
        data = pkt.to_bytes()
        # self.sock.______(____, ________)
        # udp 기반 송신, 직렬화한 패킷 데이터를 상대 주소로 전송

    def recv_packet(self):
        data, addr = self.sock.recvfrom(4096)
        # pkt = ______._______(data)
        # 수신한 raw 데이터를 parsing하여 저장
        return pkt, addr
     

    def connect(self):
        # 클라이언트 쪽 연결 절차
        start_time = time.time()
        self.send_packet(SYN)
        while True:
            try:
                # _____, _____ = self.________()
                # 서버로부터 무언가를 수신하려고 함
            except socket.timeout:
                print("Timeout waiting for SYN+ACK, resend SYN")
                self.send_packet(SYN)
                continue
            # SYN + ACK 응답인지 확인
            if pkt.flags & SYN and pkt.flags & ACK:
                handshake_rtt = time.time() - start_time
                # self.ack = ___.______ + 1
                # 서버가 보낸 무언가+1을 ack 번호로 설정
                # self._______(___)
                # 서버에게 무언가를 어떻게 하여 3-way handshake 과정 완료
                break
        # 초기 cwnd 기록
        self.cwnd_history.append((handshake_rtt, self.cc.cwnd))

    def accept(self):
        # 서버 쪽 연결 절차
        while True:
            try:
                pkt, addr = self.recv_packet()
            except socket.timeout:
                continue
            if pkt.flags & SYN:
                self.peer = (addr[0], pkt.src_port)
                # self.ack = ____._____ + 1
                # 클라이언트의 무언가+1을 ack번호로 설정
                # self.send_packet(___ | ____)
                # TCP 연결에 필요한 무언가 2가지를 전송
                start_time = time.time()
                break
        # 기다려서 클라이언트의 ACK 받기
        while True:
            try:
                pkt2, _ = self.recv_packet() 
            except socket.timeout:
                continue
            if pkt2.flags & ACK:
                handshake_rtt = time.time() - start_time
                break
        # 기록 시작 (핸드셰이크 RTT 사용)
        self.cwnd_history.append((handshake_rtt, self.cc.cwnd))

    def send(self, data: bytes):
        # 단순화: 한 번에 전체 데이터 전송
        # 실제 운용 시에는 데이터를 조각 내서 여러 패킷 보내도록 구현 가능
        # 혼잡 제어: 현재 cwnd 허용 범위 이하 수만큼 보내야 하지만, 간단화함
        start_time = time.time()  # RTT 측정 시작
        self.send_packet(ACK, data)
        self.seq += len(data)
        # send 후 ACK 기대 -> wait for ACK
        try:
            pkt, _ = self.recv_packet()
            if pkt.flags & ACK:
                rtt = time.time() - start_time  # RTT 계산
                # ACK 받은 경우에 혼잡 제어를 위한 처리 함수 실행
                # self.cc.______()
                self.cwnd_history.append((rtt, self.cc.cwnd))
        except socket.timeout:
            print("ACK timeout")
            # ACK를 못받았을 경우에 혼잡 제어를 위해 함수 실행
            # self.cc._______()
            self.cwnd_history.append((TIMEOUT, self.cc.cwnd))

    def recv(self):
        while True:
            try:
                pkt, _ = self.recv_packet()
            except socket.timeout:
                continue
            # 수신된 패킷이 데이터 포함이면 처리
            # ACK 응답 필요하면 send ACK
            data = pkt.payload
            # ACK 응답
            self.ack = pkt.seq_num + len(pkt.payload)
            # 수신받은 이후에 수신받았다는 무언가의 행동을 함
            # self._______(____)
            return data

    def close(self):
        # ___ 전송 
        # self.send_packet(___)
        # (선택) ACK 응답 기다리기 생략 가능
        # 종료 지점에서 시각화 호출
        plot_cwnd(self.cwnd_history)
        self.sock.close()
