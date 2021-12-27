import random
import socket
import struct
import time
import threading
from _thread import *
from termcolor import colored


# setting the ports and ip
portUDP = random.randint(2000, 30000)
portTCP = random.randint(2000, 30000)
local_ip = socket.gethostbyname(socket.gethostname())
globalPort = "255.255.255.255"

# message formatting
magic_cookie = 0xabcddcba
msg_type = 0x2
FORMAT = 'utf-8'
messageSize = 2048

# global arguments
connected_clients = []
question = None
correctAnswer = None
answer = None
TCPServerSocket = None
UDPServerSocket = None
UDP_continue = True


def main():
    # re-starting the game
    while True:
        # global thread_udp
        global portTCP
        portTCP += 1
        thread_udp = threading.Thread(target=broadcasting, args=())
        thread_tcp = threading.Thread(target=connecting_to_clients, args=())

        thread_udp.start()
        thread_tcp.start()

        thread_udp.join()
        thread_tcp.join()


# start broadcasting the entire network
def broadcasting():
    global UDP_continue
    UDP_continue = True
    global UDPServerSocket
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        # broadcasting
        UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        UDPServerSocket.bind(('', portUDP))
        message = "Server started, listening on IP address " + local_ip
        print(colored(message, 'blue'))

        #message_decode = struct.pack('QQQ', portTCP, magic_cookie, msg_type)  # TODO- change
        message_decode = struct.pack('HLB', portTCP, magic_cookie, msg_type)
        while UDP_continue:
            UDPServerSocket.sendto(message_decode, (globalPort, 13117))
            time.sleep(1)
    except Exception as e:
        UDPServerSocket.close()


def connecting_to_clients():
    global TCPServerSocket, UDP_continue, connected_clients
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # setting the TCP socket
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind(('', portTCP))
        TCPServerSocket.listen(5)

        # adding two clients
        add_client()
        add_client()
        UDP_continue = False

        # creating thread for each client
        start_new_thread(get_messages, (connected_clients[0][1], connected_clients[0][0],))
        start_new_thread(get_messages, (connected_clients[1][1], connected_clients[1][0],))

        # two clients are connected
        time.sleep(3)  # TODO: change
        game_on()
    except Exception as e:
        close_connection()


def add_client():
    global connected_clients, TCPServerSocket
    try:
        conn, addr = TCPServerSocket.accept()
        name = conn.recv(messageSize).decode(FORMAT)
        connected_clients.append((name, conn, addr))
    except Exception as e:
        close_connection()


def game_on():
    global question, correctAnswer, connected_clients, answer, TCPServerSocket
    question = (random.randint(1, 4), random.randint(1, 5))
    correctAnswer = question[0] + question[1]
    # global connected_clients
    client_1 = connected_clients[0]
    client_2 = connected_clients[1]
    welcome_message = f"Welcome to Quick Maths.\n" \
                      f"Player 1: {client_1[0]}" \
                      f"\nPlayer 2: {client_2[0]}" \
                      "==\n" \
                      "Please answer the following question as fast as you can:\n" \
                      f"How much is {question[0]}+{question[1]}?"

    send_message_to_players(client_1, client_2, welcome_message)

    # global answer
    winner = None

    for i in range(10):
        if answer is None:
            time.sleep(1)
        else:
            name = answer[1]
            if answer[0] == correctAnswer:  # the answer is right
                winner = name
            else:  # the answer is wrong
                if name == client_1[0]:
                    winner = client_2[0]
                else:
                    winner = client_1[0]
            break

    game_over = "\nGame over!\n" \
                f"The correct answer was {correctAnswer}!\n"
    send_message_to_players(client_1, client_2, game_over)
    if winner is not None:
        winner_msg = f"Congratulations to the winner: {winner}"
    else:
        winner_msg = f"There was a tie"  # TODO: format
    send_message_to_players(client_1, client_2, winner_msg)
    print(colored("Game over, sending out offer requests...", 'green'))
    close_connection()


def send_message_to_players(client_1, client_2, message):
    try:
        client_1[1].send(message.encode(FORMAT))
        client_2[1].send(message.encode(FORMAT))
    except Exception as e:
        close_connection()


def get_messages(conn, name):
    global answer, messageSize, connected_clients, TCPServerSocket
    try:
        msg = conn.recv(messageSize).decode(FORMAT)
        if answer is None:
            answer = (msg, name)
    except Exception as e:
        close_connection()


def close_connection():
    global TCPServerSocket, connected_clients, answer
    TCPServerSocket.close()
    connected_clients = []
    answer = None


main()
