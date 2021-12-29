import socket
import struct

from random import randrange
import getch




FORMAT = "utf-8"
messageSize = 2048

team_number = randrange(50)
team_name = f"Team {team_number}"
key_ = None


def getInput():
    pass


def main():
    # running the program
    while True:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tcp_socket = socket.socket()
        try:
            # finding a server to connect to
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # listening to the general port and connection to the first message
            udp_socket.bind(("0.0.0.0", 13117))
            print("Client started, listening for offer requests...")
            print(f"client name: {team_name}")  # TODO: remove
            data, addr = udp_socket.recvfrom(messageSize)
            print(f"Received offer from {addr[0]}, attempting to connect...")

            # connecting to found server
            address = struct.unpack('IBH', data)  # TODO- change
            tcp_socket.connect((addr[0], address[2]))

            message = team_name + "\n"
            tcp_socket.send(message.encode(FORMAT))

            # getting the question
            data, addr = tcp_socket.recvfrom(messageSize)
            print(data.decode(FORMAT))
            # answering the question

            input_char = getInput()
            tcp_socket.send(input_char.encode(FORMAT))

            # finish message
            data = tcp_socket.recv(messageSize)
            print(data.decode(FORMAT))
            data = tcp_socket.recv(messageSize)
            print(data.decode(FORMAT))

            tcp_socket.close()

        except Exception as e:
            # print(e)
            tcp_socket.close()
            continue


main()
