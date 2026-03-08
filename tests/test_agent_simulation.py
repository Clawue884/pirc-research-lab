from simulation.agent_based_network import PiNetworkAgentSimulation

def test_agent_simulation():

    sim = PiNetworkAgentSimulation(
        total_agents=1000,
        sybil_ratio=0.1
    )

    history = sim.run(epochs=10)

    assert len(history) == 10
