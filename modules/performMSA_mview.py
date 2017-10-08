##########################################################################################################################################################
#### The function "performMSA_mview" executes Mafft for multisequence alignment of the repsective leader against it's associated cluster family sequences
#### and perfrom 'mview' operation on the alignment to generate html file which is helpful for visualization.
#### This function provides additional visualization feature by creating .bed file if genome or accession number is given as input
##########################################################################################################################################################

import os
from shutil import copyfile
import platform
from Bio.Align.Applications import MafftCommandline

def performMSA_mview(AccessionNumber, CRISPR_Leader_Provided):	
	'''
	:param AccessionNumber- This parameter is required to edit the .bed file 
	:CRISPR_Leader_Provided - This boolean parameter decide the type of execution and it depends on the given input. 
							  This parameter is enabled if repeat and leader are given as input in the runtime arguments.
	'''
	
	ClustersAndNumberOfLeaders = {}	# dictionary to store information about the number of repeats that belongs to one cluster
	
	if CRISPR_Leader_Provided:	# if repeat and leader are given as input in runtime arguments
		NumberOfCRISPR = 1
		LeaderFileInfo = open("Output/Output.txt","r") # read the file that contains repeat, final leader and its associated cluster information
		Leaderline = LeaderFileInfo.readline() # ignore the header of the file
		Leaderline = LeaderFileInfo.readline() # ignore the delimeter that follows the header
		Leaderline = LeaderFileInfo.readline() # get the repeat, final leader and its associated cluster information

		if not "No_Cluster" in Leaderline:	# if there exists a cluster for the repeat, proceed the execution, or else return to the caller
			Leader = Leaderline.split()
			Cluster = Leader[0]			# get the ClusterID
			Leader = Leader[-1]			# get the leader
			
			# copy the cluster information from 'lib' folder to temporary folder inorder to add the leader into existing list 
			copyfile("lib/"+Cluster+"_Seqs.fa", "temp_folder/"+Cluster+"_Seqs.fa")	
			
			# add the final leader to the list of existing family sequences in fasta format to perform multisequence alignment
			ClusterSeqsFile = open( "temp_folder/"+Cluster+"_Seqs.fa","a")
			ClusterSeqsFile.write(">L"+str(NumberOfCRISPR)+"\n")    # fasta format
			ClusterSeqsFile.write(Leader.lower()+"\n")              # trasforming the characters to lowercase 
			ClusterSeqsFile.close()
			
			#TotalClusters = [Cluster+"_Seqs.fa"]
			TotalClusters = [Cluster]	# list to store the clusters of all repeats, in this case it would be only one cluster in the list
			
			ClustersAndNumberOfLeaders[Cluster] = 1	# dictionary to store the number of repeats that belong to a cluster, in this case there is only 1 repeat to 1 cluster
			
		else:	# if no cluster found, return to the caller
			print "\nNo related cluster found"
			return
			
	else:	# if a genome or accession number is given in the runtime arguments, proceed with the below
		
        # .bed format requires the Acession number,leader start-end position and its corresponding strand in a line.
        # The following line should contain the same Accession number, crispr start-end position and the strand.
		ReadClusterInfoFile = open("Output/CRISPR_Info.txt","r") # read the required inforamtion from this file
		
        # create the .bed file
		WriteBedFormat = open("Output/CRISPR_Array_Leader_Annotation.bed","w")
		
		LeaderOfCRISPR = ReadClusterInfoFile.readline() # ignore the header
		LeaderOfCRISPR = ReadClusterInfoFile.readline() # igonre the delimeter
		
		LeaderOfCRISPR = ReadClusterInfoFile.readline() # read the first cripsr inforamtion
		
		TotalClusters = [] # list to store the clusters of all repeats which is used in execution of mafft and mview
		NumberOfCRISPR = 0  # variable to note each CRISPR serial number which is also needed for .bed file
		
		while not LeaderOfCRISPR in ('\n', ''): # loop through all the CRISPRs information from the file "CRISPR_Info.txt"
			
			LeaderOfCRISPR = LeaderOfCRISPR.split()
			
			NumberOfCRISPR = NumberOfCRISPR + 1 # increment the serial order as you visit new CRISPR in the file
			
            # write the information of a CRISPR to .bed file only if it belongs to a valid cluster and there exists a potential leader
			if not "No_ClusterID" in LeaderOfCRISPR: 
				
				if not "Leaderless" in LeaderOfCRISPR:
					
					CRISPR_ID = LeaderOfCRISPR[0]
					Cluster = LeaderOfCRISPR[-3]
					Leader = LeaderOfCRISPR[-1]
					
					LeaderPos = LeaderOfCRISPR[-2].split("-")
					LeaderStartPos = LeaderPos[0]
					LeaderEndPos = LeaderPos[1]
					
                    # write the information to .bed file
					WriteBedFormat.write(AccessionNumber+"\t"+LeaderStartPos+"\t"+LeaderEndPos+"\tLeader"+str(NumberOfCRISPR)+"\t"+"."+"\t"+LeaderOfCRISPR[3]+"\n")
					
                    # Along with the editing of .bed file, also copy the cluster family inforamtion to temporary folder to append the leader
                    # of the current processing CRISPR to the existing list of cluster family. Thereafter perfom mafft and mview
					if not Cluster in TotalClusters:    # if cluster's information is already copied then don't copy it again
						copyfile("lib/"+Cluster+"_Seqs.fa", "temp_folder/"+Cluster+"_Seqs.fa")  # copy the inforamtion
						#TotalClusters.append(Cluster+"_Seqs.fa")
						TotalClusters.append(Cluster)   # add the cluster to the list
						
					ClusterSeqsFile = open( "temp_folder/"+Cluster+"_Seqs.fa","a") # open the temporary cluster information 
					ClusterSeqsFile.write(">L"+str(NumberOfCRISPR)+"\n")           # to append the current leader
					ClusterSeqsFile.write(Leader.lower()+"\n")
					ClusterSeqsFile.close()
					
                    # Information about number of leaders that belong to a single cluster is maintained in the dictionary "ClustersAndNumberOfLeaders"
                    # Increment the value of the key 'Cluster' if a new leader belong to it.
					ClustersAndNumberOfLeaders[Cluster] = ClustersAndNumberOfLeaders.get(Cluster, 0) + 1
					
            # get the crispr start and end position which is also required for .bed file
			CRISPR_pos = LeaderOfCRISPR[2].split("-")
			CRISPR_StartPos = CRISPR_pos[0]
			CRISPR_EndPos = CRISPR_pos[1]
			
            # write accession number, crispr start-end position and also its strand
			WriteBedFormat.write(AccessionNumber+"\t"+CRISPR_StartPos+"\t"+CRISPR_EndPos+"\tCRISPR"+str(NumberOfCRISPR)+"\t"+"."+"\t"+LeaderOfCRISPR[3]+"\n")
			
			LeaderOfCRISPR = ReadClusterInfoFile.readline() # read next crispr inforamtion
			
		ReadClusterInfoFile.close()
		WriteBedFormat.close()
	
	if len(TotalClusters) == 0:
		print "\nNo Leader found"
		return
	
	Platform = platform.architecture()					## check the platform is 64bit or 32 bit and 
														## accordingly select the mafft path
	if '64bit' in Platform:
		maffPath = "bin/Mafft/mafft-linux64/mafft.bat"
		
	elif '32bit' in Platform:
		maffPath = "bin/Mafft/mafft-linux32/mafft.bat"
		
    
    # Perfrom the mafft command line operation on each cluster family to find the alignment of the leader against the cluster family sequences and
    # invoke mview tool to visulaize the alignment in a html page
	for eachCluster in TotalClusters:
		
		mafft_cline = MafftCommandline(maffPath,input= "temp_folder/"+eachCluster+"_Seqs.fa") # create a mafft command line object for the cluster family
		mafft_cline.set_parameter("--auto","True") # Automatically selects an appropriate strategy from L-INS-i, FFT-NS-i and FFT-NS-2, according to data size
		mafft_cline.set_parameter("--reorder","True") # Output order: aligned
		mafft_cline.set_parameter("--ep",0.0) # Offset value, which works like gap extension penalty, for group-to-group alignment
		stdout, stderr = mafft_cline()  # execute the mafft command line with the given parametes on the cluster family. 'stdout' and 'stderr' conatins the ouput and error of mafft respectively
		
		if CRISPR_Leader_Provided: # if repeat and leader is provided as input, print the cluster of the leader
			print "The given leader belong to "+ eachCluster
		
		else: # print the number of leaders that belong to a cluster if genome or accession number is given as input
			print str(ClustersAndNumberOfLeaders[eachCluster])+" leader(s) belong to "+ eachCluster
		
		with open("temp_folder/FamilyAlignment.aln", "w") as handle:    # write the mafft output to a file
			handle.write(stdout.upper())
		handle.close()
        
		#generate  reader-friendly HTML page from the above created file using mview tool and store it in 'Output' folder
		cmd = "cat temp_folder/FamilyAlignment.aln | bin/mview -in fasta -html body -coloring consensus -con_threshold 90 -rule on -consensus on > Output/"+eachCluster+"_NewLeader_MSA.html"
		os.popen(cmd) # execute the above command
		
	print "Generated html output files."
	
	if os.path.exists("Output"):				## if there exists 'Output' directory, the following statement provide all the required permissions to 
		os.system('chmod 777 -R Output/*')		## access all the files present in that folder
		

