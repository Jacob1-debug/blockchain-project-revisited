import time

from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

"""
This code imports the Blockchain class from backend.blockchain.blockchain and the SECONDS constant from backend.config.
It then creates an instance of the Blockchain class, initializes an empty list to store the time it takes to mine each block,
and then loops 1000 times to add blocks to the blockchain. For each iteration, it starts a timer, adds a block to the blockchain, 
stops the timer, calculates the time it took to mine the block in seconds, appends the time to mine the block to the list of times,
calculates the average time it takes to mine blocks, and prints the difficulty of the most recent block mined, the time it took to mine
the most recent block, and the average time it takes to mine blocks.

"""
# Initialize an instance of the Blockchain class
blockchain = Blockchain()

# Create an empty list to store the time it takes to mine each block
times = []

# Loop 1000 times to add blocks to the blockchain
for i in range(1000):
    # Start a timer
    start_time = time.time_ns()
    # Add a block to the blockchain
    blockchain.add_block(i)
    # Stop the timer
    end_time = time.time_ns()

    # Calculate the time it took to mine the block in seconds
    time_to_mine = (end_time - start_time) / SECONDS
    # Append the time to mine the block to the list of times
    times.append(time_to_mine)

    # Calculate the average time it takes to mine blocks
    average_time = sum(times) / len(times)

    # Print the difficulty of the most recent block mined
    print(f'New block difficulty: {blockchain.chain[-1].difficulty}')
    # Print the time it took to mine the most recent block
    print(f'Time to mine new block: {time_to_mine}s')
    # Print the average time it takes to mine blocks
    print(f'Average time to add blocks: {average_time}s\n')
