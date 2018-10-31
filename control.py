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
            try:
                PCB_obj.print_active_processes()
            except AttributeError:
                print("\nThe queue is currently empty of processes")

        elif action == 'schedule':

            queue_list_copy = PCB_obj.getProcesses()[:]

            #determine if user needs to be prompted for io_duration, quantum and context_switch_penalty
            if PCB_obj.schedule_values_exist() == True:
                run_interface = 'n'
                io_duration, quantum, context_switch_penalty = PCB_obj.getScheduleValues()
                PCB_obj = rrValues(queue_list_copy, run_interface, io_duration, quantum, context_switch_penalty)
            else:
                run_interface = 'y'
                PCB_obj = rrValues(queue_list_copy, run_interface)
            


        elif action == 'finish':
            print("Smell ya later")
            sys.exit()

if __name__ == '__main__':
    main()