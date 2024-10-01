
def hexRead(str):
    hexLetters = '1234567890aAbBcCdDeEfF'
    word = ""
    endSum = 0
    for letter in str:
        if letter not in hexLetters:
            if word:
                endSum = endSum + int(word, 16)
            word = ""
        else:
            word += letter
    if word:
        endSum = endSum + int(word, 16)
    print(endSum)

# I know that I could have done a much better code, I can explain if unclear


