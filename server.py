import socket
import threading

IP = "0.0.0.0"
PORT = 13370
PASSWORD = "99df698e726c1a51c7e3a1b9dc468102"
BUFFER_SIZE = 2048
g_id = 0
g_range_list = []
client_list = []
unchecked_ranges = []


def main():
    global g_id

    s = socket.socket()
    s.bind((IP, PORT))
    s.listen(1)
    cracker, cracker_address = s.accept()

    try:
        message = cracker.recv(BUFFER_SIZE).decode()
    except:
        return

    if message == "Howdy":
        cracker.send(str(g_id).encode())
    else:
        return

    threading.Thread(target=handle_client, args=(cracker_address, g_id,)).start()
    g_id += 1


def init_ranges() -> list:
    global g_range_list

    start = "aaaaaa"
    for i in range(26):
        for j in range(1, 26):
            g_range_list.append([start, chr(ord(start[0]) + i) + chr(ord(start[1]) + j) + start[2:]])
            start = chr(ord(start[0]) + i) + chr(ord(start[1]) + j) + start[2:]
    return [0, 0]  # PLACEHOLDER


def get_range():
    return [0, 0]  # PLACEHOLDER


def finish(passwd_hash: str, password: str):
    """
    This function lets all of the crackers know that the job was finished and a password was found.
    :param passwd_hash: Hash of the password found by the cracker
    :param password: Clear text password found by the cracker.
    :return: 
    """
    print('--------------------------\n* Password found! *\nPassword: {passwd}\nHash: {hash}\n--------------------------').format(passwd=password, hash=passwd_hash)
    print('Relying finish message to crackers...')
    msg = 'finish,{md5}'.format(md5=passwd_hash)
    for client_socket in client_list:
        # Safely send the ranges to the client.
        try:
            client_socket.send(msg.encode())
        except socket_error as e:
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
    client_socket = socket.socket()
    client_socket.connect((ip, port))
    client_list.append(client_socket)

    # Communicate with the client until the client disconnects or until the password was found.
    while True:
        brute_range = get_range()
        msg = '{start},{stop},{md5}'.format(start=brute_range[0], stop=brute_range[1], md5=PASSWORD)
        # Safely send the ranges to the client.
        try:
            client_socket.send(msg.encode())
        except socket_error as e:
            print(e)
            client_list.remove(client_socket)
            unchecked_ranges.append(brute_range)
            break
        response = client_socket.recv(BUFFER_SIZE)  # id,true/false,md5,password

        # Stop loop if client disconnected, remove it from the client list, and add its unchecked range to the unchecked ranges list.
        if not response:
            client_list.remove(client_socket)
            unchecked_ranges.append(brute_range)
            break

        response = response.decode().split(',')
        if response[1] == 'true':
            if md5(response[3].encode()).hexdigest() == PASSWORD:
                finish(response[2], response[3])
                break


            # start,end,md5
            # id,true/false,md5,password
            # finish,md5


if __name__ == "__main__":
    while True:
        main()

"""
id:8200                 security
f:1/0                   less work/stop algorithm
if 1        
pass:password           check password
else if has range       if not found in the range  
delete range            delete the range from the list
give another range      
else 
give range              
"""
