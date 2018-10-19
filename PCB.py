import queue
from PCB_utils import *

class Process(object):
    #instance variables for process
    def __init__(self, pid, active, priority, timestamp, mode):
        self.pid = pid
        self.active = active
        self.priority = priority
        self.timestamp = timestamp
        self.mode = mode

    #standard get methods
    def getpid(self):
        return self.pid

    def getPriority(self):
        return self.priority

    def getTimestamp(self):
        return self.timestamp

    def getMode(self):
        return self.mode

    def isActive(self):
        return self.active == 'True'

    def setPriority(self, newPriority):
        self.priority = newPriority

    def setTimestamp(self, newTimestamp):
        self.timestamp = newTimestamp

    def setMode(self, newMode):
        self.mode = newMode

    def setActive(self, newActive):
        self.active = newActive

    def __str__(self):
        s = "pid: " + self.getpid()
        s += "Priority: " + self.getPriority()
        s += "Timestamp: " + self.getTimestamp()
        s += "Mode: ", self.getMode()
        s += "isActive: ", self.isActive()
        return s

class PCB(object):
    def __init__(self, processes = []):
        self.processes = processes
        self.PCBqueue = queue.Queue()
        self.readFile()

    #Prints the processes, active and inactive, in the queue
    def printQueue(self, *args):
        if len(args) == 0:
            print("Current process queue: ")

        elif len(args) == 1:
            string = str(args).replace("(", '').replace(')', '').replace(',', '').replace("'", '')
            print(string,'process queue:')

        for elem in list(self.PCBqueue.queue):
            print("Process ID:", elem.getpid(), ", Priority:", elem.getPriority())

    def printList(self):
        for elem in self.processes:
            print(elem.getpid(), elem.getPriority())

    #standard method to print out all active processes
    def print_active_processes(self):
        print("Of the processes you inputted, the active processes are:")
        for process in self.processes:
            if process.isActive():
                print(process.getpid())

        print("Of the processes you inputted, the inactive processes are:")
        for process in self.processes:
            if not process.isActive():
                print(process.getpid())

    def print_process_info(self, process):
        print(process)

    #searches for a process by ID, returns false if it does not exist
    def searchProcesses(self, pid):
        for process in self.processes:
            if process.getpid() == processID:
                return process
        return False

    #Scheduling algorithm
    #Updates the queue with new processes from user
    def merge(self, process):
        self.processes.append(process)
        self.processes.sort(key=lambda process: int(process.priority), reverse = True)
        self.PCBqueue.put(process)

    #method to read in a list of processes from a .txt file (of CSV)
    def readFile(self):
        processList = []
        loopFlag = True
        filename = input("Please enter the filename of the file you would like to read in: ")
        while (not fileCheck(filename)):
            print("Invalid file name.")
            filename = input("Please enter the filename of the file you would like to read in: ")

        while loopFlag:
            try:
                print('\n --- READING FILE ---\n')

                with open(filename) as infile:
                    for i in infile:
                        #stip other stuff too, not just r
                        i = i.rstrip().replace(' ', '')
                        x = i.split(",")

                        #throw error if false
                        if type_check(self.processes, x) == False:
                            print('Process ID ' + x[0] + " isn't valid. Moving on to the next process...")
                            continue

                        #maybe return values in correct data format
                        print('Process ID ' + x[0] + ' has been validated')

                        #process is created for a given line of CSV here
                        newP = Process(x[0], x[1], x[2], x[3], x[4])
                        processList.append(newP)

                    loopFlag = False
                    processList.sort(key=lambda process: int(process.priority), reverse = True)

                    for i in processList:
                        self.merge(i)
                    print('\n --- FINISHING READING FILE ---\n')

                    self.print_active_processes()
            #exception handling for nonexistent file names
            except (FileNotFoundError):
                print("File not found. Try again")
                filename = input("Please enter the filename of the file you would like to read in: ")

    #method to accept new processes dynamically (instead of from a file)
    def add(self):
        loopFlag = True
        process_list = []

        while loopFlag:
            try:
                #print from queue IDs instead of process list
                self.printQueue()

                ans = input("\nCreate a process, \"True\" or \"False\":  ")

                while not bool_check(ans):
                    ans = input("Create a process, \"True\" or \"False\":  ")

                if ans == 'True':
                    ID, activity, priority, time, mode = getProcessInfo(self.processes)

                    #create, append a process to queue
                    newP = Process(ID, activity, priority, time, mode)
                    self.merge(newP)

                elif ans == "False":
                    loopFlag = False
                    self.printQueue('Updated')

            except ValueError:
                print("Error. Please try again")

    #updates a process' info
    def updateProcessInfo(self):
        print("You will now be prompted to enter new process definitions for the selected process")
        newList = []

        activity = getActivity()
        priority = getPriority()
        time = getTime()
        mode = getMode()

        newList.append(priority)
        newList.append(time)
        newList.append(mode)
        newList.append(activity)

        return newList

    #method to update a process of the user's choice
    def update(self):
        pid = input("Please enter the process ID of the process you would like to update: ").lower()
        while self.searchProcesses(pid) == False:
            print("Process with ID:", pid, "does not exist.")
            pid = input("Please enter the process ID of the process you would like to update: ").lower()

        existingProcess = self.searchProcesses(pid)
        existingProcessIndex = self.processes.index(existingProcess)

        self.print_process_info(existingProcess)

        newProcessValues = self.updateProcessInfo()

        self.processes[existingProcessIndex].setPriority(newProcessValues[0])
        self.processes[existingProcessIndex].setTimestamp(newProcessValues[1])
        self.processes[existingProcessIndex].setMode(newProcessValues[2])
        self.processes[existingProcessIndex].setActive(newProcessValues[3])

        self.print_process_info(existingProcess)
