import hashlib
import json
import time
import random
from fastapi import FastAPI

app = FastAPI()


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

    def weight(self):

        return int(self.utility_score * 0.5 + self.reputation * 3 + 1)

    def reward(self, utility):

        self.utility_score += utility
        self.reputation += utility * 0.05


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

    def register_validator(self, address):

        self.validators[address] = Validator(address)

    def add_task(self, task_type, payload):

        task = Task(self.task_counter, task_type, payload)

        self.task_pool.append(task)

        self.task_counter += 1

        return task

    def utility_table(self):

        return {
            "ai_training": 10,
            "scientific_compute": 8,
            "data_processing": 6,
            "storage": 4,
            "general_compute": 3
        }

    def utility_value(self, task_type):

        table = self.utility_table()

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


blockchain = Blockchain()

blockchain.register_validator("node_A")
blockchain.register_validator("node_B")
blockchain.register_validator("node_C")


@app.get("/")
def home():

    return {"message": "Proof of Utility Node"}


@app.get("/chain")
def get_chain():

    return {
        "length": len(blockchain.chain),
        "chain": [block.__dict__ for block in blockchain.chain]
    }


@app.post("/task")
def submit_task(task_type: str, payload: str):

    task = blockchain.add_task(task_type, payload)

    return {"task_id": task.task_id}


@app.get("/mine")
def mine_block():

    block = blockchain.create_block()

    if not block:
        return {"message": "no tasks"}

    return {
        "block_index": block.index,
        "validator": block.validator,
        "hash": block.hash
    }


@app.get("/validators")
def validators():

    return {
        v.address: {
            "utility": v.utility_score,
            "reputation": v.reputation
        }
        for v in blockchain.validators.values()
    }
