#contains 3 scheduling algorithms as well as their helper functions

from PCB_utils import *
from control import *
from PCB import *
from error_checks import *
import sys

def round_robin(processes,io_duration, quantum, context_switch_penalty, total_memory):
    num_processes=len(processes)
    
    #processes is a list of all processes
    processes.sort(key=sort_time_available)
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

    #########################################NEW STUFF##########################################
    #define memory, a linked list
    memory=linked_list()
    memory.head=node(None, 0, total_memory)
    #create a list of all finished processes
    finished_processes=[]
    all_processes=[]
    #########################################NEW STUFF##########################################
    

    #while loop to run until processes complete
    while len(finished_processes)!=num_processes:
        #add processes to queue if they become available
        print('t',t)
        while i<len(processes) and int(processes[i].arrival_time)<=t:
            #initialize quantum for each process
            all_processes.append(processes[i])
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
                useable_io=enough_memory_queue(io_finished_queue, memory,t,all_processes)
                if useable_io[0]:

                    #print_list(memory)
                    
                    t+=context_switch_penalty
                    ########
                    current_process=useable_io[1]
                    ########
            if not process_queue.empty() and current_process==None:
                useable=enough_memory_queue(process_queue, memory,t,all_processes)
                if useable[0]:

                    #print_list(memory)
                    
                    t+=context_switch_penalty
                    current_process=useable[1]
            
            

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
                remove_process(current_process, memory)
                finished_processes.append(current_process)
                current_process.completion_time=t
                end_dic[current_process.key]=t
                print(current_process.key, 'is done')
                current_process.completion_time=t
                t+=context_switch_penalty
                current_process=None

        if current_process!=None:
            print("current Process", current_process.key)
            #if io_counter is 0 then either an io event is ending or an io event should start
            #if io_running is True then the io event should end, if it is False an event should begin
            if current_process.io_counter==0 and current_process.io_freq!=0:
                print("io event starting")
                io_happening.append(current_process)
                current_process.io_counter=io_duration
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
    print("Throughput: ",throughput,'\n\n')

    output(finished_processes)


#First come first serve
def first_come_first_serve(processes, io_duration, context_switch_penalty, total_memory):
    num_processes=len(processes)
    
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
    

    #########################################NEW STUFF##########################################
    #define memory, a linked list
    memory=linked_list()
    memory.head=node(None, 0, total_memory)
    #create a list of all finished processes
    finished_processes=[]
    all_processes=[]
    #########################################NEW STUFF##########################################

    
    #calculate turnaround time
    turnaround_time=0
    turnaround_list=[]
    start_dic={}
    end_dic={}
    for i in processes:
        start_dic[i.key]=int(i.arrival_time)
        all_processes.append(i)
        

    while len(finished_processes)!=num_processes:
        # serve the process at front of the io queue, then the process queue
        if front==None:
            #use a process that finished it's io if there are any waiting
            if not io_finished_queue.empty():
                useable_io=enough_memory_queue(io_finished_queue, memory,current_time,all_processes)
                if useable_io[0]:

                    #print_list(memory)
                    
                    current_time+=context_switch_penalty
                    ########
                    front=useable_io[1]
                    ########
            if not process_queue.empty() and front==None:
                useable=enough_memory_queue(process_queue, memory,current_time,all_processes)
                if useable[0]:

                    #print_list(memory)
                    
                    current_time+=context_switch_penalty
                    front=useable[1]
            

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
            remove_process(front, memory)
            front.completion_time=current_time
            end_dic[str(front.key)]=current_time
            # switch to either idle or the next process
            front.completion_time=current_time
            finished_processes.append(front)
            current_time += context_switch_penalty
            front=None
            
        current_time+=1
        
    print(current_time-1, "finished", sep="\t")

    for elem in start_dic:
        turnaround_list.append(end_dic[elem]-start_dic[elem])
    for i in turnaround_list:
        turnaround_time+=i
    #throughput is the length of processes as of now
    turnaround_time=turnaround_time/throughput
    print("Average Turnaround Time: ",turnaround_time)
    
    throughput=throughput/(current_time-1)
    print("Throughput: ",throughput)

    output(finished_processes)
    
