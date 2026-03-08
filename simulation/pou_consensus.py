"""
Proof-of-Utility (PoU) Consensus Simulator
Advanced consensus experiment for PiRC Research Lab

Utility-based validator selection using:
- Trust score
- Uptime contribution
- Compute contribution
- Sybil resistance penalty
"""

import random
import numpy as np
import networkx as nx
from dataclasses import dataclass


@dataclass
class Node:
    node_id: int
    trust: float
    uptime: float
    compute: float
    sybil_flag: bool = False

    def utility_score(self):
        """
        Core Proof-of-Utility scoring function
        """

        trust_weight = 0.4
        uptime_weight = 0.3
        compute_weight = 0.3

        score = (
            self.trust * trust_weight
            + self.uptime * uptime_weight
            + self.compute * compute_weight
        )

        if self.sybil_flag:
            score *= 0.3

        return score


class ProofOfUtilityConsensus:

    def __init__(self, num_nodes=100, sybil_ratio=0.1):
        self.num_nodes = num_nodes
        self.sybil_ratio = sybil_ratio
        self.nodes = []
        self.graph = nx.Graph()

        self._generate_network()

    def _generate_network(self):
        """
        Create simulated network with trust relationships
        """

        for i in range(self.num_nodes):

            is_sybil = random.random() < self.sybil_ratio

            node = Node(
                node_id=i,
                trust=random.uniform(0.2, 1.0) if not is_sybil else random.uniform(0.05, 0.3),
                uptime=random.uniform(0.5, 1.0),
                compute=random.uniform(0.3, 1.0),
                sybil_flag=is_sybil
            )

            self.nodes.append(node)
            self.graph.add_node(i)

        # random trust edges
        for _ in range(self.num_nodes * 3):
            a = random.randint(0, self.num_nodes - 1)
            b = random.randint(0, self.num_nodes - 1)
            if a != b:
                self.graph.add_edge(a, b)

    def select_validator(self):
        """
        Select validator using utility-weighted random choice
        """

        utilities = np.array([node.utility_score() for node in self.nodes])
        probabilities = utilities / utilities.sum()

        validator_index = np.random.choice(len(self.nodes), p=probabilities)
        return self.nodes[validator_index]

    def simulate_epoch(self):

        validator = self.select_validator()

        consensus_success = not validator.sybil_flag

        return {
            "validator_id": validator.node_id,
            "utility_score": validator.utility_score(),
            "is_sybil": validator.sybil_flag,
            "consensus_success": consensus_success
        }

    def run_simulation(self, epochs=50):

        results = []

        for _ in range(epochs):
            result = self.simulate_epoch()
            results.append(result)

        success_rate = sum(r["consensus_success"] for r in results) / epochs

        return {
            "epochs": epochs,
            "success_rate": success_rate,
            "results": results
        }


if __name__ == "__main__":

    simulator = ProofOfUtilityConsensus(
        num_nodes=200,
        sybil_ratio=0.15
    )

    output = simulator.run_simulation(epochs=100)

    print("Proof-of-Utility Simulation Results")
    print("----------------------------------")
    print("Epochs:", output["epochs"])
    print("Consensus Success Rate:", round(output["success_rate"], 3))
