##################################################################################################################################################
#### Functionality : Finding Consensus of each CRISPR.
#### This function "FindConsensus()" reads the file generated from the CRT tool. It retrieves the necessary information from this file include number of CRISPRs, 
#### number of repeats in each CRISPR, average length of repeat and spacer in each CRISPR. It also writes all the repeats in a seperate text document.
#### Using the retrieved information, this function figure out the consensus repeat of each CRISPR.
##################################################################################################################################################
import subprocess
import os
from get_leader import get_leader
def find_consensus(SequenceID):
    def cmd_remove1():
        crispr = ''
        repeats = ''
        repeat_spacer_length = ''
        
        with open('Output/CRISPRs_Repeats_Spacers.out', 'r') as f:
            for line in f:
                if 'CRISPR' in line:
                    crispr += line.split(' ')[1] + "\n"
                if 'Repeats:' in line:
                    repeats += line.split(' ')[1].split("\t")[0] + "\n"
                    repeat_spacer_length += line.split(' ')[3].split("\t")[0] + '\n' + line.split(' ')[5]
                    
        return crispr, repeats, repeat_spacer_length
            
        
    '''
    :param SequenceID : This parameter contains the accession number. This information is needed to edit the crispr summary file.
    '''
    
    result=open("Output/CRISPR_Summary.txt","a") # open the previously created summary file to write the contents in it
    
    '''
    cmd_remove1 is used to replace this
    cmd = "grep -Po '(?<=CRISPR)\W*\K[^ ]*' Output/CRISPRs_Repeats_Spacers.out"
    crispr=subprocess.check_output(cmd,shell=True)  # find the number of crispr in the genome by reading the CRT output file
    
    cmd = "grep -Po '(?<=Repeats:\s)[^\s]*' Output/CRISPRs_Repeats_Spacers.out"
    Repeats=subprocess.check_output(cmd,shell=True) # find the number of repeats in each crispr from the CRT output file
    
    cmd = "grep -Po '(?<=Average Length:\s)[^\s]*' Output/CRISPRs_Repeats_Spacers.out"
    RepeatSpacerLength=subprocess.check_output(cmd,shell=True)  # find the average length of repeats and spacers in each crispr from CRT ouput file
    '''
    
    crispr, Repeats, RepeatSpacerLength = cmd_remove1()    
    
    # To find the consensus of each crispr, read the CRT output file and store the repeats of all the CRISPRs in a file seperated with a delimeter.
    f = open("Output/CRISPRs_Repeats_Spacers.out")  # read CRT output file
    out=open('temp_folder/sample.txt','w')  # create new file to store the repeats of all the CRISPRs
    isWrite=0   # This variable acts like a flag. If it is enabled, we will write the repeats into new file
    k=0         # Since all the repeats are stored in a single string 'Repeats', this variable is used to parse through each repeat in the string
    ThreeRepeats=[] # If there are only three repeats for a crispr, store in this list and then write to the file. This additional setting is added 
                    # because if there are only 3 repeats then the chances of having a crispr are low. In this case, we are not considering this special case.
                    # Even though we are not taking this special case, this list is used here as we may add this constraint in future.
    
    # read each line in the CRT output file. Each crispr inforamtion in the output file is written like a block seperated with a delimeter.
    #  Use the deleimeter as a reference point and start recording the repeats. 
    for line in f:  
        words = line.split()
        if words[:1]==['--------']: # if a deliemter is encounterd while readng the file, start recording the repeats
            if isWrite==0:  # if recording is stopped, start recording the repeats
                isWrite=1
                if int(Repeats.split('\n',k+1)[k])==3:  # check the number of repeats for the crispr. If it is three, store them in a list
                    isWrite=2
                    k=k+1
                    out.write(words[1]+"\n")    # write the delimeter to the new file to seperate the repeats of each crispr
                    continue
            else:               # if the recording is in process and a delimeter is encountered during this process, this means that the repeats of one 
                isWrite=0       # crispr have recorded. Stop the recording now and wait for the other delimeter to start recording repeats of another crispr.
                out.write(words[1]+"\n")    # write the delimeter that indicated the end of the repeats for a crispr in the new file.
        
        if isWrite==1:  # if recording was started, write the repeat to the file.
            out.write(words[1]+"\n")
                
        elif isWrite==2:    # if recording was started and there are only three repeats for the crispr. 
            ThreeRepeats.append(words[1]) # add them in a list.
            if len(ThreeRepeats)==3:      # if all the three repeats are stored in the list, write them into the file. Please note that this setup is not 
                out.write(ThreeRepeats[0]+"\n"+ThreeRepeats[1]+"\n"+ThreeRepeats[2]+"\n") # different than the usual recording. It's just used to add constraint
                ThreeRepeats=[]                                                           # on three repeats in the future.
                
    out.write("-------------------")    # After recording all the crispr repeats, end the file with a delimeter
    out.close()
    f.close()
    # The file with all the repeats was prepared. Use this information and find the consensus repeat of each crispr.
    # Use the delimeter to select the repeats of one crispr.
    cmd = ["""/bin/grep -n - temp_folder/sample.txt | cut -d : -f1 | tr "\n" " " """]
    delimeter=subprocess.check_output(cmd,shell=True)   # retrieve the line numbers of the delimeters and stored as a string.
    delimeter = delimeter.split()                       # convert the string to list of strings
    delimeter = map(int, delimeter)                     # convert the list of strings to list of integers
        
    f = open('temp_folder/sample.txt')  # read the file containing all the repeats.
    in_file = "temp_folder/sample.fa"   
    lineNumber=i=j=k=0
    mafft = False
    iteration = 0
    p = open(in_file, 'w')              # open another file to store repeats of only one crispr.
    All_Consensus = []  # all consensus repeats are stored in this list
    
    # read the repeats of all the crispr
    for line in f:
        lineNumber += 1     # note the line number. If a line number matches with the line number that having a delimeter, start writing the repeats of a crispr into new file
        if lineNumber == delimeter[0]:

            if p.closed:                # if the file descriptor of the new file which store repeats of only one crispr is closed, open it again.
                p = open(in_file, 'w')  # This will erase all the previous contents and write the repeats of another crispr
            iteration += 1              # This flag is used further to represent that a delimeter has encountered at the current line
            
            del delimeter[0]   # remove the delimeter line number from the list, since we are interested to read only the first element in this list
        
        else:   # if the current line does not have any delimeter, start writing the repeats to the file
            mafft = True                # This boolean flag is used further to represet that all the repeats of a crispr have read.
            p.write(">R"+str(i)+"\n")   # write the file in a fasta format
            p.write(line)
            i += 1
            iteration = 0               # delimeter has not encountered at the current line
        
        if iteration==1 and mafft == True:  # if all the repeats of a crispr is completely read, then proceed with the below
            p.close()                       # stop writing the contents to new file
            
            # The most dominant repeat or the repeat which occurs for higher number of times is termed as consensus repeat of a crispr.
            # store all the repeats in a dictionary as 'key' and note their number of occurences as a 'value' of the 'key'
            DominantRepeat = {}     # dictionary to store the repeats
            CRISPR_Repeat = open("temp_folder/sample.fa","r")   # open the file which conatins repeats of a crispr
            eachRepeat = CRISPR_Repeat.readline()   # read the fasta format header, eg: >R1
            eachRepeat = CRISPR_Repeat.readline()   # read the first repeat
            
            while not eachRepeat in ("\n", ""):     # read the repeats until the end of the file
                    DominantRepeat[eachRepeat] = DominantRepeat.get(eachRepeat, 0) + 1  #  increment the number of occurence value of the recently read repeat
                    eachRepeat = CRISPR_Repeat.readline()   # read the fasta format header, eg: >R2
                    eachRepeat = CRISPR_Repeat.readline()   # read the repeat
            
            # obtain the repeat that has occured higher number of times. This is the consensus repeat
            consensus = max(DominantRepeat, key = DominantRepeat.get)
            
            if "\n" in consensus:   # if a newline delimeter '\n' in the stirng 'consensus', remove it.
                consensus = consensus [:-1]

            All_Consensus.append(str(consensus))    # add the consensus repeat to the list
            Spacers= int(Repeats.split('\n',k+1)[k])-1 # get the number of spacers in the crispr
            # write accession number, crispr ID, cosensus repeat and number of repeats in the crispr
            result.write(str(SequenceID)+"\t"+str(crispr.split('\n',k+1)[k])+"\t"+str(consensus)+"\t"+str(Repeats.split('\n',k+1)[k])+"\t")
            # along with the above statements, write average length of the repeat, number of spacers and average length of the spacers to the summary file
            result.write(str(RepeatSpacerLength.split('\n',j+1)[j])+"\t"+str(Spacers)+"\t"+str(RepeatSpacerLength.split('\n',j+2)[j+1])+"\n")
            k=k+1
            j=j+2
            
    result.close()
    os.chmod("Output/CRISPR_Summary.txt",0777)  # provide all access permissions to the file
    get_leader(All_Consensus,600)                # obtain orientation/strand of all the consenus repeats and their leaders with length 600 nucleotides
    
    # The consensus repeats with reverse strand would have modified after executing the above function 'getLeader()'.
    # The repeats with reverse strand are replaced with reverse complementary of the repeat in the 'All_Consensus' list.
    # Now, update these changes in the summary file. Create a new summary file and edit these changes.
    CRISPR_Summary_Edit = open("Output/Summary.txt","w")
    count = -1
    with open("Output/CRISPR_Summary.txt","r") as CRISPR_Summary:   # open the old summary file
        for eachLine in CRISPR_Summary: # read each line of the old summary file
            
            if count == -1 :    # if it is the first line, write the header
                CRISPR_Summary_Edit.write(eachLine) 
                count = 0
            else:               # write the same contents and edit the consensus repeat field.
                eachLine = eachLine.split()
                CRISPR_Summary_Edit.write(eachLine[0]+"\t"+eachLine[1]+"\t"+All_Consensus[count]+"\t"+eachLine[3]+"\t"+eachLine[4]+"\t"+eachLine[5]+"\t"+eachLine[6]+"\n")
                count = count + 1
    CRISPR_Summary_Edit .close()
    os.chmod("Output/Summary.txt",0777)     # provide all access permissions to the file
    os.remove("Output/CRISPR_Summary.txt")  # remove the old summary file
