#
# 

# Max spacing k-clustering

# This file describes a distance function (equivalently, a complete graph with edge costs). 
# It has the following format:
#
# [number_of_nodes]
# [edge_1_node_1] [edge_1_node_2] [edge_1_cost]
# [edge_2_node_1] [edge_2_node_2] [edge_2_cost]
#
# There is one edge (i,j) for each choice of 1≤i<j≤n, where n is the number of nodes.

# For example, the third line of the file is "1 3 5250", indicating that the distance between 
# nodes 1 and 3 (equivalently, the cost of the edge (1,3)) is 5250. You can assume that distances 
# are positive, but you should NOT assume that they are distinct.

# Your task in this problem is to run the clustering algorithm from lecture on this data set, 
# where the target number k of clusters is set to 4. What is the maximum spacing of a 4-clustering?

# load contents of text file into a list numList
NUMLIST_FILENAME = "data/clustering1.txt" 

inFile = open(NUMLIST_FILENAME, 'r')

graph = []
merged_nodes = {} 
clusters_merged = 0
num_clusters = 0
k = 4

for f in inFile:
    if(num_clusters == 0):
        num_clusters = int(f.strip())
    else:
        node1, node2, edge_cost = map(int, f.split())
        graph.append([node1, node2, edge_cost])

# sorting graph by increasing order of edge cost
graph = sorted(graph, key=lambda x: x[2])

index = 0

while num_clusters > k:
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

# result is the distance of the smallest edge after removing all redundant inner cluster edges and merging
# all clusters until reaching k number of clusters
print 'result: ' + str(graph[0][2])

