import socket
import struct
from termcolor import colored
from random import randrange
from pynput.keyboard import Key, Listener  # TODO: check if ok to use this package

FORMAT = "utf-8"
messageSize = 2048

team_number = randrange(50)
team_name = f"Team {team_number}"
key_ = None


def setKey(key):
    global key_
    key_ = key


def on_press(key):
    # print('{0} pressed'.format(
    #     key))
    # time_to_wait = time.time() + 10
    # while time.time() < time_to_wait:  # TODO: check
    #     setKey(key)
    #     return False
    setKey(key)
    return False


def on_release(key):
    # print('{0} release'.format(
    #     key))
    # time_to_wait = time.time() +10
    # while time.time() < time_to_wait:  # TODO: check
    #     # Stop listener
    #     pass
    if key_:
        return False


def keyboard_input(tcp_socket):
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    if key_:
        key_toSend = f"{key_}"
        tcp_socket.send(key_toSend.encode(FORMAT))


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
            print(colored(f"Received offer from {addr[0]}, attempting to connect...",'blue'))

            # connecting to found server
            # address = struct.unpack('QQQ', data) # TODO- change
            address = struct.unpack('HLB', data)
            tcp_socket.connect((addr[0], address[0]))

            message = team_name + "\n"
            tcp_socket.send(message.encode(FORMAT))

            # getting the question
            data, addr = tcp_socket.recvfrom(messageSize)
            print(data.decode(FORMAT))
            # answering the question
            keyboard_input(tcp_socket)

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
