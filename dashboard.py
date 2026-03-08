from pou_blockchain import Blockchain, Wallet

blockchain = Blockchain()

nodes = [
    Wallet("node_A"),
    Wallet("node_B"),
    Wallet("node_C")
]

for n in nodes:
    blockchain.register_validator(n)

tasks = [
    ("AI training", "ai_training"),
    ("Protein simulation", "compute"),
    ("Climate storage", "storage"),
    ("Genome processing", "data_processing")
]

for t in tasks:
    blockchain.add_block(t[0], t[1])

print("\n=== Proof of Utility Network Stats ===\n")

for addr, wallet in blockchain.validators.items():
    print(addr, "utility:", wallet.utility_score)

print("\nTotal blocks:", len(blockchain.chain))
