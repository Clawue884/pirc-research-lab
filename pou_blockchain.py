import hashlib
import json
import time
import random

class Block:
    def __init__(self, index, previous_hash, timestamp, data, validator, utility_score):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.validator = validator
        self.utility_score = utility_score
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "validator": self.validator,
            "utility_score": self.utility_score
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


class Wallet:
    def __init__(self, address):
        self.address = address
        self.utility_score = 0

    def add_utility(self, score):
        self.utility_score += score


class Blockchain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.validators = {}

    def create_genesis_block(self):
        return Block(
            0,
            "0",
            time.time(),
            "Genesis Block",
            "network",
            0
        )

    def get_latest_block(self):
        return self.chain[-1]

    def register_validator(self, wallet):
        self.validators[wallet.address] = wallet

    def calculate_utility(self, work_type):

        utility_table = {
            "compute": 5,
            "storage": 3,
            "ai_training": 10,
            "data_processing": 6
        }

        return utility_table.get(work_type, 1)

    def choose_validator(self):

        weighted_list = []

        for wallet in self.validators.values():
            weighted_list += [wallet.address] * (wallet.utility_score + 1)

        return random.choice(weighted_list)

    def add_block(self, data, work_type):

        validator_address = self.choose_validator()

        wallet = self.validators[validator_address]

        utility_score = self.calculate_utility(work_type)

        wallet.add_utility(utility_score)

        new_block = Block(
            len(self.chain),
            self.get_latest_block().hash,
            time.time(),
            data,
            validator_address,
            utility_score
        )

        self.chain.append(new_block)

        return new_block
