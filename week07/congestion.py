class CongestionControl:
    def __init__(self):
        self.cwnd = 1.0
        self.ssthresh = 64

    def on_ack(self):
        # 호출 시 ACK이 정상적으로 도착했을 때
        if self.cwnd < self.ssthresh:
            # Slow Start: 매 ACK마다 1씩 증가 (RTT당 약 2배 효과)
            self.cwnd += 1.0
        else:
            # Congestion Avoidance: 매 RTT마다 1씩 증가하도록
            self.cwnd += 1.0 / self.cwnd

    def on_loss(self):
        # 손실이 감지되었을 때 호출
        self.ssthresh = max(self.cwnd / 2, 1.0)
        self.cwnd = 1.0