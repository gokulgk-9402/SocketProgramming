import socket
import threading
import os

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050

BUFFER_SIZE = 64
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

server.listen()

clients = {}

def broadcast(message):
    for nickname in clients.keys():
        clients[nickname].send(message)

def handle(nickname):
    while True:
        try:
            client = clients[nickname]
            message = client.recv(1024).decode(FORMAT)
            if message.startswith("!DISCONNECT"):
                client.send("Left the chat room\n".encode(FORMAT))
                del clients[nickname]
                client.close()
                broadcast(f"{nickname} has left the chat.\n".encode(FORMAT))
                break
            elif message.startswith("!FILE"):
                print(f"Preparing to receive the file: {message.split()[-1]} ")
                filename = message.split()[-1]
                filesize = client.recv(BUFFER_SIZE).decode()

                filename = os.path.basename(filename)

                filesize = int(filesize)
                with open(filename, "wb") as f:
                    bytes_read = client.recv(filesize)
                    f.write(bytes_read)

                print(f"File {filename} received in server successfully!")

                print("Broadcasting files to other clients...")
                broadcast(message.encode(FORMAT))

                file_length = str(filesize).encode(FORMAT)
                file_length += b' ' * (BUFFER_SIZE - len(file_length))
                broadcast(file_length)
                with open(filename, "rb") as f:
                    while True:
                        bytes_read = f.read(filesize)
                        if not bytes_read:
                            break
                        broadcast(bytes_read)

                print("File broadcasted successfully")

                broadcast(f"{nickname} has shared the file {filename}\n".encode(FORMAT))

            elif message.startswith("!INFO"):
                reply = f"{nickname} used !INFO command.\n"
                reply += f"Number of people in the chat room: {len(clients.keys())}\n"
                reply += "The list of people in the room is: \n"
                for nickname in clients.keys():
                    reply += f"{nickname} \n"
                broadcast(reply.encode(FORMAT))
            
            elif message is not None:
                message = nickname + ": " + message 
                print(f"{message}")
                broadcast(message.encode(FORMAT))
        except:
            del clients[nickname]
            client.close()
            broadcast(f"{nickname} has left the chat.\n".encode(FORMAT))
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)

        broadcast(f"{nickname} has entered the chat.\n".encode(FORMAT))

        clients[nickname] = client

        print(f"Nickname of the client is {nickname}")
        client.send(f"Connected to the chat room as {nickname}\nType !DISCONNECT to disconnect\nType !FILE <filename> to send a file\nType !INFO to view the information about the chat room\n".encode(FORMAT))

        thread = threading.Thread(target = handle, args = (nickname,))
        thread.start()

print("Server is starting...")
print(f"Server is listening on {SERVER}.")
receive()