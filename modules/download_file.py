#Function to download the corresponding file from the NCBI database

from Bio import Entrez
def download_file(file_name):
	print "Downloading the genome in fasta format (DNA)... File ..."
	# ref.: http://wilke.openwetware.org/Parsing_Genbank_files_with_Biopython.html

	Entrez.email = 'whatever@mail.com'

	# accession id works, returns genome in fasta format, looks in the 'nucleotide' database:
	try:
		print file_name		
		handle=Entrez.efetch(db='nucleotide',id=file_name,rettype='fasta')  # The genome with the accession number is fetched from ncbi server and saved in 'handle' variable
		error = 0
	except:
		print "Error received in retrieving the fasta file with the given Accession Number.\nPlease check the Accession Number, or\nPlease check your internet connection or The 'NCBI' web server is down.\n"
		error = 1
		
	# store locally:
	

	if error == 0:				  # calling the function 'downloadFasta' to download the fasta file from ncbi website
		local_file=open('temp_folder/'+file_name+'.fasta', 'w') 
		local_file.write(handle.read()) # write the genome to a file
		handle.close()
		local_file.close()
		print "Downloaded."
	else:
		print "Exiting the program..."
		return -1
	File = "temp_folder/"+file_name+".fasta"		# stroing the downloaded file in temporary directory

	openDownloadFile = open(File,"r")
	if "complete" in openDownloadFile.readline():		# check if the downloaded genome is complete or partial
		Complete_partial_flag = "COMPLETE"
	else:
		Complete_partial_flag = "PARTIAL"
		
	openDownloadFile.close()
	return Complete_partial_flag
