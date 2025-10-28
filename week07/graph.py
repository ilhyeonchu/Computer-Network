import matplotlib.pyplot as plt

def plot_cwnd(cwnd_history):
    Student_no = ""
    
    # 데이터 분리: RTT와 cwnd 값들을 추출
    rtts = []
    cwnds = []
    
    for item in cwnd_history:
        if isinstance(item, tuple) and len(item) == 2:
            # (rtt, cwnd) 튜플인 경우
            rtts.append(item[0])
            cwnds.append(item[1])
        elif isinstance(item, (int, float)):
            # 단순 cwnd 값인 경우 (초기값들) - RTT를 0으로 가정
            rtts.append(len(rtts) * 0.1)  # 가상의 RTT 값
            cwnds.append(item)
    
    # RTT 순서로 정렬 (일반적인 관계 표현을 위해)
    if rtts and cwnds:
        sorted_data = sorted(zip(rtts, cwnds))
        rtts, cwnds = zip(*sorted_data)
    
    plt.plot(rtts, cwnds, marker='o')
    plt.title(f"Congestion Window Over Time_{Student_no}")
    plt.xlabel("RTT")
    plt.ylabel("cwnd")
    plt.grid(True)
    plt.show()