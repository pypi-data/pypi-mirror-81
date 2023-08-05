####################################################################################################################
# chooseYourOption.py
# topic:define different options, user chooses by selecting function
# author: Michael Heser, hesermi71995, 3172761
# date: 2020-09-29
# recent changes: first implementation
# build info: operating system: Linux Fedora 32, editor: idle3, python version: 3.8.5
####################################################################################################################

# calculateSquares
def calculateSquares(endValue):
    print('I will now calculate all squares from 1 to', endValue)
    for counter in range(1, endValue + 1):
        output = counter**2
        print(output)
    print('Done printing', endValue, 'squares')

# calculateSquareRoots
def calculateSquareRoots(endValue):
    print('I will now calculate all square roots from 1 to', endValue)
    for counter in range(1, endValue + 1):
        output = counter**(1/2)
        print(output)
    print('Done printing', endValue, 'square roots')
    
# calculateFibo
def calculateFibo(border):
# return Fibonacci series up to border
    print('I will now calculate all fibonacci numbers from 0 to', border)
    result = []
    a, b = 0, 1
    while a < border:
        result.append(a)
        a, b = b, a+b
    print('Done calculating fibonacci numbers')
    return result
    
# calculatePows
def calculatePows(exp, endValue):
    print('I will now calculate all numbers from 1 to', endValue, 'powered by', exp)
    for counter in range(1, endValue + 1):
        output = counter**exp
        print(output)
    print('Done printing', endValue, 'numbers')






