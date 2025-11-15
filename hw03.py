
def sortnodes_bychildren(R: int, adjacency_dict: dict, sorted_dict=None, visited=None) -> dict:
    """
    Given a root(parent) node label and a dictionary of form node: [adjacent_node0, adjacent_node1, ...]
     creates dict of form {node:str : tuple(child1, child2)}
    """
    # Root is needed, to know we are assigning parent -> children, not the other way around
    # print(neighbours_list)

    if sorted_dict is None:
        sorted_dict = {}
    if visited is None:
        visited = set()

    visited.add(R)
    children_list = [n for n in adjacency_dict[R] if n not in visited]
    sorted_dict[str(R)] = tuple(children_list)

    for child in children_list:
        sortnodes_bychildren(child, adjacency_dict, sorted_dict, visited)

    return sorted_dict


def locate_nodes_bintree():

    # 1) Handle inputs
    try:
        N, R, L = (int(n) for n in input().split())
    except ValueError:
        raise ValueError("Should be 3 integers separated by space.")
    if N not in range(2, 1+ 7 * 10 ** 5):
        raise ValueError("N should be in range of [1, 7*10^5].")
    if L not in range(1, 101) or L > N:
        raise ValueError("L should be in range [1, 100] and not exceed N: {N} in this case.")

    neighbours_list = [(int(n) for n in input().split()) for _ in range(N - 1)]

    try:
        inquired_list = [int(input()) for _ in range(L)]
    except ValueError:
        raise ValueError("Should be L lines ({L} in this case) of int node labels, positions of which you inquire.")

    # Debugging
    # print(N, R, L)
    # print(neighbours_list)
    # print(inquired_list)

    # 2) Sort nodes by children
    # Build the adjacency dict first for neighbours of each node
    adj = {}
    for nei1, nei2 in neighbours_list:
        if nei1 not in adj: adj[nei1] = []
        if nei2 not in adj: adj[nei2] = []
        adj[nei1].append(nei2)
        adj[nei2].append(nei1)

    # print(adj)
    # Sort into the aforementioned dictionary
    # nodechildren_dict = sortnodes_bychildren(R, adj, sorted_dict=None, visited=None)
    # print(nodechildren_dict)

    # 3) Do BFS or DFS to assign (x,y) for each node. (Also abuse the fact that left child is first)
    # IDEA: compute depth_i for node with label i
    #  The final result is of the form (depth_i, inorder_i or (depth_i, inorder_list[i])) for node with label i
    # Maybe:
    # def assigncoords(nodechildren_dict):
    #   coords_dict = {}
    #   coords_dict[root] = (0,0)
    #   for key in nodechildren_dict:
    #       leftchild = nodechildren_dict[key][0]
    #       rightchild = nodechildren_dict[key][1]
    #

    # Convert adj list into children list using DFS (respecting input order => left child first)
    children = [[] for _ in range(N)]
    parent = [-1] * N
    depth = [0] * N

    stack = [R]
    parent[R] = R
    order = []  # BFS or DFS, I use DFS
    while stack:
        node = stack.pop()
        order.append(node)
        for nei in adj[node]:
            if parent[nei] == -1:
                parent[nei] = node
                depth[nei] = depth[node] + 1
                children[node].append(nei)
                stack.append(nei)

    # Compute max depth for y-coordinate later
    max_depth = max(depth)

    # Inorder traversal to assign x-coordinates
    x = [-1] * N
    counter = 0
    stack = []
    node = R

    while stack or node != -1:
        if node != -1:
            stack.append(node)
            if children[node]:  # go to left if exists
                node = children[node][0]
            else:
                node = -1
        else:
            node = stack.pop()
            x[node] = counter
            counter += 1

            # go to right child if exists
            if len(children[node]) == 2:
                node = children[node][1]
            else:
                node = -1

    # y coordinate: higher depth → lower y
    # root should have the highest y = max_depth - depth(root) = max_depth
    y = [max_depth - d for d in depth]

    # print(x)
    # print(y)
    # Answer queries
    outpos = str()
    for node in inquired_list:
        q = int(node)
        if node != inquired_list[-1]:
            outpos += str(x[q]) + " " + str(y[q]) + "\n"
        else:
            outpos += str(x[q]) + " " + str(y[q])
        # print(x[q], y[q])
    # 4) Profit!

    # Dummy output
    # outpos = str()
    # outpos += "".join("0 0\n" for _ in range(L-1))
    # outpos += "".join("0 0")
    return outpos


if __name__ == "__main__":
    print(locate_nodes_bintree())

"""
E.g.

In:
6 1 4
3 4
3 0
4 5
1 3
2 4
5
2
1
4

Out:
0 0
2 0
5 3
1 1
"""