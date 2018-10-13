from PCB import *

#Gets the desired menu from the user and checks if it is a valid choice
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