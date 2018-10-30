def RoundRobin(processes,io_duration, quantum, context_switch_penalty):
    #processes is a list of all processes
    processes.sort(key=sort_time_available)
    #create empty queue
    process_queue=queue.Queue()
    #time variable
    t, i, io = 0, 0, 0
    q=quantum
    #while loop to run until processes complete
    while processes_not_done:
        #add processes to queue if they become available
        while processes[i].arrivalTime<=t:
            Queue.put(processes(i))
            i+=1

            
        #run current processes
        if current_process==None and !process_queue.empty():
            t+=context_switch_penalty
            current_process=process_queue.get()
        #run current process for 1 time unit
        if current_process!==None:

            if current_process.io_counter==0:
                t+=context_switch_penalty+io_duration
                current_process.io_counter=current_process.io_freq
                
            current_process.serviceTime-=1
            current_process.io_counter-=1
            
            q-=1

            if q==0:
                q=3
                current_process=null
            if current_process.serviceTime>0:
                t+=context_switch_penalty
                process_queue.put(current_process)
        
            

            
def sort_time_available(process):
    return process.time_available
            
        
