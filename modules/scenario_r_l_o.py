import os
import shutil
from findRelatedClusters import findRelatedClusters
from clusterModels import clusterModels
from performMSA_mview import performMSA_mview

def scenario_r_l_o(RepeatConsensus, Leader, Archaea_Bacteria):
	os.mkdir("temp_folder")			# create the temporary folder
	cmd = "chmod 777 temp_folder"	
	os.popen(cmd)					# Provide all the access permissions to the temporary folder using this statement

	if os.path.exists("Output"):	# if there exists 'Output' folder before, remove it
		shutil.rmtree("Output")

	os.mkdir("Output")				# create the folder 'Output' in the current working directory
	os.chmod('Output', 0777)

	TempFile = open("temp_folder/TempRepeatLeaderFile.fasta","w")	# Save the given repeat and leader in a file under temporary folder
	print("saving TempRepeatLeaderFile.fasta") 
	TempFile.write(RepeatConsensus+"\n")
	TempFile.write(Leader)
	TempFile.close()

	os.chmod('temp_folder/TempRepeatLeaderFile.fasta', 0777)	# provide all permissions to this file

	ClustersOfEachRepeatArray = findRelatedClusters(Archaea_Bacteria, True)	# calling a function to obtain the related clusters of the given repeat
																				# and their corresponding repeat sizes
	clusterModels(Archaea_Bacteria, True, ClustersOfEachRepeatArray)	#call this function to determine cluster of the given repeat and also decide its leader size

	performMSA_mview("",True)	# The function is called to view the alignment of the given leader with its cluster family sequences in a html file

	print "\nResult is saved in 'Output' folder in your current working directory\n"
