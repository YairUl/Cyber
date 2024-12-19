import pickle
import random
import socket
class BullsCode:

    def __init__(self, startCode = None):
        self.startCode = startCode if startCode is not None else str(random.randint(0000, 9999)).zfill(4)
        #1234    1781
    def check(self, bull2):
        bull_list = []

        code1 = str(self.startCode)
        code2 = str(bull2.startCode)

        cows1_count = [0] * 10
        cows2_count = [0] * 10

        for i in range(4):              # that is bulls
            if code1[i] == code2[i]:
                bull_list.append("B")
            else:
                cows1_count[int(code1[i])] += 1
                cows2_count[int(code2[i])] += 1
        #print(cows1_count)
        #print(cows2_count)
        for number in range(10):
            min_cows = min(cows1_count[number], cows2_count[number])
            num_of_cows = ["C"]*min_cows
            bull_list.extend(num_of_cows)
        return bull_list


#print(BullsCode())
'''
print(BullsCode("1234").check(BullsCode("1234")))  # Output: ['B', 'B', 'B', 'B']
print(BullsCode("1550").check(BullsCode("5587")))  # Output: ['B', 'C']
print(BullsCode("2777").check(BullsCode("7722")))  # Output: ['B', 'C', 'C']
print(BullsCode("7722").check(BullsCode("2777")))  # Output: ['B', 'C', 'C']
print(BullsCode("2787").check(BullsCode("7780")))  # Output: ['B', 'B', 'C']
print(BullsCode("7780").check(BullsCode("2787")))  # Output: ['B', 'B', 'C']
print(BullsCode("2787").check(BullsCode("7782")))  # Output: ['B', 'B', 'C', 'C']
print(BullsCode("7782").check(BullsCode("2787")))  # Output: ['B', 'B', 'C', 'C']
print(BullsCode("7340").check(BullsCode("2777")))  # Output: ['C']
'''



# Create a socket object for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a local address and port
host = '127.0.0.1'  # Localhost
port = 3567         # Port number

server_socket.bind((host, port))

# Start listening for incoming connections
server_socket.listen()
print(f"Server is listening on {host}:{port}...")

# Accept a connection from the client
(client_socket, client_address) = server_socket.accept()
print(f"Connection established with {client_address}")



secret_code = BullsCode()
print(secret_code.startCode)
for numbers in range(10):
    guess_num = client_socket.recv(1024).decode()
    # Send a message to the client
    print(guess_num)
    message = BullsCode(str(guess_num)).check(secret_code)
    print(message)
    client_socket.send(pickle.dumps(message))
    if message == ["B"]*4:
        print("you win")
        client_socket.send("False".encode())
        break
    client_socket.send("True".encode())
client_socket.send("False".encode())
    # Close the client and server sockets
client_socket.close()
server_socket.close()