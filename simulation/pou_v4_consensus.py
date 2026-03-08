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
        self.proof = None


class Validator:

    def __init__(self, address):
        self.address = address
        self.utility_score = 0
        self.reputation = 1
        self.completed_tasks = 0

    def total_weight(self):
        return int(self.utility_score * 0.6 + self.reputation * 4 + 1)

    def reward(self, utility):
        self.utility_score += utility
        self.reputation += utility * 0.05
        self.completed_tasks += 1

    def penalize(self):
        self.reputation *= 0.7


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


class PoUBlockchain:

    def __init__(self):

        self.chain = [self.genesis_block()]
        self.validators = {}
        self.task_pool = []
        self.task_counter = 0

    def genesis_block(self):

        return Block(
            0,
            "0",
            [],
            "network"
        )

    def register_validator(self, validator):

        self.validators[validator.address] = validator

    def add_task(self, task_type, payload):

        task = Task(self.task_counter, task_type, payload)
        self.task_pool.append(task)

        self.task_counter += 1

    def utility_table(self):

        return {
            "ai_training": 12,
            "scientific_compute": 9,
            "data_processing": 6,
            "storage": 4,
            "general_compute": 3
        }

    def calculate_utility(self, task_type):

        table = self.utility_table()

        return table.get(task_type, 1)

    def generate_proof(self, task, validator):

        raw = f"{task.task_id}{validator.address}{task.payload}{time.time()}"

        return hashlib.sha256(raw.encode()).hexdigest()

    def verify_proof(self, proof):

        # simple verification rule
        return proof is not None and len(proof) == 64

    def choose_validator(self):

        weighted = []

        for v in self.validators.values():

            weight = v.total_weight()

            weighted.extend([v.address] * weight)

        return random.choice(weighted)

    def process_tasks(self, max_tasks=3):

        if not self.task_pool:
            return []

        selected = self.task_pool[:max_tasks]
        self.task_pool = self.task_pool[max_tasks:]

        return selected

    def produce_block(self):

        tasks = self.process_tasks()

        if not tasks:
            return None

        validator_address = self.choose_validator()
        validator = self.validators[validator_address]

        valid_tasks = []

        for task in tasks:

            utility = self.calculate_utility(task.task_type)

            proof = self.generate_proof(task, validator)

            if self.verify_proof(proof):

                task.completed = True
                task.proof = proof

                validator.reward(utility)

                valid_tasks.append(task)

            else:
                validator.penalize()

        block = Block(
            len(self.chain),
            self.chain[-1].hash,
            valid_tasks,
            validator.address
        )

        self.chain.append(block)

        return block

    def network_stats(self):

        stats = {
            "blocks": len(self.chain),
            "validators": len(self.validators),
            "pending_tasks": len(self.task_pool)
        }

        return stats


if __name__ == "__main__":

    blockchain = PoUBlockchain()

    nodes = [
        Validator("node_A"),
        Validator("node_B"),
        Validator("node_C"),
        Validator("node_D")
    ]

    for n in nodes:
        blockchain.register_validator(n)

    blockchain.add_task("ai_training", "model_dataset_A")
    blockchain.add_task("scientific_compute", "protein_simulation")
    blockchain.add_task("data_processing", "satellite_data")
    blockchain.add_task("storage", "climate_archive")
    blockchain.add_task("general_compute", "math_simulation")

    for i in range(3):

        block = blockchain.produce_block()

        if block:
            print("Block", block.index, "produced by", block.validator)
            print("Tasks:", [t.task_id for t in block.tasks])
            print("Hash:", block.hash)
            print()

    print("Network Stats")
    print(blockchain.network_stats())
