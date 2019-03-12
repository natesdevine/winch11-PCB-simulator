def int_check(question, min_num = None, max_num = None):
    if min_num is not None and max_num is not None:
        return second_case(question, min_num, max_num)
    elif min_num is not None or max_num is not None:
        if min_num is not None:
            return first_case(question, 'min', min_num)
        else:
            return first_case(question, 'max', max_num)     
    else:
        return base_case(question)
                
def base_case(question):
    while True:
        try:
            ans = int(input(question))
        except ValueError:
            print("Invalid input.")
    return ans

def first_case(question, test_case, bound):
    while True:
        try:
            ans = int(input(question))
            
            #a min check must be run
            if test_case == 'min':
                #answer must be greater than the lower bound    
                if ans >= bound:
                    return ans
                else:
                    print("Invalid input.") 

            #a max check must be run
            else:
                if ans <= bound:
                    return ans
                else:
                    print("Invalid input.")
        
        except ValueError:
            print("Invalid input.")
    
    return ans  

def second_case(question, min_num, max_num):
    while True:
        try:
            ans = int(input(question))
            if min_check(ans, min_num) and max_check(ans, max_num):
                break
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")
    return ans


def min_check(answer, min_num):
    if answer >= min_num:
        return True
    return False

def max_check(answer, max_num):
    if answer <= max_num:
        return True
    return False
