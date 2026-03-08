import random
import networkx as nx


class TrustGraphSimulator:

    def __init__(self,
                 total_nodes=10000,
                 avg_connections=5,
                 sybil_ratio=0.1):

        self.total_nodes = total_nodes
        self.avg_connections = avg_connections
        self.sybil_ratio = sybil_ratio

        self.graph = nx.Graph()
        self.sybil_nodes = set()

        self.initialize_nodes()

    def initialize_nodes(self):

        for i in range(self.total_nodes):

            self.graph.add_node(i)

            if random.random() < self.sybil_ratio:
                self.sybil_nodes.add(i)

    def create_connections(self):

        for node in self.graph.nodes:

            for _ in range(self.avg_connections):

                target = random.randint(0, self.total_nodes - 1)

                if node != target:
                    self.graph.add_edge(node, target)

    def trust_metrics(self):

        degree_centrality = nx.degree_centrality(self.graph)

        avg_degree = sum(dict(self.graph.degree()).values()) / self.total_nodes

        return {
            "nodes": self.total_nodes,
            "edges": self.graph.number_of_edges(),
            "avg_degree": avg_degree,
            "sybil_nodes": len(self.sybil_nodes)
        }

    def run(self):

        self.create_connections()

        return self.trust_metrics()


if __name__ == "__main__":

    sim = TrustGraphSimulator(
        total_nodes=20000,
        avg_connections=4,
        sybil_ratio=0.15
    )

    result = sim.run()

    print(result)
