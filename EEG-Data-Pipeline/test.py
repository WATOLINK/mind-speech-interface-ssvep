'''
    Multiprocessing Example - Run 2 functions simultaneously at the same time 

'''
from multiprocessing import Process, Queue
from time import time, sleep
import sys

def Function_1( q ):
    print('Process 1 Done')
    
def Function_2( q ):      
    sleep(3)
    print('Process 2 Done')

if __name__ == '__main__':

    q = Queue()

    # Initialize
    process_1 = Process( target=Function_1,  args=( q, ) )
    process_2 = Process( target=Function_2,  args=( q, ) )

    # Start 
    process_1.start()
    process_2.start()

    process_1.join()
    process_2.join()
