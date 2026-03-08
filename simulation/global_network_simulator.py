import numpy as np


class GlobalNetworkSimulator:

    def __init__(self,
                 total_nodes=1000000,
                 sybil_ratio=0.1,
                 reward_pool=100000):

        self.total_nodes = total_nodes
        self.sybil_nodes = int(total_nodes * sybil_ratio)
        self.honest_nodes = total_nodes - self.sybil_nodes

        self.reward_pool = reward_pool

    def simulate_epoch(self):

        honest_rewards = np.random.normal(
            loc=1.0,
            scale=0.2,
            size=self.honest_nodes
        )

        sybil_rewards = np.random.normal(
            loc=0.3,
            scale=0.1,
            size=self.sybil_nodes
        )

        rewards = np.concatenate([honest_rewards, sybil_rewards])

        rewards = np.clip(rewards, 0, None)

        scaled_rewards = rewards / rewards.sum() * self.reward_pool

        return {
            "avg_reward": float(np.mean(scaled_rewards)),
            "max_reward": float(np.max(scaled_rewards)),
            "min_reward": float(np.min(scaled_rewards))
        }

    def run(self, epochs=20):

        results = []

        for _ in range(epochs):
            results.append(self.simulate_epoch())

        return results


if __name__ == "__main__":

    sim = GlobalNetworkSimulator(
        total_nodes=1000000,
        sybil_ratio=0.12,
        reward_pool=500000
    )

    result = sim.run(epochs=10)

    print("Final epoch stats:", result[-1])
