from string import ascii_lowercase 
import random

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
        
    def print_active_processes(self, user_process_list):
        active_list, inactive_list = [], []
        for process in user_process_list:
            if self.processes[process]:
                active_list.append(process)
            else:
                inactive_list.append(process)
            
        print("Of the processes you inputted, the active processes are: ", active_list)
        print("Of the processes you inputted, the inactive processes are: ", inactive_list)
def main():
    processes = {}

    for letter in ascii_lowercase:
        choice = random.randint(1, 101)
        if choice >= 50:
            processes[letter] = True
        else:
            processes[letter] = False

    print(processes)
            
    PCB_obj = PCB(processes)
    
    PCB_obj.print_active_processes(PCB_obj.getInput())
            
            
if __name__ == '__main__':
    main()

        
        



        
main()
