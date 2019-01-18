import camelot
tables = camelot.read_pdf('E:/Documents/School/Thesis/reading/oro2009.pdf')
print(tables)
tables.export('foo.csv', f='csv', compress=True)