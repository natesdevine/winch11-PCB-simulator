from PCB_utils import *

def RoundRobin(processes,io_duration, quantum, context_switch_penalty):
    print("yeet")
    rrValues(processes)

    # try:
    #     #processes is a list of all processes
    #     processes.sort(key=sort_time_available)
    #     #create empty queue
    #     process_queue=queue.Queue()
    #     #time variable
    #     t, i, io = 0, 0, 0
    #     q=quantum
    #     #while loop to run until processes complete
    #     while processes_not_done:
    #         #add processes to queue if they become available
    #         while processes[i].arrivalTime<=t:
    #             Queue.put(processes(i))
    #             i+=1

                
    #         #run current processes
    #         if current_process==None and not process_queue.empty():
    #             t+=context_switch_penalty
    #             current_process=process_queue.get()
    #         #run current process for 1 time unit
    #         if current_process!=None:

    #             if current_process.io_counter==0:
    #                 t+=context_switch_penalty+io_duration
    #                 current_process.io_counter=current_process.io_freq
                    
    #             current_process.serviceTime-=1
    #             current_process.io_counter-=1
                
    #             q-=1

    #             if q==0:
    #                 q=3
    #                 current_process=null
    #             if current_process.serviceTime>0:
    #                 t+=context_switch_penalty
    #                 process_queue.put(current_process)
    # except:
    #     print("THIS SHIT AINT WORKING BRUH, GOING BACK TO THE RRVALUES FUNCTION")

    #     rrValues(processes)
            

            
def sort_time_available(process):
    return process.time_available
            
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

    print(processes)

    ans = str_verify("\nYOU WANNA TEST RoundRobin (Y/N)?: ", "y,n", lower = 'uh huh')
    if ans == 'y':
        RoundRobin()
    elif ans == 'n':
        ans = str_verify("\nALRIGHT DAWG, YOU WANNA GO BACK (y/n)?: ", "y,n", lower = 'yeet') 
        if ans == 'y':
            control_script(processes, io_duration, quantum, context_switch_penalty)
        else:
            print("\nALRIGHT DAWG, THE PROGRAM FINNA DIE NOW")
            sys.exit()
