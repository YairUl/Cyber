def hexaToDeci(str):
    hexLetters = '1234567890xabcdfABCDF'
    if str not in hexLetters and str.isdigit() == False:
        print("invalid hex number")
        return
    print(int(str, 16))


