import requests
import time

"""
This script uses the requests library to interact with a server running a blockchain and wallet application. 
It first gets the current state of the blockchain by making a GET request to the server's /blockchain endpoint.
Then it creates and broadcasts a new transaction by making a POST request to the server's /wallet/transact endpoint, 
passing in a recipient address and amount as the request body. After creating and broadcasting the first transaction, 
it waits for 1 second before creating and broadcasting another transaction. The script then waits another second before 
mining a new block on the blockchain by making a GET request to the server's /blockchain/mine endpoint. Finally, it gets
the current state of the wallet by making a GET request to the

"""
from backend.wallet.wallet import Wallet

BASE_URL = 'http://localhost:5000'

# Function to get the current state of the blockchain from the server
def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()

# Function to mine a new block on the blockchain
def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()   

# Function to create and broadcast a new transaction
def post_wallet_transact(recipient, amount): 
    return requests.post(
        f'{BASE_URL}/wallet/transact',
        json={ 'recipient': recipient, 'amount': amount }
    ).json()

# Function to get the current state of the wallet from the server
def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()

# Get the current state of the blockchain
start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')

# Create and broadcast a new transaction
recipient = Wallet().address
post_wallet_transact_1 = post_wallet_transact(recipient, 21)
print(f'\npost_wallet_transact_1: {post_wallet_transact_1}')

# Wait for a second before creating and broadcasting another transaction
time.sleep(1)
post_wallet_transact_2 = post_wallet_transact(recipient, 13)
print(f'\npost_wallet_transact_2: {post_wallet_transact_2}')

# Wait for a second before mining a new block
time.sleep(1)
mined_block = get_blockchain_mine()
print(f'\nmined_block: {mined_block}')

# Get the current state of the wallet
wallet_info = get_wallet_info()
print(f'\nwallet_info: {wallet_info}')
