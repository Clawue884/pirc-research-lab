import hashlib
import json
import time
import random
from fastapi import FastAPI

app = FastAPI()


class Wallet:

    def __init__(self, address):

        self.address = address
        self.balance = 0


class Block:

    def __init__(self, index, previous_hash, transactions, validator):

        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):

        block_data = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "validator": self.validator
        }, sort_keys=True).encode()

        return hashlib.sha256(block_data).hexdigest()


class Blockchain:

    def __init__(self):

        self.chain = [self.genesis_block()]
        self.wallets = {}
        self.mempool = []

    def genesis_block(self):

        return Block(0, "0", [], "network")

    def create_wallet(self, address):

        if address not in self.wallets:

            self.wallets[address] = Wallet(address)

        return self.wallets[address]

    def add_transaction(self, sender, receiver, amount):

        tx = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }

        self.mempool.append(tx)

        return tx

    def reward_validator(self, validator):

        reward = 10

        wallet = self.wallets[validator]

        wallet.balance += reward

        return reward

    def mine_block(self):

        validator = random.choice(list(self.wallets.keys()))

        transactions = self.mempool[:]

        self.mempool = []

        reward = self.reward_validator(validator)

        transactions.append({
            "sender": "network",
            "receiver": validator,
            "amount": reward
        })

        block = Block(
            len(self.chain),
            self.chain[-1].hash,
            transactions,
            validator
        )

        self.chain.append(block)

        self.apply_transactions(transactions)

        return block

    def apply_transactions(self, txs):

        for tx in txs:

            sender = tx["sender"]
            receiver = tx["receiver"]
            amount = tx["amount"]

            if sender != "network":

                if self.wallets[sender].balance >= amount:

                    self.wallets[sender].balance -= amount

            if receiver not in self.wallets:

                self.create_wallet(receiver)

            self.wallets[receiver].balance += amount


blockchain = Blockchain()

blockchain.create_wallet("node_A")
blockchain.create_wallet("node_B")
blockchain.create_wallet("node_C")


@app.get("/")
def home():

    return {"message": "Proof of Utility Token Node"}


@app.post("/wallet")
def create_wallet(address: str):

    wallet = blockchain.create_wallet(address)

    return {"address": wallet.address}


@app.get("/wallets")
def wallets():

    return {
        w.address: w.balance
        for w in blockchain.wallets.values()
    }


@app.post("/transaction")
def transaction(sender: str, receiver: str, amount: int):

    tx = blockchain.add_transaction(sender, receiver, amount)

    return tx


@app.get("/mine")
def mine():

    block = blockchain.mine_block()

    return block.__dict__


@app.get("/chain")
def chain():

    return {
        "length": len(blockchain.chain),
        "chain": [b.__dict__ for b in blockchain.chain]
    }
