import hashlib
import json
import time
import random
from fastapi import FastAPI
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

app = FastAPI()


class Wallet:

    def __init__(self):

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        self.public_key = self.private_key.public_key()

        self.address = self.generate_address()

        self.balance = 0

    def generate_address(self):

        pub_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return hashlib.sha256(pub_bytes).hexdigest()

    def sign(self, message):

        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return signature.hex()


class Transaction:

    def __init__(self, sender, receiver, amount, signature):

        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature


class Block:

    def __init__(self, index, previous_hash, transactions, validator):

        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):

        data = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "validator": self.validator
        }, sort_keys=True).encode()

        return hashlib.sha256(data).hexdigest()


class Blockchain:

    def __init__(self):

        self.chain = [self.genesis_block()]
        self.wallets = {}
        self.mempool = []

    def genesis_block(self):

        return Block(0, "0", [], "network")

    def create_wallet(self):

        wallet = Wallet()

        self.wallets[wallet.address] = wallet

        return wallet

    def verify_signature(self, public_key, message, signature):

        try:

            public_key.verify(
                bytes.fromhex(signature),
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            return True

        except:

            return False

    def add_transaction(self, tx):

        self.mempool.append(tx)

    def mine_block(self):

        validator = random.choice(list(self.wallets.keys()))

        reward = 10

        reward_tx = Transaction(
            "network",
            validator,
            reward,
            "reward"
        )

        txs = self.mempool[:]

        txs.append(reward_tx)

        self.mempool = []

        block = Block(
            len(self.chain),
            self.chain[-1].hash,
            txs,
            validator
        )

        self.chain.append(block)

        self.apply_transactions(txs)

        return block

    def apply_transactions(self, txs):

        for tx in txs:

            if tx.sender != "network":

                sender_wallet = self.wallets.get(tx.sender)

                if sender_wallet and sender_wallet.balance >= tx.amount:

                    sender_wallet.balance -= tx.amount

            receiver_wallet = self.wallets.get(tx.receiver)

            if receiver_wallet:

                receiver_wallet.balance += tx.amount


blockchain = Blockchain()

walletA = blockchain.create_wallet()
walletB = blockchain.create_wallet()


@app.get("/")
def home():

    return {"message": "PoU Secure Node"}


@app.get("/wallets")
def wallets():

    return {
        w.address: w.balance
        for w in blockchain.wallets.values()
    }


@app.get("/mine")
def mine():

    block = blockchain.mine_block()

    return {
        "index": block.index,
        "validator": block.validator,
        "hash": block.hash
    }


@app.get("/chain")
def chain():

    return {
        "length": len(blockchain.chain)
    }
