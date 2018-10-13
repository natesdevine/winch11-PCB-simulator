import queue
import time


#method to sort list by key
def takesThird(elem):
    return elem[2]

#checks to see if provided user file name is a .txt file
def fileCheck(strFileName):
    if ".txt" not in strFileName:
        return False
    return True

class Process(object):
    
    #instance variables for process
    def __init__(self, key, active, priority, birthday, mode):
        self.key = key
        self.active = active
        self.priority = priority
        self.birthday = birthday
        self.mode = mode
    
    #standard get methods
    def getKey(self):
        return self.key
     
    def getPriority(self):
        return self.priority
         
    def getBirthday(self):
        return self.birthday
        
    def getMode(self):
        return self.mode  
    
    def isActive(self):
        return self.active == 'True'
        
    def setPriority(self, newPriority):
        self.priority = newPriority
        
    def setBirthday(self, newBirthday):
        self.birthday = newBirthday
    
    def setMode(self, newMode):
        self.mode = newMode
    
    def setActive(self, newActive):
        self.active = newActive
    

class PCB(object):

    def __init__(self, processes = []):      
        self.processes = processes
        self.PCBqueue = queue.Queue()
        self.readFile()
    
    #assorted methods to validate user inputted parameters processes
    def type_check(self, parameters):   
        if (len(parameters) != 5 or not self.bool_check(parameters[1]) or not self.bool_check(parameters[4])
            or not self.id_check(parameters[0]) or not self.int_check(parameters[2])
            or not self.time_check(parameters[3])):
            return False
        return True

    def time_check(self, parameter):
        if ":" not in parameter:
            return False

        try:
            hours, minutes = parameter.split(":")
        
            if int(hours) > 24 or int(hours) < 0:
                print('Not acceptable hours')
                return False

            elif int(minutes) > 60 or int(minutes) < 0 or len(minutes) == 1:
                print('Not acceptable minutes')
                return False

        except(ValueError):
            return False

        return True

    def bool_check(self, parameter):
        if parameter == 'True' or parameter == 'False':
            return True
        print('Not an acceptable boolean')
        return False

    def int_check(self, parameter):
        #check is digits and IF DUPlICATES
        if not parameter.isdigit():
            print('Not an integer')
            return False

        return True

    def id_check(self, parameter):
        #first check if id is an integer
        if not self.int_check(parameter):
            return False

        for elem in self.processes:
            if elem.getKey() == parameter:
                print('Error: ID ' + str(parameter) + " already exists")
                # print(elem.getKey(), parameter, "test")
                return False
        return True

    #method to read in a list of processes from a .txt file (of CSV)
    def readFile(self):
        processList = []
        loopFlag = True
        filename = input("Please enter the filename of the file you would like to read in: ")
        while (not fileCheck(filename)):
            print("Failed file checks")
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
                        if self.type_check(x) == False:
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
            
            #exception handling for nonexistent file names
            except (FileNotFoundError):
                print("File not found. Try again")
                filename = input("Please enter the filename of the file you would like to read in: ")


    #Functions used for getting process' info from User
    def getProcessInfo(self):
        ID = self.getProcessID()
        activity = self.getActivity()
        priority = self.getPriority()
        time = self.getTime()
        mode = self.getMode()
        return ID, activity, priority, time, mode

    def getProcessID(self):
        process = input("Please enter a process ID: ")

        #check for duplicates as well
        while not self.id_check(process):

            process = input("Please enter a process ID: ")          

        return process

    def getActivity(self):
        process = input("Please enter if process is active, \"True\" or \"False\": ")

        while not self.bool_check(process):
            process = input("Please enter if process is active: ")          
        return process

    def getPriority(self):
        priority = input("Please enter process' priority, an integer: ")

        while not self.int_check(priority):
            priority = input("Please enter process' priority, an integer: ")
        return priority         

    def getTime(self):
        time = input("Please enter the process' creation time (Hour:Minute): ")
        while not self.time_check(time):
            time = input("Please enter the process' creation time (Hour:Minute): ")
        return time

    def getMode(self):
        mode = input("Please enter if process is User mode, \"True\" or \"False\": ")
        while not self.bool_check(mode):
            mode = input("Please enter if process is User mode, \"True\" or \"False\": ")
        return mode


    #Updates the queue with new processes from user
    def merge(self, process):
        self.processes.append(process)
        self.processes.sort(key=lambda process: int(process.priority), reverse = True)

        #SCHEDULING ALGORITHMS
        self.PCBqueue.put(process)

    #Prints the processes, active and inactive, in the queue
    def printQueue(self, *args):
        if len(args) == 0:
            print("\nCurrent process queue: ")

        elif len(args) == 1:
            string = str(args).replace("(", '').replace(')', '').replace(',', '').replace("'", '')
            print("\n" + string + ' process queue: ')
        
        for elem in list(self.PCBqueue.queue):
            print("Process ID: " + elem.getKey() + ", Priority: " + elem.getPriority())

    #standard method to print out all active processes
    def print_active_processes(self):
        active_list, inactive_list = [], []
        for process in self.processes:
            if process.isActive():
                active_list.append(process.getKey())
            else:
                inactive_list.append(process.getKey())
                
        print("Of the processes you inputted, the active processes are: ", active_list)
        print("Of the processes you inputted, the inactive processes are: ", inactive_list)
         
    def updateProcessInfo(self):
        print("You will now be prompted to enter new process definitions for the selected process")
        newList = []
        
        activity = self.getActivity()
        priority = self.getPriority()
        time = self.getTime()
        mode = self.getMode()
        
        newList.append(priority)
        newList.append(time)
        newList.append(mode)
        newList.append(activity)
        
        return newList

    #method to accept new processes dynamically (instead of from a file)
    def add(self):
        loopFlag = True
        process_list = []

        while loopFlag:
            try:
                #print from queue IDs instead of process list
                self.printQueue()

                ans = input("\nCreate a process, \"True\" or \"False\":  ")
                
                while not self.bool_check(ans):
                    ans = input("Create a process, \"True\" or \"False\":  ")

                if ans == 'True':   
                    ID, activity, priority, time, mode = self.getProcessInfo()                  

                    #create, append a process to queue
                    newP = Process(ID, activity, priority, time, mode)
                    self.merge(newP)  
                    
                elif ans == "False":
                    loopFlag = False
                    self.printQueue('Updated')

            except ValueError:
                print("Error. Please try again")
                
    
    #searches for a process by ID, returns false if it does not exist
    def searchProcesses(self, processID):
        for process in self.processes:
            if process.getKey() == processID:
                return process
        return None

    #method to update a process of the user's choice
    def update(self):
        newProcess = input("Please enter the process ID of the process you would like to update.").lower()
        while not id_check(newProcess):
            newProcess = input("Please enter the process ID of the process you would like to update.").lower()
            print("Current process definitions: ")
            print("Key: ", self.processes[newProcess].getKey())
            print("Priority: ", self.processes[newProcess].getPriority())
            print("Birthday: ", self.processes[newProcess].getBirthday())
            print("Mode: ", self.processes[newProcess].getMode())
            print("isActive: ", self.processes[newProcess].isActive())

            if key == 'done':
                self.processes.update(updates)
                # print(self.processes)
                loop_Flag = False

                
            elif not self.verify(key):
                print("The submitted process isn't possible to update.")

            elif self.verify(key) and key not in updates:
                value = input("Please enter the process' new value, either 'True' and 'False': ")

                while value != 'True' and value != "False":
                    value = input("Sorry, acceptable answers include 'True' and 'False': ")
                
                updates[key] = value

        newProcessID = input("Please enter the process ID of the process you would like to update: ").lower()
        while not self.int_check(newProcessID):
            newProcessID = input("Please enter the process ID of the process you would like to update: ").lower()
        
        existingProcess = self.searchProcesses(newProcessID)
        existingProcessIndex = self.processes.index(existingProcess)
        
        print("Current process definitions: ")
        print("Key: ", existingProcess.getKey())
        print("Priority: ", existingProcess.getPriority())
        print("Birthday: ", existingProcess.getBirthday())
        print("Mode: ", existingProcess.getMode())
        print("isActive: ", existingProcess.isActive())
        print("\n")
        
        newProcessValues = self.updateProcessInfo()
        
        self.processes[existingProcessIndex].setPriority(newProcessValues[0])
        self.processes[existingProcessIndex].setBirthday(newProcessValues[1])
        self.processes[existingProcessIndex].setMode(newProcessValues[2])
        self.processes[existingProcessIndex].setActive(newProcessValues[3])
        
        print("New process definitions: ")
        print("Key: ", existingProcess.getKey())
        print("Priority: ", existingProcess.getPriority())
        print("Birthday: ", existingProcess.getBirthday())
        print("Mode: ", existingProcess.getMode())
        print("isActive: ", existingProcess.isActive())
        print("\n")
        print("DONE NOW")
        

def menu():
    process = input("\nPlease enter \"update\", \"add\", \"print\". Or enter \"done\" if you're finished with the program: ").lower()

    while process != 'add' and process != 'update' and process != 'done' and process != 'print':
        print("Sorry, that isn't an acceptable answer.")
        process = input("Please enter \"update\", \"add\" or \"done\": ").lower()
    return process

def main():
    loopFlag = True
    PCB_obj = PCB()

    print("\nYou can add a new process, update a process, see active processes or finish with the program")

    while loopFlag:

        process = menu()
    
        if process == 'add':
            PCB_obj.add()

        elif process == 'update':
            PCB_obj.update()

        elif process == 'print':
            PCB_obj.print_active_processes()

        elif process == 'done':
            print("Smell ya later")
            loopFlag = False

if __name__ == '__main__':
    main()
