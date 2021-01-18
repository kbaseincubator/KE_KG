import pandas as pd
import math
import numpy as np

###Available columns copied from source file
## UViG	Taxon_oid	Scaffold_oid	Coordinates ('whole' if the UViG is the entire contig)
# Ecosystem classification	vOTU	Length	Topology	Estimated completeness	MIUV
#iG quality	Gene content (total genes;cds;tRNA;VPF percentage)	Taxonomic classification
# Taxonomic classification method	Host taxonomy prediction	Host prediction meth
#od	Sequence origin (doi)	In_IMG	Gene content Pfam;VOG;VPF


subject_field = "GOLD Analysis Project ID"
subject_field_prefix = "GOLD"
subject_field_category = "biolink:Attribute"

object_fields = [
#"TaxonOID",
#"IMG Genome ID",
"GOLD Sequencing Project ID",
#"GOLD Analysis Project ID",
"GOLD Analysis Project Type",
"GOLD Study ID",
"Geographic Location",
"GOLD Ecosystem",
"GOLD Ecosystem Category",
"GOLD Ecosystem Subtype",
"GOLD Ecosystem Type",
#"GOLD Sequencing Depth",
"GOLD Sequencing Status",
"GOLD Sequencing Strategy",
"GOLD Specific Ecosystem",
"Latitude",
"Longitude",
"Habitat",
"Genome Size   * assembled",
"Gene Count   * assembled"
]

object_field_prefixes = [
#"GOLD",
#"IMG_genome_ID",
"GOLD",#"Sequencing_project_ID",
#"GOLD",
"GOLD",#"Analysis_project_type",
"GOLD",#"Study_ID",
"GOLD",#"Geographic_location",
"GOLD",
"GOLD",
"GOLD",
"GOLD",
"GOLD",
#"Depth",
"GOLD",#"Sequencing_strategy",
"GOLD",
"Latitude",
"Longitude",
"GOLD",#"Habitat",
"Assembly_size",
"Gene_count"
]

object_field_categories = [
#"biolink:OrganismTaxon",
#"IMG_genome_ID",
"biolink:Attribute",
#"biolink:Attribute",
"biolink:Attribute",
"biolink:Attribute",
"biolink:NamedThing",
"biolink:Attribute",
"biolink:Attribute",
"biolink:Attribute",
"biolink:Attribute",
"biolink:Attribute",
#"biolink:QuantityValue",
"biolink:Attribute",
"biolink:Attribute",
"biolink:QuantityValue",
"biolink:QuantityValue",
"biolink:Attribute",
"biolink:NamedThing",
"biolink:NamedThing"
]


### TBD
object_edge_labels = [
#"biolink:has taxonomic rank",
#"IMG_genome_ID",
"biolink:has_attribute",
#"Analysis Project ID",
"biolink:has_attribute",
"biolink:has_attribute",
"biolink:located_in",
"biolink:occurs_in",
"biolink:occurs_in",
"biolink:occurs_in",
"biolink:occurs_in",
#"biolink:QuantityValue",
"biolink:has_attribute",
"biolink:has_attribute",
"biolink:has_attribute",
"biolink:located_in",
"biolink:located_in",
"biolink:occurs_in",
"biolink:has_quantitative_value",
"biolink:has_quantitative_value"
]

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


kgx_header_edges = "subject\tedge_label\tobject\trelation\tprovided_by\n"
kgx_header_nodes = "id\tname\tcategory\tprovided_by\n"



def load(source_path):
    df = pd.read_csv(source_path, sep='\t')

    columns = df.columns.str
    print(type(columns))
    print(columns)

    dims = df.shape

    print("dims "+str(dims))
    subject_index = df.columns.get_loc(subject_field)#columns.str.find(primary_field)
    print("subject_index "+str(subject_index))

    return (subject_index, df)


