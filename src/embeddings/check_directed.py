import pandas as pd


edges = pd.read_csv("./IMGVR_extra_KGX_edges.tsv", sep="\t")
dims = edges.shape
print(dims)

output = []
for i in range(0, dims[0]):
    subj1 = edges.iloc[i, 0]#df['subject']
    obj1 = edges.iloc[i, 2]# df['object']\

    if( i %1000 == 0):
        print(i)

    for j in range(i+1, dims[0]):
         if(subj1 == edges.iloc[j, 2] and obj1 == edges.iloc[j, 0]):
             output.append(subj1 + "\t" + obj1)
             output.append("undirected "+str(i)+"\t"+str(j))
             print(subj1 + "\t" + obj1)
             print("undirected "+str(i)+"\t"+str(j))

outfile = "check_directed_extra.txt"
with open(outfile, "w") as outfile:
    outfile.write("\n".join(output))
