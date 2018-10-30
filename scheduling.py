'''
File: scheduling.py
Author:	Khanh Nghiem, Sam Barnes
Description: Implementation of different scheduling algorithms for the OS simulator
Created: 29-Oct-2018
Last updated: 29-Oct-2018
'''

from PCB import *
import queue

# First come first serve
# @param: a list of processes
def fcfs(process_queue, io_duration, context_switch_penalty):
    if process_queue.empty():
        print("No process to schedule")
        return

    print("TIME","STATUS/PROCESS", sep="\t")
    current_time = 0

    while not process_queue.empty():
        # serve the process at front of the queue
        front = process_queue.get()

        # get relevant
        key = front.getKey()
        time_created = front.getTimeCreated()
        service_time = front.getServiceTime()
        io_freq = front.getIOFreq()

        # the system is idle until the process arrives
        if current_time < time_created:
            print(current_time, "idle", sep="\t")

        while (current_time < time_created):
            current_time += 1

        # serve the front process
        print(current_time, "process "+str(key), sep="\t")

        # keep track of time served for the process
        time_served = 0

        # loop until process completes
        while (service_time > 0):
            service_time -= 1
            time_served += 1
            current_time += 1

            # check for io event
            if (io_freq > 0 and service_time > 0 and time_served % io_freq == 0):
                if (context_switch_penalty > 0):
                    print(current_time, "switch", sep="\t")
                    current_time += context_switch_penalty

                # announce io event
                print(current_time, "io", sep="\t")
                current_time += io_duration

                # switch back to the process
                if (context_switch_penalty > 0):
                    print(current_time, "switch", sep="\t")
                    current_time += context_switch_penalty
                print(current_time, "process "+str(key), sep="\t")

        # switch to either idle or the next process
        if (context_switch_penalty > 0):
            print(current_time, "switch", sep="\t")
            current_time += context_switch_penalty

    print(current_time, "finished", sep="\t")    


def test():
    p1 = Process(key=1, active='True', priority=0, time_created=2, mode=0, service_time=6, io_freq=3)
    p2 = Process(key=2, active='True', priority=0, time_created=3, mode=0, service_time=7, io_freq=0)
    p3 = Process(key=3, active='True', priority=0, time_created=3, mode=0, service_time=4, io_freq=5)
    p4 = Process(key=4, active='True', priority=0, time_created=4, mode=0, service_time=8, io_freq=3)
    p5 = Process(key=5, active='True', priority=0, time_created=8, mode=0, service_time=2, io_freq=1)
    p6 = Process(key=6, active='True', priority=0, time_created=6, mode=0, service_time=5, io_freq=0)

    process_queue = queue.Queue()
    process_queue.put(p1)
    process_queue.put(p2)
    process_queue.put(p3)
    process_queue.put(p4)
    process_queue.put(p5)
    process_queue.put(p6)

    fcfs(process_queue, io_duration=5, context_switch_penalty=0)
test()
