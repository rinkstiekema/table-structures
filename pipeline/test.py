import json, os, sys

folder = sys.argv[1]
outline_folder = sys.argv[2]
for json_file in os.listdir(folder):
    location = os.path.join(folder, json_file)
    with open(location, 'r+') as jfile:
        tables = json.load(jfile)
        for table in tables:
            table["outlineURL"] = os.path.join(outline_folder, os.path.basename(table["renderURL"]))
        jfile.seek(0)
        jfile.write(json.dumps(tables))
        jfile.truncate()
