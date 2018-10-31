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
        while i<len(processes) and processes[i].time_created<=t:
            process_queue.put(processes[i])
            i+=1
            not_beginning=True
            print("i",i)
            
        #get a new process if there is none, set up all variables needed
        if current_process==None and not process_queue.empty():
            t+=context_switch_penalty
            current_process=process_queue.get()
            print('got process', current_process.key)
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
                print('io running', current_process.io_counter -1, "clocks left")
                current_process.io_counter-=1
                
            #if no io event, run process
            if current_process.io_running==False:
                print('program running', current_process.key, current_process.service_time -1, "clocks left")
                current_process.service_time-=1
                current_process.io_counter-=1
            #one time unit was used on either the io event or the current process
            #so decrement quantum
            q-=1
            print('q',q)
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
        print('t',t)
            
def sort_time_available(process):
    return process.time_created
            
def rrValues(processes):
    print("\nGUCCI GANG MAN HERE, GIVE ME DEM VALUES")
    
    io_duration = input("\nGIVE ME THAT io_duration: ")
    while not int_check(io_duration):
        io_duration = input("GIVE ME THAT io_duration: ")
    
    quantum = input("\nGIVE ME THAT quantum: ")
    while not int_check(quantum):
        quantum = input("GIVE ME THAT quantum: ")

    context_switch_penalty = input("\nGIVE ME THAT context_switch_penalty: ")
    while not int_check(context_switch_penalty):
        context_switch_penalty = input("GIVE ME THAT context_switch_penalty: ")

    print("\nTHE PROCESSES passed in ARE: ")
    for elem in processes:
        print(elem.getKey())

    ans = str_verify("\nYOU WANNA TEST RoundRobin (Y/N)?: ", "y,n", lower = 'uh huh')
    if ans == 'y':
        RoundRobin(processes,io_duration, quantum, context_switch_penalty)
    elif ans == 'n':
        ans = str_verify("\nALRIGHT DAWG, YOU WANNA RESTART (y/n)?: ", "y,n", lower = 'yeet') 
        if ans == 'y':
            control_script()
        else:
            print("\nALRIGHT DAWG, THE PROGRAM FINNA DIE NOW")
            sys.exit()