def shortest_remaining_time(processes, io_duration, context_switch_penalty, total_memory):
    #processes is a list of all processes
    num_processes=len(processes)
    processes.sort(key=sort_time_available) 
    #time variable, process in processes
    t,i=0,0
    current_process=None
    not_beginning=False

    #a list for processes with io events happening
    io_happening=[]
    #a queue for processes with io events finished
    io_finished_queue=queue.Queue()
    #list to hold current processes
    process_queue_list = []
    #calculate throughput
    throughput=len(processes)

    #calculate turnaround time
    turnaround_time=0
    turnaround_list=[]
    start_dic={}
    end_dic={}

    #########################################NEW STUFF##########################################
    #define memory, a linked list
    memory=linked_list()
    memory.head=node(None, 0, total_memory)
    #create a list of all finished processes
    finished_processes=[]
    all_processes=[]
    #########################################NEW STUFF##########################################
    

    #while loop to run until processes complete
    while len(finished_processes)!=num_processes:
        #add processes to queue if they become available
        print('t',t)
        while i<len(processes) and int(processes[i].arrival_time)<=t:
            #initializion for each process
            all_processes.append(processes[i])
            start_dic[processes[i].key]=t
            process_queue_list.append(processes[i])
            i+=1
            not_beginning=True
            print("i",i)

        process_queue_list.sort(key=sort_service_time)
            
        #get a new process if there is none, set up all variables needed
        if current_process==None and not(len(process_queue_list)==0 and io_finished_queue.empty()):
            #use a process that finished it's io if there are any waiting
            #use a process that finished it's io if there are any waiting
            if not io_finished_queue.empty():
                useable_io=enough_memory_queue(io_finished_queue, memory,t,all_processes)
                if useable_io[0]:
                    print_list(memory)
                    
                    t+=context_switch_penalty
                    ########
                    current_process=useable_io[1]
                    ########
            if len(process_queue_list)!=0 and current_process==None:
                useable=enough_memory_list(process_queue_list, memory,t,all_processes)
                if useable[0]:
                    
                    print_list(memory)
                    
                    t+=context_switch_penalty
                    current_process=useable[1]
            #print('got process', current_process.key)
            #print(current_process.io_counter,current_process.io_freq, current_process.io_running)


        if current_process !=None and not process_queue_list == [] and (int(current_process.service_time) > int(process_queue_list[0].service_time)):
            useable=enough_memory_list(process_queue_list, memory,t,all_processes)
            if useable[0]:
                
                process_queue_list.append(current_process)
                
                current_process = useable[1]
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
            #run current process
            print('program running', current_process.key, int(current_process.service_time) -1, "clocks left")
            current_process.service_time=int(current_process.service_time)-1
            current_process.io_counter=int(current_process.io_counter)-1
            #one time unit was used on either the io event or the current process

                
            #if process ends, remove it, and reset all relevant variables, adn add
            #contact switch penalty
            if current_process.service_time==0:
                finished_processes.append(current_process)
                remove_process(current_process, memory)
                current_process.completion_time=t
                end_dic[current_process.key]=t
                print(current_process.key, 'is done')
                current_process.completion_time=t
                t+=context_switch_penalty
                current_process=None
        if current_process!=None:
            print("current Process", current_process.key)
            #if io_counter is 0 then either an io event is ending or an io event should start
            #if io_running is True then the io event should end, if it is False an event should begin
            if current_process.io_counter==0 and current_process.io_freq!=0:
                print("io event starting")
                io_happening.append(current_process)
                current_process.io_counter=io_duration
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

    output(finished_processes)

