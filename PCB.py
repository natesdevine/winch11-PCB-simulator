import queue
import time


def takesThird(elem):
	return elem[2]

class Process(object):
	
	#make everything except ID an optional paramater
	def __init__(self, key, active, priority, birthday, mode):
		self.key = key
		self.active = active
		self.priority = priority
		self.birthday = birthday
		self.mode = mode
	
	def getKey(self):
		return self.key
	 
	def getPriority(self):
		return self.priority
		 
	def getBirthday(self):
		return self.birthday
		
	def getMode(self):
		return self.mode  
	
	def isActive(self):
		return self.active == True
	
class PCB(object):

	def __init__(self, processes = []):      
		self.processes = processes
		self.queue = queue.Queue()

	#========
	def type_check(self, parameters):   
		#check them bools ya know
		if (len(parameters) != 5 or not self.bool_check(parameters[1]) or not self.bool_check(parameters[4])
			or not self.int_check(parameters[0]) or not self.int_check(parameters[2])
			or not self.time_check(parameters[3])):
			return False
		return True

	def time_check(self, parameter):
		if ":" not in parameter:
			return False

		hours, minutes = parameter.split(":")
		
		if int(hours) > 24 or int(hours) < 0:
			return False

		elif int(minutes) > 60 or int(minutes) < 0:
			return False

		return True

	def bool_check(self, parameter):
		if parameter == 'True' or parameter == 'False':
			return True
		return False

	def int_check(self, parameter):
		#check is digits and IF DUPlICATES
		if not parameter.isdigit():
			return False
		return True

	def id_check(self, parameter):
		for elem in self.processes:
			print(elem)
			if elem.getKey() == parameter:
				return False

	#========

	def readFile(self):
		processList = []
		filename = input("Please enter the filename of the file you would like to read in: ")
		while ".txt" not in filename:
			print("looping")

			try:
				filename = input("Please enter the filename of the file you would like to read in: ")
			except (FileNotFoundError):
				print("hi")
				print(e)

		with open(filename) as infile:
			for i in infile:
				#stip other stuff too, not just r
				i = i.rstrip()
				x = i.split(",")
				
				#throw error if false
				if self.type_check(x) == False:
					print('Process ID' + x[0] + " isn't valid. Moving on to the next process...")
					continue

				#maybe return values in correct data format
				print('Process ID' + x[0] + ' has been validated')

				#check type of x[0] through x[2], if all are not valid then throw a custom error
				newP = Process(x[0], x[1], x[2], x[3], x[4])

				processList.append(newP)  
				processList.sort(key=lambda process: process.priority)
				
				for i in processList:
					self.queue.put(i)
					self.processes.insert(0, i)

				#test print statements
				print(self.queue.empty())
				print(self.queue.qsize())
   

	def getProcessID(self):
		process = input("Please enter a process ID: ")


		#check for duplicates as well
		while not self.int_check(process):
			process = input("Please enter a process ID: ")    	    

		return process

	def getActivity(self):
		process = input("Please enter if process is active, \"True\" or \"False\": ")

		while not self.bool_check(process):
			process = input("Please enter if process is active: ")			
		return process

	def getPriority(self):
		priority = input("Please enter process' priority, an integer: ")

		while not self.int_check(priority):
			priority = input("Please enter process' priority, an integer: ")
		return priority			

	def getTime(self):
		time = input("Please enter the process' creation time (Hour:Minute): ")
		while not self.time_check(time):
			time = input("Please enter the process' creation time (Hour:Minute): ")
		return time

	def getMode(self):
		mode = input("Please enter if process is User mode, \"True\" or \"False\": ")
		while not self.bool_check(mode):
			mode = input("Please enter if process is User mode, \"True\" or \"False\": ")
		return mode

	def getInput(self):
		loopFlag = True
		process_list = []

		while loopFlag:
			try:
				#print from queue IDs instead of process list
				print("Current process list: ", self.processes)

				ans = input("Create a process, \"True\" or \"False\":  ")
				
				while not self.bool_check(ans):
					ans = input("Create a process, \"True\" or \"False\":  ")

				if ans == 'True':	
					ID = self.getProcessID()
					activity = self.getActivity()
					priority = self.getPriority()
					time = self.getTime()
					mode = self.getMode()

					#create, append a process to queue
					newP = Process(ID, activity, priority, time, mode)
					processList.append(newP)  
					

				elif ans == "False":
					loopFlag = False
					print("Final process list: ", process_list)
					return process_list
	
				#search queue and processlist to check if process exists    
				# elif process.getKey() not in process_list:
				# 	process_list.append(process)

				else:
					print("You have entered a duplicate process definition")

			except ValueError:
				print("Error. Please try again")
				

	def print_active_processes(self, user_process_list):
		active_list, inactive_list = [], []
		for process in user_process_list:
			if self.processes[process]:
				active_list.append(process)
			else:
				inactive_list.append(process)
			
		print("Of the processes you inputted, the active processes are: ", active_list)
		print("Of the processes you inputted, the inactive processes are: ", inactive_list)


	def update(self):
		updates = {}
		loop_Flag = True
		
		while loop_Flag:
			key = input("Please enter the process you would like to update. When you are finished, please type \"done\": ").lower()
			
			if key == 'done':
				self.processes.update(updates)
				# print(self.processes)
				loop_Flag = False

				
			elif not self.verify(key):
				print("The submitted process isn't possible to update.")

			elif self.verify(key) and key not in updates:
				value = input("Please enter the process' new value, either 'True' and 'False': ")

				while value != 'True' and value != "False":
					value = input("Sorry, acceptable answers include 'True' and 'False': ")
				
				updates[key] = value

		
	def add_new_process(self):
		current_processes = self.processes
			
		loopFlag = True
		while loopFlag:
			try:
				process = input("Please enter a process name and a process definition seperated by a comma. When you are finished, please type \"done\": ")
				
				process = ''.join(process.split())
				
				if process == "done":
					loopFlag = False
					return current_processes
					
				elif process.split(",")[0].lower() in self.processes:
					print("You have entered a duplicate process definition")
					
				elif process.split(",")[1].lower() != 'true' and process.split(",")[1].lower() != 'false':
					print("The process definition you entered was invalid")
				
				else:
					current_processes[process.split(",")[0]] = process.split(",")[1]
					# print(self.processes)

			except ValueError:
				print("Error. Please try again")

def main():
	
	PCB_obj = PCB()
	queue = PCB_obj.readFile()


	PCB_obj.print_active_processes(PCB_obj.getInput())

	print("\nWould you like to add a new process or update a process?")

	process = input("Please enter \"update\", \"add\". Or enter \"done\" if you're finished with the program: ").lower()

	while process != 'add' and process != 'update' and process != 'done':
		print("Sorry, that isn't an acceptable answer.")
		process = input("Please enter \"update\", \"add\" or \"done\": ").lower()

	if process == 'add':
		PCB_obj.add_new_process()
		print(processes)
	elif process == 'update':
		PCB_obj.update()
		print(processes)
	elif process == 'done':
		print("Smell ya later")


if __name__ == '__main__':
	main()
