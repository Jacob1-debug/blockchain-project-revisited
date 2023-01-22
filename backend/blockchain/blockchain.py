from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT

"""
The code defines a Blockchain class for creating and maintaining a blockchain. 
The class has methods for adding new blocks to the blockchain, replacing the existing chain with a new one,
and checking the validity of the chain. Each instance of the class contains a list of blocks, where each block is 
an instance of the Block class. The class also provides several methods for interacting with the blockchain, such as:

__init__(): Initializes a new blockchain instance with the genesis block
add_block(data): Mines a new block and adds it to the blockchain
__repr__(): Returns a string representation of the blockchain
replace_chain(chain): Replaces the local chain with the incoming one, if the incoming chain is longer and formatted properly
to_json(): Serializes the blockchain into a list of blocks
from_json(chain_json): Deserializes a list of serialized blocks into a blockchain instance
is_valid_chain(chain): Validates the incoming chain by enforcing the rules of the blockchain
is_valid_transaction_chain(chain): Validates the incoming chain by enforcing the rules of a chain composed of blocks of transactions
The class also uses the Block class, the Transaction class, the Wallet class, and the MINING_REWARD_INPUT constant from the backend package.
"""

class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()] #initialize the chain with the genesis block

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data)) #mine a new block and add it to the chain

    def __repr__(self):
        return f'Blockchain: {self.chain}' 

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following applies:
          - The incoming chain is longer than the local one.
          - The incoming chain is formatted properly.
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer.')

        try:
            Blockchain.is_valid_chain(chain) #check if incoming chain is valid
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain #replace the chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a Blokchain instance.
        The result will contain a chain list of Block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )

        return blockchain
    
    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
          - the chain must start with the genesis block
          - blocks must be formatted correctly
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of blocks of transactions.
            - Each transaction must only appear once in the chain.
            - There can only be one mining reward per block.
            - Each transaction must be valid.
        """
        transaction_ids = set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            'There can only be one mining reward per block. '\
                            f'Check block with hash: {block.hash}'
                        )

                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(
                            f'Transaction {transaction.id} has an invalid '\
                            'input amount'
                        )

                Transaction.is_valid_transaction(transaction)

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockchain.py ___name__: {__name__}')

if __name__ == '__main__':
    main()
