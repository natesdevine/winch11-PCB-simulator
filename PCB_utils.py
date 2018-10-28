#checks to see if provided user file name is a .txt file
def fileCheck(strFileName):
    if ".txt" not in strFileName:
        return False
    return True    

#assorted methods to validate user inputted parameters processes
#lets add a check for negative priority
def type_check(processes, parameters):   
    if (len(parameters) != 6 or not bool_check(parameters[1]) or not bool_check(parameters[4])
        or not id_check(processes, parameters[0]) or not int_check(parameters[2])
        or not int_check(parameters[3]) or not int_check(parameters[5])):
        return False
    return True

def time_check(parameter):
    if ":" not in parameter:
        return False

    try:
        hours, minutes = parameter.split(":")
    
        if int(hours) > 24 or int(hours) < 0:
            print('Not acceptable hours')
            return False

        elif int(minutes) > 60 or int(minutes) < 0:
            print('Not acceptable minutes')
            return False

    except(ValueError):
        return False

    return True

def bool_check(parameter):
    if parameter == 'True' or parameter == 'False':
        return True
    print('Not an acceptable boolean')
    return False

def int_check(parameter):
    #check is digits and IF DUPlICATES
    if not parameter.isdigit():
        print('Not an integer')
        return False

    return True

def id_check(processes, parameter):
    #first check if id is an integer
    if not int_check(parameter):
        return False

    for elem in processes:
        if elem.getKey() == parameter:
            print('Error: ID ' + str(parameter) + " already exists")
            # print(elem.getKey(), parameter, "test")
            return False
    return True

#Functions used for getting process' info from User
def inputProcessInfo(processes):
    ID = inputProcessID(processes)
    activity = inputActivity()
    priority = inputPriority()
    time = inputTime()
    mode = inputMode()
    service = inputService()

    return ID, activity, priority, time, mode, service

def inputProcessID(processes):
    process = input("Please enter a process ID: ")

    #check for duplicates as well
    while not id_check(processes, process):
        process = input("Please enter a process ID: ")          
    return process

def inputActivity():
    process = input("Please enter if process is active (\"True\" or \"False\"): ")

    while not bool_check(process):
        process = input("Please enter if process is active (\"True\" or \"False\"): ")          
    return process

def inputPriority():
    priority = input("Please enter the priority (an integer): ")

    while not int_check(priority):
        priority = input("Please enter the priority (an integer): ")
    return priority         

def inputTime():
    time = input("Please enter the process' arrival time (Hours): ")
    while not int_check(time):
        time = input("Please enter the process' arrival time (Hours): ")
    return time

def inputMode():
    mode = input("Please enter if process is User mode (\"True\" or \"False\"): ")
    while not bool_check(mode):
        mode = input("Please enter if process is User mode (\"True\" or \"False\"): ")
    return mode

def inputService():
    service = input("Please enter the process' service time (Hours): ")
    while not int_check(service):
        service = input("Please enter the process' service time (Hours): ")
    return service

def str_verify(question, correct_ans, lower = None, upper = None):
    accepted = correct_ans.split(',')
    
    if lower is not None:
        ans = input(question).lower()
    elif upper is not None:
        ans = input(question).upper()
    else:
        ans = input(question)

    while ans not in accepted:
        if lower is not None:
            ans = input("Inavalid input. " + question).lower()
        elif upper is not None:
            ans = input("Inavalid input. " + question).upper()
        else:
            ans = input(question)
    return ans

