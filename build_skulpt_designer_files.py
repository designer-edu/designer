import json


data_files = {
    'colors.json',
    'default_key_mappings.txt'
}


with open('dist-js/skulpt-designer-files.js', 'w') as output_file:
    for filename in data_files:
        with open(f'designer/data/{filename}') as data_file:
            data = data_file.read()
            line = f"Sk.builtinFiles['files']['src/lib/designer/data/{filename}']={json.dumps(data)};\n"
            output_file.write(line)