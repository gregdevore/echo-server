import socket
import sys
import traceback

# Constant for number of bytes to read from messages
BYTES = 1024

def client(log_buffer=sys.stderr):
    msgs = ['This is a test message',
            'This is another test message',
            'Here comes a third message']
    server_address = ('localhost', 10000)
    # Instantiate two TCP sockets with IPv4 Addressing
    socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP),
            socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)]
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    # Connect sockets to the server
    for s in socks:
        s.connect(server_address)
    # Iterate over messages to send/receive
    for msg in msgs:
        # Use both sockets to send messages
        for s in socks:
            print('{0} sending "{1}"'.format(s.getsockname(),msg), file=log_buffer)
            s.send(msg.encode('utf8'))
        # Use both sockets to reveive messages
        for s in socks:
            data = s.recv(BYTES)
            print('{0} received "{1}"'.format(s.getsockname(),data.decode('utf8')), file=log_buffer)
            if not data:
                print('closing socket {}'.format(s.getsockname()), file=log_buffer)
                s.close()

if __name__ == '__main__':
    client()
