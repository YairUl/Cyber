import socket
import pickle

# Create a socket object for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's address and port
host = '127.0.0.1'  # Localhost
port = 3567         # The same port used by the server

# Connect to the server
client_socket.connect((host, port))
cont = True
try:
    while cont:
        client_socket.send(input("guess a number").encode())
        received_data = client_socket.recv(1024)
        bull_cows = pickle.loads(received_data)
        print(f"the score is {bull_cows}")
        cont = bool(client_socket.recv(1024))
except Exception as e:
    print("game over")


# Send a response to the server









client_socket.close()

