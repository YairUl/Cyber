def factorial(num : int):
    if num == 0:
        return 1
    return multi(factorial(num-1), num)

def multi(num1, num2):
    if num1 == 0:
        return 0
    return add(num2, multi(num1 - 1, num2))
def add(num1, num2):
    if num1 == 0:
        return 0
    x = add(num1 - 1, num2) + 1
    if x == num1:
        return x + num2
    return x


#print(factorial(5))