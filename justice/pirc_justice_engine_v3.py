import time
import uuid


class JusticeCase:

    def __init__(self, accused_node, violation):

        self.case_id = str(uuid.uuid4())
        self.accused_node = accused_node
        self.violation = violation
        self.timestamp = time.time()
        self.votes = {}
        self.resolved = False
        self.result = None


class PiRCJusticeEngineV3:

    def __init__(self):

        self.cases = {}
        self.reputation = {}
        self.validators = set()

        self.penalties = {
            "invalid_block": 25,
            "fake_utility": 20,
            "double_spend": 30,
            "spam": 10
        }

    def register_validator(self, node_id):

        self.validators.add(node_id)

        if node_id not in self.reputation:
            self.reputation[node_id] = 100

    def create_case(self, accused_node, violation):

        case = JusticeCase(accused_node, violation)

        self.cases[case.case_id] = case

        return case.case_id

    def vote(self, validator_id, case_id, vote):

        if validator_id not in self.validators:
            return "not validator"

        case = self.cases.get(case_id)

        if not case:
            return "case not found"

        case.votes[validator_id] = vote

        return "vote recorded"

    def resolve_case(self, case_id):

        case = self.cases.get(case_id)

        if not case:
            return "case not found"

        guilty = sum(1 for v in case.votes.values() if v == "guilty")
        innocent = sum(1 for v in case.votes.values() if v == "innocent")

        if guilty > innocent:

            self.apply_penalty(case.accused_node, case.violation)

            case.result = "guilty"

        else:

            case.result = "innocent"

        case.resolved = True

        return case.result

    def apply_penalty(self, node_id, violation):

        penalty = self.penalties.get(violation, 10)

        if node_id not in self.reputation:
            self.reputation[node_id] = 100

        self.reputation[node_id] -= penalty

        if self.reputation[node_id] < 0:
            self.reputation[node_id] = 0

    def slash_validator(self, node_id, amount):

        if node_id not in self.reputation:
            return

        self.reputation[node_id] -= amount

        if self.reputation[node_id] < 0:
            self.reputation[node_id] = 0

    def reward_validator(self, node_id, score=5):

        if node_id not in self.reputation:
            self.reputation[node_id] = 100

        self.reputation[node_id] += score

    def flagged_nodes(self):

        return {
            n: rep
            for n, rep in self.reputation.items()
            if rep < 50
        }

    def justice_stats(self):

        return {
            "total_cases": len(self.cases),
            "validators": len(self.validators),
            "flagged_nodes": len(self.flagged_nodes())
        }
