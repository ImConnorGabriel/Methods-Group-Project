import math
import pytest

## opens a file in read mode
## filename received as a parameter
def openFile(filename):
    infile = open(filename, "r")

    print("File opened.")

######################################################
## takes two numbers and returns
## the result of a division
def numbers(num1, num2):
    return num1 / num2

#PyTest function for numbers success
def test_numbers():
    assert numbers(10,2) == 5

#PyTest function for numbers failure
def test_numbers_fail():
    assert numbers(20,4) == 10
#####################################################

#####################################################
## takes in two points
## finds the distance between the points
def dist(x1, y1, x2, y2):
    dist = (x2 - x1) ** 2 + (y2 - y1) ** 2
    dist = math.sqrt(dist)

    return dist

#PyTest function for success of dist function
def test_dist():
    assert dist(1,2,3,4) == 2.8284271247461903
    
def test_dist_failure():
    assert dist(1,2,3,4) == 10
#####################################################

#####################################################
## takes in a string -- reverses it
## then compares the two
def isPalindrome(temp):
    test = temp[::-1]

    if(test == temp):
        return True

    else:
        return False

#PyTest Function for success
def test_isPalindrome():
    assert isPalindrome("loool") == True
    
#PyTest Function for failure     
def test_isPalindrome_failure():
    assert isPalindrome("Palindrome") == True
####################################################
    
## has input to receive two numbers
## divides the two, then outputs the result
def divide():
    num1 = int(input("Enter a number: "))
    num2 = int(input("Enter another number: "))

    div = num1 / num2

    print("Your numbers divided is:", div)

## returns the squareroot of a particular number
def sq(num):
    return math.sqrt(num)

## grabs user's name
## greets them by their entire name
## names should be strings
def greetUser(first, middle, last):
    print("Hello!")
    print("Welcome to the program", first, middle, last)
    print("Glad to have you!")

## takes in a Python list
## attempts to display the item at the index provided
def displayItem(numbers, index):
    print("Your item at", index, "index is", numbers[index])
