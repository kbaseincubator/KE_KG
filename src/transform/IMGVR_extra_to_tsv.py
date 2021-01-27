import pandas as pd
import math
import numpy as np

###Available columns copied from source file
# IMG_taxon_oid	GOLD_Analysis_Project_ID	UViG_Taxon_oid	Scaffold_oid_unclear_field_do_not_use
# Scaffold_ID	Coordinates_.whole_if_the_UViG_is_the_entire_contig.	Ecosystem_classification
# vOTU	Length	Topology	Estimated_completeness	MIUViG_quality
# Gene_content_.total_genes.cds.tRNA.VPF_percentage.	Taxonomic_classification
# Taxonomic_classification_method	Host_taxonomy_prediction	Host_prediction_method
# Sequence_origin_.doi.	In_IMG	Gene_content_Pfam.VOG.VPF


subject_field = "GOLD_Analysis_Project_ID"
subject_field_prefix = "GOLD"
subject_field_category = "biolink:Attribute"

object_fields = [
    # 'IMG_TaxonOID',
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
    # 'IMG_TaxonOID',
    'GOLD',
    ## UViG_Taxon_oid
    # 'Scaffold_oid_unclear_field_do_not_use',
    # Scaffold_oid
    # Coordinates ('whole' if the UViG is the entire contig)
    'GOLD',
    'vOTU',
    'Contig_length',
    'Virus_topology',
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
    # 'IMG_TaxonOID',
    'biolink:Attribute',
    ## UViG_Taxon_oid
    # 'Scaffold_oid_unclear_field_do_not_use',
    # Scaffold_oid
    # Coordinates ('whole' if the UViG is the entire contig)
    'biolink:Attribute',
    'kbase:otu',
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
    # 'IMG_TaxonOID',
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
    'biolink:has_taxonomic_rank',
    # Taxonomic classification method
    'biolink:has_taxonomic_rank'
    # Host prediction method
    # Sequence origin (doi)
    # In_IMG
    # Gene content Pfam;VOG;VPF
]

kgx_header_edges = "subject\tpredicate\tobject\trelation\tprovided_by\n"
kgx_header_nodes = "id\tname\tcategory\tprovided_by\n"


def load(source_path):  # , tax_map_path):
    df = pd.read_csv(source_path, sep='\t')

    columns = df.columns.str
    print(type(columns))
    print(columns)

    dims = df.shape

    print("dims " + str(dims))
    subject_index = df.columns.get_loc(subject_field)  # columns.str.find(primary_field)
    print("subject_index " + str(subject_index))

    # taxdf = pd.read_csv(tax_map_path, sep='\t')

    return (subject_index, df)  # , taxdf)


def make_log10(addval):
    if (addval == 0):
        addval = np.NAN
    else:
        addval = math.log10(addval)
        if math.isnan(addval):
            addval = np.NAN
        else:
            addval = int(round(addval, 0))
    return addval


