import queue
from PCB_utils import *

class Process(object):

    #instance variables for process
    def __init__(self, key, active, priority, time_created, mode, service_time, io_freq):
        self.key = key
        self.active = active
        self.priority = priority
        self.time_created = time_created
        self.mode = mode
        self.service_time = service_time
        self.io_freq, self.io_counter = io_freq, io_freq
        self.io_running = False

    #standard get methods
    def getKey(self):
        return self.key

    def getPriority(self):
        return self.priority

    def getTimeCreated(self):
        return self.time_created

    def getMode(self):
        return self.mode

    def isActive(self):
        return self.active == 'True'

    def getServiceTime(self):
        return self.service_time

    def getIOFreq(self):
        return self.io_freq

    def getIOCounter(self):
        return self.io_counter

    def print_vals(self):
        print(self.key, self.active, self.priority, self.time_created, self.mode, self.service_time, self.io_freq, self.io_counter)       

    def setPriority(self, newPriority):
        self.priority = newPriority

    def setTimeCreated(self, newtime_created):
        self.time_created = newtime_created

    def setMode(self, newMode):
        self.mode = newMode

    def setActive(self, newActive):
        self.active = newActive

    def setServiceTime(self, new_service_time):
        self.service_time = new_service_time

    def setIOFreq(self, new_io_freq):
        self.io_freq = new_io_freq

    def setIOCounter(self, new_io_counter):
        self.io_counter = new_io_counter
        
