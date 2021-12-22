import socket
import struct
import time
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# sock.bind(("0.0.0.0", 13117))
# while True:
#     data, addr = sock.recvfrom(1024)
#     print(data)

team_name = "Shnatz"
def main():
    #portTCP = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        print("Client started, listening for offer requests...")
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # TODO: check
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0", 13117))
        data, addr = sock.recvfrom(2048)  # TODO: check buffer size
        print(f"Received offer from {addr[0]}, attempting to connect...")
        #portTCP = struct.unpack('QQ', data)
    except Exception as e:
        print(f"at main() in client: {e}")

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    portTCP = 10000  # TODO: change
    tcp_socket.connect((addr[0], portTCP))
    print("client connected")  # TODO: remove
    tcp_socket.send(team_name.encode('utf-8'))

    server_answer1 = tcp_socket.recv(2048)  # TODO: check buffer size
    server_answer2 = tcp_socket.recv(2048)
    server_answer3 = tcp_socket.recv(2048)

    time_to_wait = time.time() + 10
    while time.time() < time_to_wait:  # wait for input
        time.sleep(1)
        pass
    print(server_answer1.decode('utf-8'))
    print(server_answer2.decode('utf-8'))
    print(server_answer3.decode('utf-8'))


main()