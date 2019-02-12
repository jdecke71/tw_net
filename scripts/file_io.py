import json
import sys

'''
Write json to file
'''
def WriteJSON(obj,filename):
    try:
        with open(filename, 'w') as outfile:
            obj_json = json.dumps(obj, sort_keys=True, indent=4,default=str)
            outfile.write(obj_json)
    except Exception as e:
        print(e, file=sys.stderr)
        print('File not written.')

'''
Read and return json object from file. If none, return empty object.
'''
def ReadJSON(filename):
    try: 
        with open(filename, 'r') as infile:
            obj = json.load(infile)
    except Exception as e: 
        obj = [] 
    return obj
