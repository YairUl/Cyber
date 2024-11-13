#   $$$$$***   ....  /n
#    &&&&&(,,/ ##))   /n
#    **   ****./,///

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def rotate(image: str, degrees: int):
    if degrees == 0:
        return image
    if degrees == 90:

        #turn the string to a matrix
        cur_matrix = [list(line) for line in image.splitlines()]
        cols = len(cur_matrix[0])
        rows = len(cur_matrix)

        # open a new (empty) matrix in the opposite rows and columns
        end_matrix = [[None for _ in range(rows)] for _ in range(cols)]

        # add to the end_matrix in a 90 degree rotation
        for col in range(cols):
            for row in range(rows):
                end_matrix[col][row] = cur_matrix[row][cols-1-col]

        #convert the matrix back to a string
        end_str = "\n".join("".join(line) for line in end_matrix)

        return end_str
    elif degrees == 180:
        return image[::-1].strip()                  # in case of
    elif degrees == 270:
        end180str = rotate(image, 180)
        return rotate(end180str, 90)
    elif degrees == 360:
        split360str = image.split("\n")
        end360str = ""
        for col in split360str:
            end360str += col[::-1]
            end360str += "\n"
        return end360str.strip("\n")

    else: rotate(image, int(input("please enter a valid number")))



def convert(image: str, convertion_table: list, conv_choice: int):
    new_str = ""
    if conv_choice == 0:
        return image
    for letter in image:
        found = False
        for item in convertion_table:
            if item[0] == letter:
                found = True
                new_str += item[conv_choice]
                break
        if not found:
            if letter == "\n":
                new_str += "\n"
            else:
                new_str += "X"
    return new_str


def serialize(string, rotation, conv_choice, conversion_table, to_print=False):
    rotated_string = rotate(string, rotation)
    converted_string = convert(rotated_string, conversion_table, conv_choice)
    list_string = converted_string.split("\n")
    serialize_string = ""
    for line in list_string:
        current_letter = line[0]
        count_letter = 0
        for letter in line:
            if letter != current_letter:
                serialize_string += f"{count_letter}{current_letter}"
                current_letter = letter
                count_letter = 1
            else:
                count_letter += 1
        serialize_string += f"{count_letter}{current_letter}"
        serialize_string += "\n"
        count_letter = 0
    if to_print:
        return serialize_string
    with open("serialize.txt", "w") as file:
        file.write(serialize_string)
    return "serialize.txt"


def deserialize(string, rotation, conv_choice, conversion_table, to_print=False):
    des_list = string.splitlines()
    char_num = 0
    end_str = ""
    for line in des_list:
        for char in line:
            try:
                char_num = int(char)
            except:
                end_str += char * char_num
        end_str += "\n"
    rotated_str = rotate(end_str, rotation)
    converted_str = convert(rotated_str, conversion_table, conv_choice)
    if to_print:
        return converted_str
    with open("deserialize.txt", "w") as file:
        file.write(converted_str)
    return "deserialize.txt"







#print(rotate("$$$$$***   ....\n&&&&&(,,/  ##))\n**   ****./,///", 90))
#print(convert("$$$$$***   ....\n&&&&&(,,/  ##))\n**   ****./,///", ["(^$", "$;!", "*|#"], 1))
#print(serialize("$$$$$***   ....\n&&&&&(,,/  ##))\n**   ****./,///", 0, 0, ["(^$", "$;!", "*|#"], True))
#print(deserialize("5$3*3 4.\n5&1(2,1/2 2#2)\n2*3 4*1.1/1,3/", 270, 0, ["(^$", "$;!", "*|#"], True))
#print(rotate("$$$$$***   ....\n#&&&&(,,/  ##))\n**   ****./,///", 270))
#
#$$$$$***   ....
#&&&&(,,/ ##))
#**   ****./,///