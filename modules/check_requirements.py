#Function to check if folder contains the necessary libraries

import os
def check_requirements():   
	if not os.path.exists("bin"):   # if there is no 'bin' folder, throw an error and exit the program.
		print "'bin' folder does not exist. Exiting the program.."
		sys.exit()
		
	if not os.path.exists("lib"):   # if there is no 'lib' folder, throw an error and exit the program.
		print "'lib' folder does not exist. Exiting the program.."
		sys.exit()
	
    # These are the name of the programs that should exist in the 'bin' folder
	bin_check_list = ["CRT1.2-CLI.jar","EDeN","prodigal","needleall","hmmsearch", "mview"]
	
	for each in bin_check_list:     # check whether all the listed files present in the 'bin' folder. If not, throw an error and exit the program.
		if not os.path.isfile("bin/"+each):
			print each+" is missing from 'bin' folder. Exiting the program.."
			sys.exit()
	# These are the check list of the files that should be exist in 'lib' folder
	lib_check_list = ["DR_Repeat_model", "Archaea_Final_Repeat_dataset.fa", "Bacteria_Final_Repeat_dataset.fa","clustInfos.tab","Bacteria_LeaderClusters_mean_std.tab", "Archaea_LeaderClusters_mean_std.tab"]
	
	for eachFile in lib_check_list: # check whether all the listed files present in the 'lib' folder. If not, throw an error and exit the program.
		if not os.path.isfile("lib/"+eachFile):
			print eachFile+" is missing from 'lib' folder. Exiting the program.."
			sys.exit()
	print("The setting satisfies the requirements")






