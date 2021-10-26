import socket
import threading


IP="0.0.0.0"
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
    s.bind((IP,PORT))
    s.listen(1)
    cracker, cracker_address = s.accept()
    
    try:
        message = cracker.recv(BUFFER_SIZE).decode()
    except:
        cracker.close()
        return

    if message == "Howdy":
        cracker.send(str(g_id).encode())
    else:
        cracker.close()
        return
    
    threading.Thread(target=handle_client, args=(cracker_address[0],g_id + PORT,)).start()
    g_id+=1
    cracker.close()

def init_ranges():
    global g_range_list

    start = "aaaaaa"
    for i in range(26):
        for j in range(1,26):
            g_range_list.append([start, chr(ord(start[0]) + i) + chr(ord(start[1]) + j) + start[2:]])
            start = chr(ord(start[0]) + i) + chr(ord(start[1]) + j) + start[2:]
    g_range_list.append([g_range_list[-1][-1], "zzzzzz"])

    
def get_range():
    global g_range_list
    return g_range_list.pop(0)

def finish(hash: str, password: str):
    pass

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
        client_socket.send(msg.encode())
        response = client_socket.recv(BUFFER_SIZE)  # id,true/false,md5,password
 
        # Stop loop if client disconnected, remove it from the client list, and add its unchecked range to the unchecked ranges list.
        if not response:
            client_list.remove(client_socket)
            unchecked_ranges.append(brute_range)
            return
 
        response = response.decode().split(',')
        if response[1] == 'true':
            finish(response[2], response[3])
            return

if __name__ == "__main__":
    init_ranges()
    print(g_range_list)
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