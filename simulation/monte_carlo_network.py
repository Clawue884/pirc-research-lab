import random
import numpy as np

class PiNetworkSimulation:

    def __init__(self, users=10000, sybil_ratio=0.1):
        self.users = users
        self.sybil_ratio = sybil_ratio
        self.honest_users = int(users * (1 - sybil_ratio))
        self.sybil_users = int(users * sybil_ratio)

    def simulate_epoch(self):

        rewards = []

        for _ in range(self.honest_users):
            reward = random.gauss(1.0, 0.2)
            rewards.append(max(reward, 0))

        for _ in range(self.sybil_users):
            reward = random.gauss(0.3, 0.1)
            rewards.append(max(reward, 0))

        return np.mean(rewards)

    def run(self, epochs=100):

        results = []

        for _ in range(epochs):
            results.append(self.simulate_epoch())

        return np.mean(results)


if __name__ == "__main__":

    sim = PiNetworkSimulation(users=100000, sybil_ratio=0.15)

    result = sim.run(epochs=500)

    print("Average reward per epoch:", result)
