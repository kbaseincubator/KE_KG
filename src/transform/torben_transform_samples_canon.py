"""
Convert data from `Torben_IMG-data_linked_to-GOLD_v2.tsv` into a set of Biolink
formatted node and edge TSV files.

Every column is parsed into a node/vertex.
There is an edge from the first column (the Torben ID) to (most) every other
column. For now, there are no other edges between columns.

This should be run with the current working directory as the project/repo root
path.

Example:
./transform/torben_transform_samples_canon.py ./data/source/torben/Torben_IMG-data_linked_to-GOLD_v2_withGA.tsv ./data/transform/torben_samples/torben_samples-{nodes,edges}.tsv

"""
import csv
import os
import math
import sys

# Configuration for every header from the source file.
# - "edges_out" is a mapping from other column names to edge categories
# - "prefix" is the biolink prefix (ie. namespace) for the value of each column
# - "node_category" is the biolink node category/class for each column/vertex. If
#   this is None, then we skip creation of a node for this column.
_COLUMN_CONFIG = {
    "GOLD_Analysis_Project_ID": {
        "edges_out": {
#            "taxon_oid": "biolink:has_taxonomic_rank",
#            "Domain": "biolink:has_attribute",
#            "Sequencing_Status": "biolink:has_attribute",
#            "Study_Name": "biolink:has_attribute",
#            "Genome_Name_/_Sample_Name": "biolink:has_attribute",
#            "Sequencing_Center": "biolink:has_attribute",
            "Geographic_Location": "biolink:located_in",
            "GOLD_Ecosystem": "biolink:occurs_in",
            "GOLD_Ecosystem_Category": "biolink:occurs_in",
            "GOLD_Ecosystem_Subtype": "biolink:occurs_in",
            "GOLD_Ecosystem_Type": "biolink:occurs_in",
#            "GOLD_Sequencing_Quality": "biolink:has_attribute",
#            "GOLD_Sequencing_Status": "biolink:has_attribute",
            "GOLD_Sequencing_Strategy": "biolink:has_attribute",
            "GOLD_Specific_Ecosystem": "biolink:has_attribute",
            "Habitat": "biolink:located_in",
#            "Latitude": "biolink:located_in",
#            "Longitude": "biolink:located_in",
            "Genome_Size_assembled": "biolink:has_quantitative_value",
            "Gene_Count_assembled": "biolink:has_quantitative_value",
        },
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "taxon_oid": {
        "prefix": "IMG",
#        "node_category": "biolink:OrganismTaxon",
        "node_category": None,
    },
    "Domain": {
        "prefix": "GOLD",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "Sequencing_Status": {
        "prefix": "GOLD",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "Study_Name": {
        "prefix": "GOLD",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "Genome_Name_/_Sample_Name": {
        "prefix": "GOLD",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "Sequencing_Center": {
        "prefix": "GOLD",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "IMG_Genome_ID": {  # Same as taxon_oid; skip
        "node_category": None,
    },
    "JGI_Project_ID_/_ITS_SP_ID": {  # Same as first column; skip
        "node_category": None,
    },
    "Geographic_Location": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "GOLD_Ecosystem": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "GOLD_Ecosystem_Category": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "GOLD_Ecosystem_Subtype": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "GOLD_Ecosystem_Type": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "GOLD_Sequencing_Depth": {
        "prefix": "GOLD",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "GOLD_Sequencing_Quality": {
        "prefix": "GOLD",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "GOLD_Sequencing_Status": {
        "prefix": "GOLD",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "GOLD_Sequencing_Strategy": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "GOLD_Specific_Ecosystem": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "Habitat": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "Latitude": {
        "prefix": "Latitude",
        "node_category": None,
#        "node_category": "biolink:NamedThing",
    },
    "Longitude": {
        "prefix": "Longitude",
#        "node_category": "biolink:NamedThing",
        "node_category": None,
    },
    "Genome_Size_assembled": {
        "prefix": "Assembly_size",
        "node_category": "biolink:NamedThing",
    },
    "Gene_Count_assembled": {
        "prefix": "Gene_count",
        "node_category": "biolink:NamedThing",
    },
    "Torbens_MetaG_Dir_Name": {
        "node_category": None,
    },
}

_CONVERT_LIST = [ 
    "Genome_Size_assembled",
    "Gene_Count_assembled"
]

# Output headers for the edge data
_OUT_EDGE_HEADERS = [
    "subject",
    "edge_label",
    "object",
    "relation",
    "provided_by",
]
# Output headers for the node data
_OUT_NODE_HEADERS = [
    "id",
    "name",
    "category",
    "provided_by",
]

def to_pow10(addval):
    if addval==0:
        return 0
    addval = math.log10(addval)
    addval = int(round(addval, 0))
    return addval



def load(source_file):
    """
    Load the source data and transform into data structures we can use to
    easily generate a biolink formatted TSV
    """
    nodes_d = dict()
    edges_d = dict()
    with open(source_file) as fd:
        reader = csv.reader(fd, delimiter='\t')
        headers = next(reader)
        # Output data
        nodes = list()
        edges = list()
        # Validate headers
        for header in headers:
            if header not in _COLUMN_CONFIG:
                raise RuntimeError(f"Header {header} not found in _COLUMN_CONFIG")
        for idx, row in enumerate(reader):
            # Validate row length
            if len(row) != len(headers):
                raise RuntimeError(f"Row {idx} has length {len(row)}, should be {len(headers)}")
            # Iterate over columns
            for (col_idx, col) in enumerate(row):
                header = headers[col_idx]
                config = _COLUMN_CONFIG[header]
                col = col.strip().lower().replace(' ','_').replace('*', '').replace(',', '')
                if header in _CONVERT_LIST:
                    col = '%d' % (to_pow10(int(col)))
                if not config["node_category"] or _col_blank(col):
                    # Skip this column
                    continue
                if header+':'+col not in nodes_d:
                  nodes.append({
                    "id": config["prefix"] + ":" + col,
                    "name": col,
                    "category": config["node_category"],
                    "provided_by": 'GOLD'
                  })
                nodes_d[header+':'+col] = 1 
                # Create any edges to other columns
                if config.get("edges_out"):
                    for (col_name, edge_category) in config["edges_out"].items():
                        if col_name not in headers:
                            raise RuntimeError("Edge column '{col_name}' not in headers")
                        if not _COLUMN_CONFIG[col_name]:
                            raise RuntimeError("Edge column '{col_name}' has no config")
                        obj_config = _COLUMN_CONFIG[col_name]
                        obj_prefix = obj_config["prefix"]
                        obj_idx = headers.index(col_name)
                        obj_id = row[obj_idx].strip().lower().replace(' ', '_').replace('*', '').replace(',', '')
                        if _col_blank(obj_id):
                            continue
                        if col_name in _CONVERT_LIST:
                            obj_id = '%d' % (to_pow10(int(obj_id)))
                        if col+":"+obj_id not in edges_d:
                          edges.append({
                            "subject": config["prefix"] + ":" + col,
                            "object": obj_prefix + ":" + obj_id,
                            "edge_label": edge_category,
                            "relation": edge_category,
                            "provided_by": 'GOLD',
                          })
                        edges_d[col+":"+obj_id] = 1
  
    return (nodes, edges)


def _col_blank(col) -> bool:
    """Is the column value null, unknown, or empty?"""
    return not isinstance(col, str) or len(col.strip()) == 0 or "data not in IMG" in col


def write(nodes, edges, node_path, edge_path):
    """
    Write nodes and edges to TSV output files based on the _OUT_NODE_HEADERS
    and _OUT_EDGE_HEADERS.
    """
    with open(node_path, 'w', newline='') as fd:
        writer = csv.writer(fd, lineterminator='\n', delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(_OUT_NODE_HEADERS)
        for node in nodes:
            row = [node[h] for h in _OUT_NODE_HEADERS]
            writer.writerow(row)
    print(f"Wrote {node_path}")
    with open(edge_path, 'w', newline='') as fd:
        writer = csv.writer(fd, lineterminator='\n', delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(_OUT_EDGE_HEADERS)
        for edge in edges:
            row = [edge[h] for h in _OUT_EDGE_HEADERS]
            writer.writerow(row)
    print(f"Wrote {edge_path}")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: script <input> <node out> <edge out>")
        sys.exit(1)
    source_path = sys.argv[1]
    node_path = sys.argv[2]
    edge_path = sys.argv[3]

    (nodes, edges) = load(source_path)
    write(nodes, edges, node_path, edge_path)
