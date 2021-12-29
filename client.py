import socket
import struct
import sys
import threading

from random import randrange
import getch




FORMAT = "utf-8"
messageSize = 2048

team_number = randrange(50)
team_name = f"Winx Club"
key_ = None


def getInput(tcp_socket):
    for line in sys.stdin:
        if 'q' == line.rstrip():
            key_ = line
            break
    tcp_socket.send(line.encode(FORMAT))
    # if key_:
    #     key_toSend = f"{key_}"
    #     tcp_socket.send(key_toSend.encode(FORMAT))


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

            #########
            def send_msg(sock):
                # while True:
                #     data = sys.stdin.readline()
                #     sock.send(data.encode(FORMAT))
                data = None
                for i in range(9):
                    data = sys.stdin.readline()
                    sock.send(data.encode(FORMAT))
                    if data is not None:
                        break


            def recv_msg(sock):
                data = None
                for i in range(9):
                    data, addr = sock.recvfrom(1024)
                    sys.stdout.write(data.decode(FORMAT))
                    if data is not None:
                        print(data.decode(FORMAT))
                        break


            th1 =threading.Thread(target=send_msg, args=(tcp_socket,)).start()
            th2 =threading.Thread(target=recv_msg, args=(tcp_socket,)).start()
            #########
            # th1.join()
            # th2.join()
            # tcp_socket.send(input_char.encode(FORMAT))

            # finish message
            # data = tcp_socket.recv(messageSize)
            # print(data.decode(FORMAT))
            data = tcp_socket.recv(messageSize)
            print(data.decode(FORMAT))
            # th1.join()
            # th2.join()
            tcp_socket.close()

        except Exception as e:
            # print(e)
            tcp_socket.close()
            continue


main()
