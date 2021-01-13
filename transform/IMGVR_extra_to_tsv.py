import pandas as pd
import math
import numpy as np

###Available columns copied from source file
#IMG_taxon_oid	GOLD_Analysis_Project_ID	UViG_Taxon_oid	Scaffold_oid_unclear_field_do_not_use
# Scaffold_ID	Coordinates_.whole_if_the_UViG_is_the_entire_contig.	Ecosystem_classification
# vOTU	Length	Topology	Estimated_completeness	MIUViG_quality
# Gene_content_.total_genes.cds.tRNA.VPF_percentage.	Taxonomic_classification
# Taxonomic_classification_method	Host_taxonomy_prediction	Host_prediction_method
# Sequence_origin_.doi.	In_IMG	Gene_content_Pfam.VOG.VPF


subject_field = "GOLD_Analysis_Project_ID"
subject_field_prefix = "GOLD"
subject_field_category = "biolink:Attribute"

object_fields = [
#'IMG_TaxonOID',
    'GOLD_Analysis_Project_ID',
## UViG_Taxon_oid
# 'Scaffold_oid_unclear_field_do_not_use',
    # Scaffold_oid
    # Coordinates ('whole' if the UViG is the entire contig)
'Ecosystem_classification',
'vOTU',
'Length',
'Topology',
#        Estimated completeness
    #        MIUViG quality
    #        Gene content (total genes;cds;tRNA;VPF percentage)
'Taxonomic_classification',
    # Taxonomic classification method
'Host_taxonomy_prediction'
# Host prediction method
    # Sequence origin (doi)
    # In_IMG
    # Gene content Pfam;VOG;VPF

]

object_field_prefixes = [
#'IMG_TaxonOID',
'GOLD',
## UViG_Taxon_oid
# 'Scaffold_oid_unclear_field_do_not_use',
    # Scaffold_oid
    # Coordinates ('whole' if the UViG is the entire contig)
'GOLD',
'GOLD',
'Contig_length',
'GOLD',
#        Estimated completeness
    #        MIUViG quality
    #        Gene content (total genes;cds;tRNA;VPF percentage)
'NCBItaxon',
    # Taxonomic classification method
'NCBItaxon'
# Host prediction method
    # Sequence origin (doi)
    # In_IMG
    # Gene content Pfam;VOG;VPF
]

object_field_categories = [
#'IMG_TaxonOID',
'biolink:Attribute',
## UViG_Taxon_oid
# 'Scaffold_oid_unclear_field_do_not_use',
    # Scaffold_oid
    # Coordinates ('whole' if the UViG is the entire contig)
'biolink:Attribute',
'biolink:Attribute',
'biolink:QuantityValue',
'biolink:Attribute',
#        Estimated completeness
    #        MIUViG quality
    #        Gene content (total genes;cds;tRNA;VPF percentage)
'biolink:OrganismTaxon',
    # Taxonomic classification method
'biolink:OrganismTaxon'
# Host prediction method
    # Sequence origin (doi)
    # In_IMG
    # Gene content Pfam;VOG;VPF
]


object_edge_labels = [
#'IMG_TaxonOID',
'biolink:has_attribute',
## UViG_Taxon_oid
    # Scaffold_oid
    # Coordinates ('whole' if the UViG is the entire contig)
'biolink:has_attribute',
    'biolink:has_attribute',
    'biolink:has_attribute',
'biolink:has_attribute',
#        Estimated completeness
    #        MIUViG quality
    #        Gene content (total genes;cds;tRNA;VPF percentage)
'biolink:has taxonomic rank',
    # Taxonomic classification method
'biolink:has taxonomic rank'
# Host prediction method
    # Sequence origin (doi)
    # In_IMG
    # Gene content Pfam;VOG;VPF
]

kgx_header_edges = "subject\tedge_label\tobject\trelation\tprovided_by\n"
kgx_header_nodes = "id\tname\tcategory\tprovided_by\\n"



def load(source_path, tax_map_path):
    df = pd.read_csv(source_path, sep='\t')

    columns = df.columns.str
    print(type(columns))
    print(columns)

    dims = df.shape

    print("dims "+str(dims))
    subject_index = df.columns.get_loc(subject_field)#columns.str.find(primary_field)
    print("subject_index "+str(subject_index))

    taxdf = pd.read_csv(tax_map_path, sep='\t')

    return (subject_index, df, taxdf)


def parse(subject_index, df, taxdf):
    edges = []
    nodes = []
    dims = df.shape

    # convert chars to underscore
    #
    df = df.replace(',', '_', regex=True)
    df = df.replace(' ', '_', regex=True)
    # convert to lower case for variation
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)

    for i in range(0, dims[0]):#100):#

        if(i % 1000 == 0):
            print("."+str(i))
        for j in range(0, len(object_fields)):
            #secondary_index = columns.str.find(object_fields[j])
            secondary_index = df.columns.get_loc(object_fields[j])
            #print("secondary_index " + str(secondary_index))
            addval = df.iloc[i, secondary_index]
           #print("addval "+str(addval))

            if "Length" == object_fields[j]:
                addval_orig = addval

                if (addval == 0):
                    addval = np.NAN
                else:
                    addval = math.log10(addval)
                    if math.isnan(addval):
                        addval = np.NAN
                    else:
                        addval = int(round(addval, 0))
            #elif "Taxonomic classification" == object_fields[j]:
            #    print("Virus "+addval)

            #elif "Taxonomic classification" == object_fields[j]:
            #    print("Host " + addval)

            ###write the edge
            if not pd.isnull(addval):

                newstr = subject_field_prefix+":"+str(df.iloc[i, subject_index]) +"\t"+object_edge_labels[j]+"\t"+object_field_prefixes[j]+":"+str(addval)+"\t"+object_edge_labels[j]+"\t"+"GOLD"
                #print("adding "+newstr)
                if newstr not in edges:
                    edges.append(newstr)

                node1str = subject_field_prefix + ":" + str(df.iloc[i, subject_index]) + "\t" + str(df.iloc[i, subject_index]) +"\t"+subject_field_category +"\tGOLD"
                #print("adding " + node1str)
                if node1str not in nodes:
                    nodes.append(node1str)

                node2str = object_field_prefixes[j] + ":" + str(addval) + "\t" + str(addval) + "\t" + object_field_categories[j] +"\tGOLD"
                #print("adding " + node2str)
                if node2str not in nodes:
                    nodes.append(node2str)

    return (edges, nodes)

def write(output, outfile, header):
    with open(outfile, "w") as outfile:
        outfile.write(header)
        outfile.write("\n".join(output))



###
source_path = '/Users/marcin/Documents/KBase/KE/IMGVR/IMGVR_all_Sequence_information_InIMG-Yes_Linked-to_TaxonOIDs_v2.tsv'
tax_map_path = '/Users/marcin/Documents/KBase/KE/NCBItaxonomy/new_taxdump/nodes.tsv'

tuple1 = load(source_path, tax_map_path)
subject_index = tuple1[0]
df = tuple1[1]
taxdf = tuple1[2]

tuple2 = parse(subject_index, df, taxdf)
edge_output = tuple2[0]
edge_outfile = "IMGVR_extra_KGX_edges.tsv"
print("writing "+edge_outfile)
write(edge_output, edge_outfile, kgx_header_edges)

node_output = tuple2[1]
node_outfile = "IMGVR_extra_KGX_nodes.tsv"
print("writing "+node_outfile)
write(node_output, node_outfile, kgx_header_nodes)