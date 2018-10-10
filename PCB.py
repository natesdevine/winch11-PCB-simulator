from string import ascii_lowercase 
import random

class PCB(object):

	def __init__(self, processes):      
		self.processes = processes

	def getInput(self):
		loopFlag = True
		process_list = []
		while loopFlag:
			try:
				print("Current process list: ", process_list)
				process = input("Please enter a process definition. When you are finished, please type \"done\": ").lower()
				
				if process == "done":
					loopFlag = False
					print("Final process list: ", process_list)
					return process_list

				elif not self.verify(process):
					print("The process definition you entered was invalid")
					
				elif process not in process_list:
					process_list.append(process)
				else:
					print("You have entered a duplicate process definition")
					
			except ValueError:
				print("Error. Please try again")
				
	def verify(self, process):
		if process in self.processes:
			return True
		return False
		
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
	processes = {}

	for letter in ascii_lowercase:
		choice = random.randint(1, 101)
		if choice >= 50:
			processes[letter] = True
		else:
			processes[letter] = False

	print(str(processes) + "\n")
	
	PCB_obj = PCB(processes)
	
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
