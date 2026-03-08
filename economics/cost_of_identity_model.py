def cost_of_identity(kyc_cost, infrastructure_cost, identities):

    return identities * (kyc_cost + infrastructure_cost)


def attack_feasibility(cost, potential_gain):

    if potential_gain > cost:
        return True
    return False


if __name__ == "__main__":

    cost = cost_of_identity(
        kyc_cost=5,
        infrastructure_cost=2,
        identities=1000
    )

    gain = 2000

    print("Attack profitable:", attack_feasibility(cost, gain))
