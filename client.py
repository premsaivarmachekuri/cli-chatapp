import colorama
from colorama import Fore
import pickle
import socket
import sys
import select
from _thread import *
import time
import shutil
import click

emojis = {
    ":)": "😊",
    ":(": "😞",
    ":D": "😃",
}

def list_rooms(rooms_list):
    if len(rooms_list) != 0:
        for keys in rooms_list:
            print(f"Room No : {keys}")
    else:
        print("No rooms available")

def main():
    port = 12344
    host = '127.0.0.1'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        name = input("Hey what's your good name: ")
        if len(name) != 0:
            break
        else:
            print("Please provide your name to start")

    s.send(name.encode('utf-8'))

    salute_message = s.recv(1024).decode()
    print(salute_message)

    while True:
        print("Please choose one of these choices!")
        print("1: List all the available rooms")
        print("2: Join a room")
        print("3: Create a room")
        print("4: Exit")

        choice1 = input("Your Choice: ")

        if choice1 == "1":
            s.send("LIST".encode('utf-8'))
            data_loaded = s.recv(1024)
            try:
                rooms_list = pickle.loads(data_loaded)
            except EOFError:
                rooms_list = {}
            list_rooms(rooms_list)

        elif choice1 == "2":
            room_number = input("Room Number: ")
            s.send("JOIN".encode('utf-8'))
            time.sleep(0.2)
            s.send(room_number.encode('utf-8'))

            success = s.recv(1024).decode()
            print("")
            if success == "True":
                print(f"Joining Room No : {room_number}, DAATEBAYO!")
                print("")

                welcome_message = s.recv(1024).decode()
                print(welcome_message)
                print("")

                while True:
                    sockets_list = [sys.stdin, s]
                    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

                    for socks in read_sockets:
                        if socks == s:
                            message = socks.recv(1024).decode()
                            width = shutil.get_terminal_size()[0]
                            print(' ' * (width - len(message)), end="")
                            sys.stdout.write(Fore.RED + emojis.get(message, message))
                            print(Fore.WHITE + "")
                            sys.stdout.flush()

                        else:
                            message = sys.stdin.readline()
                            if message.strip() == '/q':
                                print("**BYE**")
                                quit()

                            else:
                                s.send(message.encode('utf-8'))
                            print("")
                            sys.stdout.flush()

            else:
                print("Enter a valid Room No, DATTEBAYO!")
                print("")

        elif choice1 == "3":
            s.send("CREATE".encode('utf-8'))
            new_room_num = s.recv(1024).decode()
            print(f"Room Number {new_room_num} created successfully")
            print("")

        elif choice1 == "4":
            print("As you like it!")
            quit()

        else:
            print("Enter a valid choice!")
            print("")
            s.send("CONTINUE".encode('utf-8'))


if __name__ == '__main__':
    main()
