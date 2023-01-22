import os
import requests
import random

from flask import Flask, jsonify, request
from flask_cors import CORS

# import blockchain and wallet modules
from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub

# initialize flask app and CORS
app = Flask(__name__)
CORS(app,resources={r'/*': {'origins': 'http://localhost:3000'}})

# initialize blockchain, wallet and transaction pool
blockchain = Blockchain()
wallet = Wallet()
transaction_pool = TransactionPool()

# initialize PubSub module with blockchain and transaction pool instances
pubsub = PubSub(blockchain, transaction_pool)

# default route
@app.route('/')
def route_default():
    return 'Welcome to the blockchain'

# route to return blockchain
@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

# route to mine a new block
@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'

    # add a block with transaction data
    blockchain.add_block(transaction_data)

    block = blockchain.chain[-1]
    # broadcast the mined block
    pubsub.broadcast_block(block)

    return jsonify(block.to_json())

# route to make a transaction
@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    # get transaction data from the request
    transaction_data = request.get_json()
    # check if there is an existing transaction
    transaction = transaction_pool.existing_transaction(wallet.address)

    if transaction:
        # update the existing transaction
        transaction.update(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )
    else:
        # create a new transaction
        transaction = Transaction(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )

    # broadcast the transaction
    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

# check if the script is running as a peer
if os.environ.get('PEER') == 'True':
    # set a random port for the peer
    PORT = random.randint(5001, 6000)

    # make a request to the root node to get the blockchain
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    result_blockchain = Blockchain.from_json(result.json())

    try:
        # try to replace the local chain with the retrieved blockchain
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'\n -- Error synchronizing:
