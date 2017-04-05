class Copytask(object):



    def __init__(self, id):
        self.id = id



    def __init__(self, name, balance=0.0):
            """Return a Customer object whose name is *name* and starting
            balance is *balance*."""
            self.name = name
            self.balance = balance

    def withdraw(self, amount):
            """Return the balance remaining after withdrawing *amount*
            dollars."""
            if amount > self.balance:
                raise RuntimeError('Amount greater than available balance.')
            self.balance -= amount
            return self.balance
