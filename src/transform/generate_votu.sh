#!/bin/sh


cut -f1|grep vOTU|sort|uniq|sed 's/vOTU://'|awk '{print "vOTU:"$1"	"$1"	kbase:otu	GOLD"}'

