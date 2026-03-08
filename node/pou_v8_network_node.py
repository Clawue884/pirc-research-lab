import hashlib
import json
import time
import random
import requests
from fastapi import FastAPI

app = FastAPI()

peers = set()


class Block:

    def __init__(self, index, previous_hash, data, validator):

        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.data = data
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):

        block_data = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "validator": self.validator
        }, sort_keys=True).encode()

        return hashlib.sha256(block_data).hexdigest()


class Blockchain:

    def __init__(self):

        self.chain = [self.genesis_block()]

    def genesis_block(self):

        return Block(0, "0", "Genesis", "network")

    def latest_block(self):

        return self.chain[-1]

    def add_block(self, data, validator):

        block = Block(
            len(self.chain),
            self.latest_block().hash,
            data,
            validator
        )

        self.chain.append(block)

        return block

    def is_valid_chain(self, chain):

        for i in range(1, len(chain)):

            prev = chain[i-1]
            curr = chain[i]

            if curr["previous_hash"] != prev["hash"]:
                return False

        return True

    def replace_chain(self, new_chain):

        if len(new_chain) > len(self.chain):

            self.chain = new_chain


blockchain = Blockchain()


@app.get("/")
def home():

    return {"message": "PoU Network Node"}


@app.get("/chain")
def get_chain():

    return {
        "length": len(blockchain.chain),
        "chain": [block.__dict__ for block in blockchain.chain]
    }


@app.post("/mine")
def mine(data: str):

    validator = random.choice(["node_A", "node_B", "node_C"])

    block = blockchain.add_block(data, validator)

    broadcast_block(block)

    return block.__dict__


@app.post("/register_peer")
def register_peer(peer_url: str):

    peers.add(peer_url)

    return {"peers": list(peers)}


@app.get("/peers")
def get_peers():

    return list(peers)


@app.get("/sync")
def sync():

    longest_chain = blockchain.chain

    for peer in peers:

        try:

            response = requests.get(f"{peer}/chain")

            data = response.json()

            chain = data["chain"]

            if len(chain) > len(longest_chain):

                longest_chain = chain

        except:

            pass

    blockchain.replace_chain(longest_chain)

    return {"status": "synced", "length": len(blockchain.chain)}


def broadcast_block(block):

    for peer in peers:

        try:

            requests.post(
                f"{peer}/receive_block",
                json=block.__dict__
            )

        except:

            pass


@app.post("/receive_block")
def receive_block(block: dict):

    blockchain.chain.append(block)

    return {"status": "received"}
