
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
            if key == "sample-metadata":
                print(curdata['attributes'])
                for attr_data in curdata['attributes']:
                    if attr_data["key"] in dict_all:
                        if str(attr_data["value"]) not in str(dict_all[key]):
                            dict_all[attr_data["key"]] = str(dict_all[key]) + " ** " + str(attr_data["value"])
                    else:
                        dict_all[attr_data["key"]] = attr_data["value"]

                    if attr_data["key"] in dict_count and dict_count[attr_data["key"]] != 'None':
                        dict_count[attr_data["key"]] = dict_count[attr_data["key"]] + 1
                    else:
                        dict_count[attr_data["key"]] = 1
            else:
                if key in dict_all:
                    if str(curdata['attributes'][key]) not in str(dict_all[key]):
                        dict_all[key] = str(dict_all[key]) + " ** " + str(curdata['attributes'][key])
                else:
                    dict_all[key] = curdata['attributes'][key]

                if key in dict_count and dict_count[key] != 'None':
                    dict_count[key] = dict_count[key] + 1
                else:
                    dict_count[key] =  1


f = open("mgnify_sample_key_count.txt","w")
f.write( str(dict_count) )
f.close()

f = open("mgnify_sample_dict.txt","w")
f.write( str(dict_all) )
f.close()