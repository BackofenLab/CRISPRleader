##############################################################################################################################################
##### This function "clusterModels" gatheres the average leader size of the related clusters of all the leaders.
##### For each leader, the function "CalculateHmmScore" is invoked to find the most relevant cluster of the leader.
##### Finally, this function calls another function 'refineLeader' to decide size of the potential leader of each
##### repeat based on the average size of their associated cluster.
##############################################################################################################################################
import re
from calculate_hmm_score import calculate_hmm_score
from refine_leader import refine_leader
import os

def clusterModels(Archaea_Bacteria, CRISPR_Leader_PROVIDED, ClustersOfEachRepeatArray):
    '''
    :param Archaea_Bacteria : This parameter is passed to 'CalculateHmmScore' function to pick the corresponding cluster mean and standard deviation file .
    :param CRISPR_Leader_PROVIDED : This boolean parameter decide the type of execution and it depends on the given input.
									This parameter is enabled if repeat and leader are given as input in the runtime arguments.
    :param ClustersOfEachRepeatArray : Each row in this matrix represents the corresponding related clusters and a final cluster is determined using "CalculateHmmScore" function
    '''

    if CRISPR_Leader_PROVIDED:	# if repeat and leader are given in runtime arguments
		print "\nRefning the leaders and deciding the cluster of the given repeat..\n"
    else:	# if a genome or accession number is given in the runtime arguments, proceed with the below
		print "\nRefning the leaders and deciding the cluster of each repeat..\n"

    ClusterAverageSizeDictionary = {}	# dictionary to store the clusterID and its coresponding leader size

    #Read each cluster and thier leader size from the file "temp_folder/clusterSizeInfo.txt" and store them in dictionary
    ClustersAverageSizeFile = open("temp_folder/clusterSizeInfo.txt","r")
    eachLine = ClustersAverageSizeFile.readline()

    # loop through each cluster and note the cluster ID and their average size of the leader
    while not eachLine in ("\n", ''):
		name_size = eachLine.split()
		name = name_size[0]						#get the cluster name, say 'A15'
		ClusterID = re.findall(r'\d+', name)[0] #pick the clusterID from the cluster name, say '15' from 'A15'

		ClusterAverageSize = int(name_size[1])	# get the average size of the leader
		ClusterAverageSizeDictionary[ClusterID ] = ClusterAverageSize	# add the info to dictionary
		eachLine = ClustersAverageSizeFile.readline()	# read the next line

	#End reading from the file "temp_folder/clusterSizeInfo.txt"

	# get the leader of each repeat
    if CRISPR_Leader_PROVIDED: # if repeat and leader are given in runtime arguments
		TempRepeatLeaderFile = open("temp_folder/TempRepeatLeaderFile.fasta","r")
		eachLeaderSequence = TempRepeatLeaderFile.readline()
		eachLeaderSequence = TempRepeatLeaderFile.readline()	# read the given leader which is stored in the file "temp_folder/TempRepeatLeaderFile.fasta"
		TempRepeatLeaderFile.close()

    elif not CRISPR_Leader_PROVIDED:	# if a genome or accession number is given in the runtime arguments, proceed with the below
		LeaderInfoFile = open("temp_folder/CRISPR_LeaderInfo.txt","r")	# read this file to check whether there exists a potential leader for a particular CRISPR
		LeaderFile = open("temp_folder/CRISPR_Final_Leader.txt","r")	# read this file to get the leader of each CRISPR

		eachLeaderSequence = LeaderFile.readline() # reading '>' line
		eachLeaderSequence = LeaderFile.readline() # reading leader line

		eachLeader = LeaderInfoFile.readline() # reading header line
		eachLeader = LeaderInfoFile.readline() # reading delimeter =======
		eachLeader = LeaderInfoFile.readline() # reading Leader info

    NumberOfRepeats = 0
    FinalClusterOfEachRepeat = []	# store the final clusters of all the repeats in a list
    

    # iterate over all the consensus repeats and determine its cluster among all the related clusters
    for EachRepeat in ClustersOfEachRepeatArray:

		NumberOfRepeats = NumberOfRepeats + 1
		FinalCluster = "-"
		if CRISPR_Leader_PROVIDED:	# if repeat and leader are given in runtime arguments
			# call this function to determine the cluster
			FinalCluster = calculate_hmm_score(EachRepeat, ClusterAverageSizeDictionary, eachLeaderSequence, Archaea_Bacteria)
			print "\nThe leader belongs to cluster "+FinalCluster+"\n"

		elif not CRISPR_Leader_PROVIDED:	# if a genome or accession number is given in the runtime arguments, proceed with the below

			if "yes" in eachLeader: # if there exists a potential leader then the cluster can be determined
				# call this function to determine the cluster
				FinalCluster = calculate_hmm_score(EachRepeat, ClusterAverageSizeDictionary, eachLeaderSequence, Archaea_Bacteria)
				eachLeaderSequence = LeaderFile.readline()	# since we are given with genome or accession number, there could be more than 1 consensus repeat
				eachLeaderSequence = LeaderFile.readline()	# read the leader of the next repeat

				print "\nCRISPR "+str(NumberOfRepeats)+" belongs to cluster "+FinalCluster+"\n"

			else:
				print "CRISPR "+str(NumberOfRepeats)+" has no leader, hence no related clusters\n"

			print "=========================================================================="


			eachLeader = LeaderInfoFile.readline()	# read the next line in the file "temp_folder/CRISPR_LeaderInfo.txt" to check the status of potential leader for the next repeat

		FinalClusterOfEachRepeat.append(FinalCluster)	# add the determined cluster of the repeat to a list

	# call this function to decide the size of the leader of all the repeats which is defined by their associated cluster
    refine_leader(Archaea_Bacteria, ClusterAverageSizeDictionary, CRISPR_Leader_PROVIDED, FinalClusterOfEachRepeat)
