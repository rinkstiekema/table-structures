from chardet import detect

def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def open_file(location):
    return open(location, 'r+', encoding=get_encoding_type(location), errors='ignore')