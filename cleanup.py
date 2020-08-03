
# cleanup file

import numpy as np

def main():

	with open('citations_med.txt', 'r') as file:
		with open('med.txt','w') as outfile:
		    for line in file:
		    	if ('#%' in line):
		    		if (int(line[len('#%'):].strip('\n')) > 600000):
		    			continue
		    	if ('#!' in line or '#*' in line or '#@' in line or '#t' in line or '#c' in line):
		    		continue
		    	else:
		    		outfile.write(line)
				# read through each line of the file one by one, delete huge numbers

main()









