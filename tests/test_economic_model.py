from economics.economic_stability_simulator import EconomicStabilitySimulator

def test_economic_stability():

    sim = EconomicStabilitySimulator(
        initial_supply=100000,
        reward_rate=0.02,
        burn_rate=0.01,
        users=1000
    )

    history = sim.run(epochs=10)

    assert len(history) == 10
