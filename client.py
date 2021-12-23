import socket
import select
import threading
import time
from random import randrange
from pynput.keyboard import Key, Listener  #TODO: check if ok to use this package


IP = socket.gethostbyname(socket.gethostname())
portTCP = 10010
FORMAT = "utf-8"

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
    #print(f"final key: {key_}")
    if key_:
        key_tosend = f"{key_}"
        tcp_socket.send(key_tosend.encode(FORMAT))


def main():

    # finding a server to connect to
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listening to the general port and connection to the first message
    udp_socket.bind(("0.0.0.0", 13117))
    print("Client started, listening for offer requests...")
    print(f"client name: {team_name}")  # TODO: remove
    data, addr = udp_socket.recvfrom(2048)
    print(f"Received offer from {addr[0]}, attempting to connect...")
    print(f"{addr[1]} - port?")
    # connecting to found server

    tcp_socket = socket.socket()
    tcp_socket.connect((addr[0], portTCP))

    message = team_name + "\n"
    try:
        tcp_socket.send(message.encode(FORMAT))
    except:
        print("connection failed")  # TODO- if the server has no more room- do we continue listening with while loop?

    while True:
        # getting the question
        data, addr = tcp_socket.recvfrom(2048)
        print(data.decode(FORMAT))
        game_on = True
        # while game_on:
        #     keyboard_input(tcp_socket)
        #     data = tcp_socket.recv(1024)
        #     if data:
        #         game_on = False
        keyboard_input(tcp_socket)

        #msg = input("") # TODO- change to dynamic input
        #tcp_socket.send(msg.encode(FORMAT))
        data = tcp_socket.recv(1024)
        print(data.decode(FORMAT))
    # numSent = tcp_socket.send("thank you for connecting me".encode('utf-8'))



main()
