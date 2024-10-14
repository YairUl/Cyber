def morse_file(fileName):
    morse_to_english = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
                        '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
                        '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
                        '-.--': 'Y', '--..': 'Z', " ": ""}
    endString = ""
    with open(fileName, "r") as file:
        morse_string = file.read()
        morse_words = morse_string.split("/")
        for word in morse_words:
            word = word.strip()
            morse_letters = word.split()
            for letter in morse_letters:
                try:
                    endString = endString + morse_to_english[letter]
                except:
                    return "Error in Morse Code"
            endString = endString + " "
        endString = endString.strip()
        return endString


#print(morse_file("Data/morse1.txt"))

def count_symbols(fileName):
    word_string = morse_file(fileName).replace(" ", "")
    words_dict = {}
    for letter in word_string:
        if words_dict.get(letter) is None:
            words_dict[letter] = word_string.count(letter)
    #now sorting the dict (we did something very similar on the self py course)
    end_dict = dict(sorted(words_dict.items(), key = lambda item: item[1], reverse=True))
    return end_dict

#print(count_symbols("Data/morse2.txt"))

#{'E': 28, 'T': 22, 'A': 16, 'H': 13, 'R': 12, 'I': 10, 'L': 9, 'N': 9, 'S': 8, 'O': 6, 'D': 6, 'U': 5, 'B': 4, 'W': 3, 'F': 3, 'C': 3, 'Y': 3, 'P': 3, 'M': 2, 'G': 2, 'V': 1, 'Q': 1}

def print_count(fileName):
    letter_dict = count_symbols(fileName)
    end_string = ""
    curValue = list(letter_dict.values())[0]
    for letter in letter_dict:
        if letter_dict[letter] == curValue:
            end_string += letter
        else:
            end_string = end_string + "-" + str(curValue)
            print(end_string)
            curValue = letter_dict[letter]
            end_string = letter
    print(end_string + "-" + str(curValue))

#print_count("Data/morse2.txt")

