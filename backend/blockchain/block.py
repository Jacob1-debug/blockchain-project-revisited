import time
"""
The code defines a Block class for creating and storing blocks in a blockchain.
Each block contains a timestamp, a reference to the previous block's hash, a hash of
the current block, data (transactions), a difficulty value, and a nonce. The class also 
provides several methods for interacting with the blocks, such as:

__init__(): Initializes a new block instance with the given properties
__repr__(): Returns a string representation of the block
__eq__(): Compares the block with another block
to_json(): Serializes the block into a dictionary of its attributes
mine_block(last_block, data): Mines a new block by finding a hash that meets the proof-of-work requirement
genesis(): Generates the Genesis block (first block of the blockchain)
from_json(block_json): Deserializes a block's json representation back into a block instance
adjust_difficulty(last_block, new_timestamp): Adjusts the difficulty of the block according to the MINE_RATE
is_valid_block(last_block, block): Validates a block by enforcing several rules such as proper last_hash reference and meeting proof of work requirement.
The class also uses the crypto_hash and hex_to_binary utility functions from the backend.util package, and the MINE_RATE constant from the backend.config package.

"""

# import crypto_hash and hex_to_binary utility functions
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary

# import MINE_RATE from config
from backend.config import MINE_RATE

# Initial Genesis data
GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}

class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    # returns a string representation of the block
    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    # compares the block with other block
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # returns json representation of the block
    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes
        """
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until a block hash
        is found that meets the leading 0's proof of work requirement.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        # mine the block until the leading 0's proof of work is met
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        # return mined block
        return Block(timestamp, last_hash, hash, data, difficulty, nonce)


    @staticmethod
    def genesis():
        """
        Generate the genesis block.
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block's json representation back into a block instance.
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the MINE_RATE.
        Increase the difficulty for quickly mined blocks.
        Decrease the difficulty for slowly mined blocks.
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate block by enforcing the following rules:
          - the block must have the proper last_hash reference
          - the block must meet the proof of work requirement
          - the difficulty must only adjust by 1
          - the block hash must be a valid combination of the block fields
        """
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof of work requirement was not met')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must only adjust by 1')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')

def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'foo')
    bad_block.last_hash = 'evil_data'

    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')

if __name__ == '__main__':
    main()
