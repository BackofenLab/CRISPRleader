# -*- coding: utf-8 -*-
"""CRISPRleader.
Usage:
  CRISPRleader.py r_l_o (<repeat> <leader> <organism>)
  CRISPRleader.py f_c_o (<file> <completeness> <organism>)
  CRISPRleader.py d_f_o (<acc_num> <organism>)
  
Options:
  -h --help     

@author: CRISPRleader Team  
"""

import os
import shutil
import sys
import string
from docopt import docopt



def include_modules():
	path = os.path.realpath(__file__)
	path = string.replace(path, "\\", "//")
	path = path.split("/")
	for i in range(len(path)):
		path[i] = path[i] + "/"
	path[len(path) - 1] = "modules"
	path = "".join(path)
	sys.path.insert(0, path)	
	print("modules were included in the path")	

	
#############################################################################################################################################################
#### Main function 
#### Starting point of the program. It will remove if there exists a "temp_folder" in the current working directory before validating the input.
#### The function will again remove the "temp_folder" at the end of program execution which stores all the temporary files.
############################################################################################################################################################
		




if __name__ == '__main__':
	
	include_modules()
	from check_requirements import check_requirements
	from validate_input import validate_input
	
	
	arguments = docopt(__doc__)
	
	print("starting the script with corresponding parameters")	
	
	check_requirements()										## This function checks whether all the file requirements exist in the repective folders
	
	
	if os.path.exists("temp_folder"):							## if there already exists a "temp_folder", remove it
		shutil.rmtree("temp_folder")
		
	scenario = validate_input(arguments)						## This function validates the input and call the corresponding functions to proceed the further execution
		
	if scenario[0] == "Scenario_r_l_o":
		from scenario_r_l_o import scenario_r_l_o
		scenario_r_l_o(scenario[1], scenario[2], scenario[3])
	if scenario[0] == "Scenario_f_c_o":
		from scenario_f_c_o import scenario_f_c_o	
		scenario_f_c_o(scenario[1], scenario[2], scenario[3])
	if scenario[0] == "Scenario_d_f_o":
		from scenario_d_f_o import scenario_d_f_o
		scenario_d_f_o(scenario[1], scenario[2])
				
