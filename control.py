from PCB import *
from PCB_utils import *
#from Scheduling import *
import sys

#Gets the desired menu from the user and checks if it is a valid choice
def menu():
    print("\nYou can type:\n\t\"add\" to add a new process\n\t\"update\" to update a process\n\t\"print\" to see active processes\n\t\"schedule\" to schedule the processes\n\t\"finish\" to exit the program.")
    process = str_verify("\nI want to: ", "update,add,print,schedule,finish", lower = "yeet, juju on the beat")

    return process

def main():
    PCB_obj = PCB()

    while True:

        process = menu()

        if process == 'add':
            PCB_obj.add()

        elif process == 'update':
            PCB_obj.update()

        elif process == 'print':
            PCB_obj.print_active_processes()

        elif process == 'schedule':
            print("\nuh huh okay alright")

        elif process == 'finish':
            print("Smell ya later")
            sys.exit()

if __name__ == '__main__':
    main()