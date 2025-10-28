import struct

SYN = 0x02
ACK = 0x10
FIN = 0x01

class MiniTCPPacket:
    HEADER_FORMAT = "!HHIIHHHH"  # src_port, dst_port, seq, ack, flags, window, unused1, unused2
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, src_port, dst_port, seq_num, ack_num, flags, window, payload=b""):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.flags = flags
        self.window = window
        self.payload = payload

    def to_bytes(self):
        header = struct.pack(
            self.HEADER_FORMAT,
            self.src_port,
            self.dst_port,
            self.seq_num,
            self.ack_num,
            self.flags,
            self.window,
            0,  # unused
            0   # unused
        )
        return header + self.payload

    @classmethod
    def from_bytes(cls, data):
        header = data[:cls.HEADER_SIZE]
        payload = data[cls.HEADER_SIZE:]
        fields = struct.unpack(cls.HEADER_FORMAT, header)
        src_port, dst_port, seq_num, ack_num, flags, window, _, _ = fields
        return cls(src_port, dst_port, seq_num, ack_num, flags, window, payload)
