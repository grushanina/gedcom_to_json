from GedcomToJson import GedcomToJsonParser
import json

gedcom_to_json_parser = GedcomToJsonParser('data/Musterstammbaum.ged')

json_string = json.dumps(gedcom_to_json_parser.get_json())
print(json_string)

with open('json_data.json', 'w') as outfile:
    outfile.write(json_string.replace('[{', '[\n {').replace('}]', '}\n]').replace('},', '},\n'))
