# Caesar Cipher

import string
letters : str = string.ascii_lowercase

alphabets = []


for letter in letters:
    alphabets.append(letter)

class Caesar():
    """
    This is for encryption and decryption
    """ 
    SHIFT = 2

    def encryption(input: str) -> str:
        # encrypted_output = []
        # Qaanitat
        for char in input.lower():
            print(char)
            for i in range(0,27):
                if alphabets[i] == char:
                    position = Caesar.SHIFT + 1 + i
                    encrypted_output.append[alphabets[position]] 

    def decryption() -> str:
        pass