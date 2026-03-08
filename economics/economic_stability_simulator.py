import numpy as np

class EconomicStabilitySimulator:

    def __init__(self,
                 initial_supply=1000000,
                 reward_rate=0.02,
                 burn_rate=0.005,
                 users=100000):

        self.supply = initial_supply
        self.reward_rate = reward_rate
        self.burn_rate = burn_rate
        self.users = users

        self.history = []

    def simulate_epoch(self):

        rewards = self.supply * self.reward_rate
        burned = self.supply * self.burn_rate

        self.supply = self.supply + rewards - burned

        avg_reward = rewards / self.users

        self.history.append({
            "supply": self.supply,
            "avg_reward": avg_reward
        })

    def run(self, epochs=100):

        for _ in range(epochs):
            self.simulate_epoch()

        return self.history


if __name__ == "__main__":

    sim = EconomicStabilitySimulator(
        initial_supply=1000000,
        reward_rate=0.02,
        burn_rate=0.01,
        users=200000
    )

    result = sim.run(epochs=50)

    print("Final Supply:", result[-1]["supply"])
