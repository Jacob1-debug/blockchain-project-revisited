
"""
The TransactionPool class is used to manage a pool of transactions.
It keeps track of the transactions that have been added to the pool,
and it provides methods for adding and removing transactions from the pool.
The set_transaction method is used to add a new transaction to the pool,
and the existing_transaction method can be used to check if a transaction has already been added.
The transaction_data method returns all the transactions in the pool in a json serialized form.
The clear_blockchain_transactions method is used to remove transactions that have been recorded on the blockchain,
to prevent double-spending.
"""



class TransactionPool:
    def __init__(self):
        self.transaction_map = {}

    def set_transaction(self, transaction):
        """
        Set a transaction in the transaction pool.
        """
        self.transaction_map[transaction.id] = transaction


    def existing_transaction(self, address):
        """
        Find a transaction generated by the address in the transaction pool
        """
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == address:
                return transaction

    def transaction_data(self):
        """
        Return the transactions of thje transaction pool represented in their
        json serialized form.
        """
        return list(map(
            lambda transaction: transaction.to_json(),
            self.transaction_map.values()
        ))

    def clear_blockchain_transactions(self, blockchain):
        """
        Delete blockchain recorded transactions from the transaction pool.
        """
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass
