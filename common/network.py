import socket


class ByteStream:
    def __init__(self):
        self.buf = bytearray()

    def push(self, data):
        self.buf.extend(data)

    def peek(self, size):
        return self.buf[:size]

    def pop(self, size):
        data = self.peek(size)
        del self.buf[:size]
        return data

    def __len__(self):
        return len(self.buf)


class NetworkConnection:
    def __init__(self, socket):
        self.recv_queue = ByteStream()
        self.send_queue = ByteStream()
        self.socket = socket

    def _process_send(self):
        stream_sz = len(self.send_queue)
        if stream_sz != 0:
            try:
                advance = self.socket.send(self.send_queue.peek(stream_sz))
                self.send_queue.pop(advance)
            except BlockingIOError:
                pass

    def _process_recv(self):
        try:
            temp = self.socket.recv(1024)
            self.recv_queue.push(temp)
        except BlockingIOError:
            pass

    def process(self):
        self._process_send()
        self._process_recv()

    def send(self, data):
        self.send_queue.push(int.to_bytes(len(data), 2))
        self.send_queue.push(data)

    def recv(self):
        if len(self.recv_queue) < 2:
            return None
        size = int.from_bytes(self.recv_queue.peek(2))
        if len(self.recv_queue) < 2 + size:
            return None
        self.recv_queue.pop(2)
        return self.recv_queue.pop(size)
