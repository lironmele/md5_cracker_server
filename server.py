import hashlib
import socket
import threading
from hashlib import md5
import RangeDivider

IP = "0.0.0.0"
PORT = 13370
#PASSWORD = "99df698e726c1a51c7e3a1b9dc468102"
#PASSWORD = "01fc680014fa524420a949427f3acc4d"
# PASSWORD = "3dbe00a167653a1aaee01d93e77e730e"
PASSWORD = input("What do you want to crack?")
if not PASSWORD:
    PASSWORD = 'aaaaaaaa'
print(PASSWORD)
PASSWORD = hashlib.md5(PASSWORD.encode()).hexdigest()
print(PASSWORD)
BUFFER_SIZE = 2048
g_range_list = []
client_list = []
unchecked_ranges = []


def main():
    current_id = 1

    # Initiates server socket
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()

    while True:
        print("Waiting for connections")
        (cracker, cracker_address) = server_socket.accept()
        if cracker_address[0] == "10.30.56.206":
            cracker.close()
            continue

        print(f"Accepted address {cracker_address}")

        # Safely send the ranges to the client.
        try:
            message = cracker.recv(BUFFER_SIZE).decode()
            print(f"Got {message}")
	
        except Exception as e:
            print(e)
            cracker.close()
            continue

        if message == "Howdy":
            try:
                cracker.send(str(current_id).encode())
            except Exception as e:
                print(e)
                cracker.close()
        else:
            cracker.close()
            continue
        
        print(f"Starting conversation with ({cracker_address[0]}, {PORT+current_id})")
        threading.Thread(target=handle_client, args=(cracker_address[0], current_id + PORT,)).start()
        current_id += 1
        cracker.close()


def init_ranges():
    global g_range_list

    start = 'aaaaaaaa'
    stop = 'zzzzzzzz'
    ranges = RangeDivider.Range(start=start, stop=stop, range_count=1000)

    g_range_list = ranges.to_list()

    print(g_range_list[0])


# def init_ranges():
#     global g_range_list

#     start = "aaaaaaaa"
#     for i in range(26):
#         for j in range(1, 26):
#             g_range_list.append([chr(ord(start[0]) + i) + chr(ord(start[1]) + j - 1) + start[2:],
#                                  chr(ord(start[0]) + i) + chr(ord(start[1]) + j) + start[2:]])
#         g_range_list.append([g_range_list[-1][-1], chr(ord(start[0]) + i) + "zzzzzzz"])

#     print(g_range_list[0])


def get_range():
    global g_range_list
    return g_range_list.pop(0)


def finish(passwd_hash: str, password: str):
    """
    This function lets all of the crackers know that the job was finished and a password was found.
    :param passwd_hash: Hash of the password found by the cracker
    :param password: Clear text password found by the cracker.
    :return: 
    """
    print('--------------------------\n* Password found! *\nPassword: {passwd}\nHash: {hash}\n--------------------------'.format(passwd=password, hash=passwd_hash))
    print('Relying finish message to crackers...')
    msg = 'finish,{md5}'.format(md5=passwd_hash)
    for client_socket in client_list:
        # Safely send the ranges to the client.
        try:
            client_socket.send(msg.encode())
        except Exception as e:
            print(e)
            client_list.remove(client_socket)  # Not sure if we need this line.
    print('Done relying finish message to crackers...')


def handle_client(ip: str, port: int):
    """
    Connects to the cracker's machine and send it ranges to check. Also handle the cracker's response accordingly.
    :param ip: IP address of the cracker's machine.
    :param port: port on which the cracker's server is hosted on.
    """
    # Initiate the client connection socket and add it to the client list.
    try:
        client_socket = socket.socket()
        client_socket.connect((ip, port))
        print(f"Connected to {ip},{port}")
        client_list.append(client_socket)
    except Exception as e:
        print(e)
        return

    # Communicate with the client until the client disconnects or until the password was found.
    while True:
        brute_range = get_range()
        msg = '{start},{stop},{md5}'.format(start=brute_range[0], stop=brute_range[1], md5=PASSWORD)
        # Safely send the ranges to the client.
        try:
            client_socket.send(msg.encode())
            response = client_socket.recv(BUFFER_SIZE)  # id,true/false,md5,password
        except Exception as e:
            print(e)
            client_list.remove(client_socket)
            unchecked_ranges.append(brute_range)
            break

        print(f"Got response {response} from {ip}")

        # Stop loop if client disconnected, remove it from the client list, and add its unchecked range to the unchecked ranges list.
        if not response:
            client_list.remove(client_socket)
            unchecked_ranges.append(brute_range)
            break

        response = response.decode().split(',')
        if response[1] == 'True' or response[1] == 'true':
            if md5(response[3].encode()).hexdigest() == PASSWORD:
                finish(response[2], response[3])
                break


if __name__ == "__main__":
    init_ranges()
    main()
