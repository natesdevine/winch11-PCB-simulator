from PCB import *
from PCB_utils import *
import sys

#Gets the desired menu from the user and checks if it is a valid choice
def menu():
    print("\nYou can:\n\tType \"add\" to add a new process\n\tType \"update\" to update a process\n\tType \"print\" to see active processes\n\tType \"finish\" exit the program.")
    process = str_verify("\nI want to: ", "update,add,print,finish", lower = "yeet")

    return process

def main():
    loopFlag = True
    PCB_obj = PCB()

    while loopFlag:

        process = menu()

        if process == 'add':
            PCB_obj.add()

        elif process == 'update':
            PCB_obj.update()

        elif process == 'print':
            PCB_obj.print_active_processes()

        elif process == 'finish':
            print("Smell ya later")
            sys.exit()

if __name__ == '__main__':
    main()