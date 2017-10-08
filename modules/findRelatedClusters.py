##################################################################################################################################################################
#### The finction "findRelatedClusters()" find the related clusters for the given consensus repeat. The function execution differs with the given input.
#### If "r_l_o" is chosen, the repeat is written to a text file. If other input is chosen, all the consensus repeat of all the CRISPR is written to a text file.
#### The text file is passed as input to needleman wunsch program which run against the "Bacteria / Arhcea" family to find the similarity scores of each repeat.
#### The top three members of the family having high score are for each repeat and their associated clusters are selected.
##################################################################################################################################################################

import os
import subprocess
import numpy as np
import sys

def cmd_replace1():
	
	def last_num_to_float(last_num):
		last_num = last_num[1:-2]
		last_num = float(last_num)
		return last_num
	
	list_of_lines = []
	list_result = []	
	with open ('temp_folder/TmpFamilyInfo.txt') as f:
		for line in f:
			if line == "\n":
				break				
			else:
				list_of_lines.append(line.split(' '))
	
	for line in list_of_lines:
		line[-1] = last_num_to_float(line[-1])
		
	list_of_lines = sorted(list_of_lines, key=lambda line: line[3], reverse=True)
	
	counter = 0
	for line in list_of_lines:
		if counter > 4:
			break
		else:
			if line[1] not in list_result:
				list_result.append(line[1])
				counter += 1
			
	
		
	return list_result
	
def cmd_replace2(archaea_bacteria_flag, each_member_num, cluster_info_file):
	with open(cluster_info_file) as f:
		for line in f:
			if (archaea_bacteria_flag + each_member_num) in line:
				return line
			
	
	
		

