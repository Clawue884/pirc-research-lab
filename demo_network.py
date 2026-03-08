from pou_blockchain import Blockchain, Wallet

blockchain = Blockchain()

# create validators
alice = Wallet("alice_node")
bob = Wallet("bob_node")
charlie = Wallet("charlie_node")

blockchain.register_validator(alice)
blockchain.register_validator(bob)
blockchain.register_validator(charlie)

# simulate work
blockchain.add_block("AI model training", "ai_training")
blockchain.add_block("Scientific compute", "compute")
blockchain.add_block("Store climate data", "storage")
blockchain.add_block("Process satellite data", "data_processing")

# show blockchain
for block in blockchain.chain:
    print("Block:", block.index)
    print("Validator:", block.validator)
    print("Utility:", block.utility_score)
    print("Hash:", block.hash)
    print("-----")
