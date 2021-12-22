import socket
import struct
import sys
import time
import threading

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
magic_cookie = 0xabcddcba
msg_type = 0x2
all_clients = {}

def broadcasting():

    try:
        UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        portUDP = 20000  # TODO: change
        UDPServerSocket.bind((local_ip, portUDP))
        message = "Server started, listening on IP address " + local_ip
        print(message)
        UDPServerSocket.settimeout(0.5) #TODO:check if ok

        message = struct.pack('QQ', magic_cookie, msg_type) #TODO: check if correct with 'QQ'
        time_to_wait = time.time() + 10  # TODO: change
        while time_to_wait > time.time():
            UDPServerSocket.sendto(message, ("255.255.255.255", 13117))
            time.sleep(1)
    except Exception as e:
        UDPServerSocket.close()
        print(f"in broadcast: {e}")


def connecting_to_clients(tcp_connect):

    new_player = False
    try:
        time_to_wait = time.time() + 10
        #tcp_connect.settimeout(time_to_wait - time.time())
        tcp_connect.settimeout(10)
        while True:
            conn, client_address = tcp_connect.accept()
            data = conn.recv(1024)  # TODO: check if 1024 enough
            team_name = data.decode('utf-8')
            # threading.lock.acquire()
            all_clients[team_name] = conn, client_address
            print(f"team {team_name} connected")  # TODO: remove
            new_player = True
            threading.lock.release()
    except Exception as e:
        if new_player:
            # need to start game ?
            print("")  # TODO: remove?
        else:
            # no player connected, close tcp connection
            tcp_connect.close()


def welcome_message(c1,c2):
    message = "Welcome to Quick Maths.\n"
    message += f"Player 1: {c1}\n"
    message += f"Player 2: {c2}\n"
    message += "==\n"
    message += "Please answer the following question as fast as you can:\n"
    message += "How much is 2+2?\n"
    return message


def game_over_message():
    message = "Game over!\n"
    message += "The correct answer was 4!\n"
    # TODO: add the name of the winner team
    return message


def gameOn():

    try:
        all_clients_items = [x for x in all_clients.items()]
        client1 = all_clients_items[0]
        #client2 = all_clients_items[1]  #TODO:
        #welcome_msg = welcome_message(client1[0], client2[0])  #TODO:
        welcome_msg = welcome_message(client1[0], "no c2")
        welcome_msg = welcome_msg.encode()
        gameOver_message = game_over_message()
        gameOver_message = gameOver_message.encode()
        client1[1][0].send(welcome_msg)
        #client2[1][0].send(welcome_msg)  #TODO:
        # TODO: receive client answer
        time_plus_10 = time.time() + 10
        while time.time() < time_plus_10:
            time.sleep(1)
            pass
        client1[1][0].send(gameOver_message)
        #client2[1][0].send(gameOver_message)  #TODO:
    except Exception as e:
        print(f"in game on: {e}")




def main():
    # interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    # allips = [ip[-1][0] for ip in interfaces]
    #
    # msg_string = f"Server started, listening on IP address {socket.gethostbyname(socket.gethostname())}"
    # print(msg_string)
    # msg = str.encode(msg_string)


    # while True:
    #
    #     for ip in allips:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    #         sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #         sock.bind((ip, 0))
    #         sock.sendto(msg, ("255.255.255.255", 13117))
    #         sock.close()
    #     sleep(1)

    try:
        try:
            TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            portTCP = 10000 #TODO: change
            TCPServerSocket.bind((local_ip, portTCP))
            TCPServerSocket.listen(10)
        except :
            print("no answer from client")

        all_clients = {}
        thread_udp = threading.Thread(target = broadcasting, args = ())
        thread_tcp = threading.Thread(target = connecting_to_clients, args=(TCPServerSocket,))

        thread_udp.start()
        time.sleep(1)
        thread_tcp.start()
        thread_udp.join()
        thread_tcp.join()
        #threading.Thread.sleep(10)
        gameOn()
        TCPServerSocket.close()
    except :
        print("client connection lost")


main()
