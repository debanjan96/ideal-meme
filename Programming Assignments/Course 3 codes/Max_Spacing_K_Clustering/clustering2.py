# Max spacing k-clustering

# In this question your task is again to run the clustering algorithm from lecture, but on a 
# MUCH bigger graph. So big, in fact, that the distances (i.e., edge costs) are only defined 
# implicitly, rather than being provided as an explicit list.
#
# The format is:
#
# [# of nodes] [# of bits for each node's label]
# [first bit of node 1] ... [last bit of node 1]
# [first bit of node 2] ... [last bit of node 2]
#
# For example, the third line of the file "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1" 
# denotes the 24 bits associated with node #2.
#
# The distance between two nodes u and v in this problem is defined as the Hamming distance--- 
# the number of differing bits --- between the two nodes' labels. For example, the Hamming 
# distance between the 24-bit label of node #2 above and the label 
# "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3 (since they differ in the 3rd, 7th, and 21st bits).
#
# The question is: what is the largest value of k such that there is a k-clustering with spacing 
# at least 3? That is, how many clusters are needed to ensure that no pair of nodes with all but 
# 2 bits in common get split into different clusters?
#
# NOTE: The graph implicitly defined by the data file is so big that you probably can't write it 
# out explicitly, let alone sort the edges by cost. So you will have to be a little creative to 
# complete this part of the question. For example, is there some way you can identify the smallest 
# distances without explicitly looking at every pair of nodes?

# load contents of text file into a list numList
NUMLIST_FILENAME = "data/clustering_big.txt" 

inFile = open(NUMLIST_FILENAME, 'r')

bits = []
graph = []
far_nodes = {}
merged_nodes = {} 
clusters_merged = 0
num_nodes = 0
num_bits = 0
node = 1
spacing = 3

for f in inFile:
    if(num_nodes == 0):
        num_nodes, num_bits = map(int, f.split())
    else:
        distance = str(f.strip())
        distance = "".join(distance.split())
        bits.append([node, distance])
        node += 1

num_clusters = num_nodes

def hammingDist(s1, s2, spacing):
    """Calculate the hamming distance between two bit strings"""
    distance = 0
    for c1, c2 in zip(s1, s2):
        if distance >= spacing:
            distance = spacing + 1
            break
        if c1 != c2:
            distance += 1

    return distance

print 'initial num_nodes: ' + str(num_nodes)
    
for n in bits:
    for i in range(n[0], num_nodes):
        same_cluster = False
        if n[0] in merged_nodes and i+1 in merged_nodes:
            if merged_nodes[n[0]] == merged_nodes[i+1]:
                continue
            
        distance = hammingDist(n[1], bits[i][1], spacing)

        if distance < spacing:
            graph.append([n[0], i+1, distance])


# sorting graph by increasing order of edge cost
graph = sorted(graph, key=lambda x: x[2])

index = 0

while len(graph) > 0 and graph[0][2] < spacing:
    merged = False

    # merge of single node to a clusters
    if graph[index][0] not in merged_nodes:
        if graph[index][1] not in merged_nodes:
            clusters_merged += 1
            cluster = clusters_merged
        else:
            cluster = merged_nodes[graph[index][1]]
        merged_nodes[graph[index][0]] = cluster 
        merged = True

    # merge of single node to a clusters
    if graph[index][1] not in merged_nodes:
        if graph[index][0] not in merged_nodes:
            if not merged:
                clusters_merged += 1
            cluster = clusters_merged
        else:
            cluster = merged_nodes[graph[index][0]]
        merged_nodes[graph[index][1]] = cluster 
        merged = True

    nodes_in_merged_nodes = graph[index][0] in merged_nodes and graph[index][1] in merged_nodes

    # inner merge of clusters with multiple nodes
    if nodes_in_merged_nodes and merged_nodes[graph[index][0]] != merged_nodes[graph[index][1]]:
        min_cluster = min(merged_nodes[graph[index][0]], merged_nodes[graph[index][1]])
        max_cluster = max(merged_nodes[graph[index][0]], merged_nodes[graph[index][1]])
        for key in merged_nodes:
            if merged_nodes[key] == max_cluster:
                merged_nodes[key] = min_cluster
                merged = True

    # removing the edge
    del graph[index]

    if merged:
        idx = 0
        while len(graph) > idx:
            nodes_in_merged_nodes = graph[idx][0] in merged_nodes and graph[idx][1] in merged_nodes
            if nodes_in_merged_nodes and merged_nodes[graph[idx][0]] == merged_nodes[graph[idx][1]]:
                # removing inner cluster edges
                del graph[idx]
            else:
                idx += 1
        num_clusters -= 1

print 'result: ' + str(num_clusters)