def shortest_process_next(processes, io_duration, context_switch_penalty, total_memory):
   #processes is a list of all processes
    num_processes=len(processes)
    processes.sort(key=sort_time_available) 
    #time variable, process in processes
    t,i=0,0
    current_process=None
    not_beginning=False

    #a list for processes with io events happening
    io_happening=[]
    #a queue for processes with io events finished
    io_finished_queue=queue.Queue()
    #list to hold current processes
    process_queue_list = []
    #calculate throughput
    throughput=len(processes)

    #calculate turnaround time
    turnaround_time=0
    turnaround_list=[]
    start_dic={}
    end_dic={}


    #########################################NEW STUFF##########################################
    #define memory, a linked list
    memory=linked_list()
    memory.head=node(None, 0, total_memory)
    #create a list of all finished processes
    finished_processes=[]
    all_processes=[]
    #########################################NEW STUFF##########################################
    print(memory.head.next, memory.head.start, memory.head.end)

    #while loop to run until processes complete
    while len(finished_processes)!=num_processes:
        #add processes to queue if they become available
        print('t',t)
        while i<len(processes) and int(processes[i].arrival_time)<=t:
            #initializion for each process
            all_processes.append(processes[i])
            
            start_dic[processes[i].key]=t
            process_queue_list.append(processes[i])
            i+=1
            not_beginning=True
            print("i",i)

        process_queue_list.sort(key=sort_service_time)
            
        #get a new process if there is none, set up all variables needed
        ####################NEW PROCESS################################
        if current_process==None and not(len(process_queue_list)==0 and io_finished_queue.empty()):
            #use a process that finished it's io if there are any waiting
            if not io_finished_queue.empty():
                useable_io=enough_memory_queue(io_finished_queue, memory,t,all_processes)
                if useable_io[0]:
                    print_list(memory)
                    
                    t+=context_switch_penalty
                    ########
                    current_process=useable_io[1]
                    ########
            if len(process_queue_list)!=0 and current_process==None:
                useable=enough_memory_list(process_queue_list, memory,t,all_processes)
                if useable[0]:
                    
                    print_list(memory)
                    
                    t+=context_switch_penalty
                    current_process=useable[1]

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
            #run current process
            print('program running', current_process.key, int(current_process.service_time) -1, "clocks left")
            current_process.service_time=int(current_process.service_time)-1
            current_process.io_counter=int(current_process.io_counter)-1
            #one time unit was used on either the io event or the current process

                
            #if process ends, remove it, and reset all relevant variables, and add
            #contact switch penalty
            ####################PROCESS ENDS################################
            if current_process.service_time==0:
                remove_process(current_process, memory)
                current_process.completion_time=t
                print_list(memory)
                end_dic[current_process.key]=t
                print(current_process.key, 'is done')
                t+=context_switch_penalty
                finished_processes.append(current_process)
                current_process=None
        if current_process!=None:
            print("current Process", current_process.key)
            #if io_counter is 0 then either an io event is ending or an io event should start
            #if io_running is True then the io event should end, if it is False an event should begin
            if current_process.io_counter==0 and current_process.io_freq!=0:
                print("io event starting")
                io_happening.append(current_process)
                current_process.io_counter=io_duration
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


    output(finished_processes)
    

def output(finished_processes):
    print('\n\n')
    for i in finished_processes:
        print("process:", i.key, "completed:", i.completion_time)
        for j in range(len(i.location1)):
            print("\t Allocated at time:",i.when_allocated[j],"From address:",i.location1[j], "to:",i.location2[j])

            
def print_list(memory):
    list_crawler=memory.head
    print(list_crawler.process, list_crawler.start, list_crawler.end)
    while list_crawler.next!=None:
        list_crawler=list_crawler.next
        print(list_crawler.process, list_crawler.start, list_crawler.end)

