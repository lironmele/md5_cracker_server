import socket

ip = "localhost"
port = 13370

def main():
    soc = socket.socket()
    soc.connect((ip, port))
    soc.send("Howdy".encode())
    id = int(soc.recv(1024).decode())

    soc = socket.socket()
    soc.bind((ip, port+id))
    soc.listen()
    client, _ = soc.accept()
    print(client.recv(1024).decode())

    md5 = "99df698e726c1a51c7e3a1b9dc468102"
    password = "zaaaaa"

    client.send("1,true,{md5},{pass}".encode())

    print(client.recv(1024).decode())
    print(client.recv(1024).decode())

main()