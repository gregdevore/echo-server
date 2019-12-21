import socket
import sys
import traceback

# Constant for number of bytes to read from message
BYTES = 16

def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    # Create a TCP socket with IPv4 addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    # In case the program thinks the port is already in use, the line below will
    # reuse a local socket that's waiting to time out (in TIME_WAIT state)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Bind socket to address and listen for connections
    sock.bind(address)
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # Make a new socket when client connects. Also grab client address
            conn, addr = sock.accept()
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # Receive 16 bytes of data from the client
                    data = conn.recv(BYTES)
                    print('received "{0}"'.format(data.decode('utf8')))
                    # Send the data back to the client, and log it
                    if data:
                        conn.sendall(data)
                        print('sent "{0}"'.format(data.decode('utf8')))
                    else: # Break if message is empty
                        print('no data received, closing connection')
                        break
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                # Close socket created above when a client connected.
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        # Use the python KeyboardInterrupt exception as a signal to
        # close the server socket and exit from the server function.
        sock.close()
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
