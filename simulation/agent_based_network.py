import random
import numpy as np

class Agent:

    def __init__(self, agent_id, agent_type="honest"):

        self.agent_id = agent_id
        self.agent_type = agent_type
        self.balance = 0

    def act(self):

        if self.agent_type == "honest":
            return random.uniform(0.8, 1.2)

        if self.agent_type == "sybil":
            return random.uniform(0.1, 0.5)


class PiNetworkAgentSimulation:

    def __init__(self, total_agents=10000, sybil_ratio=0.1):

        self.total_agents = total_agents
        self.sybil_ratio = sybil_ratio

        self.agents = []

        self.initialize_agents()

    def initialize_agents(self):

        for i in range(self.total_agents):

            if random.random() < self.sybil_ratio:
                agent_type = "sybil"
            else:
                agent_type = "honest"

            self.agents.append(Agent(i, agent_type))

    def simulate_epoch(self):

        rewards = []

        for agent in self.agents:

            reward = agent.act()

            agent.balance += reward

            rewards.append(reward)

        return np.mean(rewards)

    def run(self, epochs=50):

        history = []

        for _ in range(epochs):

            avg_reward = self.simulate_epoch()

            history.append(avg_reward)

        return history


if __name__ == "__main__":

    sim = PiNetworkAgentSimulation(
        total_agents=50000,
        sybil_ratio=0.15
    )

    result = sim.run(epochs=30)

    print("Average reward trend:", result[-5:])
