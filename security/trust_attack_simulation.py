from simulation.trust_graph_simulator import TrustGraphSimulator


def simulate_trust_attack():

    results = []

    for sybil_ratio in [0.01, 0.05, 0.1, 0.2]:

        sim = TrustGraphSimulator(
            total_nodes=10000,
            avg_connections=5,
            sybil_ratio=sybil_ratio
        )

        metrics = sim.run()

        results.append({
            "sybil_ratio": sybil_ratio,
            "edges": metrics["edges"],
            "avg_degree": metrics["avg_degree"]
        })

    return results


if __name__ == "__main__":

    print(simulate_trust_attack())
