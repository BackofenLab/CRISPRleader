#######################################################################################################################################################
#### Functionality : Finding leader of each CRISPR.
#### This function "getLeader()" uses the range (starting and ending positions) of each CRISPR in the Genome and calls the 'getOrientation()' function  
#### to find the strand of the CRISPR. Leader of the CRISPR is decided based on its strand.
#######################################################################################################################################################
import subprocess
import numpy as np
import re
from get_orientation import get_orientation	
def get_leader(All_Consensus,extraLength):
	def cmd_remove1():
		
		str_low_range = ''
		with open('Output/CRISPRs_Repeats_Spacers.out' , 'r') as f:
			for line in f:
				if 'Range:' in line:
					str_low_range += line.split(' ')[5] + '\n'
		return str_low_range

	def cmd_remove2():

		str_high_range = ''
		with open('Output/CRISPRs_Repeats_Spacers.out' , 'r') as f:
			for line in f:
				if 'Range:' in line:
					str_high_range += line.split(' ')[7]
		return str_high_range
		
	def cmd_remove3():
		
		with open('temp_folder/sequence.fasta', 'r') as f:
			list_lines = f.readlines()
			return len(list_lines[1])
			
	def cmd_remove4(start, end):		

		sequence = ''
		with open('temp_folder/sequence.fasta' , 'r') as f:
			list_lines = f.readlines()
		return list_lines[1][start-1:end]
		
	'''
	:param All_Consensus : This list contains the consensus repeat of all the CRISPR sequences in a string format. Leader of each repeat from this list is determined.
												 If the strand is reverse, the repeat in this list is replaced with the reverse complementary of it.
	:param extraLength : This parameter defines length of the leaders of all the repeats.
	'''

	print "Retrieving all the Repeats, their orientation"
	#MaxLenRepeat = max(All_Consensus, key=len) # maximum length of a Repeat in the list
	
	'''
	this part was replaced by cmd_remove1 cmd_remove2
	cmd1 = "grep -oP 'Range: \K(.*)' Output/CRISPRs_Repeats_Spacers.out | awk '{print $1}'"
	cmd2 = "grep -oP 'Range: \K(.*)' Output/CRISPRs_Repeats_Spacers.out | awk '{print $3}'"
	# Leader of the repeat is selected based on the strand of the repeat. To find the strand of the repeat, we need CRISPR low range and high range
	lowRange=subprocess.check_output(cmd1,shell=True) # low range values of all CRISPR are gathered in string format
	highRange=subprocess.check_output(cmd2,shell=True) # high range values of all CRISPR are gathered in string format
	'''
	
	lowRange = cmd_remove1()
	highRange = cmd_remove2()
	
	lowRange= map(int,lowRange.split())	  # convert the low range string seperated with space to list of integers
	highRange= map(int,highRange.split()) # convert the high range string seperated with space to list of integers


	lowRange= np.asarray(lowRange)		  # convert the list to numpy array
	highRange= np.asarray(highRange)	 # convert the list to numpy array

	# The genome can be viewed in a cirlce manner, the end of the genome is appennded with the beginning of the genome and can be visualized as a circle.
	# Leader of the crispr at the endpoitns (beginning and end) can be made complete if the other end of the sequence is appended with leader.
	# Eg: Assume the range of a forward strand crispr is 11-700 and the lenght of the leader to be 600. The leader of the repeat can be taken as 590 nucleotides
	# from the end of the genome and 10 nucleotides from the beginning of the genome. In this case, length of the genome should be known.
	'''
	cmd="awk 'NR==2' temp_folder/sequence.fasta | awk '{ print length($0); }'" ## Finding length of the Genome from the fasta file	
	SequenceLength= int(subprocess.check_output(cmd,shell=True))
	'''
	SequenceLength = cmd_remove3()
	
	# write the crispr information like CRISPR ID, its range, consensus repeat, strand, leader and leader range to a file.
	p = open("temp_folder/CRISPR_Sequences.txt", 'w')

	p.write("CRISPR\tCRISPR_Range\tConsensus\t Strand\tLeader_Range\tLeader\n")
	p.write("---------------------------------------------------------------------------------------------------------------------\n")

	# for each crispr, pick the upstream and downstream sequences with the length of leader size. Once the strand is known, one of them is considered as leader of the repeat.
	for i in range(len(lowRange)):
		
		# if both the upstream and downstream sequences are not crossing the end points,retrieve the crispr sequence along with upstreamm and downsteam sequences
		if (lowRange[i]-extraLength >= 0) and (highRange[i]+extraLength <= SequenceLength):						
			'''
			cmd="awk 'NR==2' temp_folder/sequence.fasta | cut -c"+str(lowRange[i]-extraLength)+"-"+str(highRange[i]+extraLength)
			sequence = subprocess.check_output(cmd,shell=True)		  # retrieve the sequence from the genome
			'''
			
			sequence = cmd_remove4(lowRange[i]-extraLength, highRange[i]+extraLength)			

			LeaderUpstreamStart = lowRange[i]-extraLength # starting position of upstream sequence
			LeaderUpstreamEnd = lowRange[i] - 1							# ending position of upstream sequence

			LeaderDownstreamStart = highRange[i] + 1	 # starting position of downstream sequence
			LeaderDownstreamEnd = highRange[i]+extraLength # ending position of downstream sequence

		#if the upstream sequence of the crispr is crossing the beginning endpoint but not the downstream.
		elif (lowRange[i]-extraLength < 0) and (highRange[i]+extraLength <= SequenceLength):						
			
			'''
			cmd="awk 'NR==2' temp_folder/sequence.fasta | cut -c"+str(1)+"-"+str(highRange[i]+extraLength)
			sequence_start = subprocess.check_output(cmd,shell=True)	 # retrieve the sequence from the beginning until the end of the downstream
			'''
			sequence = cmd_remove4(1, highRange[i]+extraLength)
			FirstChars = extraLength-lowRange[i]	 # find the number of nucleotides to be appended to the above sequence
			LastChars = SequenceLength - FirstChars # get the index in the genome from which the nucleotides to be appended
			
			'''
			cmd="awk 'NR==2' temp_folder/sequence.fasta | cut -c"+str(LastChars)+"-"+str(SequenceLength)
			sequence_end = subprocess.check_output(cmd,shell=True) # retrieve the other part of the upstream sequence from the end of the genome
			'''
			'''
			sequence_end = cmd_remove4(LastChars, SequenceLength)
			sequence = sequence_end + sequence_start	 # append the end of the upstream sequence with the 'sequence_start'
			'''

			LeaderUpstreamStart = 1	  # starting position of upstream sequence
			LeaderUpstreamEnd = lowRange[i] -1 # ending position of upstream sequence

			LeaderDownstreamStart = highRange[i] + 1	 # starting position of downstream sequence
			LeaderDownstreamEnd = highRange[i]+extraLength # ending position of downstream sequence

		#if the downstream sequence of the crispr is crossing the last endpoint of the genome but not the upstream.
		elif (highRange[i]+extraLength > SequenceLength) and (lowRange[i]-extraLength >= 0):						
			'''
			cmd="awk 'NR==2' temp_folder/sequence.fasta | cut -c"+str(lowRange[i]-extraLength)+"-"+str(SequenceLength)
			sequence_start = subprocess.check_output(cmd,shell=True)	 # retrieve the sequence along with the upstream from the end
			'''
			sequence = cmd_remove4(lowRange[i]-extraLength, SequenceLength)
			
			LastChars = SequenceLength - highRange[i] # find the number of nucleotides to be appended from the beginning
			FirstChars = extraLength - LastChars	 # find the index in the genome until which the nucleotides to be selected from the beginning inorder to append at the end to the 'sequence_start'
			'''
			
			cmd="awk 'NR==2' temp_folder/sequence.fasta | cut -c"+str(1)+"-"+str(FirstChars)
			sequence_end = subprocess.check_output(cmd,shell=True) # select the sequence from the beginning
			'''			

			LeaderUpstreamStart = lowRange[i]-extraLength
			LeaderUpstreamEnd = lowRange[i] - 1

			LeaderDownstreamStart = highRange[i] + 1
			LeaderDownstreamEnd = SequenceLength

		UpStream = sequence[:extraLength] ## select the upstream sequence with leader size from the retrieved sequence i.e, first 600 characters
		sequence = sequence[extraLength:]	  ## removing first 600 characters from sequence
		DownStream = sequence[-extraLength-1:]	 ## select the downstream sequence with leader size i.e,last 600 characters
		sequence = sequence[:-extraLength]	 ## removing last 600 characters from sequence

		strand = get_orientation(lowRange[i], highRange[i])	 # obtain the strand of the repeat sequence
		p.write(str(i+1)+"\t"+str(lowRange[i])+"-"+str(highRange[i])+"\t")	 # write the crispr low range and high range to the file

		if strand == 1: # if the repeat is in forward strand, select the upstream of the sequence as leader
			Leader = UpStream
			p.write(All_Consensus[i]+"\t") # write the repeat, its strand, leader position
			p.write("Forward\t"+str(LeaderUpstreamStart)+"-"+str(LeaderUpstreamEnd)+"\t")

		else: # if the repeat is in reverse strand, select the downstream of the sequence as leader
				Repeat	 = All_Consensus[i]	 # select the repeat
				DownStream.replace('U','T')
				Repeat.replace('U','T')

				# perform the reverse complementary of the leader and repeat
				Leader = re.sub('.', lambda m: {'A':'T', 'G':'C','T':'A', 'C':'G'}.get(m.group(), m.group()), DownStream)	 ## complementary sequence
				Repeat = re.sub('.', lambda m: {'A':'T', 'G':'C','T':'A', 'C':'G'}.get(m.group(), m.group()), Repeat)	 ## complementary sequence

				if "\n" in Leader:		 ## if newline deleimeter "\n" in Leader sequence, remove it
						Leader = Leader[:-1]

				Leader = Leader[::-1]	 ## Reverse the Leader sequence
				Repeat = Repeat[::-1]	 ## Reverse the Repeat sequence

				All_Consensus[i] = Repeat # update the reverse complementary of the repeat in the list
				p.write(All_Consensus[i]+"\t") # write the updated repeat to the file
				p.write("Reverse\t"+str(LeaderDownstreamStart)+"-"+str(LeaderDownstreamEnd)+"\t")

		p.write(Leader+"\n")
	p.close()
