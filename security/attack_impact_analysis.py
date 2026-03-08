from simulation.global_network_simulator import GlobalNetworkSimulator


def analyze_attack():

    results = []

    for sybil_ratio in [0.01, 0.05, 0.1, 0.2]:

        sim = GlobalNetworkSimulator(
            total_nodes=500000,
            sybil_ratio=sybil_ratio,
            reward_pool=100000
        )

        result = sim.run(epochs=5)

        results.append({
            "sybil_ratio": sybil_ratio,
            "avg_reward": result[-1]["avg_reward"]
        })

    return results


if __name__ == "__main__":

    print(analyze_attack())
