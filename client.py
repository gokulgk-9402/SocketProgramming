import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import time
import os

BUFFER_SIZE = 64
FORMAT = 'utf-8'

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050

class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Enter a nickname", parent = msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target = self.gui_loop)
        receive_thread = threading.Thread(target = self.receive)

        gui_thread.start()
        time.sleep(0.5)
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg= "#00ffff")

        self.chat_label = tkinter.Label(self.win, text = "Chat: ", bg="#00ffff")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text = "Message: ", bg="#00ffff")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height = 3, bg = "#ffccff")
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text = "Send", bg = "#ffff80", command=self.write)
        self.send_button.config(font = ("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("VM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.input_area.get('1.0', 'end')}"
        if message.startswith("!FILE"):
            filename = message.split()[-1]

            if os.path.isfile(filename):     
                print(f"Sending the file {message.split()[-1]}...")           
                self.sock.send(message.encode(FORMAT))
                filesize = os.path.getsize(filename)
                file_length = str(filesize).encode(FORMAT)
                file_length += b' ' * (BUFFER_SIZE - len(file_length))
                self.sock.send(file_length)
                with open(filename, "rb") as f:
                    while True:
                        bytes_read = f.read(filesize)
                        if not bytes_read:
                            break
                        self.sock.send(bytes_read)

                print(f"File {filename} sent successfully")
                self.input_area.delete('1.0', 'end')
                return
            
            else:
                print("File doesn't exist")
                self.input_area.delete('1.0', 'end')
                return
            
        elif message.startswith("!DISCONNECT"):
            print("Leaving the chat room...")
            self.stop()
        self.sock.send(message.encode(FORMAT))
        self.input_area.delete('1.0', 'end')
        

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode(FORMAT)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode(FORMAT))
                elif message.startswith('!FILE'):
                    print(f"Preparing to receive the file...")
                    filename = message.split()[-1]
                    filesize = self.sock.recv(BUFFER_SIZE).decode()

                    filename = os.path.basename(filename)

                    filesize = int(filesize)
                    with open(filename, "wb") as f:
                        bytes_read = self.sock.recv(filesize)
                        f.write(bytes_read)
                    
                    print(f"File: {filename} received successfully")

                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(HOST, PORT)