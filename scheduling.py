from PCB_utils import *
from control import *
from PCB import *

def RoundRobin(processes,io_duration, quantum, context_switch_penalty):

    #not passing in correct quantum, context_switch_pentaly and io_duration on
    #automatic reading of files
    
    #processes is a list of all processes
    processes.sort(key=sort_time_available)
    #create empty queue
    process_queue=queue.Queue()
    #time variable, process in processes
    t,i=0,0
    #q=quantum
    current_process=None
    not_beginning=False

    #a list for processes with io events happening
    io_happening=[]
    #a queue for processes with io events finished
    io_finished_queue=queue.Queue()

    #calculate throughput
    throughput=len(processes)

    #calculate turnaround time
    turnaround_time=0
    turnaround_list=[]
    start_dic={}
    end_dic={}
    

    #while loop to run until processes complete
    while not(not_beginning and process_queue.empty() and io_finished_queue.empty() and io_happening==[] and current_process==None):
        #add processes to queue if they become available
        print('t',t)
        while i<len(processes) and int(processes[i].arrival_time)<=t:
            #initialize quantum for each process
            processes[i].quantum=quantum
            start_dic[processes[i].key]=t
            process_queue.put(processes[i])
            i+=1
            not_beginning=True
            print("i",i)
            
        #get a new process if there is none, set up all variables needed
        if current_process==None and not (process_queue.empty() and io_finished_queue.empty()):
            #use a process that finished it's io if there are any waiting
            if not io_finished_queue.empty():
                t+=context_switch_penalty
                current_process=io_finished_queue.get()
            else:
                t+=context_switch_penalty
                current_process=process_queue.get()
            #print('got process', current_process.key)
            #print(current_process.io_counter,current_process.io_freq, current_process.io_running)

        #for each process with an io event running, decrement the length of time to completion
        if io_happening!=[]:
            for process in io_happening:
                print('io running', int(process.io_counter) -1, "clocks left")
                process.io_counter=int(process.io_counter)-1
                if process.io_counter==0:
                    print("io event ending")
                    process.io_counter=process.io_freq
                    io_finished_queue.put(process)
                    io_happening.remove(process)
                        
        #run current process for 1 time unit
        if current_process!=None:
            print("current Process", current_process.key)
            #if io_counter is 0 then either an io event is ending or an io event should start
            #if io_running is True then the io event should end, if it is False an event should begin
            if current_process.io_counter==0 and current_process.io_freq!=0:
                print("io event starting")
                io_happening.append(current_process)
                current_process.io_counter=io_duration
                current_process=None
                #get a new process
                #use a process that finished it's io if there are any waiting
                if not io_finished_queue.empty():
                    t+=context_switch_penalty
                    current_process=io_finished_queue.get()
                elif not process_queue.empty():
                    t+=context_switch_penalty
                    current_process=process_queue.get()
        if current_process!=None:          
            #run current process
            print('program running', current_process.key, int(current_process.service_time) -1, "clocks left")
            current_process.service_time=int(current_process.service_time)-1
            current_process.io_counter=int(current_process.io_counter)-1
            #one time unit was used on either the io event or the current process
            #so decrement quantum
            current_process.quantum-=1
            #print('q',q)
            #if quantum runs out kick current program
            if current_process.quantum==0:
                print("quantum used")
                current_process.quantum=quantum
                #if the current process isn't done, send it back to the end of the queue
                if current_process.service_time>0:
                    t+=context_switch_penalty
                    process_queue.put(current_process)
                    current_process=None
                
            #if process ends, remove it, and reset all relevant variables, adn add
            #contact switch penalty
            if current_process !=None and current_process.service_time==0:
                end_dic[current_process.key]=t
                print(current_process.key, 'is done')
                t+=context_switch_penalty
                current_process=None
                
        #increment time at each iteration
        print('\n')
        t+=1
        
    for elem in start_dic:
        turnaround_list.append(end_dic[elem]-start_dic[elem])
    for i in turnaround_list:
        turnaround_time+=i
    #throughput is the length of processes as of now
    turnaround_time=turnaround_time/throughput
    print("Average Turnaround Time: ",turnaround_time)
    
    throughput=throughput/(t-1)
    print("Throughput: ",throughput)

    
