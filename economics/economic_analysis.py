import matplotlib.pyplot as plt
from economic_stability_simulator import EconomicStabilitySimulator

sim = EconomicStabilitySimulator(
    initial_supply=1000000,
    reward_rate=0.02,
    burn_rate=0.01,
    users=200000
)

history = sim.run(epochs=100)

supply = [h["supply"] for h in history]

plt.plot(supply)

plt.title("PiRC Economic Stability Simulation")
plt.xlabel("Epoch")
plt.ylabel("Total Supply")

plt.show()
