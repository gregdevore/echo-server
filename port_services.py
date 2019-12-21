'''
Print list of services for a given range of ports
'''
import socket
import sys

def print_port_ranges(lower=0, upper=10):
    '''
    Print services for a given range of ports

    Args:
        lower (int):
            Lower bound (default = 0)
        upper (int):
            Upper bound (default = 100)

    Returns:
        None
    '''
    print('port -> service')
    for port in range(lower,upper+1):
        try:
            service = socket.getservbyport(port)
            print('{:d} -> {}'.format(port, service))
        except OSError:
            # Given port not found
            continue

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_port_ranges()
    elif len(sys.argv) == 3:
        lower, upper = [int(arg) for arg in sys.argv[1:]]
        # Check for valid range
        if lower < 0 or upper > 65535:
            raise ValueError('Port bounds must be between 0 and 65535, inclusive')
        print_port_ranges(lower, upper)
    else:
        usage = '\nusages: python port_services.py\n        python port_services.py lower_bound upper_bound\n'
        print(usage)
