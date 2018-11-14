#checks to see if provided user file name is a .txt file
def fileCheck(question):
    strFileName = input(question)
    while ".txt" not in strFileName:
        print("Invalid file name.")
        strFileName = input(question)
    return strFileName

#assorted methods to validate user inputted parameters processes
#lets add a check for negative priority
def type_check(processes, parameters, show_errors = 'yeet'):   
    if (len(parameters) != 7 or not bool_check(parameters[1], show_errors) or not bool_check(parameters[4], show_errors)
        or not id_check(processes, parameters[0], show_errors) or not int_check(parameters[2], show_errors)
        or not int_check(parameters[3], show_errors) or not int_check(parameters[5], show_errors)):
        return False
    return True

def pass_the_blunts():
    pass


def time_check(parameter, show_errors = 'yeet'):
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

    except ValueError:
        return False

    return True

def bool_check(parameter,show_errors = 'yeet'):
    if parameter.lower() == 'true' or parameter.lower() == 'false':
        #print("We boolin")
        return True
    if show_errors == 'yeet':
        print('Not an acceptable boolean')
    return False

def int_check(parameter, show_errors = 'yeet'):
    #check is digits and IF DUPlICATES
    if not parameter.isdigit():
        if show_errors == 'yeet':
            print('Not an integer')
        return False

    return True

def id_check(processes, parameter, show_errors = 'yeet'):
    #first check if id is an integer
    if not int_check(parameter):
        return False


    for elem in processes:
        if elem.getKey() == parameter:
            if show_errors == 'yeet':
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
    io_freq = input_io_freq()

    return ID, activity, priority, time, mode, service, io_freq

def inputProcessID(processes):
    process = input("\nPlease enter a process ID: ")

    #check for duplicates as well
    while not id_check(processes, process):
        process = input("Please enter a process ID: ")          
    return process

def inputActivity():
    process = input("Please enter if process is active (\"True\"/\"False\"): ")

    while not bool_check(process):
        process = input("Please enter if process is active (\"True\"/\"False\"): ")          
    return process

def inputPriority():
    priority = input("Please enter the priority: ")

    while not int_check(priority):
        priority = input("Please enter the priority: ")
    return priority         

def inputTime():
    time = input("Please enter the process' arrival time: ")
    while not int_check(time):
        time = input("Please enter the process' arrival time: ")
    return time

def inputMode():
    mode = input("Please enter if process is User mode (\"True\"/\"False\"): ")
    while not bool_check(mode):
        mode = input("Please enter if process is User mode (\"True\"/\"False\"): ")
    return mode

def inputService():
    service = input("Please enter the process' service time: ")
    while not int_check(service):
        service = input("Please enter the process' service time: ")
    return service

def inputIOFreq():
    io_freq = input("Please enter the process' IO frequency: ")
    while not int_check(io_freq):
        io_freq = input("Please enter the process' IO frequency: ")
    return io_freq

def inputIOCounter():
    io_counter = input("Please enter the process' IO counter: ")
    while not int_check(io_counter):
        io_counter = input("Please enter the process' IO frequency: ")
    return io_counter



def str_verify(question, correct_ans, lower = None, upper = None, multiple = None):
    accepted = correct_ans.split(',')
    
    if lower is not None:
        ans = input(question).lower().replace(' ', '')
    elif upper is not None:
        ans = input(question).upper().replace(' ', '')
    else:
        ans = input(question).replace(' ', '')

    
    if multiple is None:
        ans = check_acceptable_answers(accepted, question, ans, lower, upper)
        return ans
    
    elif multiple is not None:
        final_ans = ''
        answers = ans.split(',')

        for answer in answers:
            if answer == ' ':
                continue
            ans = check_acceptable_answers(accepted, question, answer, lower, upper)
            final_ans+= ans+','
        return final_ans

def check_acceptable_answers(accepted_answers, question, user_answer, lower, upper):
    while user_answer not in accepted_answers:
        if lower is not None:
            user_answer = input("Inavalid input. " + question).lower().replace(' ', '')
        elif upper is not None:
            user_answer = input("Inavalid input. " + question).upper().replace(' ', '')
        else:
            user_answer = input(question).replace(' ', '')
    return user_answer    


#cheeky sort function for use in scheduling algs
def sort_time_available(process):
    return process.arrival_time
    
def sort_service_time(process):
    return int(process.getServiceTime())

