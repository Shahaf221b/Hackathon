import socket
from time import sleep


def main():
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]

    msg_string = f"Server started, listening on IP address {socket.gethostbyname(socket.gethostname())}"
    msg = str.encode(msg_string)
    while True:

        for ip in allips:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip, 0))
            sock.sendto(msg, ("255.255.255.255", 13117))
            sock.close()

        sleep(1)


main()
