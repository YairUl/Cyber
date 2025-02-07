import random
import socket
class Arena:
    def __init__(self, matrix):
        self.matrix = matrix
        self.treasure = self.random_place()
        self.thief = self.random_place(exclude=[self.treasure])
        self.cop = self.random_place(exclude=[self.treasure, self.thief])
    def random_place(self, exclude=[]):
        while True:
            rand_line = random.randint(0, len(self.matrix) - 1)
            rand_row = random.randint(0, len(self.matrix[0]) - 1)
            place = (rand_line, rand_row)
            if self.matrix[rand_line][rand_row]:  # Ensure the cell is walkable (False in original code)
                continue
            if place not in exclude:
                return place



    def printall(self):
        matrixPrint(self.matrix)
        print(f"treasure: {self.treasure}")
        print(f"thief: {self.thief}")
        print(f"cop: {self.cop}")

    def changeLocation(self):
        x, y = self.treasure
        self.matrix[x][y] = 2
        x, y = self.thief
        self.matrix[x][y] = 1
        x, y = self.cop
        self.matrix[x][y] = 3



def load_zone(file_name):
    global line_len
    with open(file_name, "rb") as file:
        line_length = file.read(1)
        line_len = ord(line_length)
        matrix = []
        more_lines = True
        while more_lines:
            byte_line = file.read(line_len)
            if not byte_line:
                break
            matrix.append([int(byte) for byte in byte_line])       # for bool type map: [bool(int(byte))

        return matrix

def player_move(arena, step):
    x, y = arena.thief
    x2, y2 = x, y
    if step == "UP":
        x2 = x - 1
    if step == "DOWN":
        x2 = x + 1
    if step == "RIGHT":
        y2 = y + 1
    if step == "LEFT":
        y2 = y - 1
    if x2 < 0 or x2 >= len(arena.matrix) or y2 < 0 or y2 >= len(arena.matrix[0]):
        return "WALL"
    elif arena.matrix[x2][y2] == 1:
        return "WALL"
    elif (x2, y2) == arena.treasure:
        return "WON"
    elif (x2, y2) == arena.cop:
        return "LOST"

    arena.matrix[x][y] = 0
    arena.thief = (x2, y2)
    arena.changeLocation()
    return("OK")
def cop_move(arena):
    x, y = arena.cop
    x2, y2 = x, y
    change_num = random.randint(0, 8)
    if change_num == 0:   # stay
        return False
    if change_num == 1:
        y2 = y -1
    if change_num == 2:
        x2, y2 = x+1, y-1
    if change_num == 3:
        x2 = x + 1
    if change_num == 4:
        x2, y2 = x + 1, y + 1
    if change_num == 5:
        y2 = y + 1
    if change_num == 6:
        x2, y2 = x + 1, y - 1
    if change_num == 7:
        y2 = y - 1
    if change_num == 8:
        x2, y2 = x - 1, y - 1
    if x2 < 0 or x2 >= len(arena.matrix) or y2 < 0 or y2 >= len(arena.matrix[0]):
        return False
    elif (x2, y2) == arena.thief:
        return True
    elif arena.matrix[x2][y2] == 1:
        return False
    arena.matrix[x][y] = 0
    arena.cop = (x2, y2)
    arena.changeLocation()
    return False
def matrixPrint(matrix):
    for _ in range(len(matrix)):
        print(matrix[_])
def load_players(arena):
    arena.changeLocation()

def get_location(arena):
    x, y = arena.thief
    return f"{y + 1}, {x + 1}"
def get_status(arena):
    x, y = arena.thief
    x1, y1 = arena.treasure
    x2, y2 = arena.cop
    copnear = abs(x - x2) + abs(y - y2) == 1
    treasurenear = abs(x - x1) + abs(y - y1) == 1
    status = {"cop": copnear, "treasure": treasurenear}
    return status


def map_printer(arena):
    arenamatrix = arena.matrix
    x, y = arena.thief
    arenamatrix[x][y] = "T"
    x, y = arena.cop
    arenamatrix[x][y] = "C"
    x, y = arena.treasure
    arenamatrix[x][y] = "X"

    arena_str = ""
    for row in arenamatrix:
        arena_str += " ".join(map(str, row)) + "\n"
    arena_str = arena_str.replace("1", "*").replace("0", " ")
    print(arena_str)


def main():
    host = "127.0.0.1"
    port = 3567

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Server is running...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            zone_name = conn.recv(1024).decode()

            matrix = load_zone(zone_name)  # input("enter an arena")
            arena = Arena(matrix)
            load_players(arena)


            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                command = data.split()
                if not command:
                    continue
                action = command[0]
                if action == "MOVE":
                    p_move = player_move(arena, command[1].upper())
                    conn.send(p_move.encode())

                else:
                    if action == "STATUS":
                        s = get_status(arena)
                        if s["cop"] == True:
                            end_s = "COP NEAR"
                        elif s["treasure"] == True:
                            end_s = "TREASURE NEAR"
                        else:
                            end_s = "GAME ON"
                        conn.send(end_s.encode())
                    if action == "LOCATION":
                        location = get_location(arena)
                        conn.send(location.encode())
                    map_printer(arena)
                end_game = cop_move(arena)
                if end_game == True:
                    capturd = "LOST"
                    conn.send(capturd.encode())

if __name__ == "__main__":
    main()

