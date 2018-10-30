'''
File: scheduling.py
Author:	Khanh Nghiem, Sam Barnes
Description: Implementation of different scheduling algorithms for the OS simulator
Created: 29-Oct-2018
Last updated: 29-Oct-2018
'''

from PCB_utils import *
import queue

# First come first serve
# @param: a list of processes
def fcfs(process_queue):
    while not process_queue.empty():
        



def test():
    p1 = Process(key=1, active='True', priority=0, time_created=2, mode=0, service_time=6, io_freq=3)
    p2 = Process(key=2, active='True', priority=0, time_created=3, mode=0, service_time=7, io_freq=0)
    p3 = Process(key=3, active='True', priority=0, time_created=3, mode=0, service_time=4, io_freq=5)
    p4 = Process(key=4, active='True', priority=0, time_created=4, mode=0, service_time=8, io_freq=3)
    p5 = Process(key=5, active='True', priority=0, time_created=8, mode=0, service_time=2, io_freq=1)
    p6 = Process(key=6, active='True', priority=0, time_created=6, mode=0, service_time=5, io_freq=0)

    process_queue = Queue()
    process_queue.put(p1)
    process_queue.put(p2)
    process_queue.put(p3)
    process_queue.put(p4)
    process_queue.put(p5)
    process_queue.put(p6)

    fcfs(process_queue)
