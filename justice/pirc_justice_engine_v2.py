import time


class JusticeCase:

    def __init__(self, node_id, violation_type):

        self.node_id = node_id
        self.violation_type = violation_type
        self.timestamp = time.time()
        self.resolved = False


class PiRCJusticeEngineV2:

    def __init__(self):

        self.cases = []
        self.penalties = {
            "invalid_block": 20,
            "fake_utility": 15,
            "spam_transactions": 5,
            "double_spend": 25
        }

        self.reputation = {}

    def register_node(self, node_id):

        if node_id not in self.reputation:
            self.reputation[node_id] = 100

    def report_violation(self, node_id, violation):

        case = JusticeCase(node_id, violation)

        self.cases.append(case)

        self.apply_penalty(node_id, violation)

        return case

    def apply_penalty(self, node_id, violation):

        penalty = self.penalties.get(violation, 5)

        if node_id not in self.reputation:
            self.register_node(node_id)

        self.reputation[node_id] -= penalty

        if self.reputation[node_id] < 0:
            self.reputation[node_id] = 0

    def reward_node(self, node_id, score=2):

        if node_id not in self.reputation:
            self.register_node(node_id)

        self.reputation[node_id] += score

    def get_reputation(self, node_id):

        return self.reputation.get(node_id, 0)

    def flagged_nodes(self):

        return {
            n: rep
            for n, rep in self.reputation.items()
            if rep < 50
        }

    def justice_stats(self):

        return {
            "total_cases": len(self.cases),
            "flagged_nodes": len(self.flagged_nodes())
        }
