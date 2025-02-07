import socket

def main():
    host = "127.0.0.1"
    port = 3567

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connected to the server")
        client_socket.send(input("enter file name").encode())

        while True:
            command = input("Enter command (MOVE direction, STATUS, LOCATION): ").strip()
            if not command:
                continue
            client_socket.send(command.encode())
            response = client_socket.recv(1024).decode()
            print("Server Response:", response)

            if response in ["WON", "LOST"]:
                print("Game Over!")
                break

if __name__ == "__main__":
    main()
