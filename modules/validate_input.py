############################################################################################################################################################
#### The function "validateInput()" verify the correctness of provided runtime arguments.
#### If argument is not correct, program exit with an error.
#### If yes, the function redirect the execution to the corresponding function. A folder "temp_folder" is created to store 
#### all the temporary files and folders. It will be deleted at the end of the program execution.
#### If "-g" included as an argument, the function look for the given fasta file name in the given path in local system.
#### If "-a" is chosen as argument, the inforamtion of the given Accession number will be downloaded from "ncbi" website.
#### if "-r" or "-l" is chosen, related clusters for the repeat are selected using function 'findRelatedClusters()' and final cluster will be deicided by 
#### function 'clusterModels()'
#############################################################################################################################################################

import sys
import re
import os

def validate_input(arguments):
	
	def if_correct_seq(seq):
		validateSequence = re.compile(r'[^ATGC]').search # input is a DNA seq
		if bool(validateSequence(seq)):
			return "Incorrect"
		else:
			return "Correct"
	
	def if_correct_organism(flag_organism):
		if flag_organism == "A" or flag_organism == "B":
			return "Correct"
		else:
			return "Incorrect"   
			
		
	if arguments["r_l_o"] is True:
		
		for key in arguments:
			if type(arguments[key]) is str:
				arguments[key] = arguments[key].upper()
		
		
		check_repeat = if_correct_seq(arguments["<repeat>"])
		if check_repeat == "Incorrect":
			print ("Incorrect repeat sequence")
			return "Input Error"
			
		check_leader = if_correct_seq(arguments["<leader>"])
		if check_leader == "Incorrect":
			print ("Incorrect leader sequence")
			return "Input Error"
			
		check_organism = if_correct_organism(arguments["<organism>"])		
		if check_organism == "Incorrect":
			print ("Incorrect organism")
			return "Input Error"	   
    
		else:    
			print "Scenario where the repeat, the leader and the organism are provided"
			return "Scenario_r_l_o", arguments["<repeat>"], arguments["<leader>"], arguments["<organism>"]
			
	elif arguments["f_c_o"] is True:
		print "Scenario where the fasta file, completeness and the organism are provided"
		return "Scenario_f_c_o", arguments["<file>"], arguments["<completeness>"], arguments["<organism>"]
		
	elif arguments["d_f_o"] is True:
		print "Scanario where accession number and organism are provided to download from NCBI"
		return "Scenario_d_f_o", arguments["<acc_num>"], arguments["<organism>"]
	else:
		print "Wrong parameters, use -h for help"		
		
    
