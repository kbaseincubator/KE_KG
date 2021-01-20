"""
Convert data from `Torben_IMG-data_linked_to-GOLD_v2.tsv` into a set of Biolink
formatted node and edge TSV files.

Every column is parsed into a node/vertex.
There is an edge from the first column (the Torben ID) to (most) every other
column. For now, there are no other edges between columns.
"""
# import math
# import numpy as np
import csv
import sys
import os

# Configuration for every header from the source file.
# - "edges_out" is a mapping from other column names to edge categories
# - "prefix" is the biolink prefix (ie. namespace) for the value of each column
# - "node_category" is the biolink node category/class for each column/vertex. If
#   this is None, then we skip creation of a node for this column.
_COLUMN_CONFIG = {
    "Torbens_MetaG_Dir_Name": {
        "edges_out": {
            "taxon_oid": "biolink:has_taxonomic_rank",
            "Domain": "biolink:has_attribute",
            "Sequencing_Status": "biolink:has_attribute",
            "Study_Name": "biolink:has_attribute",
            "Genome_Name_/_Sample_Name": "biolink:has_attribute",
            "Sequencing_Center": "biolink:has_attribute",
            "Geographic_Location": "biolink:located_in",
            "GOLD_Ecosystem": "biolink:located_in",
            "GOLD_Ecosystem_Category": "biolink:located_in",
            "GOLD_Ecosystem_Subtype": "biolink:located_in",
            "GOLD_Ecosystem_Type": "biolink:located_in",
            "GOLD_Sequencing_Quality": "biolink:has_attribute",
            "GOLD_Sequencing_Status": "biolink:has_attribute",
            "GOLD_Sequencing_Strategy": "biolink:has_attribute",
            "GOLD_Specific_Ecosystem": "biolink:located_in",
            "Habitat": "biolink:located_in",
            "Latitude": "biolink:located_in",
            "Longitude": "biolink:located_in",
            "Genome_Size_assembled": "biolink:has_quantitative_value",
            "Gene_Count_assembled": "biolink:has_quantitative_value",
        },
        "prefix": "IMG",
        "node_category": "biolink:NamedThing",
    },
    "taxon_oid": {
        "prefix": "IMG",
        "node_category": "biolink:OrganismTaxon",
    },
    "Domain": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "Sequencing_Status": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "Study_Name": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "Genome_Name_/_Sample_Name": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "Sequencing_Center": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
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
        "node_category": "biolink:NamedThing",
    },
    "GOLD_Sequencing_Quality": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
    },
    "GOLD_Sequencing_Status": {
        "prefix": "GOLD",
        "node_category": "biolink:NamedThing",
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
        "prefix": "Habitat",
        "node_category": "biolink:NamedThing",
    },
    "Latitude": {
        "prefix": "Latitude",
        "node_category": "biolink:NamedThing",
    },
    "Longitude": {
        "prefix": "Longitude",
        "node_category": "biolink:NamedThing",
    },
    "Genome_Size_assembled": {
        "prefix": "Assembly_size",
        "node_category": "biolink:NamedThing",
    },
    "Gene_Count_assembled": {
        "prefix": "Gene_count",
        "node_category": "biolink:NamedThing",
    },
}

# Output headers for the edge data
_OUT_EDGE_HEADERS = [
    "subject",
    "edge_label",
    "object",
    "relation",
]
# Output headers for the node data
_OUT_NODE_HEADERS = [
    "id",
    "name",
    "category",
]


def load(source_path):
    with open(source_path) as fd:
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
                col = col.strip()
                if not config["node_category"] or _col_blank(col):
                    # Skip this column
                    continue
                nodes.append({
                    "id": config["prefix"] + ":" + col,
                    "name": col,
                    "category": config["node_category"],
                })
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
                        obj_id = row[obj_idx].strip()
                        if _col_blank(obj_id):
                            continue
                        edges.append({
                            "subject": config["prefix"] + ":" + col,
                            "object": obj_prefix + ":" + obj_id,
                            "edge_label": edge_category,
                            "relation": edge_category,
                        })
    return (nodes, edges)


def _col_blank(col) -> bool:
    """Is the column value null, unknown, or empty?"""
    return not isinstance(col, str) or len(col.strip()) == 0 or "data not in IMG" in col


def write(nodes, edges, source_path):
    """
    Write nodes and edges to TSV output files based on the _OUT_NODE_HEADERS
    and _OUT_EDGE_HEADERS.
    """
    basename = os.path.splitext(os.path.basename(source_path))[0]
    node_path = basename + '.biolink-nodes.tsv'
    edge_path = basename + '.biolink-edges.tsv'
    with open(basename + '.nodes.tsv', 'w', newline='') as fd:
        writer = csv.writer(fd, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for node in nodes:
            row = [node[h] for h in _OUT_NODE_HEADERS]
            writer.writerow(row)
    print(f"Wrote {node_path}")
    with open(basename + '.edges.tsv', 'w', newline='') as fd:
        writer = csv.writer(fd, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for edge in edges:
            row = [edge[h] for h in _OUT_EDGE_HEADERS]
            writer.writerow(row)
    print(f"Wrote {edge_path}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.stderr.write("Pass in the source file path as the first argument\n")
        sys.exit(1)
    source_path = sys.argv[1]
    (nodes, edges) = load(source_path)
    write(nodes, edges, source_path)
