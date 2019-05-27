import re 
import random 

class TexGenerator():
    def __init__(self):
        self.doc_start = r"""\documentclass{article}\usepackage{booktabs}\usepackage{colortbl}\begin{document}\thispagestyle{empty}\begin{table}"""
        self.doc_end = r"""\end{table}\end{document}"""
        self.lengths = r"""\setlength{\aboverulesep}{0pt}\setlength{\belowrulesep}{0pt}"""            
        self.lengths_outlines = r"""\setlength{\aboverulesep}{0.1pt}\setlength{\belowrulesep}{0.1pt}\setlength{\heavyrulewidth}{0.4pt}\setlength{\lightrulewidth}{0.4pt}"""
        self.colors = r"""\color{white}\arrayrulecolor{red}"""
        
    def generate_tex(self, table):
        latex = table.df.to_latex(bold_rows=table.bold_stub, column_format=table.column_format, header=table.n_headers > 0, index=table.n_stubs > 0)
        occurences = [m.start() for m in re.finditer(r"\\\\", latex)]
        for idx, i in enumerate(sorted(occurences, reverse=True)):
            color = "black" if idx in table.h_lines else "white"
            latex = latex[:i] + r"\\ \arrayrulecolor{"+ color +r"}\cline{1-"+str(table.n_columns + table.n_stubs)+r"}\arrayrulecolor{black} " + latex[i+len(r"\\\\")-1:]
        return self.doc_start + self.lengths + table.font_size + latex + self.doc_end

    def generate_tex_outline(self, table):
        latex = table.df.to_latex(column_format=table.column_format, header=table.n_headers > 0, index=table.n_stubs > 0)
        latex = self.replace_unwanted(table, latex)
        latex = self.add_hlines(latex)
        return self.doc_start + table.font_size + self.lengths_outlines + self.colors + latex + self.doc_end
    
    def replace_unwanted(self, table, latex):
        latex = re.sub(r"\\\\", r"\\\\ \\cline{1-"+str(table.n_columns + table.n_stubs)+"}", latex)
        latex = re.sub(r"\\arrayrulecolor{white} \\midrule \\arrayrulecolor{black} \\midrule", r"\n\\midrule", latex)
        latex = re.sub(r"\\midrule \n\\bottomrule", r"\n\\bottomrule", latex)
        return latex
        

    def add_hlines(self, latex):
        idx = latex.find(r"\begin{tabular}{") + len(r"\begin{tabular}{")
        idx_end = idx + latex[idx:].find(r"}") + 1
        ruling = latex[idx:idx_end-1]
        ruling = ruling.replace("|", "")
        ruling = "|" + "|".join(ruling) + "|}"
        latex = latex[:idx] + ruling + latex[idx_end:]
        return latex
