
import json
import os

path = "/global/cfs/cdirs/kbase/KE-Catboost/jrb/data/mgnify/samples"
dict_all = dict()
for x in os.listdir(path):
    with open(path+"/"+x+"/sample.json") as json_file:
        curdict = json.load(json_file)
        dict_all.update(curdict)


f = open("mgnify_sample_dict.txt","w")
f.write( str(dict_all) )
f.close()