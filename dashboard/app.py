from flask import Flask, jsonify, request
from simulation.global_network_simulator import GlobalNetworkSimulator

app = Flask(__name__)


@app.route("/")
def home():
    return "PiRC Research Lab Dashboard"


@app.route("/simulate", methods=["POST"])
def simulate():

    data = request.json

    nodes = data.get("nodes", 100000)
    sybil = data.get("sybil_ratio", 0.1)
    reward_pool = data.get("reward_pool", 100000)

    sim = GlobalNetworkSimulator(
        total_nodes=nodes,
        sybil_ratio=sybil,
        reward_pool=reward_pool
    )

    result = sim.run(epochs=5)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