def sort_time_available(process):
    return process.arrival_time


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

    front=None
    
    #a list for processes with io events happening
    io_happening=[]
    #a queue for processes with io events finished
    io_finished_queue=queue.Queue()
    
    #calculate throughput
    throughput=len(processes)

    #calculate turnaround time
    turnaround_time=0
    turnaround_list=[]
    start_dic={}
    end_dic={}
    for i in processes:
        start_dic[i.key]=int(i.arrival_time)
        

    while not (process_queue.empty() and io_finished_queue.empty() and io_happening==[] and front==None):
        # serve the process at front of the io queue, then the process queue
        if front==None:
            if not io_finished_queue.empty():
                current_time += context_switch_penalty
                front = io_finished_queue.get()
            
            elif not process_queue.empty():
                current_time += context_switch_penalty
                front = process_queue.get()

        # the system is idle until the process arrives
        if front!=None:
            if current_time < int(front.arrival_time):
                print(current_time, "idle", sep="\t")

            while (current_time < int(front.arrival_time)):
                current_time += 1

        #run io events
        if io_happening!=[]:
            for process in io_happening:
                print('io running', int(process.io_counter) -1, "clocks left")
                process.io_counter=int(process.io_counter)-1
                if process.io_counter==0:
                    print("io event ending")
                    process.io_counter=process.io_freq
                    io_finished_queue.put(process)
                    io_happening.remove(process)
                    
        # run program for one iteration
        if front!=None:
            # serve the front process
            front.service_time = int(front.service_time)-1
            front.io_counter= int(front.io_counter)-1
            print(current_time, "running process"+str(front.key), sep="\t")
            
            # check for io event
            if (int(front.io_freq) > 0 and front.service_time > 0 and front.io_counter==0):
                current_time += context_switch_penalty

                # announce io event
                print(current_time, "io", sep="\t")
                front.io_counter=io_duration
                io_happening.append(front)
                front=None

        if front!=None and front.service_time==0:
            print(current_time, "process "+str(front.key)+" has finished", sep="\t")
            #for turnaround
            end_dic[str(front.key)]=current_time
            # switch to either idle or the next process
            current_time += context_switch_penalty
            front=None
            
        current_time+=1
        
    print(current_time, "finished", sep="\t")

    for elem in start_dic:
        turnaround_list.append(end_dic[elem]-start_dic[elem])
    for i in turnaround_list:
        turnaround_time+=i
    #throughput is the length of processes as of now
    turnaround_time=turnaround_time/throughput
    print("Average Turnaround Time: ",turnaround_time)
    
    throughput=throughput/(current_time-1)
    print("Throughput: ",throughput)

def rrValues(processes, run_interface, context_switch_penalty = None, quantum = None, io_duration = None):
    if run_interface == 'y':
        print("\nThe data file didn't contain critical values: IO Duration, Quantum, Context Switch Penalty")
        print("\nPlease enter those values below")
        
        io_duration = input("IO duration: ")
        while not int_check(io_duration):
            io_duration = input("IO duration: ")
        
        quantum = input("quantum: ")
        while not int_check(quantum):
            quantum = input("quantum: ")

        context_switch_penalty = input("context switch penalty: ")
        while not int_check(context_switch_penalty):
            context_switch_penalty = input("context switch penalty: ")

    print("\nThe program detected the following variables from the data file: ")
    print("\tio_duration = " + str(io_duration) + "\n\tquantum = " + str(quantum) + "\n\tcontext_switch_penalty = " + str(context_switch_penalty))

    print("\nThe keys of the processes passed in are: ")
    for elem in processes:
        print(elem.getKey())
        
    print("\nType:\n\t\"rr\" to schedule using Round Robin\n\t\"fcfs\" to schedule using First Come First Serve.")
    ans = str_verify("\nI choose: ", "rr,fcfs", lower = 'uh huh')
    if ans == 'rr':
        RoundRobin(processes,int(io_duration), int(quantum), int(context_switch_penalty))
        return 'rr'
    elif ans == 'fcfs':
        FirstComeFirstServe(processes,int(io_duration), int(context_switch_penalty))
        return 'fcfs'

