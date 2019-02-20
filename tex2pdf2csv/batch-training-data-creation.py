import os 
import multiprocessing as mp
import sys
import json
import subprocess
import itertools
from tex2png import tex2png

if __name__ == '__main__':
	if len(sys.argv) < 3:
	    print("Missing arguments. Usage: <input-folder> <output-folder>")
	    exit(-1)

	input_folder = sys.argv[1]
	output_folder = sys.argv[2]

	aux_folder = os.path.join(output_folder, 'aux-bs')
	if not os.path.exists(aux_folder):
		os.makedirs(aux_folder)

	input_folder_list = os.listdir(input_folder)
	for input_file in input_folder_list:
		tex2png(input_folder+input_file, output_folder)

	# processes = [mp.Process(target=tex2png, args=(input_folder + input_file, output_folder)) for input_file in input_folder_list]

	# # Run processes
	# for p in processes:
	#     p.start()

	# # Exit the completed processes
	# for p in processes:
	#     p.join()
