from string import ascii_lowercase 
import random
import queue

def takesThird(elem):
    return elem[2]

class Process(object):
    
    #make everything except ID an optional paramater
    def __init__(self, key, active, priority, birthday, mode):
        self.key = key
        self.active = active
        self.priority = priority
        self.birthday = birthday
        self.mode = mode
    
    def getKey(self):
        return self.key
     
    def getPriority(self):
        return self.priority
         
    def getBirthday(self):
        return self.birthday
        
    def getMode(self):
        return self.mode  
    
    def isActive(self):
        return self.active == True
    
class PCB(object):
    
    def __init__(self, processes = []):      
        self.processes = processes

    def type_check(self, paramaters):
    	print(self.typesgit )


    def getKey(self, obj):
        return obj
        
    def getKey(self, elem):
        return elem[2]
        
    def getInputFromFile(self):
        filename = input("Please enter the filename of the file you would like to read in: ")
        while ".txt" not in filename:
            filename = input("Please enter the filename of the file you would like to read in: ")
            #catch nonexistent file error here
        processList = []
        with open(filename) as infile:
            for i in infile:
                x = i.split(",")
                
                #throw error
                if not self.type_check(x):
                	pass

                #check type of x[0] through x[2], if all are not valid then throw a custom error
                newP = Process(x[0], x[1], x[2], x[3], x[4])

                processList.append(newP)  
            processList.sort(key=lambda process: process.priority)
            myQueue = queue.Queue()
            for i in processList:
                myQueue.put(i)
            print("HELLO")
            print(myQueue.empty())
            print(myQueue.qsize())
            return myQueue

    def getInput(self):
        loopFlag = True
        process_list = []
        while loopFlag:
            try:
                print("Current process list: ", process_list)
                process = input("Please enter a process definition. When you are finished, please type \"done\": ").lower()
                
                if process == "done":
                    loopFlag = False
                    print("Final process list: ", process_list)
                    return process_list

                elif not self.verify(process):
                    print("The process definition you entered was invalid")
                    
                elif process not in process_list:
                    process_list.append(process)
                else:
                    print("You have entered a duplicate process definition")
                    
            except ValueError:
                print("Error. Please try again")
                
    def verify(self, process):
        if process in self.processes:
            return True
        return False
        
    def print_active_processes(self, user_process_list):
        active_list, inactive_list = [], []
        for process in user_process_list:
            if self.processes[process]:
                active_list.append(process)
            else:
                inactive_list.append(process)
            
        print("Of the processes you inputted, the active processes are: ", active_list)
        print("Of the processes you inputted, the inactive processes are: ", inactive_list)


    def update(self):
        updates = {}
        loop_Flag = True
        
        while loop_Flag:
            key = input("Please enter the process you would like to update. When you are finished, please type \"done\": ").lower()
            
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

        
    def add_new_process(self):
        current_processes = self.processes
            
        loopFlag = True
        while loopFlag:
            try:
                process = input("Please enter a process name and a process definition seperated by a comma. When you are finished, please type \"done\": ")
                
                process = ''.join(process.split())
                
                if process == "done":
                    loopFlag = False
                    return current_processes
                    
                elif process.split(",")[0].lower() in self.processes:
                    print("You have entered a duplicate process definition")
                    
                elif process.split(",")[1].lower() != 'true' and process.split(",")[1].lower() != 'false':
                    print("The process definition you entered was invalid")
                
                else:
                    current_processes[process.split(",")[0]] = process.split(",")[1]
                    # print(self.processes)

            except ValueError:
                print("Error. Please try again")

def main():

    
    PCB_obj = PCB()
    
    PCB_obj.getInputFromFile()
    
    
    
    #CB_obj.print_active_processes(PCB_obj.getInput())
def main():
	
	PCB_obj = PCB()
	
	PCB_obj.print_active_processes(PCB_obj.getInput())

    print("\nWould you like to add a new process or update a process?")

    process = input("Please enter \"update\", \"add\". Or enter \"done\" if you're finished with the program: ").lower()

    while process != 'add' and process != 'update' and process != 'done':
        print("Sorry, that isn't an acceptable answer.")
        process = input("Please enter \"update\", \"add\" or \"done\": ").lower()

    if process == 'add':
        PCB_obj.add_new_process()
        print(processes)
    elif process == 'update':
        PCB_obj.update()
        print(processes)
    elif process == 'done':
        print("Smell ya later")


if __name__ == '__main__':
    main()
