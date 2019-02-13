import subprocess
import os 
import multiprocessing

# tex_files = os.listdir("tex")

# for file in tex_files:
# 	job = os.system('pdflatex -interaction nonstopmode -output-directory pdf tex/' + file)
# 	t1 = multiprocessing.Process(target=job)

for item in os.listdir("pdf"):
    if not item.endswith(".pdf"):
        os.remove(os.path.join("pdf", item))