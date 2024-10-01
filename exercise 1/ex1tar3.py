import statistics


def average_mid():
    num = input("enter a number")
    arr = []
    average = 0
    midian = 0
    while num.isdigit() == True:
        arr.append(num)
        average += int(num)
        num = input("enter a number")

    try:
        print("average is:", average / len(arr))
        print("median is:" , statistics.median(arr))
        return
    except:
        print("please enter a valid number")
        average_mid()

average_mid()