import random

def simulation(iterations):
    # draw a hand with multiple iterations
    success = 0
    for i in range(iterations):
        deck = [0, 0, 0] + [1 for j in range(16)] + [2 for j in range(21)]
        trap = 0
        myrmello = 0
        rest = 0
        for i in range(5):
            card = random.randint(0,39-i)
            if deck[card] == 0:
                myrmello += 1
            if deck[card] == 1:
                trap += 1
            else:
                rest += 1
            del deck[card]
        if myrmello >= 1 and trap >= 1:
            success += 1

    return [success, iterations, "{}%".format(success/iterations*100)]

print(simulation(10000))
