import threading
import time
import random

class Customer(threading.Thread):
    def __init__(self, customerid, shared_resources):
        super().__init__()
        self.customerid = customerid
        self.shared_resources=shared_resources
        self.door = shared_resources['door']
        self.teller_ready= shared_resources['teller_ready']

        self.transaction_type = None
        self.transaction_amount = None
        self.current_teller = None

        def run(self):
            self.determine_transaction()
        def determine_transaction():
            self.transaction_type = random.choice(['Deposit','Withdraw'])
            self.transaction_amount = random.randint(10,5000)
            print(f'Customer {self.customerid} wants to conduct a {self.transaction_type} for {self.transaction_amount}')
            
    