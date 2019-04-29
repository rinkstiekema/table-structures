import sys
import os
from random import randint, getrandbits, choice, sample
import string 

class TableGenerator():
    def __init__(self):
        self.doc_start = r"""\documentclass{article}\usepackage{colortbl}\begin{document}\thispagestyle{empty}\begin{table}"""
        self.doc_end = r"""\end{table}\end{document}"""
        self.min_col = 2
        self.max_col = 8
        self.min_row = 2
        self.max_row = 15
        self.min_characters = 1
        self.max_characters = 10
        self.max_characters_caption = 30
        self.min_digits = 1
        self.max_digits = 5

    def generate(self):
        def get_tabular(n_col, n_vlines):
            start = r"""\begin{tabular}{"""
            end = r"""\end{tabular}"""
            positions = ""
            for i in range(n_col):
                positions += choice(["l", "r", "S", "c"])
            for i in range(n_vlines):
                placed = False
                while not placed:
                    location = randint(0, len(positions))
                    if location == len(positions):
                        if not positions[location-1] == "|":
                            positions += "|"
                            placed = True
                    elif not(positions[location] == "|" or (positions[location-1] == "|" and not location-1 == -1)):
                        positions = positions[:location] + "|" + positions[location:]
                        placed = True

            positions += "}"
            return start+positions, end

        def get_header(n_col):
            textbf = r"""\textbf{}"""
            if choice([True, False, False, False]):
                textbf = ""
            header = ""
            for _ in range(n_col):
                word = textbf
                n_letters = randint(self.min_characters, self.max_characters)
                for _ in range(n_letters):
                    word = word[:-1] + choice(string.ascii_letters + string.digits) + word[-1:]
                header += word + " & "
            header = header[:-2]

            header += "\\\\ "
            if choice([True, True, True, False]):
                header += " \\hline "
            if choice([True, False]):
                header = " \\hline " + header

            header += "\n "
            return header

        def get_body(n_row, n_col, n_hlines):
            use_bold = False
            if choice([True, False, False]):
                use_bold = True

            body = ""
            for _ in range(n_row):
                for _ in range(n_col):
                    word = ""
                    n_letters = randint(self.min_characters, self.max_characters)
                    for _ in range(n_letters):
                        word = word[:-1] + choice(string.ascii_letters + string.digits) + word[-1:]
                    
                    if use_bold:
                        if choice([True, False, False, False, False, False, False, False, False, False]):
                            word = r"""\textbf{""" + word + r"""}"""

                    body += word + " & "
                body = body[:-2]
                body += r"""\\"""

            locations = sample(range(1, n_row+2), n_hlines)
            locations.sort(reverse = True)

            body = body.split(r"""\\""")
            h_line = "\\\\ \hline \n "
            d_hline = "\\\\ \hline \hline \n "
            end_line = "\\\\ \n "

            for idx, _ in reversed(list(enumerate(body))):
                if idx in locations:
                    if choice([True, True, True, True, True, True, True, True, False]):
                        body.insert(idx, h_line)
                    else:
                        body.insert(idx, d_hline)
                elif not idx == 0:
                    body.insert(idx, end_line)

            body = "".join(body)
            return body

        n_col = randint(self.min_col, self.max_col)
        n_row = randint(self.min_row, self.max_row)
        n_hlines = randint(0, n_row+1)
        n_vlines = randint(0, n_col+1)

        tabular_start, tabular_end = get_tabular(n_col, n_vlines)
        header = get_header(n_col)
        body = get_body(n_row, n_col, n_hlines)

        table = self.doc_start + tabular_start + header + body + tabular_end + self.doc_end
         
        return table

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Missing argument: amount location")

    n = int(sys.argv[1])
    location = sys.argv[2]
    generator = TableGenerator()
    
    for i in range(n):
        try:
            table = generator.generate()
            with open(os.path.join(location, str(i)+".tex"), "w") as outfile:
                outfile.write(table)
        except Exception as e:
            print(e)
            continue
