import hashlib
import json
import random
import time


class Task:

    def __init__(self, task_id, task_type, payload):

        self.task_id = task_id
        self.task_type = task_type
        self.payload = payload
        self.completed = False


class Validator:

    def __init__(self, address):

        self.address = address
        self.utility_score = 0
        self.reputation = 1
        self.blocks = 0

    def weight(self):

        return int(self.utility_score * 0.5 + self.reputation * 3 + 1)

    def reward(self, utility):

        self.utility_score += utility
        self.reputation += utility * 0.05
        self.blocks += 1

    def penalize(self):

        self.reputation *= 0.8


class Block:

    def __init__(self, index, previous_hash, tasks, validator):

        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.tasks = tasks
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):

        block_data = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "tasks": [t.task_id for t in self.tasks],
            "validator": self.validator
        }, sort_keys=True).encode()

        return hashlib.sha256(block_data).hexdigest()


class Blockchain:

    def __init__(self):

        self.chain = [self.genesis_block()]
        self.validators = {}
        self.task_pool = []
        self.task_counter = 0

    def genesis_block(self):

        return Block(0, "0", [], "network")

    def register_validator(self, validator):

        self.validators[validator.address] = validator

    def add_task(self, task_type, payload):

        task = Task(self.task_counter, task_type, payload)

        self.task_pool.append(task)

        self.task_counter += 1

    def utility_value(self, task_type):

        table = {
            "ai_training": 10,
            "scientific_compute": 8,
            "data_processing": 6,
            "storage": 4,
            "general_compute": 3
        }

        return table.get(task_type, 1)

    def choose_validator(self):

        pool = []

        for v in self.validators.values():

            pool.extend([v.address] * v.weight())

        return random.choice(pool)

    def create_block(self):

        if not self.task_pool:
            return None

        validator_address = self.choose_validator()

        validator = self.validators[validator_address]

        tasks = self.task_pool[:3]

        self.task_pool = self.task_pool[3:]

        for t in tasks:

            utility = self.utility_value(t.task_type)

            validator.reward(utility)

            t.completed = True

        block = Block(
            len(self.chain),
            self.chain[-1].hash,
            tasks,
            validator_address
        )

        self.chain.append(block)

        return block

    def is_chain_valid(self):

        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i-1]

            if current.previous_hash != previous.hash:
                return False

            if current.hash != current.calculate_hash():
                return False

        return True


class Node:

    def __init__(self, node_id):

        self.node_id = node_id
        self.blockchain = Blockchain()
        self.peers = []

    def connect_peer(self, peer):

        self.peers.append(peer)

    def broadcast_block(self, block):

        for peer in self.peers:

            peer.receive_block(block)

    def receive_block(self, block):

        self.blockchain.chain.append(block)

    def produce_block(self):

        block = self.blockchain.create_block()

        if block:

            self.broadcast_block(block)

        return block


if __name__ == "__main__":

    nodeA = Node("node_A")
    nodeB = Node("node_B")

    nodeA.connect_peer(nodeB)
    nodeB.connect_peer(nodeA)

    validators = [
        Validator("A"),
        Validator("B"),
        Validator("C")
    ]

    for v in validators:

        nodeA.blockchain.register_validator(v)
        nodeB.blockchain.register_validator(v)

    nodeA.blockchain.add_task("ai_training", "dataset_A")
    nodeA.blockchain.add_task("scientific_compute", "protein")
    nodeA.blockchain.add_task("data_processing", "satellite")
    nodeA.blockchain.add_task("storage", "climate_data")

    block = nodeA.produce_block()

    if block:

        print("Block produced by", block.validator)
        print("Hash:", block.hash)

    print("\nNode A chain length:", len(nodeA.blockchain.chain))
    print("Node B chain length:", len(nodeB.blockchain.chain))
