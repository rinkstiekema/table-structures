import os 
import multiprocessing as mp
import sys
import json
import subprocess
import itertools
import shutil
from tex2png import tex2png
from combine import combine

if __name__ == '__main__':
	if len(sys.argv) < 3:
	    print("Missing arguments. Usage: <input-folder> <output-folder>")
	    exit(-1)

	input_folder = sys.argv[1]
	output_folder = sys.argv[2]

	aux_folder = os.path.join(output_folder, 'aux-bs')
	#if not os.path.exists(aux_folder):
	#	os.makedirs(aux_folder)

	#input_folder_list = os.listdir(input_folder)
	#count = 0
	#for input_file in input_folder_list:
	#	tex2png(input_folder+input_file, output_folder)
	#	count += 1
	#	if count % 100 == 0:
	#		print(count, " out of ", len(input_folder_list))
	# # processes = [mp.Process(target=tex2png, args=(input_folder + input_file, output_folder)) for input_file in input_folder_list]

	# # # Run processes
	# # for p in processes:
	# #     p.start()

	# # # Exit the completed processes
	# # for p in processes:
	# #     p.join()
	#shutil.rmtree(aux_folder) 
	combine(output_folder)

