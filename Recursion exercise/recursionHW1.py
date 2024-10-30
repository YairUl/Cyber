#n! = (n-1)! * n

def factorial(num : int):
    if num == 0:
        return 1
    return factorial(num - 1) * num

print(factorial(7))
