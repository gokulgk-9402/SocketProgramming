# Socket Programming Project
## Multi-media Group Chat

### Prereqisites
Python version: 3.10.0 <br/>
The libraries threading, socket, os, tkinter are all part of The Python Standard Library, so no need to install any additional packages. <br/>
You **may** have to disable the firwall on your computer when trying to run the files.

### Description
*  This is a simple Multi-media Group chat application made using Socket Programming in python, where a client can connect to the chat room, send messages, files, etc. There is still a lot of room for improvement and a lot of features can be added to this in the future. <br/>
*  Server creates a thread for each client that is connected to it, so it can listen to multiple clients at once. <br/>
*  Client creates one thread for maintaining the GUI and one for receiving messages fromt the server. <br/>
*  tkinter is used to create a Graphical User Interface at the client side. <br/>
*  os is used to get various information about the file when trying to send a file to the chat room. <br/>
*  simple send(), recv() functions are used to share data between clients and the server. <br/>

### Server file
  Download the file server.py and if you want to connect with a client in a different network, replace the SERVER ip with the public IP Address of the system in which the server is running. Just run the server.py file
  
### Client file
  Download the file client.py in how many ever clients you need and run the code. You will be prompted to enter a nickname for each of the client. Other instructions will be visible for you in the tkinter Graphical User Interface you get in the client. Just enter whichever message you want to send to the chat room or the respective commands and the server will broadcast your file, message or respond to your command.

### Commands
**!INFO:** Get information about the number of clients connected to the chat room, display their nick names. <br/>
**!FILE <filename>:** Send the file <filename> from the same directory as the client.py file to the chat room. <br/>
**!DISCONNECT:** Leave the chat room.
  
### References
1. https://docs.python.org/3/library/tkinter.html
2. https://www.geeksforgeeks.org/socket-programming-python/
3. https://realpython.com/python-sockets/
4. https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
5. https://www.tutorialspoint.com/python/python_gui_programming.htm
6. https://www.youtube.com/watch?v=3QiPPX-KeSc
