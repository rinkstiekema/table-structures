import sys
import os
import json
import subprocess


def substring_indexes(substring, string):
    last_found = -1  # Begin at -1 so the next position to search from is 0
    result = []
    while True:
        # Find next index of substring, by starting after its last known position
        last_found = string.find(substring, last_found + 1)
        if last_found == -1:
            break  # All occurrences have been found
        result.append(last_found)
    return result


def strip_comments(input):
    table_list = input.split("\n")
    result = ""
    for line in table_list:
        idx = line.find("%")
        if idx == 0 or (idx > 0 and line[idx-1] != "\\"):
            continue
        result += line + '\n'
    return result


def get_tables(input):
    input = strip_comments(input)
    lengths = [len(r"\begin{table}"), len(r"\begin{table*}")]
    starts = [r"\begin{table}", r"\begin{table*}"]
    ends = [r"\end{table}", r"\end{table*}"]

    result = []
    for start_idx, start in enumerate(starts):
        start_occurrences = []
        for match in substring_indexes(start, input):
            start_occurrences.append(match)

        end_occurrences = []
        for match in substring_indexes(ends[start_idx], input):
            end_occurrences.append(match)

        for idx, occurrence in enumerate(start_occurrences):
            result.append(input[occurrence + lengths[start_idx]: end_occurrences[idx]])
    return result


def get_tabular(table):
    length = len(r"\begin{tabular}")
    start = table.find(r"\begin{tabular}")
    end = table.find(r"\end{tabular}")
    return table[start + length:end]


def get_no_columns(tabular):
    tabular = tabular.replace("@{}", "")
    spec = tabular.split("{")[1].split("}")[0]
    return spec.count("r") + spec.count("c") + spec.count("l")


def get_no_rows(tabular):
    return tabular.count(r"\\")


def get_caption(table):
    length = len(r'\caption{')
    start = table.find(r'\caption{')
    result = table[start+length:]

    # Every time a tag is opened, we need to skip the next '{' to get the right closing '}'.
    openings = substring_indexes("{", result)
    endings = substring_indexes("}", result)
    end = 0
    for opening in openings:
        if opening < endings[end]:
            end += 1
        else:
            break

    return result[:endings[end]]


if len(sys.argv) < 3:
    print("Missing arguments. Usage: <input-file> <output-folder>")
    exit(-1)

input_file = sys.argv[1]
output_folder = sys.argv[2]

json = []


ext = input_file.split(".")[-1]
if ext != "tex":
    print("Not a .text file")
    exit(-1)

output = []
with open(input_file) as f:
    data = f.read()
    tables = get_tables(data)

    for table in tables:
        caption = get_caption(table)
        tabular = get_tabular(table)
        noCols = get_no_columns(tabular)
        noRows = get_no_rows(tabular)

        output.append({
            "file": input_file,
            "table": table,
            "caption": caption,
            "shape": (noCols, noRows)
        })

doc_start = r"""\documentclass{article}
\begin{document}
\begin{table}"""

doc_end = r"""
\end{table}
\end{document}"""

for idx, table in enumerate(output):
    doc = doc_start + table["table"] + doc_end
    outfile_path = output_folder + '/' + str(idx) +'-result.pdf'
    with open(outfile_path, 'x') as outfile:
        outfile.write(doc)
        subprocess.call('pdflatex '+ outfile_path)