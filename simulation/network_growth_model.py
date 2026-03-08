import random
import numpy as np

class NetworkGrowthModel:

    def __init__(self,
                 initial_users=1000,
                 growth_rate=0.05,
                 max_users=1000000):

        self.users = initial_users
        self.growth_rate = growth_rate
        self.max_users = max_users

        self.history = []

    def grow(self):

        new_users = int(self.users * self.growth_rate)

        self.users += new_users

        if self.users > self.max_users:
            self.users = self.max_users

        self.history.append(self.users)

    def simulate(self, steps=100):

        for _ in range(steps):
            self.grow()

        return self.history


if __name__ == "__main__":

    model = NetworkGrowthModel(
        initial_users=10000,
        growth_rate=0.08,
        max_users=10000000
    )

    result = model.simulate(steps=50)

    print("Final users:", result[-1])
