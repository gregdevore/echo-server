import socket
import sys
import traceback

# Constant for number of bytes to read from message
BYTES = 16

def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    # Instantiate a TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    # Connect socket to the server
    sock.connect(server_address)

    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.sendall(msg.encode('utf-8'))

        # Accumulate 16 byte chunks of reply from the server. Exit loop
        # once entire message has been received
        # Log each chunk received
        while True:
            chunk = sock.recv(BYTES)
            if chunk:
                received_message += chunk.decode('utf-8')
            else: # If no data received, break loop
                print('received nothing, exiting')
                break
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        # After message received, close client socket.
        print('closing socket', file=log_buffer)
        sock.close()
        print('Received message:\n{}'.format(received_message))
        # Return the entire reply from server as return value of function
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
