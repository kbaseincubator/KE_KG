import pandas as pd
import math
import numpy as np


kgx_header_edges = "subject\tedge_label\tobject\trelation\tprovided_by\n"
kgx_header_nodes = "id\tname\tcategory\tprovided_by\n"



def load(source_path):
    df = pd.read_csv(source_path, sep='\t', index_col=0)

    columns = df.columns.values
    print(type(columns))
    print(columns)

    print(type(df.index.values))
    print(df.index.values)

    dims = df.shape

    print("dims "+str(dims))

    return df


def parse(df):
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
        print(".")
        for j in range(0, dims[1]):

            if(int(df.iloc[i, j]) > 0):
                newstr = "GTDB:" + df.index.values[i] + "\tbiolink:occurs_in\t" + \
                         "Sample:" + df.columns.values[j] + "\tbiolink:occurs_in\t" + "Torben"
                print("adding " + newstr)
                if newstr not in edges:
                    edges.append(newstr)

                node1str = "GTDB:" + df.index.values[i] + "\t" + df.index.values[i] + "\tbiolink:OrganismalEntity" +"\tTorben"
                print("adding " + node1str)
                if node1str not in nodes:
                    nodes.append(node1str)

                node2str = "TorbenSample:" + df.columns.values[j] + "\t" + df.columns.values[j] + "\tbiolink:MaterialSample"+"\tTorben"
                print("adding " + node2str)
                if node2str not in nodes:
                    nodes.append(node2str)

    return (edges, nodes)

def write(output, outfile, header):
    with open(outfile, "w") as outfile:
        outfile.write(header)
        outfile.write("\n".join(output))



###
source_path = '/Users/marcin/Documents/KBase/KE/Torben/Torben_metaG_GTDB-taxa-count_summary_v1.tsv'
tax_mapping_path = '/Users/marcin/Documents/KBase/KE/mappings/'

df = load(source_path)

tuple2 = parse(df)
edge_output = tuple2[0]
edge_outfile = "Torben_abundance_KGX_edges.tsv"
print("writing "+edge_outfile)
write(edge_output, edge_outfile, kgx_header_edges)

node_output = tuple2[1]
node_outfile = "Torben_abundance_KGX_nodes.tsv"
print("writing "+node_outfile)
write(node_output, node_outfile, kgx_header_nodes)