"""calculator
    This is a simple calculator where you ask the users for two numbers 
    and try to
    perform some mathematical operation like {
        1. Addition
        2. Subtraction
        3. Multiplication
        4. Division 
        5. modulo 
        6. Exponentiation
        7. floor division
    }
"""

# def is a keyword defining functions

def takeTwoNumbers() -> (int, int):
    a = int(input("Enter Your First Number: "))
    b = int(input("Enter Your Second Number: "))
    return (a, b)


def addition() -> int:
    firstNumber, secondNumber = takeTwoNumbers()
    result = firstNumber + secondNumber
    print(f"The result of {firstNumber} + {secondNumber} = {result}") 


def subtraction() -> int:
    firstNumber, secondNumber = takeTwoNumbers()
    result = firstNumber - secondNumber
    print(f"The result of {firstNumber} - {secondNumber} = {result}") 


def multiplication() -> int:
    firstNumber, secondNumber = takeTwoNumbers()
    result = firstNumber * secondNumber
    print(f"The result of {firstNumber} * {secondNumber} = {result}")


def division() -> int:
    firstNumber, secondNumber = takeTwoNumbers()
    result = firstNumber / secondNumber
    print(f"The result of {firstNumber} / {secondNumber} = {result}")



def modulo() -> int:
    firstNumber, secondNumber = takeTwoNumbers()
    result = firstNumber % secondNumber
    print(f"The result of {firstNumber} % {secondNumber} = {result}")


def exponentiation() -> int:
    firstNumber, secondNumber = takeTwoNumbers()
    result = firstNumber ** secondNumber
    print(f"The result of {firstNumber} ** {secondNumber} = {result}")


def floorDivision() -> int:
    firstNumber, secondNumber = takeTwoNumbers()
    result = firstNumber // secondNumber
    print(f"The result of {firstNumber} // {secondNumber} = {result}")
    


def calculator():
    print("Starting All Engines")
    print("Select a number from 1-7 to perform an operation")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulo")
    print("6. Exponentiation")
    print("7. Floor division")
    userChoice = int(input("What is your choice?" ))
    if (userChoice == 1):
        addition()
    elif userChoice == 2 :
        subtraction()
    elif userChoice == 3 :
        multiplication()
    elif userChoice == 4 :
        division()
    elif userChoice == 5 :
        modulo
    elif userChoice == 6 :
        exponentiation()
    elif userChoice == 7 :
        floorDivision()

    else:
        print("No valid point detected")       






calculator()