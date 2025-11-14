import threading
import time
from Teller import Teller
from Customer import Customer


num_tellers = 3
num_customers = 50
def main():
    
    print(f"Starting Simulation: TELLERS={num_tellers} CUSTOMERS={num_customers}")

    shared = {
        'manager': threading.Semaphore(1),
        'safe': threading.Semaphore(2),
        'door': threading.Semaphore(2),
        'teller_ready': threading.Semaphore(0),
        'Tellers': {},
        'available': [],
        'lock': threading.Lock(),
        'all_served': False,
    }
    tell_threads = []
    cust_threads=[]

    for i in range(num_tellers):
        tell = Teller(i, shared)
        tell_threads.append(tell)
        tell.start()
        time.sleep(0.1)

    time.sleep(.2)

    for i in range(num_customers):
        cust = Customer(i, shared)
        cust_threads.append(cust)
        cust.start()
        time.sleep(0.1)
    for cust in cust_threads:
        cust.join()
    print("All customers have been served")

    with shared['lock']:
        shared['all_served'] = True

    time.sleep(.5)

    for tell in tell_threads:
        tell.join(timeout = 2)

    print("Bank Simulation Complete")
    print(f"Number of Customers Served: {num_customers}")
    print(f"Number of Tellers: {num_tellers}")
if __name__== "__main__":
    main()