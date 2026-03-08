import random
from simulation.consensus_simulator import ConsensusSimulator


def simulate_consensus_attack():

    results = []

    for nodes in [500, 1000, 2000]:

        sim = ConsensusSimulator(total_nodes=nodes)

        outcome = sim.simulate(rounds=20)

        results.append({
            "nodes": nodes,
            "consensus_rate": sum(outcome)/len(outcome)
        })

    return results


if __name__ == "__main__":

    print(simulate_consensus_attack())
