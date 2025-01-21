import random
import time
import threading
#the point of the code is to estimate the value of pai using threads in a random prosses
def rand_calc(times):
    time_in_loop = 1000000

    for batches in range(times):
        all_tries = 0
        land_in_pai = 0
        for i in range(time_in_loop):
            if random.random()**2 + random.random()**2 < 1:
                land_in_pai += 1
            all_tries +=1
        print(f"real pi value: 3.141592, Calculated value: {4*land_in_pai/all_tries}, number of tries = {all_tries}")

batch = int(input("enter number of banches"))
thread1 = threading.Thread(target=rand_calc, args=(batch,))
thread1.start()
print("Main thread is free to do other tasks.")

thread1.join()