class SybilAttackSimulation:

    def __init__(self, attackers, honest):
        self.attackers = attackers
        self.honest = honest

    def attack_success_probability(self):

        total = self.attackers + self.honest

        influence = self.attackers / total

        if influence > 0.5:
            return 1.0

        return influence ** 2


if __name__ == "__main__":

    sim = SybilAttackSimulation(
        attackers=2000,
        honest=8000
    )

    print("Attack probability:", sim.attack_success_probability())
