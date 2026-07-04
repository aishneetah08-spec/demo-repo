class Calculator():
    """
    This is a calculator class that can do a whole lot of things
    """
    @classmethod
    def takeTwoNumbers(cls) -> (int, int):
        a = int(input("Enter Your First Number: "))
        b = int(input("Enter Your Second Number: "))
        return (a, b)
    
    @classmethod
    def addition(cls):
        firstNumber, secondNumber = Calculator.takeTwoNumbers()
        result = firstNumber + secondNumber
        print(f"The result of {firstNumber} + {secondNumber} = {result}") 


# Option 2 
Calculator.addition()  
