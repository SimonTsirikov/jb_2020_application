import yaml
import csv
from pathlib import Path


def parse_file(name):
    structure = yaml.safe_load(Path(name).read_text()) 
    result = []
    
    result.append(structure.get('name'))
    result.append(structure.get('description'))
    if 'authors' in structure:
        result.append(' '.join(structure.get('authors')))
    elif 'author' in structure:
        result.append(''.join(structure.get('author')))
    
    result.extend(parse_section(structure.get('input')))
    result.extend(parse_section(structure.get('output')))
    result.extend(parse_section(structure.get('param')))
    
    return result


def parse_section(section):
	if (section is None):
		return [0, 0]
	else:
		return [len(section), length_of_named(section)]
	

def length_of_named(section):
	result = 0
	for item in section:
		if type(item) == dict:
			result += 1
	return result
                  
    
def parse_fs():
    filenames = [wrap for wrap in Path('.').glob('**/meta.yaml')]
    return filenames

with open('table.csv', 'w', newline='\n') as csvfile:
    spamwriter = csv.writer(csvfile, escapechar=' ', delimiter=',', quoting=csv.QUOTE_NONE)
    
    for name in parse_fs():
        spamwriter.writerow(parse_file(name))
