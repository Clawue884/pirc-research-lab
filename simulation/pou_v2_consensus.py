"""
Proof-of-Utility v2 Consensus Simulator
Research-grade model for PiRC Research Lab

Features
- Utility based validator selection
- Trust graph reputation propagation
- Sybil cluster resistance
- Committee-based consensus
- Monte Carlo simulation
"""

import random
import numpy as np
import networkx as nx


class Node:

    def __init__(self, node_id, sybil=False):
        self.id = node_id
        self.sybil = sybil

        self.trust = random.uniform(0.2, 1.0) if not sybil else random.uniform(0.01, 0.3)
        self.uptime = random.uniform(0.5, 1.0)
        self.compute = random.uniform(0.3, 1.0)

        self.utility = 0

    def compute_utility(self):

        trust_weight = 0.45
        uptime_weight = 0.30
        compute_weight = 0.25

        score = (
            self.trust * trust_weight +
            self.uptime * uptime_weight +
            self.compute * compute_weight
        )

        if self.sybil:
            score *= 0.2

        self.utility = score
        return score


class ProofOfUtilityV2:

    def __init__(self, nodes=200, sybil_ratio=0.15):

        self.nodes = []
        self.graph = nx.Graph()

        for i in range(nodes):

            sybil = random.random() < sybil_ratio
            node = Node(i, sybil)

            self.nodes.append(node)
            self.graph.add_node(i)

        self._create_trust_network(nodes)

    def _create_trust_network(self, nodes):

        edges = nodes * 4

        for _ in range(edges):

            a = random.randint(0, nodes-1)
            b = random.randint(0, nodes-1)

            if a != b:
                self.graph.add_edge(a, b)

    def propagate_trust(self):

        """
        EigenTrust-like reputation propagation
        """

        adjacency = nx.to_numpy_array(self.graph)
        trust_vector = np.array([n.trust for n in self.nodes])

        for _ in range(5):
            trust_vector = adjacency @ trust_vector
            trust_vector = trust_vector / np.linalg.norm(trust_vector)

        for i, node in enumerate(self.nodes):
            node.trust = float(trust_vector[i])

    def compute_utilities(self):

        for node in self.nodes:
            node.compute_utility()

    def select_committee(self, size=10):

        utilities = np.array([n.utility for n in self.nodes])
        probabilities = utilities / utilities.sum()

        indices = np.random.choice(
            len(self.nodes),
            size=size,
            replace=False,
            p=probabilities
        )

        committee = [self.nodes[i] for i in indices]
        return committee

    def run_consensus(self):

        committee = self.select_committee()

        votes = []

        for node in committee:

            if node.sybil:
                vote = random.random() < 0.4
            else:
                vote = random.random() < 0.9

            votes.append(vote)

        consensus = sum(votes) > len(votes) * 0.66

        return consensus, committee

    def simulate(self, epochs=100):

        success = 0

        for _ in range(epochs):

            self.propagate_trust()
            self.compute_utilities()

            consensus, committee = self.run_consensus()

            if consensus:
                success += 1

        return {
            "epochs": epochs,
            "success_rate": success / epochs
        }


if __name__ == "__main__":

    simulator = ProofOfUtilityV2(
        nodes=300,
        sybil_ratio=0.20
    )

    result = simulator.simulate(epochs=200)

    print("Proof-of-Utility v2 Results")
    print("--------------------------")
    print("Epochs:", result["epochs"])
    print("Consensus Success Rate:", round(result["success_rate"], 3))
