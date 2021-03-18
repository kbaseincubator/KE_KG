
import json
import os

path = "/global/cfs/cdirs/kbase/KE-Catboost/jrb/data/mgnify/samples"
dict_all = dict()
dict_count = dict()
for x in os.listdir(path):
    print(x)
    with open(path+"/"+x+"/sample.json") as json_file:

        curdata = json.load(json_file)

        #print(curdata['attributes'])

        #for key in curdata['attributes']:
        #    print(key+"\t"+str(curdata['attributes'][key]))


        for key in curdata['attributes']:
            #print(key)
            if key in dict_all:
                if str(curdata['attributes'][key]) not in str(dict_all[key]):
                    dict_all[key] = str(dict_all[key]) + " ** " + str(curdata['attributes'][key])
            else:
                dict_all[key] = curdata['attributes'][key]

            if key in dict_count:
                dict_count[key] = dict_count[key] + 1
            else:
                dict_count[key] =  1


f = open("mgnify_sample_key_count.txt","w")
f.write( str(dict_count) )
f.close()

f = open("mgnify_sample_dict.txt","w")
f.write( str(dict_all) )
f.close()