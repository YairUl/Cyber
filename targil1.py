def hexaToDeci(str):
    hexLetters = '1234567890xabcdfABCDF'
    if str not in hexLetters and str.isdigit() == False:
        print("invalid hex number")
        return
    print(int(str, 16))


hexaToDeci('11')
hexaToDeci('0xa')
hexaToDeci('0x1a')
hexaToDeci('10dz')
