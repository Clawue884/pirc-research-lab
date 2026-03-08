import random


class Node:

    def __init__(self, node_id, quorum_size=3):

        self.node_id = node_id
        self.quorum_slice = set()
        self.quorum_size = quorum_size

    def add_trust(self, node):

        if len(self.quorum_slice) < self.quorum_size:
            self.quorum_slice.add(node)

    def vote(self):

        return random.choice([True, True, True, False])


class ConsensusSimulator:

    def __init__(self, total_nodes=1000):

        self.total_nodes = total_nodes
        self.nodes = []

        self.initialize_nodes()
        self.build_quorum()

    def initialize_nodes(self):

        for i in range(self.total_nodes):
            self.nodes.append(Node(i))

    def build_quorum(self):

        for node in self.nodes:

            while len(node.quorum_slice) < node.quorum_size:

                peer = random.choice(self.nodes)

                if peer != node:
                    node.add_trust(peer)

    def run_round(self):

        votes = []

        for node in self.nodes:
            votes.append(node.vote())

        approval = sum(votes) / len(votes)

        return approval > 0.66

    def simulate(self, rounds=20):

        results = []

        for _ in range(rounds):
            results.append(self.run_round())

        return results


if __name__ == "__main__":

    sim = ConsensusSimulator(total_nodes=2000)

    result = sim.simulate(rounds=30)

    print("Consensus success rate:", sum(result)/len(result))
