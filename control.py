from PCB import *
from PCB_utils import *
from scheduling import *
from ShortestRemainingTime import *
import sys

#Gets the desired menu from the user and checks if it is a valid choice
def menu():
    print("\nType:\n\t\"add\" to add a new process\n\t\"update\" to update a process\n\t\"print\" to see active processes\n\t\"schedule\" to schedule the processes\n\t\"read\" to read a new data file\n\t\"finish\" to exit the program.")
    action = str_verify("\nI want to: ", "update,add,print,read,schedule,finish", lower = "yeet, juju on the beat")

    return action

def main():
    control_script()

def control_script():
    PCB_obj = PCB()
        
    while True:

        action = menu()

        if action == 'add':
            PCB_obj.add()

        elif action == 'update':
            PCB_obj.update()

        elif action == 'print':
            try:
                PCB_obj.print_active_processes()
            except AttributeError:
                print("\nThe queue is currently empty of processes")

        elif action == 'schedule':

            queue_list_copy = PCB_obj.getProcesses()[:]

            #determine if user needs to be prompted for io_duration, quantum and context_switch_penalty
            if PCB_obj.schedule_values_exist() == True:
                run_interface = 'n'
                context_switch_penalty, quantum, io_duration = PCB_obj.getScheduleValues()
                schedule = get_values(queue_list_copy, run_interface, context_switch_penalty, quantum, io_duration)
            else:
                run_interface = 'y'
                schedule = get_values(queue_list_copy, run_interface)
            
            if schedule == 'fcfs' or schedule == 'rr':
                PCB_obj.empty()
                PCB_obj.readFile(forced_rerun = 'yeet')
                # PCB_obj.printQueue()

        elif action == 'read':
            if PCB_obj.isEmpty():
                PCB_obj.readFile()

            else:
                print("\nThe queue currently isn't empty. You can either add to or clear the current queue.")
                ans = str_verify("\nWould you like to add or clear the current queue (add/clear)?: ", "add,clear", lower = "uh huh")
                
                if ans == 'clear':
                    PCB_obj.empty()
                    print("\nClearing the queue...")
                    print("Ready for a new file...\n")
                    PCB_obj.readFile()
                else:
                    print()
                    PCB_obj.readFile()

        elif action == 'finish':
            print("Smell ya later")
            sys.exit()

if __name__ == '__main__':
    main()