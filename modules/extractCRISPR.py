####################################################################################################################################################
#### Functionality : Executing CRT (CRISPR Recognition Tool) and calling other functions to proceed further execution.
#### This function "extractCRISPR()" gets the Accession number of a Genome. It converts multiline fasta file to a singleline fasta file and pass it to CRT tool.
#### The CRT generates a file contatining the information of all CRISPRs in the Genome. This information is then forwaded to other functions.
####################################################################################################################################################

import os
import shutil
import subprocess
from acc_from_header import acc_from_header

def extractCRISPR(Fastafile,Complete_partial_flag,Archaea_Bacteria):
    def cmd_remove1():
        with open(Fastafile) as f:
            list_lines = f.readlines()
        header = list_lines[0]
        longstr = ''
        for line in range(1, len(list_lines)):
            longstr += (list_lines[line].rstrip())
            
        f = open('temp_folder/sequence.fasta', 'w')
        f.write(header)
        f.write(longstr)
        f.close()
            
        
                
    # Read the given fasta file and note the Accession number of the genome.
    f= open(Fastafile,'r')
    header=f.readline() # read the first line which contains the accession  number
    
    SequenceID = acc_from_header(header)    
    f.close()
    
    # The fasta file contains the header in the first line following the genome in next lines. The genome is arranged in multiple lines.
    # Inorder to find the leader of each crispr, a single line genome would be more convenient.
    '''
    cmd = "sed '1d' "+ Fastafile+" > temp_folder/tmpfile.fa"    # remove the header from the fasta file and copy the multiline genome into a temporary file
    os.popen(cmd)
    
    
    cmd = "echo $(cat temp_folder/tmpfile.fa) |sed -r 's/\s+//g' > temp_folder/sequence.fasta"  # convert multiline genome to single line genome in a different file under temporary directory
    os.popen(cmd)
    os.remove("temp_folder/tmpfile.fa") # remove the temporary file 'tmpfile.fa' which would not be used in the future
        
    cmd = "sed -i '1i\''>"+header+"' temp_folder/sequence.fasta"    # Add the header at the beginning to the single line genome file
    os.popen(cmd)
    
    cmd_remove1 is used instead    
    '''
    cmd_remove1()
    
    # To store all the output files, a directory with name 'Output' is created. If there already exists a 'Output' folder, remove it and create a new one.
    if os.path.exists("Output"):
        shutil.rmtree("Output") # remove the 'Output' folder if it already exists
        
    os.mkdir("Output")  # create the 'Output' folder
    cmd = "chmod 777 Output"    # provide all access permissions to it
    os.popen(cmd)
    
    
    # execute the CRT tool on the multiline fastafile to obtain information about all the possible CRISPRs in the genome. Save the output in the 'Output' folder
    print "\nExecuting CRT tool.."
    subprocess.call(['java', '-cp', 'bin/CRT1.2-CLI.jar', 'crt', '-minRL', '18', '-maxRL', '47', '-minSL', '17', '-maxSL', '72', Fastafile,'Output/CRISPRs_Repeats_Spacers.out'])
    print "Generated Output file.\nReading the Output file.\n"
    
    # read the CRT output file to check the existence of crispr in the genome
    fp=open("Output/CRISPRs_Repeats_Spacers.out")
    # The information about the crispr can be seen in th 6th line of the file. 
    for countHeader, eachLine in enumerate(fp):
        if countHeader == 6:    # ignore the first 5 lines
            break
    fp.close()
    
    # if the 6th line in the output file does not have the statement "No CRISPR elements were found.", then proceed with furhter execution, or else exit the program
    if eachLine!="No CRISPR elements were found.":
        
        # Write the summary of the all the crispr information into a new file
        # write the information like CRISPR ID, its consensus repeat, total repeats and spacers of each cripsr, average length of the both repeats and spacers.
      
        result=open("Output/CRISPR_Summary.txt","w") # Writing header of the file. The contents of the file is edited in 'FindConsensus()' function
        result.write("Sequence_ID"+"\t"+"CRISPR_ID"+"\t"+ "Consensus" +"\t"+"No.of Repeaters"+"\t"+"Avg_length_Repeaters"+"\t"+"No.of Spacers"+"\t"+"Avg_length_Spacers"+"\n")
        result.close()        
        # call this function to find the consensus repeat of each crispr        
        return SequenceID
        
    else:   # exit the program if no crispr elements were found in the genome
        print "No CRISPR elements were found.\nThe Output from CRT tool is saved in the directory Results_"+SequenceID
        print "\nExiting the program..\n"
        return -1
