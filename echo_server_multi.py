import socket
import sys
import select
import queue

# Constant for number of bytes to read from message
BYTES = 1024

def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    # Create a TCP socket with IPv4 addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    # Set to non-blocking mode
    sock.setblocking(0)
    # In case the program thinks the port is already in use, the line below will
    # reuse a local socket that's waiting to time out (in TIME_WAIT state)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Bind socket to address and listen for connections
    sock.bind(address)
    # Set to accept up to two simultaneous connections
    sock.listen(2)

    # Sockets for reading
    inputs = [sock]
    # Sockets for writing
    outputs = []
    # Outgoing message queues
    message_queues = {}

    # Main loop
    while inputs:
        print('waiting for a connection', file=log_buffer)
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        # Inputs
        for s in readable:
            if s is sock: # If s is main socket, connect
                conn, addr = s.accept()
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                conn.setblocking(0)
                inputs.append(conn)
                # Add connection to queue
                message_queues[conn] = queue.Queue()
            else: # If connection already established, check for data
                data = s.recv(BYTES)
                if data:
                    print('received "{0}" from {1}'.format(data.decode('utf8'), s.getpeername()))
                    message_queues[s].put(data)
                    # Add output channel for response
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # If no data, assume connection closed
                    print('no data received, closing connection')
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    # Remove from queue
                    del message_queues[s]
        # Outputs
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                print('output queue for {} is empty'.format(s.getpeername()))
                outputs.remove(s)
            else:
                print('sent "{0}" from {1}'.format(next_msg, s.getpeername()))
                s.send(next_msg)
        # Exceptional Conditions
        for s in exceptional:
            print('handling exceptional condition for {}'.formnat(s.getpeername()))
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            # Remove from queue
            del message_queues[s]

if __name__ == '__main__':
    server()
    sys.exit(0)
