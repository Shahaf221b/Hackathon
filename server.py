import socket
import struct
import time
import threading
from _thread import *

portUDP = 20022
portTCP = 10010
local_ip = socket.gethostbyname(socket.gethostname())
magic_cookie = 0xabcddcba
msg_type = 0x2
FORMAT = 'utf-8'

# thread_lock = threading.Lock()
connected_clients = []
answer = None


def main():
    thread_udp = threading.Thread(target=broadcasting, args=())
    thread_tcp = threading.Thread(target=connecting_to_clients, args=())

    thread_udp.start()
    thread_tcp.start()
    thread_udp.join()
    thread_tcp.join()


# start broadcasting the entire network
def broadcasting():
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPServerSocket.bind((local_ip, portUDP))
    message = "Server started, listening on IP address " + local_ip
    print(message)

    message_decode = struct.pack('QQ', magic_cookie, msg_type)
    while True:
        UDPServerSocket.sendto(message_decode, ("255.255.255.255", 13117))
        time.sleep(1)


def connecting_to_clients():
    # setting the TCP socket
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(('', portTCP))
    TCPServerSocket.listen(5)

    # waiting until we have 2 clients
    while len(connected_clients) < 2:
        conn, addr = TCPServerSocket.accept()
        name = conn.recv(2048).decode(FORMAT)  # TODO- is 2048 enough?
        name_with_index = name, str(len(connected_clients))  # TODO- remove before submitting
        connected_clients.append((name_with_index, conn, addr))
        start_new_thread(get_messages, (conn, name,))

    # two clients are connected
    time.sleep(10)  # TODO: change
    game_on()


# TODO- more questions?

def game_on():
    client_1 = connected_clients[0]
    client_2 = connected_clients[1]
    welcome_message = f"Welcome to Quick Maths.\n" \
                      f"Player 1: {client_1[0][0]}" \
                      f"\nPlayer 2: {client_2[0][0]}" \
                      "==\n" \
                      "Please answer the following question as fast as you can:\n" \
                      "How much is 2+2?"

    send_message_to_players(client_1, client_2, welcome_message)

    winner = None

    starting_time = time.time()
    while time.time() < starting_time + 10:
        if answer is not None:
            name = answer[1]
            if answer[0] == '4':  # the answer is right
                winner = name
            else:  # the answer is wrong
                if name == client_1[0][0]:
                    winner = client_2[0][0]
                else:
                    winner = client_1[0][0]
            break


    game_over = "\nGame over!\n" \
                "The correct answer was 4!\n"
    send_message_to_players(client_1, client_2, game_over)
    print("message was sent")  # TODO: remove
    if winner is not None:
        winner_msg = f"Congratulations to the winner: {winner}"
    else:
        winner_msg = f"There was a tie"  # TODO: format
    send_message_to_players(client_1, client_2, winner_msg)


def send_message_to_players(client_1, client_2, message):
    client_1[1].send(message.encode(FORMAT))
    client_2[1].send(message.encode(FORMAT))


def get_messages(conn, name):
    while True:
        msg = conn.recv(2048).decode(FORMAT)
        global answer
        answer = (msg, name)
        #print(answer)  # TODO: remove


main()
