import json

def put_vals(dictionary,path):
	with open(path,'w') as fp:
		json.dump(dictionary,fp,indent=4)

def load_config(file):
	f = open(file)
	a = json.load(f)
	return a 
