from string import ascii_lowercase 
import random

def main():
    processes = {}

    for letter in ascii_lowercase:
        choice = random.randint(1, 101)
        if choice >= 50:
            processes[letter] = True
        else:
            processes[letter] = False
    
    PCB_obj = PCB(processes)

    user_process_defs = PCB_obj.getInput()

class PCB(object):

    def __init__(self, processes):      
        self.processes = processes

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
            



        
        



        
main()
