#!/bin/sh

echo "subject	edge_label	object	relation	provided_by"

grep -v ^\# | \
   awk '{print $1"	biolink:has_function	"$2"	biolink:has_function	eggnog"}'

