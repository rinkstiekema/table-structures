import re 
import random 
from pprint import pprint

class TexGenerator():
    def __init__(self):
        self.doc_start = r"""\documentclass{article}\usepackage{makecell}\usepackage{colortbl}\begin{document}\thispagestyle{empty}\begin{table}"""
        self.doc_end = r"""\end{table}\end{document}"""
        self.colors = r"""\color{white}\arrayrulecolor{red}"""

    def generate_tex(self, table):
        latex = table.df.to_latex(bold_rows=table.bold_stub, column_format=table.column_format, index=table.n_stubs > 0, header=table.n_headers > 0)
        hline = "\\\\ \hline" 
        next_line = "\\\\[\\arrayrulewidth]"  
        row_size = "\\renewcommand{\\arraystretch}{%f}" % table.row_size
        latex_splitted = re.split(r"\\\\", latex)
        latex = ""
        for idx, i in enumerate(latex_splitted):
            if idx in table.h_lines or idx == 0 or idx == len(latex_splitted)-1 or idx == len(latex_splitted)-2:
                if idx == len(latex_splitted)-1:
                    latex = latex + i
                else:
                    latex = latex + i + hline
            else:
                latex = latex + i + next_line
        latex = latex.replace("\\toprule", "\hline")
        latex = latex.replace("\\bottomrule", "")
        latex = latex.replace("\\midrule", "")
        latex = self.make_cells(latex)

        return self.doc_start + row_size + table.font_size + latex + self.doc_end

    def generate_tex_outline(self, table):
        latex = table.df.to_latex(bold_rows=table.bold_stub, column_format=table.column_format, header=table.n_headers > 0, index=table.n_stubs > 0)
        latex = self.replace_unwanted(table, latex)
        latex = self.add_vlines(latex)
        latex = self.make_cells(latex)
        row_size = "\\renewcommand{\\arraystretch}{%f}" % table.row_size
        return self.doc_start + row_size + table.font_size + self.colors + latex + self.doc_end
    
    def replace_unwanted(self, table, latex):
        latex = re.sub(r"\\\\", r"\\\\ \\hline", latex)
        latex = re.sub(r"\\toprule", r"\\hline", latex)
        latex = re.sub(r"\\midrule", r"", latex)
        latex = re.sub(r"\\bottomrule", r"", latex)
        return latex
        
    def add_vlines(self, latex):
        idx = latex.find(r"\begin{tabular}{") + len(r"\begin{tabular}{")
        idx_end = idx + latex[idx:].find(r"}") + 1
        ruling = latex[idx:idx_end-1]
        ruling = ruling.replace("|", "")
        ruling = "|" + "|".join(ruling) + "|}"
        latex = latex[:idx] + ruling + latex[idx_end:]
        return latex

    def make_cells(self, latex):
        latex = latex.replace("makecell\\", r"\makecell")
        latex = latex.replace("\\}", "}")
        latex = latex.replace(r"\textbackslash \textbackslash", "\\\\")
        latex = latex.replace(r"\textbackslash", "")
        return latex