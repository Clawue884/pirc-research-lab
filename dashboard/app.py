from flask import Flask, jsonify, request, render_template
import numpy as np
import networkx as nx
import random

app = Flask(__name__, template_folder=".")

# contoh simulasi sederhana: reward distribusi
def simulate_rewards(nodes=1000, sybil_ratio=0.1, epochs=10):
    rewards = []
    for epoch in range(epochs):
        honest_nodes = int(nodes * (1 - sybil_ratio))
        sybil_nodes = int(nodes * sybil_ratio)

        # reward setiap epoch
        honest_reward = np.random.normal(loc=1.0, scale=0.1, size=honest_nodes)
        sybil_reward = np.random.normal(loc=0.5, scale=0.1, size=sybil_nodes)

        rewards.append({
            "epoch": epoch,
            "honest_avg": float(np.mean(honest_reward)),
            "sybil_avg": float(np.mean(sybil_reward))
        })
    return rewards

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulate-graph", methods=["POST"])
def simulate_graph():
    data = request.json
    nodes = int(data.get("nodes", 1000))
    sybil = float(data.get("sybil_ratio", 0.1))
    epochs = int(data.get("epochs", 10))

    result = simulate_rewards(nodes=nodes, sybil_ratio=sybil, epochs=epochs)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
