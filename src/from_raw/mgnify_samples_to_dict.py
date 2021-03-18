
import json
import os

path = "/global/cfs/cdirs/kbase/KE-Catboost/jrb/data/mgnify/samples"
dict_all = dict()
for x in os.listdir(path):
    print(x)
    with open(path+"/"+x+"/sample.json") as json_file:

        curdata = json.load(json_file)

        #print(curdata['attributes'])

        for key in curdata['attributes']:
            print(key+"\t"+str(curdata['attributes'][key]))

        curdict = dict()

        for key in curdata['attributes']:
            if key in dict_all:
                if curdata['attributes'][key] not in dict_all[key]:
                    dict_all[key] = dict_all[key] + " ** " + curdata['attributes'][key]
            else:
                dict_all[key] = curdata['attributes'][key]

        #curdict['type'] = curdata['type']
        #curdict['id'] = curdata['id']

        #dict_all.update(curdict)


f = open("mgnify_sample_dict.txt","w")
f.write( str(dict_all) )
f.close()