class PCB(object):

    def __init__(self, processes = []):
        self.processes = processes
        self.PCBqueue = queue.Queue()
        
        self.context_switch_penalty = None
        self.quantum = None
        self.io_duration = None

        self.readFile()

    def empty(self):
        self.processes = []
        self.PCBqueue = queue.Queue()
        
        self.context_switch_penalty = None
        self.quantum = None
        self.io_duration = None        

    def isEmpty(self):
        if len(self.processes) == 0:
            return True
        return False

    def schedule_values_exist(self):
        var1, var2, var3 = self.getScheduleValues()

        if var1 is not None and var2 is not None and var3 is not None:
            return True
        else:
            return False

    def getScheduleValues(self):
        return (self.context_switch_penalty, self.quantum, self.io_duration)

    def getProcesses(self):
        return self.processes

    #Prints the processes, active and inactive, in the queue
    def printQueue(self, *args):
        word = "Current"
        if len(args) > 0:
            word = str(args).replace("(", '').replace(')', '').replace(',', '').replace("'", '')
            
        print("\n" + word + ' process queue: ')    

        for elem in list(self.PCBqueue.queue):
            print("Process ID: " + elem.getKey() + ", Priority: " + elem.getPriority() + ", Arrival Time: " + elem.getTimeCreated() + ", Service Time: " + elem.getServiceTime() + ", IO Freq: " + elem.getIOFreq())

    def printList(self):
        for elem in self.processes:
            print(elem.getKey(), elem.getPriority())

    #standard method to print out all active processes
    def print_active_processes(self):
        active_list, inactive_list = [], []
        
        for process in self.processes:
            if process.isActive():
                active_list.append(process.getKey())
            else:
                inactive_list.append(process.getKey())

        print("\nThe active processes are: ", active_list)
        print("The inactive processes are: ", inactive_list)
       
    def print_process_info(self, someProcess, *args):
        word = "Current"
        if len(args) > 0:
            word = 'Updated'

        print("\n" + word + " process definition: ")

        print("Key: ", someProcess.getKey())
        print("Priority: ", someProcess.getPriority())
        print("Arrival Time: ", someProcess.getTimeCreated())
        print("Service Time: ", someProcess.getServiceTime())
        print("User Mode: ", someProcess.getMode())
        print("isActive: ", someProcess.isActive())
        print("IO Frequency: ", someProcess.getIOFreq())
        print("IO Counter: ", someProcess.getIOCounter())
        

    #searches for a process by ID, returns false if it does not exist
    def searchProcesses(self, processID):
        for process in self.processes:
            if process.getKey() == processID:
                return process
        return False

    #Scheduling algorithm
    #Updates the queue with new processes from user
    def merge(self, process):
        self.processes.append(process)
        self.processes.sort(key=lambda process: int(process.priority), reverse = True)
        self.PCBqueue.put(process)

    def catchParams(self, line):
        params = ["ContextSwitchPenalty", "Quantum", "I/ODuration"]
        
        value = line.split("=")
        
        if value[0] == params[0]:
            self.context_switch_penalty = value[1]
        elif value[0] == params[1]:
            self.quantum = value[1]
        elif value[0] == params[2]:
            self.io_duration = value[1]
        else:
            pass
            # print('nuh uh, you aint getting a value')

    #method to read in a list of processes from a .txt file (of CSV)
    def readFile(self):
        processList = []
        loopFlag = True

        filename = fileCheck("Please enter the filename of the file you would like to read in: ")

        while loopFlag:
            try:
                print('\n --- READING FILE ---\n')

                with open(filename) as infile:
                    for i in infile:
                        #stip other stuff too, not just r
                        i = i.rstrip().replace(' ', '')
                        x = i.split(",")

                        if len(x) == 1:
                            x = "".join(x)
                            self.catchParams(x)
                            # try:
                            #     print("Contxt", self.context_switch_penalty, "quant", self.quantum, "ioduration", self.io_duration)                            
                            # except AttributeError as e:
                            #     print(e)
                            continue

                        #throw error if false
                        if type_check(self.processes, x) == False:
                            # print("type check failed")
                            print('Process ID ' + x[0] + " isn't valid. Moving on to the next process...")
                            continue

                        #process is created for a given line of CSV here
                        try:
                            newP = Process(x[0], x[1], x[2], x[3], x[4], x[5], x[6])
                            processList.append(newP)
                            # newP.print_vals()
                            print('Process ID ' + x[0] + ' has been validated')

                        except IndexError as e:
                            print(e)
                            print('Process ID ' + x[0] + " isn't valid. Moving on to the next process...")
                            continue
                            
                    loopFlag = False
                    processList.sort(key=lambda process: int(process.priority), reverse = True)

                    for i in processList:
                        self.merge(i)
                    print('\n --- FINISHED READING FILE ---\n')

                    self.print_active_processes()

            #exception handling for nonexistent file names
            except (FileNotFoundError):
                print("File not found. Try again")
                filename = input("Please enter the filename of the file you would like to read in: ")

    #method to accept new processes dynamically (instead of from a file)
    def add(self):
        process_list = []
        loopFlag = True
        repeated = False
        more_words = 'a'

        while loopFlag:
            try:
                #print from queue IDs instead of process list
                if repeated == True:
                    self.printQueue("Updated")
                    more_words = "another"
                elif repeated == False:
                    self.printQueue()

                ans = str_verify("\nWould you like to create " + more_words + " process (\"True\"/\"False\")?: ", "true,false", lower = 'yeet')
                
                if ans == 'true':   
                    ID, activity, priority, time, mode, service, io_freq = inputProcessInfo(self.processes)                  

                    #create, append a process to queue
                    newP = Process(ID, activity, priority, time, mode, service, io_freq)
                    self.merge(newP)
                    repeated = True

                elif ans == "false":
                    loopFlag = False
                    self.printQueue('Updated')

            except ValueError as e:
                print(e)
                print("Error. Please try again")

    #updates a process' info
    def updateProcessInfo(self):
        print("\nYou will now be prompted to enter new process definitions for the selected process")
        newList = []

        activity = inputActivity()
        priority = inputPriority()
        time = inputTime()
        mode = inputMode()
        service = inputService()
        io_freq = inputIOFreq()
        io_counter = inputIOCounter()

        newList.append(priority)
        newList.append(time)
        newList.append(mode)
        newList.append(activity)
        newList.append(service)
        newList.append(io_freq)
        newList.append(io_counter)

        return newList

    #method to update a process of the user's choice
    def update(self):
        keys = [elem.getKey() for elem in self.processes]
        print("\nThe following processes can be updated: " + str(keys))

        ans = str_verify("\nWould you like to update one of the processes (True/False)?: ", "true,false", lower = "yeet")
        if ans == 'true':

            processID = input("Please enter the process ID of the process you would like to update: ").lower()

            while self.searchProcesses(processID) == False:
                print("Process with ID:", processID, "does not exist.")
                processID = input("Please enter the process ID of the process you would like to update: ").lower()

            existingProcess = self.searchProcesses(processID)
            existingProcessIndex = self.processes.index(existingProcess)

            self.print_process_info(existingProcess)

            newProcessValues = self.updateProcessInfo()

            self.processes[existingProcessIndex].setPriority(newProcessValues[0])
            self.processes[existingProcessIndex].setTimeCreated(newProcessValues[1])
            self.processes[existingProcessIndex].setMode(newProcessValues[2])
            self.processes[existingProcessIndex].setActive(newProcessValues[3])
            self.processes[existingProcessIndex].setServiceTime(newProcessValues[4])
            self.processes[existingProcessIndex].setIOFreq(newProcessValues[5])
            self.processes[existingProcessIndex].setIOCounter(newProcessValues[6])


            self.print_process_info(existingProcess, 'uh huh okay, let me milly rock on these lamez')
        
