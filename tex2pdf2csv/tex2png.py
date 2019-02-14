import sys
import os
import json
import subprocess
import itertools

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

def insert_v_lines(tabular):
    original_spec = tabular.split("{")[1].split("}")[0]
    spec = original_spec

    for idx, i in enumerate(spec):
        spec = spec[:idx*2] + '|' + spec[idx*2:]
    spec = spec + "|"

    spec = ''.join(ch for ch, _ in itertools.groupby(spec))

    tabular = tabular.replace(original_spec, spec, 1)
    return tabular

def insert_h_lines(tabular):
    tabular = tabular.replace(r"\hline", "")
    lines = tabular.split(r'\\')
    tabular = r'\\ \hline'.join(lines)

    heading_idx = tabular[tabular.find("{"):].find("}") + 1
    tabular = tabular[:heading_idx] + r"\hline" + tabular[heading_idx:]
    return tabular

def insert_color(doc, color):
    length = len(r'\begin{tabular}')
    col_structure_start = doc.find(r'\begin{tabular}') + length
    col_structure_end = col_structure_start + doc[col_structure_start:].find("}") + 1
    result = doc[:col_structure_end] + r"\arrayrulecolor{"+color+"}" + doc[col_structure_end:]
    return result

def cleanup(dir_name):
    dir_list = os.listdir(dir_name)

    for item in dir_list:
        if not item.endswith(".png"):
            os.remove(os.path.join(dir_name, item))

def tex2png(input_file, output_folder):
    json = []
    ext = os.path.splitext(input_file)[1]
    if ext != ".tex":
        exit(-1)

    output = []

    try:
        with open(input_file) as f:
            data = f.read()
            tables = get_tables(data)
            print(str(len(tables)) + " tables found")

            for table in tables:
                caption = get_caption(table)
                tabular = get_tabular(table)
                tabular = insert_v_lines(tabular)
                tabular = insert_h_lines(tabular)
                noCols = get_no_columns(tabular)
                noRows = get_no_rows(tabular)

                table = r" \begin{tabular}" + tabular + r" \end{tabular}"

                output.append({
                    "file": f.name,
                    "table": table,
                    "caption": caption,
                    "shape": (noCols, noRows)
                })

        doc_start = r"""\documentclass{article}
        \usepackage{colortbl}
        \begin{document}
        \thispagestyle{empty}
        \begin{table}"""

        doc_end = r"""
        \end{table}
        \end{document}"""

        for idx, table in enumerate(output):
            doc = doc_start + table["table"] + doc_end

            doc_color = insert_color(doc, "red")
            doc_white = insert_color(doc, "white")

            file_name = os.path.splitext(input_file)[0].split("/")[-1]

            outpath_borders = output_folder + file_name + '-' + str(idx) + '-borders'
            outpath_noborders = output_folder + file_name + '-' + str(idx) + '-noborders'

            with open(outpath_borders+'.tex', 'w+') as outfile:
               outfile.write(doc_color)

            with open(outpath_noborders+'.tex', 'w+') as outfile:
                outfile.write(doc_white)

            subprocess.call('latex -aux-directory /aux-bs -quiet -interaction batchmode -output-directory '+ output_folder + ' ' + outpath_borders + '.tex', stdout=open(os.devnull, 'wb'))
            subprocess.call('dvipng -q* -T tight -o ' + outpath_borders + '.png ' + outpath_borders + '.dvi', stdout=open(os.devnull, 'wb'))
            subprocess.call('latex -aux-directory /aux-bs -quiet -interaction batchmode -output-directory '+ output_folder + ' ' + outpath_noborders + '.tex', stdout=open(os.devnull, 'wb'))
            subprocess.call('dvipng -q* -T tight -o ' + outpath_noborders + '.png ' + outpath_noborders + '.dvi',stdout=open(os.devnull, 'wb'))

            #subprocess.call('pdflatex -interaction nonstopmode -output-directory '+ output_folder + ' ' + outfile_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e: print(e)

    cleanup(output_folder)