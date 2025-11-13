import threading
import time
import random

class Customer(threading.Thread):
    def __init__(self, customerid, shared):
        super().__init__()
        self.customerid = customerid
        self.shared=shared
        self.door = shared['door']
        self.teller_ready= shared['teller_ready']

        self.transaction_type = None
        self.transaction_amount = None
        self.current_teller = None

    def run(self):
        self.determine_transaction()
        wait_time = random.randint(0,100)/1000.0
        time.sleep(wait_time)
        self.enter()
        self.get_teller()
        print(f'Customer {self.customerid} [Teller {self.current_teller.tellerid}]: Introduces itself to the bank teller')
        self.current_teller.customer_approach.release()
        action_type = "Withdraw" if self.transaction_type == "Withdraw" else "deposit"
        print(f'Customer {self.customerid} [Teller {self.current_teller.tellerid}]: requests {action_type} transaction')
        self.current_teller.transaction_received.release()
        self.current_teller.transaction_complete.acquire()
        print(f"Customer {self.customerid} [Teller {self.current_teller.tellerid}]:the transaction was completed")
        self.leave()
        print(f"Customer {self.customerid} has left the bank")
        
    def determine_transaction(self):
        self.transaction_type = random.choice(['Deposit','Withdraw'])
        self.transaction_amount = random.randint(10,5000)
        print(f'Customer {self.customerid} wants to conduct a {self.transaction_type} for {self.transaction_amount}')                       
    def enter(self):
        print(f'Customer {self.customerid}: entering the bank')
        self.door.acquire()
    def get_teller(self):
        print(f'Customer {self.customerid}: gets into line for Teller ')   
        self.teller_ready.acquire()
        with self.shared['lock']:
            for tellerid, teller in self.shared['tellers'].items():
                self.current_teller = teller
                break
        transaction = {'type': self.transaction_type, 'amount': self.transaction_amount}
        self.current_teller.assign_customer(self.customerid, transaction)
        print(f'Customer {self.customerid}: goes to Teller {self.current_teller.tellerid}')
    def leave(self):
        print(f'Customer {self.customerid}: leaving the Teller and the bank ')
        self.current_teller.customer_left.release()
        self.door.release()