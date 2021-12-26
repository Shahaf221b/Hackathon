import random
import socket
import struct
import time
import threading
from _thread import *

portUDP = random.randint(2000, 30000)
portTCP = random.randint(2000, 30000)
# local_ip = socket.gethostbyname(socket.gethostname())
local_ip = '172.1.0.27'
magic_cookie = 0xabcddcba
msg_type = 0x2
FORMAT = 'utf-8'
# thread_lock = threading.Lock()
connected_clients = []
answer = None
UDPServerSocket = None
# thread_udp = None
UDP_continue = True


def main():

    while True:
        # global thread_udp
        global portTCP
        portTCP += 1
        thread_udp = threading.Thread(target=broadcasting, args=())
        thread_tcp = threading.Thread(target=connecting_to_clients, args=())
        # print("hello")
        thread_udp.start()
        thread_tcp.start()
        # print("hello")

        thread_udp.join()
        thread_tcp.join()


# start broadcasting the entire network
def broadcasting():
    global UDP_continue
    UDP_continue = True
    global UDPServerSocket
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # UDPServerSocket.bind((local_ip, portUDP))
        UDPServerSocket.bind(('', portUDP))
        message = "Server started, listening on IP address " + local_ip
        print(message)

        # message_decode = struct.pack('QQ', magic_cookie, msg_type)
        message_decode = struct.pack('QQQ', portTCP, magic_cookie, msg_type)
        while UDP_continue:
            UDPServerSocket.sendto(message_decode, ("255.255.255.255", 13117))
            time.sleep(1)
    except Exception as e:
        print(e)
        raise e
    finally:
        if UDPServerSocket is not None:
            UDPServerSocket.close()
            print("closing UDP socket")


def connecting_to_clients():
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # setting the TCP socket
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind(('', portTCP))
        TCPServerSocket.listen(5)

        # adding two clients
        add_client(TCPServerSocket)
        add_client(TCPServerSocket)
        global UDP_continue
        UDP_continue = False
        # creating thread for each client
        global connected_clients
        start_new_thread(get_messages, (connected_clients[0][1], connected_clients[0][0],))
        start_new_thread(get_messages, (connected_clients[1][1], connected_clients[1][0],))

        # two clients are connected
        time.sleep(3)  # TODO: change
        game_on(TCPServerSocket)
    except Exception as e:
        print(e)
        raise e
    # finally:
    #     if TCPServerSocket is not None:
    #         TCPServerSocket.close()
    #         print("closing TCP socket")


def add_client(TCPServerSocket):
    global connected_clients
    conn, addr = TCPServerSocket.accept()
    # print(conn, addr)
    name = conn.recv(2048).decode(FORMAT)  # TODO- is 2048 enough?
    # print("name", name)
    connected_clients.append((name, conn, addr))


def game_on(TCPServerSocket):
    global connected_clients
    client_1 = connected_clients[0]
    client_2 = connected_clients[1]
    welcome_message = f"Welcome to Quick Maths.\n" \
                      f"Player 1: {client_1[0]}" \
                      f"\nPlayer 2: {client_2[0]}" \
                      "==\n" \
                      "Please answer the following question as fast as you can:\n" \
                      "How much is 2+2?"

    send_message_to_players(client_1, client_2, welcome_message)

    global answer
    winner = None

    starting_time = time.time()
    while time.time() < starting_time + 10:
        if answer is not None:
            name = answer[1]
            if answer[0] == '4':  # the answer is right
                winner = name
            else:  # the answer is wrong
                if name == client_1[0]:
                    winner = client_2[0]
                else:
                    winner = client_1[0]
            break

    game_over = "\nGame over!\n" \
                "The correct answer was 4!\n"
    send_message_to_players(client_1, client_2, game_over)
    if winner is not None:
        winner_msg = f"Congratulations to the winner: {winner}"
    else:
        winner_msg = f"There was a tie"  # TODO: format
    send_message_to_players(client_1, client_2, winner_msg)
    answer = None
    TCPServerSocket.close()
    print("Game over, sending out offer requests...")
    # global connected_clients
    connected_clients = []
    # global thread_udp
    # thread_udp = threading.Thread(target=broadcasting, args=())


def send_message_to_players(client_1, client_2, message):
    client_1[1].send(message.encode(FORMAT))
    client_2[1].send(message.encode(FORMAT))


def get_messages(conn, name):
    # while True:
    msg = conn.recv(2048).decode(FORMAT)
    global answer
    if answer is None:
        answer = (msg, name)
        # print(answer)  # TODO: remove


main()
