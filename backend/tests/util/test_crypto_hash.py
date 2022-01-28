from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
    # It should create the same hash with arguments of different data types
    # in any order
    assert crypto_hash(1, [2], 'three') == crypto_hash('three', 1, [2])
    assert crypto_hash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'
    
# import hashlib
# import json

# def crypto_hash(*args):
#     """
#     Return a sha-256 hash of the given arguments.
#     """
#     stringified_args = sorted(map(lambda data: json.dumps(data), args))
#     joined_data = ''.join(stringified_args)

#     return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

# def main():
#     print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
#     print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")

# if __name__ == '__main__':
#     main()