import numpy as np

class RewardDistribution:

    def __init__(self, total_rewards, users):

        self.total_rewards = total_rewards
        self.users = users

    def distribute(self):

        base_reward = self.total_rewards / self.users

        rewards = np.random.normal(base_reward, base_reward*0.2, self.users)

        rewards = np.clip(rewards, 0, None)

        return rewards

    def stats(self):

        rewards = self.distribute()

        return {
            "mean": float(np.mean(rewards)),
            "max": float(np.max(rewards)),
            "min": float(np.min(rewards))
        }


if __name__ == "__main__":

    sim = RewardDistribution(
        total_rewards=1000000,
        users=100000
    )

    print(sim.stats())
