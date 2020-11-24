import pandas as pd
import math
import numpy as np

imgvr_df = pd.read_csv('/Users/marcin/Documents/KBase/KE/IMGVR/IMGVR_samples.tsv', sep='\t')


columns = imgvr_df.columns.str
print(type(columns))
print(columns)


#'TaxonOID', 'Domain', 'Sequencing Status', 'Study Name',
#       'Genome Name / Sample Name', 'Sequencing Center', 'IMG Genome ID',
#       'GOLD Analysis Project ID', 'GOLD Analysis Project Type',
#       'GOLD Sequencing Project ID', 'GOLD Study ID', 'Geographic Location',
#       'GOLD Ecosystem', 'GOLD Ecosystem Category', 'GOLD Ecosystem Subtype',
#       'GOLD Ecosystem Type', 'GOLD Sequencing Depth',
#       'GOLD Sequencing Quality', 'GOLD Sequencing Status',
#       'GOLD Sequencing Strategy', 'GOLD Specific Ecosystem', 'Habitat',
#       'Latitude', 'Longitude', 'Genome Size   * assembled',
#       'Gene Count   * assembled'


primary_field = "GOLD Analysis Project ID"#"GOLD Sequencing Project ID"
linked_fields = ["TaxonOID",
"IMG Genome ID",
"GOLD Sequencing Project ID",
#"GOLD Analysis Project ID",
"GOLD Analysis Project Type",
"GOLD Study ID",
"Geographic Location",
"GOLD Ecosystem",
"GOLD Ecosystem Category",
"GOLD Ecosystem Subtype",
"GOLD Ecosystem Type",
"GOLD Sequencing Depth",
"GOLD Sequencing Strategy",
"GOLD Specific Ecosystem",
"Habitat",
"Genome Size   * assembled",
"Gene Count   * assembled"]

#TaxonOID
#IMG Genome ID
#GOLD Analysis Project ID
#GOLD Analysis Project Type
#GOLD Sequencing Project ID
#GOLD Study ID
#Geographic Location
#GOLD Ecosystem
#GOLD Ecosystem Category
#GOLD Ecosystem Subtype
#GOLD Ecosystem Type
#GOLD Sequencing Depth
#GOLD Sequencing Strategy
#GOLD Specific Ecosystem Habitat
#Genome Size   * assembled
#Gene Count   * assembled


dims = imgvr_df.shape

print("dims "+str(dims))
primary_index = imgvr_df.columns.get_loc(primary_field)#columns.str.find(primary_field)
print("primary_index "+str(primary_index))

output = []
for i in range(0, dims[0]) :
    for j in range(0, len(linked_fields)):
        #secondary_index = columns.str.find(linked_fields[j])
        secondary_index = imgvr_df.columns.get_loc(linked_fields[j])
        print("secondary_index " + str(secondary_index))
        addval = imgvr_df.iloc[i, secondary_index]
        print("addval "+str(addval))

        if("Genome Size   * assembled" == linked_fields[j] or "Gene Count   * assembled" == linked_fields[j]):
            if (addval == 0):
                addval = np.NAN
            else:
                addval = math.log10(addval)
        newstr = str(imgvr_df.iloc[i, primary_index]) +"\thas_quality\t"+str(addval)
        output.append(newstr)

with open("IMGVR_sample.tsv", "w") as outfile:
        outfile.write("\n".join(output))

#compression_opts = dict(method='zip', archive_name='out.csv')
#df.to_csv('IMGVR_sample.tsv', sep = "\t")# index=False,compression=compression_opts)