def parse(subject_index, df, debug=False):  # , taxdf):
    edges = []
    nodes = []
    dims = df.shape

    print("Object fields")
    print(object_fields)

    # convert chars to underscore
    #
    #df = df.replace(',', '_', regex=True)
    #df = df.replace(' ', '_', regex=True)

    df = df.replace(',', '_', regex=True)
    df = df.replace(' ', '_', regex=True)
    df = df.replace(':', '_', regex=True)
    df = df.replace('__', '_', regex=True)
    # convert to lower case for variation
    df = df.applymap(lambda s: s.lower() if type(s) == str else s)

    for i in range(0, dims[0]):  # 100):#

        if (i % 1000 == 0):
            print("." + str(i))
        for j in range(0, len(object_fields)):

            subject_val = str(df.iloc[i, subject_index])
            object_index = df.columns.get_loc(object_fields[j])
            # print("object_index " + str(object_index))
            addval = df.iloc[i, object_index]
            # print("addval "+str(addval))

            if "Length" == object_fields[j]:
                addval_orig = addval
                addval = make_log10(addval)

            # elif "Taxonomic classification" == object_fields[j]:
            #    print("Virus "+addval)

            # elif "Taxonomic classification" == object_fields[j]:
            #    print("Host " + addval)

            ###write the nodes and edges

            if (debug):
                print("addval " + str(addval))
            if not pd.isnull(addval) and addval != 'nan':
                addval = str(addval)
                # vOTU to host, length, topology
                if "vOTU" == object_fields[j]:

                    object_index_now = object_fields.index('Host_taxonomy_prediction')
                    j_second = df.columns.get_loc(object_fields[object_index_now])
                    addvalnow = df.iloc[i, j_second]
                    if not pd.isnull(addvalnow):
                        newstr = object_field_prefixes[object_index_now] + ":" + str(
                            addvalnow) + "\tkbase:is_host_for\t" + object_field_prefixes[j] + ":" + addval \
                                 + "\tkbase:is_host_for\t" + "GOLD"
                        if (debug):
                            print("adding O " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = object_field_prefixes[j] + ":" + addval + "\t" + addval + "\t" + \
                                   object_field_categories[j] + "\tGOLD"
                        if (debug):
                            print("adding O " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

                        node2str = object_field_prefixes[object_index_now] + ":" + str(addvalnow) + "\t" + str(
                            addvalnow) + "\t" + object_field_categories[object_index_now] + "\tGOLD"
                        if (debug):
                            print("adding O " + node2str)
                        if node2str not in nodes:
                            nodes.append(node2str)

                    object_index_now = object_fields.index('Length')
                    j_second = df.columns.get_loc(object_fields[object_index_now])
                    addvalnow = make_log10(df.iloc[i, j_second])
                    if not pd.isnull(addvalnow):
                        addvalnow = str(addvalnow)
                        newstr = object_field_prefixes[j] + ":" + str(
                            addval) + "\tbiolink:has_attribute\t" + \
                                 object_field_prefixes[object_index_now] + ":" + str(
                            addvalnow) + "\tbiolink:has_attribute\t" + "GOLD"
                        if (debug):
                            print("adding O " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = object_field_prefixes[j] + ":" + addval + "\t" + addval + "\t" + \
                                   object_field_categories[j] + "\tGOLD"
                        if (debug):
                            print("adding O " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

                        node2str = object_field_prefixes[object_index_now] + ":" + str(addvalnow) + "\t" + str(
                            addvalnow) + "\t" + \
                                   object_field_categories[object_index_now] + "\tGOLD"
                        if (debug):
                            print("adding O " + node2str)
                        if node2str not in nodes:
                            nodes.append(node2str)

                    object_index_now = object_fields.index('Topology')
                    j_second = df.columns.get_loc(object_fields[object_index_now])
                    addvalnow = df.iloc[i, j_second]
                    if not pd.isnull(addvalnow):
                        addvalnow = str(addvalnow)
                        newstr = object_field_prefixes[j] + ":" + str(
                            addval) + "\tbiolink:has_attribute\t" + \
                                 object_field_prefixes[object_index_now] + ":" + str(
                            addvalnow) + "\tbiolink:has_attribute\t" + "GOLD"
                        if (debug):
                            print("adding O " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = object_field_prefixes[j] + ":" + addval + "\t" + addval + "\t" + \
                                   object_field_categories[j] + "\tGOLD"
                        if (debug):
                            print("adding O  " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

                        node2str = object_field_prefixes[object_index_now] + ":" + str(addvalnow) + "\t" + str(
                            addvalnow) + "\t" + \
                                   object_field_categories[object_index_now] + "\tGOLD"
                        if (debug):
                            print("adding O  " + node2str)
                        if node2str not in nodes:
                            nodes.append(node2str)
                # taxa to host, length, topology, vOTU
                elif "Taxonomic_classification" == object_fields[j]:

                    object_index_now = object_fields.index('Host_taxonomy_prediction')
                    j_second = df.columns.get_loc(object_fields[object_index_now])
                    addvalnow = df.iloc[i, j_second]
                    if not pd.isnull(addvalnow):
                        addvalnow = str(addvalnow)
                        newstr = object_field_prefixes[object_index_now] + ":" + str(
                            addvalnow) + "\tkbase:is_host_for\t" + \
                                 object_field_prefixes[j] + ":" + str(
                            addval) + "\tkbase:is_host_for\t" + "GOLD"
                        if (debug):
                            print("adding V " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = object_field_prefixes[j] + ":" + addval + "\t" + addval + "\t" + \
                                   object_field_categories[j] + "\tGOLD"
                        if (debug):
                            print("adding V " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

                        node2str = object_field_prefixes[object_index_now] + ":" + str(addvalnow) + "\t" + str(
                            addvalnow) + "\t" + object_field_categories[object_index_now] + "\tGOLD"
                        if (debug):
                            print("adding V " + node2str)
                        if node2str not in nodes:
                            nodes.append(node2str)

                    object_index_now = object_fields.index('Length')
                    j_second = df.columns.get_loc(object_fields[object_index_now])
                    addvalnow = make_log10(df.iloc[i, j_second])
                    if not pd.isnull(addvalnow):
                        addvalnow = str(addvalnow)
                        newstr = object_field_prefixes[j] + ":" + str(
                            addval) + "\tbiolink:has_attribute\t" + \
                                 object_field_prefixes[object_index_now] + ":" + str(
                            addvalnow) + "\tbiolink:has_attribute\t" + "GOLD"
                        if (debug):
                            print("adding V " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = object_field_prefixes[j] + ":" + addval + "\t" + addval + "\t" + \
                                   object_field_categories[j] + "\tGOLD"
                        if (debug):
                            print("adding V " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

                        node2str = object_field_prefixes[object_index_now] + ":" + str(addvalnow) + "\t" + str(
                            addvalnow) + "\t" + \
                                   object_field_categories[object_index_now] + "\tGOLD"
                        if (debug):
                            print("adding V " + node2str)
                        if node2str not in nodes:
                            nodes.append(node2str)

                    object_index_now = object_fields.index('Topology')
                    j_second = df.columns.get_loc(object_fields[object_index_now])
                    addvalnow = df.iloc[i, j_second]
                    if not pd.isnull(addvalnow):
                        addvalnow = str(addvalnow)
                        newstr = object_field_prefixes[j] + ":" + str(
                            addval) + "\tbiolink:has_attribute\t" + \
                                 object_field_prefixes[object_index_now] + ":" + str(
                            addvalnow) + "\tbiolink:has_attribute\t" + "GOLD"
                        if (debug):
                            print("adding V " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = object_field_prefixes[j] + ":" + addval + "\t" + addval + "\t" + \
                                   object_field_categories[j] + "\tGOLD"
                        if (debug):
                            print("adding V " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

                        node2str = object_field_prefixes[object_index_now] + ":" + str(addvalnow) + "\t" + str(
                            addvalnow) + "\t" + \
                                   object_field_categories[object_index_now] + "\tGOLD"
                        if (debug):
                            print("adding V " + node2str)
                        if node2str not in nodes:
                            nodes.append(node2str)

                    object_index_now = object_fields.index('vOTU')
                    j_second = df.columns.get_loc(object_fields[object_index_now])
                    addvalnow = df.iloc[i, j_second]
                    if not pd.isnull(addvalnow):
                        addvalnow = str(addvalnow)
                        newstr = object_field_prefixes[j] + ":" + str(
                            addval) + "\tbiolink:has_attribute\t" + \
                                 object_field_prefixes[object_index_now] + ":" + str(
                            addvalnow) + "\tbiolink:has_attribute\t" + "GOLD"
                        if (debug):
                            print("adding V " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = object_field_prefixes[j] + ":" + addval + "\t" + addval + "\t" + \
                                   object_field_categories[j] + "\tGOLD"
                        if (debug):
                            print("adding V " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

                        node2str = object_field_prefixes[object_index_now] + ":" + str(addvalnow) + "\t" + str(
                            addvalnow) + "\t" + \
                                   object_field_categories[object_index_now] + "\tGOLD"
                        if (debug):
                            print("adding V " + node2str)
                        if node2str not in nodes:
                            nodes.append(node2str)
                # adding just edge for host -> virus topology (in host genome)
                elif "Host_taxonomy_prediction  " == object_fields[j]:

                    object_index_now = object_fields.index('Topology')
                    j_second = df.columns.get_loc(object_fields[object_index_now])
                    addvalnow = df.iloc[i, j_second]
                    if not pd.isnull(addvalnow):
                        addvalnow = str(addvalnow)
                        newstr = object_field_prefixes[j] + ":" + str(
                            addval) + "\tbiolink:has_attribute\t" + \
                                 object_field_prefixes[object_index_now] + ":" + str(
                            addvalnow) + "\tbiolink:has_attribute\t" + "GOLD"
                        if (debug):
                            print("adding V " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

            elif "Ecosystem_classification" == object_fields[j]:
                if (addval not in ['na;na;na;na;na;na']):
                    addval_orig = addval
                    if (debug):
                        print("Ecosystem " + str(addval))
                    terms = addval.split(";")
                    for k in range(0, len(terms)):
                        newstr = subject_field_prefix + ":" + subject_val + "\t" + object_edge_labels[j] + "\t" + \
                                 object_field_prefixes[j] + ":" + terms[k] + "\t" + object_edge_labels[
                                     j] + "\t" + "GOLD"
                        if (debug):
                            print("adding E " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = subject_field_prefix + ":" + subject_val + "\t" + subject_val + "\t" + subject_field_category + "\tGOLD"
                        if (debug):
                            print("adding E " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

                        node2str = object_field_prefixes[j] + ":" + terms[k] + "\t" + terms[k] + "\t" + \
                                   object_field_categories[j] + "\tGOLD"
                        if (debug):
                            print("adding E " + node2str)
                        if node2str not in nodes:
                            nodes.append(node2str)

                        ###link individual terms to quintiplet
                        newstr = object_field_prefixes[j] + ":" + terms[k] + "\t" + object_edge_labels[j] + \
                                 "\t" + subject_field_prefix + ":" + str(addval_orig) + "\t" + object_edge_labels[
                                     j] + "\t" + "GOLD"
                        if (debug):
                            print("adding E " + newstr)
                        if newstr not in edges:
                            edges.append(newstr)

                        node1str = subject_field_prefix + ":" + str(addval_orig) + "\t" + str(addval_orig) + "\t" + subject_field_category + "\tGOLD"
                        if (debug):
                            print("adding E " + node1str)
                        if node1str not in nodes:
                            nodes.append(node1str)

            # Add final excluding viral metadata
            if object_fields[j] not in ['Length', 'Topology', 'Ecosystem_classification'] and subject_val != 'nan':
                ###add default to sample - X link
                if (addval not in ['na;na;na;na;na;na']):
                    newstr = subject_field_prefix + ":" + subject_val + "\t" + object_edge_labels[j] + "\t" + \
                             object_field_prefixes[j] + ":" + str(addval) + "\t" + object_edge_labels[j] + "\t" + "GOLD"
                    if (debug):
                        print("adding S " + newstr)
                    if newstr not in edges:
                        edges.append(newstr)

                    node1str = subject_field_prefix + ":" + subject_val + "\t" + subject_val + "\t" + subject_field_category + "\tGOLD"
                    if (debug):
                        print("adding S " + node1str)
                    if node1str not in nodes:
                        nodes.append(node1str)

                    node2str = object_field_prefixes[j] + ":" + str(addval) + "\t" + str(addval) + "\t" + object_field_categories[
                        j] + "\tGOLD"
                    if (debug):
                        print("adding S " + node2str)
                    if node2str not in nodes:
                        nodes.append(node2str)


    return (edges, nodes)


def write(output, outfile, header):
    with open(outfile, "w") as outfile:
        outfile.write(header)
        outfile.write("\n".join(output))


###
source_path = '/kbase/ke/data/IMG_VR/IMG_VR_2020-09-10_5/IMGVR_all_Sequence_information_InIMG-Yes_Linked-to_TaxonOIDs_v2_Completeness-50-100_nocol20_v1.tsv'
# source_path = '/Users/marcin/Documents/KBase/KE/IMGVR/IMGVR_all_Sequence_information_InIMG-Yes_Linked-to_TaxonOIDs_v2_Completeness-50-100_nocol20_v1_1000.tsv'
# tax_map_path = '/Users/marcin/Documents/KBase/KE/NCBItaxonomy/new_taxdump/nodes.tsv'

tuple1 = load(source_path)  # , tax_map_path)
subject_index = tuple1[0]
df = tuple1[1]
# taxdf = tuple1[2]

tuple2 = parse(subject_index, df, False)  # , taxdf)
edge_output = tuple2[0]
edge_outfile = "IMGVR_extra_KGX_edges.tsv"
print("writing " + edge_outfile)
write(edge_output, edge_outfile, kgx_header_edges)

node_output = tuple2[1]
node_outfile = "IMGVR_extra_KGX_nodes.tsv"
print("writing " + node_outfile)
write(node_output, node_outfile, kgx_header_nodes)
