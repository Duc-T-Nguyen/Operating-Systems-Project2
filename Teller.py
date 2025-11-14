import threading
import time
import random

class Teller(threading.Thread):
    def __init__(self, tellerid, shared):
        super().__init__()
        self.tellerid = tellerid
        self.shared = shared
        self.transaction_complete = threading.Semaphore(0)
        self.transaction_received = threading.Semaphore(0)
        self.customer_approach = threading.Semaphore(0)
        self.customer_left = threading.Semaphore(0)

        self.current_id = None
        self.current_transaction=None
        self.shared['Tellers'][tellerid] = self
    def run(self):
        while True:
            print(f'Teller {self.tellerid} []: ready to serve')
            print(f'Teller {self.tellerid } []: waiting for a customer')
            with self.shared['lock']:
                self.shared['available'].append(self.tellerid)
            self.shared['teller_ready'].release()
            if not self.customer_approach.acquire(timeout=0.1):
                if self.shared['all_served']:
                    break
                continue
            cid = self.current_id
            print(f'Teller {self.tellerid} [Customer {cid}]: now serving a customer')
            print(f'Teller {self.tellerid} [Customer {cid}]: asks for a transaction')

            self.transaction_received.acquire()
            transaction_type = self.current_transaction['type']
            transaction_amount = self.current_transaction['amount']
            print(f'Teller {self.tellerid} [Customer {cid}]: handling {transaction_type.lower()} transaction')

            if transaction_type == 'Withdraw':
                print(f'Teller {self.tellerid} [Customer {cid}]: Asking Manager')
                self.shared['manager'].acquire()
                print(f"Teller {self.tellerid } [Customer {cid}]: Getting the Manager's permission for {transaction_amount} amount transaction")
                time.sleep(random.randint(5,30)/1000)
                print(f"Teller {self.tellerid} [Customer {cid}]: Manager approved transaction")
                self.shared['manager'].release()

            print(f'Teller {self.tellerid} [Customer {cid}]: Entering the safe')
            self.shared['safe'].acquire()
            print(f'Teller {self.tellerid} [Customer {cid}]: Now starting the transaction')
            time.sleep(random.randint(1,50)/1000)
            print(f'Teller {self.tellerid} [Customer {cid}]: Done with transaction, now leaving the safe')
            self.shared['safe'].release()

            print(f'Teller {self.tellerid} [Customer {cid}]: finishing {transaction_type} transaction ')
            print(f'Teller {self.tellerid} [Customer {cid}]: coming back to the customer and waiting for the customer to leave')
            self.transaction_complete.release()

            self.customer_left.acquire()

            print(f'Teller {self.tellerid} []: Leaving the bank' )

     

