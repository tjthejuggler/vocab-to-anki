#this should make our ocal dictionaries print pretty and make everything in them lowercase
import json
import os
from os import path

cwd = os.getcwd()
local_dict = {}
local_dict_file = 'en_es.json'
if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
	with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
		local_dict = json.load(json_file)

jsonString = local_dict
print(jsonString)
def get_pretty_print(json_object):
    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))



print(get_pretty_print(jsonString))

my_json = get_pretty_print(jsonString)
f = open(cwd+'/local_dictionaries/en_es_pretty.json',"w")
f.write(my_json)
f.close()