def findRelatedClusters(Archaea_Bacteria, CRISPR_Leader_PROVIDED):
	def cmd_replace1():
		
		def last_num_to_float(last_num):
			last_num = last_num[1:-2]
			last_num = float(last_num)
			return last_num
		
		list_of_lines = []
		list_result = []	
		with open ('temp_folder/TmpFamilyInfo.txt') as f:
			for line in f:
				if line == "\n":
					break				
				else:
					list_of_lines.append(line.split(' '))
		
		for line in list_of_lines:
			line[-1] = last_num_to_float(line[-1])		
			
		list_of_lines = sorted(list_of_lines, key=lambda line: line[3], reverse=True)		
				
		counter = 0
		for line in list_of_lines:
			if counter > 4:
				break
			else:
				if line[1] not in list_result:
					list_result.append(line[1])
					counter += 1
		
		return list_result
	
	def cmd_replace2(archaea_bacteria_flag, each_member_num, cluster_info_file):
		with open(cluster_info_file) as f:
			for line in f:
				if (archaea_bacteria_flag + each_member_num) in line:
					return line
	'''
	:param AccessionNumber: This parameter allows us to choose the dataset file to compare with the repeat(s) inorder to find the related clusters.
	:param CRISPR_Leader_PROVIDED : This boolean parameter decide the type of execution and it depends on the given input.
									This parameter is enabled if repeat and leader are given as input in the runtime arguments.
	'''

	print "\nFinding related clusters.."
	NumberOfRelatedClusters = 1

	if CRISPR_Leader_PROVIDED:	# if repeat and leader are given in runtime arguments
		TempRepeatLeaderFile = open("temp_folder/TempRepeatLeaderFile.fasta","r") # open the file which contains repeat-leader & read them
		Repeat = TempRepeatLeaderFile.readline()
		TempRepeatLeaderFile.close()
		TempRepeat = open("temp_folder/TempRepeatFile.fasta","w")	# save the above repeat in a new fasta file under temporary folder
		TempRepeat.write(">R1\n"+Repeat)
		TempRepeat.close()
		NumberOfRepeat = 1

	else:	# if a genome or accession number is given in the runtime arguments, proceed with the below
		Repeat_Leader_InfoFile = open("temp_folder/CRISPR_LeaderInfo.txt","r") #read the file that contains consensus repeats of all the CRISPRs,
																			   #protein & leader pos in the given sequence
		eachRepeat = Repeat_Leader_InfoFile.readline() ## reading header
		eachRepeat = Repeat_Leader_InfoFile.readline() ## reading delimeter ===========
		eachRepeatLine = Repeat_Leader_InfoFile.readline() ## reading first Repeat info
		NumberOfRepeat = 0

		# create a temporary fasta file to store all the repeats in fasta format
		TempRepeat = open("temp_folder/TempRepeatFile.fasta","w")
		while eachRepeatLine != "":

			 eachRepeatLine = eachRepeatLine.split()
			 NumberOfRepeat = NumberOfRepeat + 1

			 TempRepeat.write(">R"+str(NumberOfRepeat)+"\n"+eachRepeatLine[1]+"\n")

			 eachRepeatLine = Repeat_Leader_InfoFile.readline() ## reading another line in the file "temp_folder/CRISPR_LeaderInfo.txt" to retireve another CRISPR info

		TempRepeat.close()
		Repeat_Leader_InfoFile.close()

	# select the corresponding dataset file to compare with the given repeat inorder to find the related clusters
	if Archaea_Bacteria == "A":
		datasetPath = "lib/Archaea_Final_Repeat_dataset.fa"
	else:
		datasetPath = "lib/Bacteria_Final_Repeat_dataset.fa"

	os.chmod('temp_folder/TempRepeatFile.fasta', 0777)	# provide all access permssions to the file

	#Execute the needleman wunch command line operation on the repeat(s) against selected dataset to find their similarity score for all the clusters
	cmd = "bin/./needleall -asequence temp_folder/TempRepeatFile.fasta -bsequence "+datasetPath+" -gapopen 10 -gapextend 0.5 -outfile temp_folder/TmpFamilyInfo.txt"
	cmd = cmd + " > /dev/null 2>&1"
	os.popen(cmd)

	# Remove the file "needleall.error" which is created after executing the above command
	if os.path.exists("needleall.error"):
		os.remove("needleall.error")

	if not os.path.exists("temp_folder/TmpFamilyInfo.txt"):	# Needleman wunsch result should be saved in the file "TmpFamilyInfo.txt" under temporary folder
		print "Error in executing needleman-wunsch."		# Throw an error and exit the program if the file is missing after execution of needleman wunsch
		sys.exit()

	os.chmod('temp_folder/TmpFamilyInfo.txt', 0777)			# if the file is saved in the temporary folder, provide all access permissions to it

	RepeatNumber = 1
	Clusters = []					#This 1D list is to store all the related clusters of all the repeats
	ClustersOfEachRepeatArray = []	# This 2D list is to store all the related clusteres of each repeat as a list

	while NumberOfRepeat >= RepeatNumber :	# loop through all the repeats and find the top 5 related clusters for each repeat
		
		
		'''
		#cmd = "grep 'R"+str(RepeatNumber)+"' temp_folder/TmpFamilyInfo.txt | sort -r -k 4,4 -V | sort -u -k 2,2 | sort -r -k 4,4 -V | head -n 5 | awk '{print $2}'"
		cmd1 = "grep 'R"+str(RepeatNumber)+"' temp_folder/TmpFamilyInfo.txt | sort -r -k 4,4 -V >temp_folder/test1.txt"
		TempFamily1 = subprocess.check_output(cmd1,shell=True)
		
		cmd2 = "grep 'R"+str(RepeatNumber)+"' temp_folder/TmpFamilyInfo.txt | sort -r -k 4,4 -V | sort -u -k 2,2 >temp_folder/test2.txt"
		TempFamily2 = subprocess.check_output(cmd2,shell=True)
		
		cmd3 = "grep 'R"+str(RepeatNumber)+"' temp_folder/TmpFamilyInfo.txt | sort -r -k 4,4 -V | sort -u -k 2,2 | sort -r -k 4,4 -V >temp_folder/test3.txt"
		TempFamily3 = subprocess.check_output(cmd3,shell=True)
		
		print cmd_replace1()
		'''
		'''
		cmd = "grep 'R"+str(RepeatNumber)+"' temp_folder/TmpFamilyInfo.txt | sort -r -k 4,4 -V | sort -u -k 2,2 | sort -r -k 4,4 -V | head -n 5 | awk '{print $2}'"		
		TempFamily1 = subprocess.check_output(cmd1,shell=True)
		TempFamily = TempFamily.split()
		'''
		
		TempFamily = cmd_replace1()
		

		ClustersOfEachRepeatArray.append(TempFamily)	# store the related clusters as a list in anothter list  'ClustersOfEachRepeatArray'
		Clusters.extend(TempFamily)						# store the related clusters as elements in another list 'Clusters'
		RepeatNumber = RepeatNumber + 1

	Clusters = list(set(Clusters))	# remove duplicates from 1D list 'Clusters'

	###### copy the related cluster IDs of all the repeats and their corresponding repeat size from "lib/clustInfos.tab" file to another temporary file
	write_ClusterAverageSizeFile = open("temp_folder/clusterSizeInfo.txt","w")
	ClustersInfoFile = "lib/clustInfos.tab"
	for eachMember in Clusters:		# collect the repeat size of each cluster and write to a file		
		try:
			
			AverageSize = cmd_replace2(Archaea_Bacteria, eachMember, ClustersInfoFile)					
		except:
			
			print "Error: finding related cluster size"

		if "\n" in AverageSize:				# if the retrieved line from "lib/clustInfos.tab" file contains 'newline' delimeter,
			AverageSize = AverageSize[:-1]	#delete it by removing the last character

		write_ClusterAverageSizeFile.write(AverageSize)	# write the retrieved size in the temporary file
		write_ClusterAverageSizeFile.write("\n")
	write_ClusterAverageSizeFile.close()

	ClustersOfEachRepeatArray = np.asarray(ClustersOfEachRepeatArray) # Each index of this array represents related clusters of a consensus repeat
	print "\nRelated clusters are found."
	print ClustersOfEachRepeatArray
	return ClustersOfEachRepeatArray