def parse(subject_index, df):
    edges = []
    nodes = []
    dims = df.shape

    # convert chars to underscore
    #
    df = df.replace(',', '_', regex=True)
    df = df.replace(' ', '_', regex=True)
    df = df.replace(':', '_', regex=True)
    df = df.replace('__', '_', regex=True)
    # convert to lower case for variation
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)

    for i in range(0, dims[0]):#100):#
        print(".")
        for j in range(0, len(object_fields)):
            #secondary_index = columns.str.find(object_fields[j])
            secondary_index = df.columns.get_loc(object_fields[j])
            #print("secondary_index " + str(secondary_index))
            addval = df.iloc[i, secondary_index]
           #print("addval "+str(addval))

            if "Genome Size   * assembled" == object_fields[j] or "Gene Count   * assembled" == object_fields[j]:
                addval_orig = addval

                if (addval == 0):
                    addval = np.NAN
                else:
                    addval = math.log10(addval)
                    if math.isnan(addval):
                        addval = np.NAN
                    else:
                        addval = int(round(addval, 0))

                #print("addval "+str(addval_orig)+"\t"+str(addval))
            elif "GOLD Ecosystem Subtype" == object_fields[j] and addval in ["Unclassified"]:
                addval = np.NAN
            elif "Latitude" == object_fields[j] or "Longitude" == object_fields[j]:
                ###load pairwise distance file and ingest as sample-sample in separate code block
                addval = np.NAN

            ###write the edge
            if not pd.isnull(addval):

                ##special case to link study -> project and skip analysis -> project (analysis -> study happens independently)
                if "GOLD Sequencing Project ID" == object_fields[j]:
                    if (debug):
                        print("making study -> project")

                    subject_index_now = object_fields.index("GOLD Study ID")

                    newstr = object_field_prefixes[subject_index_now] + ":" + str(df.iloc[i, subject_index_now]) + "\tbiolink:has_attribute\t" + \
                             object_field_prefixes[j] + ":" + str(addval) + "\tbiolink:has_attribute\t" + "GOLD"
                    if (debug):
                        print("adding " + newstr)
                    if newstr not in edges:
                        edges.append(newstr)

                    node1str = object_field_prefixes[subject_index_now]  + ":" + str(df.iloc[i, subject_index_now]) + "\t" + str(
                        df.iloc[i, subject_index]) + "\t" + object_field_categories[subject_index_now]+"\tGOLD"
                    if (debug):
                        print("adding " + node1str)
                    if node1str not in nodes:
                        nodes.append(node1str)

                    node2str = object_field_prefixes[j] + ":" + str(addval) + "\t" + str(addval) + "\t" + \
                               object_field_categories[j]+"\tGOLD"
                    if (debug):
                        print("adding " + node2str)
                    if node2str not in nodes:
                        nodes.append(node2str)
                else:
                    #print(i)
                    #print(j)
                    #print(subject_index)
                    #print(addval)
                    #print(df.iloc[i, subject_index])
                    #print(subject_field_prefix)

                    newstr = subject_field_prefix+":"+str(df.iloc[i, subject_index]) +"\t"+object_edge_labels[j]+"\t"+object_field_prefixes[j]+":"+str(addval)+"\t"+object_edge_labels[j]+"\t"+"GOLD"
                    if (debug):
                        print("adding "+newstr)
                    if newstr not in edges:
                        edges.append(newstr)

                    node1str = subject_field_prefix + ":" + str(df.iloc[i, subject_index]) + "\t" + str(df.iloc[i, subject_index]) +"\t"+subject_field_category +"\tGOLD"
                    if (debug):
                        print("adding " + node1str)
                    if node1str not in nodes:
                        nodes.append(node1str)

                    node2str = object_field_prefixes[j] + ":" + str(addval) + "\t" + str(addval) + "\t" + object_field_categories[j] +"\tGOLD"
                    if (debug):
                        print("adding " + node2str)
                    if node2str not in nodes:
                        nodes.append(node2str)

    return (edges, nodes)

def write(output, outfile, header):
    with open(outfile, "w") as outfile:
        outfile.write(header)
        outfile.write("\n".join(output))



###
source_path ='/kbase/ke/data/IMG_VR/IMG_VR_2020-09-10_5/IMG_VR_In-IMG-Only_Unique-IMG-IDs_Unique-Non-Isolate-Only_v1.tsv'
#source_path = '/Users/marcin/Documents/KBase/KE/IMGVR/IMGVR_samples_table.tsv'

tuple1 = load(source_path)
subject_index = tuple1[0]
df = tuple1[1]

tuple2 = parse(subject_index, df,  debug)
edge_output = tuple2[0]
edge_outfile = "IMGVR_sample_KGX_edges.tsv"
print("writing "+edge_outfile)
write(edge_output, edge_outfile, kgx_header_edges)

node_output = tuple2[1]
node_outfile = "IMGVR_sample_KGX_nodes.tsv"
print("writing "+node_outfile)
write(node_output, node_outfile, kgx_header_nodes)
