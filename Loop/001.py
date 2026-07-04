""" write a script to print out multiplication table of the user input
    input: 2
    2 * 2 =2
    ----
    2 * 12 =24
"""

# collect input 
user_input = int(input("What is your input:? "))
limit = 12


for a in range(1, limit+1):
    result: int = user_input * a
    message: str = f"{user_input} * {a} = {result}"
    print(message)