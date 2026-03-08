from simulation.network_growth_model import NetworkGrowthModel

def test_growth():

    model = NetworkGrowthModel(
        initial_users=1000,
        growth_rate=0.1,
        max_users=100000
    )

    result = model.simulate(steps=10)

    assert result[-1] > 1000
