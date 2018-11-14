from PCB_utils import *
from control import *
from PCB import *

def SRT(processes, io_duration, context_switch_penalty):
    #processes is a list of all processes
    processes.sort(key=sort_service_time) 
    #create empty queue
    process_queue=queue.Queue()
    #time variable, process in processes
    t,i=0,0
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
            #initializion for each process
            start_dic[processes[i].key]=t
            process_queue.put(processes[i])
            i+=1
            not_beginning=True
            print("i",i)
        process_queue_list = list(process_queue.queue)
        process_queue_list.sort(key=sort_service_time)
            
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


        if current_process !=None and not process_queue_list == [] and (int(current_process.service_time) > int(process_queue_list[0].service_time)):
            process_queue.put(current_process)
            current_process == process_queue.get()
            t+=context_switch_penalty

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

def sort_service_time(process):
    return process.service_time
