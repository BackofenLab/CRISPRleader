# CRISPRleader - An efficient tool to determining CRISPR leader boundaries

**CRISPRleader version 1.0.3**

CRISPRleader takes a complete genome or draft genome as input and selects all possible CRISPR arrays in the correct orientation, and annotates the CRISPR leader boundaries. 

**Please run test_bin.py script before executing the main program.**
It will check if executable files can be run and change the path in the mview file to the correct one.

**To execute the program, please open your terminal console.** Make sure "CRISPRleader.py" file and "bin","lib" and "Dataset" folder exists in your current working directory.

**Requirements**
- Python 2.7. Additionally, please install the corresponding libraries(Docopt, Numpy, Urllib3 and Biopython). 
For example: pip install numpy --user OR  sudo pip install numpy

**Dependencies**
The following dependencies should be present in the respective folders for the successful execution of the program:

- [bin folder]
  - CRT1.2-CLI.jar
  - EDeN executable file
  - prodigal executable file
  - hmmsearch executable file
  - mview executable file
  - Mafft folder
  - needleall executable file	(please install EMBOSS 6.3.1 or above). Please note that if 'needleall' does not work, please copy  the 'needleall' executable file from the EMBOSS directory  to the    CRISPRleader/bin folder
  
- [lib folder]
  - Archaea_Final_Repeat_dataset.fa
  - Archaea_LeaderClusters_mean_std.tab
  - Bacteria_Final_Repeat_dataset.fa
  - Bacteria_LeaderClusters_mean_std.tab
  - clustInfos.tab
  - DR_Repeat_model
 
**The program execution can be carried out with three input categories as given below:**

  - Input with Repeat, Leader and the organism type. Execution is proceed as follows:
  
  
     CRISPRleader.py r_l_o  "repeat" "leader" "organism" . 
  
    For Repeat and Leader DNA sequances are expected as input Organism type 'a' for archea and 'b' for bacteria
    
    Example: python CRISPRleader.py r_l_o GAAATCAAAAGATAGTTGAAAC       AAGAATGGCGTTGGGCCTCGGCGTTTTCTCAACCTCCACGTTGCTGTGCTTGCGAAGAATGGCGGCCGCCCACCCCGAAAAGAGACATATATGAATGTAAAACGCGGCAGAAAAGCGTCCACCGAAGA    TACAAAAAACCTACAAAAAACTTAAAAACCCACAAAAACCAACAAAACCAGCCCCA a
    
	
  - Input with Accession number. Run the program by giving the following command:
  
  
    CRISPRleader.py d_f_o "acc_num" "organism"
    
    
	Provides an option to enter desired accession number and the organism type.
	Corresponding fasta file will be downloaded from NCBI
	Organism type 'a' for archea and 'b' for bacteria
	

	Example:
	python CRISPRleader.py d_f_o CP003098 a


## Contribution

Feel free to contribute to this project by writing 
[Issues](https://github.com/BackofenLab/CRISPRleader/issues) 
with feature requests, bug reports, or just contact messages.

## Citation
If you use CRISPRleader, please cite our article
- [CRISPRleader: Characterizing leader sequences of CRISPR loci ](https://doi.org/10.1093/bioinformatics/btw454)
  Omer S. Alkhnbashi, Shiraz A. Shah, Roger A. Garrett, Sita J. Saunders, Fabrizio Costa, Rolf Backofen , 
  Bioinformatics, 32(17), i576-i585, 2016, DOI(10.1093/bioinformatics/btw454).
