import os

list_exec_files = ['EDeN',
					'hmmsearch',					
					'needleall',
					'prodigal']					
					
for file_name in list_exec_files:
	cmd = 'bin/' + file_name + ' -h'
	os.system(cmd)
	print('===============')
	
crt_cmd = 'java -cp bin/CRT1.2-CLI.jar -h'
os.system(crt_cmd)
	
dir_path = os.path.dirname(os.path.realpath(__file__))
mview_path = dir_path +'/bin/mview'

with open(mview_path, 'r') as f:
	mwiew_lines = f.readlines()
	
new_line = 'use lib \'' + dir_path +'/bin/mview-1.60.1/lib' + '\';\n'

f = open(mview_path, 'w')
for line in mwiew_lines:
	if ('use lib' in line) and (line[0] != '#'):		
		f.write(new_line)		
	else:
		f.write(line)
f.close()

