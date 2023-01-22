import hashlib
import json

"""
The purpose of the code is to define a function called crypto_hash that takes any number of arguments and returns 
a sha-256 hash of those arguments. The arguments are first stringified, sorted, and then joined together into a single string.
This string is then encoded as UTF-8 and a sha-256 hash of the encoded string is returned. The function main is then called to 
demonstrate the usage of the crypto_hash function by printing the result of calling it with different arguments.
"""

def crypto_hash(*args):
    """
    Return a sha-256 hash of the given arguments.
    """
    # sort the arguments so that the same data passed in different orders will produce the same hash
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    # join all of the arguments together as one string
    joined_data = ''.join(stringified_args)

    # create a sha256 hash object
    sha256 = hashlib.sha256()
    # update the hash object with the joined string data
    sha256.update(joined_data.encode('utf-8'))
    # return the hexadecimal representation of the hash
    return sha256.hexdigest()

def main():
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")

if __name__ == '__main__':
    main()