def compaction(memory,all_processes,t):
    list_crawler=memory.head
    prev='head'
    while list_crawler!=None:
        
        if list_crawler.process==None:
            output=find_next(list_crawler)
            if output[0]==True:

                c1=output[1]
                c2=output[2]
                c1_size=c1.end-c1.start
                list_crawler_size=list_crawler.end-list_crawler.start
                difference=c1_size-list_crawler_size
                process=c1.process
                #print(c1.process, c1.start, c1.end,list_crawler.process, list_crawler.start, list_crawler.end)
                c1.process,list_crawler.process=list_crawler.process,c1.process
                c1.end=c1.start+list_crawler_size
                list_crawler.end=list_crawler.start+c1_size

                #print(c1.process, c1.start, c1.end,list_crawler.process, list_crawler.start, list_crawler.end)
                for i in all_processes:
                        if i.key==list_crawler.process:
                            i.when_allocated.append(t)
                            i.location1.append(list_crawler.start)
                            i.location2.append(list_crawler.end-1)
                            
                list_crawler=list_crawler.next
                while list_crawler.start!=c1.start:
                    list_crawler.start+=difference
                    list_crawler.end+=difference

                    for i in all_processes:
                        if i.key==list_crawler.process:
                            i.when_allocated.append(t)
                            i.location1.append(list_crawler.start)
                            i.location2.append(list_crawler.end-1)
                    list_crawler=list_crawler.next
           
        prev=list_crawler
        list_crawler=list_crawler.next
    list_crawler=memory.head
    while list_crawler.next!=None:
        list_crawler2=list_crawler
        list_crawler=list_crawler.next
        if list_crawler.process==None and list_crawler2.process==None:
            list_crawler2.end=list_crawler.end
            list_crawler2.next=list_crawler.next
            list_crawler=list_crawler2
        

def graph(memory):
    pass

            
def find_next(list_crawler):
    output=[False,'c','d']
    while list_crawler.next!=None:
        list_crawler2=list_crawler
        list_crawler=list_crawler.next
        if list_crawler.process!=None:
            return [True,list_crawler, list_crawler2]
    return output
            

def remove_process(current_process, memory):
    list_crawler=memory.head
    while list_crawler.process!=current_process.key:
        list_crawler=list_crawler.next
    list_crawler.process=None
    current_process.end_location1=list_crawler.start
    current_process.end_location2=list_crawler.end
    #combine adjacent empty memory
    list_crawler=memory.head
    while list_crawler.next!=None:
        list_crawler2=list_crawler
        list_crawler=list_crawler.next
        if list_crawler.process==None and list_crawler2.process==None:
            #print("WE REMOVING",list_crawler.process, list_crawler.start, list_crawler.end)
            list_crawler2.end=list_crawler.end
            list_crawler2.next=list_crawler.next
            list_crawler=list_crawler2
        

def partition_memory(new_process, memory,t,all_processes):
    compaction(memory,all_processes,t)
    list_crawler=memory.head
    while list_crawler.next!=None:
        if list_crawler.process==new_process.key:
            return True
        list_crawler=list_crawler.next
        
    while (list_crawler.end-list_crawler.start)<new_process.memory_required or list_crawler.process!=None:
        #if there are no spots in memory, return false
        if list_crawler.next==None:
            return False
        list_crawler=list_crawler.next
    #assign memory in linked list
    list_crawler.process=new_process.key
    new_slot=node(list_crawler.next,list_crawler.start+new_process.memory_required, list_crawler.end)
    list_crawler.end=new_slot.start
    list_crawler.next=new_slot
    new_process.when_allocated.append(t)
    new_process.location1.append(list_crawler.start)
    new_process.location2.append(list_crawler.end-1)
    return True
    
class node(object):
    def __init__(self, next, start, end):
        self.next=next
        self.start=start
        self.end=end
        self.process=None
        
class linked_list(object):
    def __init__(self, head=None):
        self.head = head

def enough_memory_list(some_list, memory,t,all_processes):
    results=[False,None]
    for i in range(len(some_list)):
        if results[0]==False and partition_memory(some_list[i],memory,t,all_processes)==True:
            #print("HERE", some_list,some_list[i].key)
            results=[True, some_list[i]]
            some_list.pop(i)
    #print(results)
    return results
        
