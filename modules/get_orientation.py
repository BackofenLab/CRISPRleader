################################################################################################################################
#### This function decides the Strand of a CRISPR.
#### Here, 'Repeat' of a CRISPR is written to a file and "EDeN" tool has been used on this file, which results a numeric value1.
#### "EDeN" tool is also used on reverese complementary of the sequence 'Repeat' resulting another numeric value2.
#### If (value1-value2)/2 greater than zero, then the 'Repeat' is in Forward Strand.
#### If not, then it is in Reverse Strand.
################################################################################################################################
import subprocess
import os
import re
def get_orientation(lowRange, highRange):
    def cmd_remove1(start, end):        
        #romove this
        #cmd="awk 'NR==2' temp_folder/sequence.fasta | cut -c"+str(lowRange)+"-"+str(highRange) #+" > INPUT_F.SEQUENCE"
        sequence = ''
        with open('temp_folder/sequence.fasta' , 'r') as f:
            list_lines = f.readlines()
            line = list_lines[1][start-1:end]
            line.replace('U', 'T')
        fi = open("temp_folder/INPUT_F.SEQUENCE", 'w')
        fi.write(line)
        fi.close()
        
        fi = open('temp_folder/INPUT_R.SEQUENCE', "w")
        line.replace('A', '1')
        line.replace('C', '2')
        line.replace('G', 'C')
        line.replace('T', 'A')
        line.replace('1', 'T')
        line.replace('2', 'G')
        line = line[::-1]
        fi.write(line)
        f.close
        
    
    '''
    :param lowRange: CRISPR low range
    :param highRange: CRISPT high range. Both these parameters  are used to get the repeat sequence from the genome file to figure out the strand
    : return - 1 if the crispr is in forward strand
             - 0 if the crispr is in reverese strand
    '''
    # select the repeat sequence using the lowRange and highRange parameters
    '''
    cmd="awk 'NR==2' temp_folder/sequence.fasta | cut -c"+str(lowRange)+"-"+str(highRange) #+" > INPUT_F.SEQUENCE"
    Repeat = subprocess.check_output(cmd,shell=True)    # save the obtained repeat in a variable 
    Repeat.replace('U','T') # repalce if there exists a nucleotide 'U' with nucleotide 'T' in the retrieved repeat
    #write the repeat to file "INPUT_F.SEQUENCE" and execute the Eden tool to compute the score in forward strand
    f = open("temp_folder/INPUT_F.SEQUENCE","w")
    f.write(Repeat) 
    f.close()
    '''
    
    cmd_remove1(lowRange, highRange)
    
    
    cmd = "bin/./EDeN -a TEST -i temp_folder/INPUT_F.SEQUENCE -M 1 -r 3 -d 3 -f SEQUENCE -g DIRECTED -m lib/DR_Repeat_model -y temp_folder/For >/dev/null"
    os.popen(cmd) # execute the eden tool on the file "INPUT_F.SEQUENCE" and save the output file in "For" folder

    
    '''
    # write reverse complementary of the repeat to file "INPUT_R.SEQUENCE"
    cmd = "tr ATGC TACG < temp_folder/INPUT_F.SEQUENCE | rev > temp_folder/INPUT_R.SEQUENCE"
    os.popen(cmd)
    '''
    # compute the Eden score on the reverse complementary repeat and store in "Rev" folder
    cmd = "bin/./EDeN -a TEST -i temp_folder/INPUT_R.SEQUENCE -M 1 -r 3 -d 3 -f SEQUENCE -g DIRECTED -m lib/DR_Repeat_model -y temp_folder/Rev >/dev/null"
    os.popen(cmd)
    
    
    cmd = "chmod 777 -R temp_folder/" # give the access permissions to the folder "For" and the file "prediction" inside the folder
    os.popen(cmd)
    
    
    f= open("temp_folder/For/prediction","r") 
    val_in_plus = float((f.readline().split())[1])  # read the score of forward strand from "prediction" file from "For" folder
    f.close()
    
    f= open("temp_folder/Rev/prediction","r")
    val_in_minus = float((f.readline().split())[1]) # read the score of reverse strand from "prediction" file from "Rev" folder
    f.close()
    
    #print val_in_plus, val_in_minus
    val_in_minus = val_in_minus  * -1   # the score from reverse strand is multiplied with -1, as the score obtained after performing reverse complementary
    #print val_in_plus, val_in_minus
    
    # if the sum of the scores from forward and reverse strand is greater than zero, then the repeat is in forward strand or else it is in reverse strand
    val = (val_in_plus + val_in_minus)/2 
    #print val
    if val > 0:
        #print "Repeat sequence in forward strand\n"
        return 1
    else:
        #print "Repeat sequence in reverse strand\n"
        return 0
