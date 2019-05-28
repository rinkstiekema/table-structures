import random
from pprint import pprint
import numpy as np
import pandas as pd
from nltk.corpus import words

class Table():
    def __init__(self, table_type, n_rows, n_columns, n_text_column):
        self.n_headers = table_type["n_headers"]
        self.n_stubs = table_type["n_stubs"]
        self.indicator_type = table_type["indicator_type"]
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.n_text_columns = n_text_column
        self.text_column_pos = self.get_text_column_pos()
        self.number_lengths = self.generate_number_lengths()
        self.word_lengths = self.generate_word_lengths()
        self.rows = self.generate_rows()
        self.product = random.choice([True, False])
        self.bold_stub = random.choice([True, False])
        self.bold_header = random.choice([True, False])
        self.headers = self.generate_headers()
        self.stubs = self.generate_stubs()
        self.indicator = self.generate_indicator()
        self.v_lines = self.generate_v_lines()
        self.h_lines = self.generate_h_lines()
        self.column_format = self.generate_column_format()
        self.font_size = random.choice([r"\normalsize", r"\large", r"\Large", r"\LARGE"])
        self.df = self.create_df()

    def create_df(self):
        if self.n_stubs > 0 and self.n_headers > 0:
            table = pd.DataFrame(data=self.rows, index=self.stubs, columns=self.headers)
        elif self.n_stubs > 0:
            table = pd.DataFrame(data=self.rows, index=self.stubs)
        elif self.n_columns > 0:
            table = pd.DataFrame(data=self.rows, columns=self.headers)
        else:
            table = pd.DataFrame(data=self.rows)

        if self.indicator_type == "stub":
            table.index.names = self.indicator
        elif self.indicator_type == "column":
            table.column.names = self.indicator
        return table


    def assemble(self):
        return np.array(self.headers + self.rows)

    def generate_indicator(self):
        n = 0
        if self.indicator_type == "stub":
            n = self.n_stubs
        elif self.indicator_type == "column":
            n = self.n_columns
        return random.sample(words.words(), n)

    def generate_stubs(self):
        stubs = [random.sample(words.words(), self.n_rows) for x in range(self.n_stubs)]
        if self.n_stubs > 0:
            return pd.MultiIndex.from_arrays(stubs)
        else:
            return stubs

    def generate_headers(self):
        headers = [random.sample(words.words(), self.n_columns) for x in range(self.n_headers)]
        if self.n_headers > 0:
            return pd.MultiIndex.from_arrays(headers)
        else:
            return headers

    def generate_rows(self):
        rows = []
        picked_words = random.sample(words.words(), sum(self.word_lengths) * self.n_rows)
        for row in range(self.n_rows):
            row = [None] * self.n_columns
            current_number_lengths = self.number_lengths.copy()
            current_word_lengths = self.word_lengths.copy()
            for idx, i in enumerate(row):
                if idx in self.text_column_pos:
                    length = current_word_lengths[0]
                    row[idx] = " ".join(picked_words[0:length-1])
                    current_word_lengths.pop(0)
                    picked_words.pop(0)
                else:
                    range_start = 10**(current_number_lengths[0]-1)
                    range_end = (10**current_number_lengths[0])-1
                    row[idx] = random.randint(range_start, range_end)
                    current_number_lengths.pop(0)
            rows.append(row)
        return rows
        
    def generate_number_lengths(self):
        return [random.randint(1, 5) for x in range(self.n_columns-self.n_text_columns)]
    
    def generate_word_lengths(self):
        return [random.randint(1, 3) for x in range(self.n_text_columns)]
        
    def get_text_column_pos(self):
        return sorted(random.sample(range(self.n_columns), self.n_text_columns))

    def set_rows(self, rows):
        self.rows = rows

    def generate_column_format(self):
        column_format = "".join(np.random.choice(['r', 'c','l'], self.n_columns+self.n_stubs, replace=True).tolist())
        for i in sorted(self.v_lines, reverse=True):
            column_format = column_format[:i] + '|' + column_format[i:]
        return column_format

    def generate_v_lines(self):
        if random.choice([True, False]):
            return random.sample(range(self.n_columns+2), random.randint(0, self.n_columns+1))
        else:
            return []

    def generate_h_lines(self):
        if random.choice([True, False]):
            return random.sample(range(self.n_rows+2), random.randint(0, self.n_rows+1))
        else:
            return []