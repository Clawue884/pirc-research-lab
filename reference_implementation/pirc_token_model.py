class PIRCToken:

    def __init__(self, total_supply):

        self.total_supply = total_supply
        self.balances = {}

    def mint(self, user, amount):

        if amount > self.total_supply:
            raise ValueError("Supply exceeded")

        self.balances[user] = self.balances.get(user, 0) + amount
        self.total_supply -= amount

    def balance_of(self, user):

        return self.balances.get(user, 0)
