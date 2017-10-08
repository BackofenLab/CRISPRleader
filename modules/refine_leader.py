#####################################################################################################################################################################
#### This function "refineLeader()" trim the potential leaders of all the CRISPR sequences according to the average size of their associated cluster and write to a file.
#### The function execution is different with different input. If "-r/-l" is chosen, then the variable "CRISPR_Leader_PROVIDED"  is enabled and only the given
#### leader is trimmed and written to the output file. If other input is provided, the variable "CRISPR_Leader_PROVIDED"  is disabled and  all the leaders of the 
#### CRISPR sequences in the Genome are trimmed and written to the output file.
#####################################################################################################################################################################
import os


def refine_leader(Archaea_Bacteria, ClusterAverageSizeDictionary, CRISPR_Leader_PROVIDED, FinalClusterOfEachRepeat):
	
	LibFiles = []
	for file in os.listdir("lib"):
		if file.endswith("Seqs.fa"):
			LibFiles.append(file)
	
	'''
	:param Archaea_Bacteria - This parameter is reqired to write the category(Archaea or Bacteria) of a cluster in an output file
	:param ClusterAverageSizeDictionary - This dictionary contains the inforamtion about the average size of the leader of all the realted clusters
                                          and is used to trim the potential leader of the repeat according to the average size.
	:param CRISPR_Leader_PROVIDED - This boolean parameter decide the type of execution and it depends on the given input.
									This parameter is enabled if repeat and leader are given as input in the runtime arguments.
	:param FinalClusterOfEachRepeat - Cluster information of each repeat is stored in this list and is used by 'ClusterAverageSizeDictionary' to get the leader size
	'''
	
	# if repeat and leader are given as input in runtime arguments
	if CRISPR_Leader_PROVIDED:	# open an output file to save the cluster name, given repeat and modified leader 
		Write_CRISPR_Cluster_InfoFile = open("Output/Output.txt","w")
		Write_CRISPR_Cluster_InfoFile.write("Cluster_ID\tRepeat\tLeader\n\n")
		
	# if a genome or accession number is given in the runtime arguments, proceed with the below
	elif not CRISPR_Leader_PROVIDED: # open an output file to save the Crispr ID, its consenus repeat, its position, strand, cluster Id, leader position and modified leader
		Write_CRISPR_Cluster_InfoFile = open("Output/CRISPR_Info.txt","w")
		Write_CRISPR_Cluster_InfoFile.write("CRISPR_ID\tConsensus\tCRISPR_Position\tStrand\tCluster_ID\tLeader_Position\tLeader\t\n==================================================================\n")
		
		LeaderInfoFile = open("temp_folder/CRISPR_LeaderInfo.txt","r")	# read this file to check whether there exists a potential leader for a particular CRISPR 
		LeaderFile = open("temp_folder/CRISPR_Final_Leader.txt","r")	# read the leader of each repeat from this file
		
		eachLeaderSequence = LeaderFile.readline() # reading '>' line
		eachLeaderSequence = LeaderFile.readline() # reading leader sequence line
		
		eachLeader = LeaderInfoFile.readline() # reading header line
		eachLeader = LeaderInfoFile.readline() # reading delimeter =======
		eachLeader = LeaderInfoFile.readline() # reading Leader info
	
	# if repeat and leader are given as input in runtime arguments
	if CRISPR_Leader_PROVIDED:	# read the given repeat and leader from "TempRepeatLeaderFile.fasta" file
			
		TempRepeatLeaderFile = open("temp_folder/TempRepeatLeaderFile.fasta","r")
		Repeat = TempRepeatLeaderFile.readline()				# read the repeat
		eachLeaderSequence = TempRepeatLeaderFile.readline()	# read the leader
		TempRepeatLeaderFile.close()
			
		if "\n" in Repeat:    		## if a newline delimeter present in the string Repeat, remove the delimeter
			Repeat = Repeat[:-1]
			
		Cluster = FinalClusterOfEachRepeat[0]	#	get the clusterID of the repeat which it belongs to
		
		if  Cluster == "-":		# if repeat is not assigned to any cluster, provide no cluster information in the output file
			Write_CRISPR_Cluster_InfoFile.write("No_Cluster\t"+Repeat+"\t"+eachLeaderSequence+"\n")
			
		else:	# if there exists a cluster for the repeat, provide the cluster name, repeat and modified leader in the output file
			ClusterAverageSize = ClusterAverageSizeDictionary[Cluster]#get the average size of the leader defined for the cluster and trim the given leader accordingly
			clusterName = next((s for s in LibFiles if s.endswith(Archaea_Bacteria+Cluster+"_Seqs.fa")), None)
			clusterName = clusterName[:clusterName.rindex('_')]
			Write_CRISPR_Cluster_InfoFile.write(clusterName+"\t"+Repeat+"\t"+eachLeaderSequence[-ClusterAverageSize:])
	
	# if a genome or accession number is given in the runtime arguments, proceed with the below
	elif not CRISPR_Leader_PROVIDED:  
		
		count = -1
		while eachLeader != "":
					
			count = count + 1
			eachWord = eachLeader.split()	
			# write CRISPR_ID, Consensus repeat, CRISPR_Position, strand of one CRISPR to output file
			
			Write_CRISPR_Cluster_InfoFile.write(eachWord[0]+"\t"+eachWord[1]+"\t"+eachWord[2]+"\t"+eachWord[5]+"\t")
				
			if not "yes" in eachLeader: # if a potential leader does not exist, then there is no cluster associated with the repeat
				Write_CRISPR_Cluster_InfoFile.write("No_ClusterID\t-\tLeaderless\n")
					
			elif "yes" in eachLeader:	# if there exists a cluster for the repeat
									
				EachCluster = FinalClusterOfEachRepeat[count]	# get the cluster of the repeat
					
				if  EachCluster == "-":	# if no cluster found
					Write_CRISPR_Cluster_InfoFile.write("No_ClusterID\t-\tLeaderless\n")
						
				else:	# if there exists a cluster, fetch the cluster from the dictionary
					ClusterAverageSize = ClusterAverageSizeDictionary[EachCluster]
					
					Leader = eachLeaderSequence[-ClusterAverageSize:]	#	trim the leader based on cluster average size info
					
					# update the leader start and end position range according to the changes made on leader after trimming it based on cluster average size info
					LeaderPos = eachWord[4].split("-")
					if eachWord[5]=="Reverse":	# if the crispr in reverse strand, update the end position
						LeadetStartPos = int(LeaderPos[0])
						LeadetEndPos = LeadetStartPos + ClusterAverageSize
							
					elif eachWord[5]=="Forward":	# if the crispr in forward strand, update the start position
						LeadetEndPos = int(LeaderPos[1])
						LeadetStartPos = LeadetEndPos - ClusterAverageSize
													
					if "\n" in Leader:	## if a newline delimeter present in the string Leader, remove the delimeter
						Leader = Leader[:-1]

					#append the statements cluster name, leader start-end position and the modified leader to the output file
					clusterName = next((s for s in LibFiles if s.endswith(Archaea_Bacteria+EachCluster+"_Seqs.fa")), None)
					clusterName = clusterName[:clusterName.rindex('_')]
					Write_CRISPR_Cluster_InfoFile.write(clusterName+"\t"+str(LeadetStartPos)+"-"+str(LeadetEndPos)+"\t"+Leader+"\n")
						
				eachLeaderSequence = LeaderFile.readline()	# read the next repeat
				eachLeaderSequence = LeaderFile.readline()	# read the next leader
					
			eachLeader = LeaderInfoFile.readline()	# read the next crispr info

	# close the file descriptors
	Write_CRISPR_Cluster_InfoFile.close()
		
	if not CRISPR_Leader_PROVIDED:	
		LeaderInfoFile.close()
		LeaderFile.close()
