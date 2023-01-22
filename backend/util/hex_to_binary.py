"""
This is a Python script that defines two functions, hex_to_binary(hex_string) and main().

The hex_to_binary(hex_string) function takes a single argument, a string that represents a
hexadecimal number, and converts it to a string that represents the equivalent binary number.
The function uses a conversion table, HEX_TO_BINARY_CONVERSION_TABLE, to convert each character
in the input hex string to its 4-digit binary equivalent. The binary digits are then concatenated to form the final binary string.

The main() function demonstrates the usage of the hex_to_binary() function. It first converts an integer to its hexadecimal representation
then calls hex_to_binary() to convert it to binary, and then converts the binary back to the original integer. This is done to show that the 
hex_to_binary() function is working correctly and that the original number is the same as the final number.

It also calls crypto_hash function of 'test-data' and then converts the returned hex string to binary using hex_to_binary function and prints the binary number

if name == 'main': makes sure that the code in the if block only runs when the script is run from the command line and not when it is imported as a module in some
other script.

"""


from backend.util.crypto_hash import crypto_hash

HEX_TO_BINARY_CONVERSION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}

def hex_to_binary(hex_string):
    binary_string = ''

    for character in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[character]

    return binary_string

def main():
    number = 451
    hex_number = hex(number)[2:]
    print(f'hex_number: {hex_number}')

    binary_number = hex_to_binary(hex_number)
    print(f'binary_number: {binary_number}')

    original_number = int(binary_number, 2)
    print(f'original_number: {original_number}')

    hex_to_binary_crypto_hash = hex_to_binary(crypto_hash('test-data'))
    print(f'hex_to_binary_crypto_hash: {hex_to_binary_crypto_hash}')

if __name__ == '__main__':
    main()