def enough_memory_queue(io_finished_queue, memory,t,all_processes):
    io_list=[]
    while not io_finished_queue.empty():
        io_list.append(io_finished_queue.get())
        
    results=[False,None]
    for i in io_list:

        if results[0]==False and partition_memory(i,memory,t,all_processes)==True:
            results=[True, i]
        else:
      
            io_finished_queue.put(i)
    #print(results)
    return results
        
def get_values(processes, context_switch_penalty = None, quantum = None, io_duration = None, total_memory = None):
    rr_required_vars = {'io_duration':io_duration, 'quantum': quantum, 'context_switch_penalty':context_switch_penalty, 'total_memory':total_memory}
    other_required_vars = {'io_duration':io_duration, 'context_switch_penalty':context_switch_penalty, 'total_memory':total_memory}

    print("\nType:\n\t\"rr\" to schedule using Round Robin\n\t\"fcfs\" to schedule using First Come First Serve\n\t\"srt\" to schedule using Shortest Remaining Time\n\t\"spn\" to schedule using Shortest Process Next")
    ans = str_verify("\nI choose: ", "rr,fcfs,srt,spn", lower = 'uh huh')

    if ans == 'rr':
        required_vars = get_required_vals(rr_required_vars)  
        final_vars = should_update_value(required_vars)
        io_duration, quantum, context_switch_penalty, total_memory = unpack(required_vars)
        round_robin(processes, io_duration, quantum, context_switch_penalty, total_memory)
        return 'rr'

    else:
        required_vars = get_required_vals(other_required_vars)
        final_vars = should_update_value(required_vars)
        io_duration, context_switch_penalty, total_memory = unpack(final_vars)

        if ans == 'fcfs':    
            first_come_first_serve(processes, io_duration, context_switch_penalty, total_memory)
            return 'fcfs'

        elif ans == 'srt':
            shortest_remaining_time(processes,io_duration, context_switch_penalty, total_memory)
            return 'srt'

        elif ans == 'spn':
            shortest_process_next(processes, io_duration, context_switch_penalty, total_memory)
            return 'spn' 

def get_required_vals(required_vars, *args):
    for variable in required_vars:
        min_num = 1
        
        if required_vars.get(variable) is None or args == 'update':
            
            if variable == 'context_switch_penalty':
                min_num = 0

            new_value = int_check("Please enter a value for " + str(variable) +": ", min_num)
            required_vars[variable] = new_value

        elif isinstance(required_vars.get(variable), str):
            new_value = int(required_vars.get(variable))
            required_vars[variable] = new_value            

    return required_vars


def unpack(required_vars):
    if len(required_vars) == 3:
        return required_vars.get('io_duration'), required_vars.get('context_switch_penalty'), required_vars.get('total_memory')
    else:
        return required_vars.get('io_duration'), required_vars.get('quantum'), required_vars.get('context_switch_penalty'), required_vars.get('total_memory')

def should_update_value(required_vars):
    names = [variable for variable in required_vars]

    for i,var in enumerate(names):
        print("\t"+var+":", required_vars.get(var))
    
    print("\nTo edit any variables, enter in the variable names seperated by commas")
    print('OR')
    print("Enter \'No\' to skip this step\n")

    ans = str_verify("Edit any of the variables: ", getdemcommas(names), lower= 'you bet',multiple = "yeet")

    if ans == 'no,':
        return required_vars

    else:
        update_vars = ans.split(',')
        for var in update_vars:
            if var == '':
                continue
                
            required_vars = update_value(required_vars,var)
        
        print("\nThe following variables below are:")        
        for name in names:
            print("\t",name+":", required_vars.get(name)) 
            print()

        return required_vars
def update_value(required_vars,var):
    min_num = 1
    if var == 'context_switch_penalty':
        min_num = 0
    
    new_value = int_check("Please enter a value for " + str(var) +": ", min_num)
    required_vars[var] = new_value
    return required_vars

def getdemcommas(names):
    ans = 'no,'
    for name in names:
        ans+=name +','
    return ans
