#Function to deal with different header types

def acc_from_header(header):
	if '|' in header:
		accession  = (header.split('|')[3]).split(".")[0]
		return accession
	else:
		accession  = (header.split(' ')[0]).split(".")[0][1::]
		return accession
