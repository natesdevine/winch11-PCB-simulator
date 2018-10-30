from PCB import *
from PCB_utils import *
# from scheduling import *
from roundRobin import *
import sys

#Gets the desired menu from the user and checks if it is a valid choice
def menu():
    print("\nType:\n\t\"add\" to add a new process\n\t\"update\" to update a process\n\t\"print\" to see active processes\n\t\"schedule\" to schedule the processes\n\t\"finish\" to exit the program.")
    action = str_verify("\nI want to: ", "update,add,print,schedule,finish", lower = "yeet, juju on the beat")

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
            PCB_obj.print_active_processes()

        elif action == 'schedule':
            PCB_obj = rrValues(PCB_obj.getProcesses())

        elif action == 'finish':
            print("Smell ya later")
            sys.exit()

if __name__ == '__main__':
    main()