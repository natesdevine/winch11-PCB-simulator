from PCB_utils import *
from control import *
from PCB import *

def RoundRobin(processes,io_duration, quantum, context_switch_penalty):
    #processes is a list of all processes
    processes.sort(key=sort_time_available)
    #create empty queue
    process_queue=queue.Queue()
    #time variable, process in processes
    t,i=0,0
    q=quantum
    current_process=None
    not_beginning=False

    #while loop to run until processes complete
    while not(not_beginning and process_queue.empty() and current_process==None):
        #add processes to queue if they become available
        print('t',t)
        while i<len(processes) and int(processes[i].time_created)<=t:
            process_queue.put(processes[i])
            i+=1
            not_beginning=True
            print("i",i)
            
        #get a new process if there is none, set up all variables needed
        if current_process==None and not process_queue.empty():
            t+=context_switch_penalty
            current_process=process_queue.get()
            #print('got process', current_process.key)
            #print(current_process.io_counter,current_process.io_freq, current_process.io_running)
            
        #run current process for 1 time unit
        if current_process!=None:
            print("current Process", current_process.key)
            #if io_counter is 0 then either an io event is ending or an io event should start
            #if io_running is True then the io event should end, if it is False an event should begin
            if current_process.io_counter==0 and current_process.io_freq!=0:
                if current_process.io_running==False:
                    print("io event starting")
                    current_process.io_running=True
                    current_process.io_counter=io_duration
                elif current_process.io_running==True:
                    print("io event ending")
                    current_process.io_running=False
                    current_process.io_counter=current_process.io_freq
                    
            #if an io event is running, use one time unit on it
            if current_process.io_running==True:
                print('io running', int(current_process.io_counter) -1, "clocks left")
                current_process.io_counter=int(current_process.io_counter)-1
                
            #if no io event, run process
            if current_process.io_running==False:
                print('program running', current_process.key, int(current_process.service_time) -1, "clocks left")
                current_process.service_time=int(current_process.service_time)-1
                current_process.io_counter=int(current_process.io_counter)-1
            #one time unit was used on either the io event or the current process
            #so decrement quantum
            q-=1
            #print('q',q)
            #if quantum runs out kick current program
            if q==0:
                print("quantum used")
                q=quantum
                #if the current process isn't done, send it back to the end of the queue
                if current_process.service_time>0:
                    t+=context_switch_penalty
                    process_queue.put(current_process)
                    current_process=None
                
            #if process ends, remove it, and reset all relevant variables, adn add
            #contact switch penalty
            if current_process !=None and current_process.service_time==0:
                print(current_process.key, 'is done')
                t+=context_switch_penalty
                current_process=None
                q=quantum
                
        #increment time at each iteration
        print('\n\n')
        t+=1
            
def sort_time_available(process):
    return process.time_created


#First come first serve
def FirstComeFirstServe(processes, io_duration, context_switch_penalty):
    
    processes.sort(key=sort_time_available)
    process_queue=queue.Queue()
    for i in processes:
        process_queue.put(i)
    
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
        time_created = int(front.getTimeCreated())
        service_time = int(front.getServiceTime())
        io_freq = int(front.getIOFreq())

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

def rrValues(processes, run_interface, io_duration = None, quantum = None, context_switch_penalty = None):
    if run_interface == 'y':
        print("\nPlease enter schedule values")
        
        io_duration = input("\nIO duration: ")
        while not int_check(io_duration):
            io_duration = input("IO duration: ")
        
        quantum = input("\nquantum: ")
        while not int_check(quantum):
            quantum = input("quantum: ")

        context_switch_penalty = input("\ncontext switch penalty: ")
        while not int_check(context_switch_penalty):
            context_switch_penalty = input("context switch penalty: ")

    print("\nThe program detected the following variables from the data file: ")
    print("\tio_duration = " + str(io_duration) + "\n\tquantum = " + str(quantum) + "\n\tcontext_switch_penalty = " + str(context_switch_penalty))

    print("\nThe processes passed in are: ")
    for elem in processes:
        print(elem.getKey())
        
    print("\nType:\n\t\"rr\" to schedule using Round Robin\n\t\"fcfs\" to schedule using First Come First Serve.")
    ans = str_verify("\nI choose: ", "rr,fcfs", lower = 'uh huh')
    if ans == 'rr':
        RoundRobin(processes,int(io_duration), int(quantum), int(context_switch_penalty))
    elif ans == 'fcfs':
        FirstComeFirstServe(processes,int(io_duration), int(context_switch_penalty))