"""
Overview:
Solves a binary graph problem aimed towards finding the min and max dangling path values, given the binary
tree graph.

Inputs(2 + M lines):
    N:int (number of nodes in a tree with labels in range [0,N-1])  R:int (label of the root)
    key_labl0:int key_labl1:int ... key_labl_last:int (N keys(values) of nodes listed in ascending order wrt node labels.
                    iow in label:key dict these values -> label_key{"0":3, "1":0} would have an input structure: 3 0
    M lines of form(for connected nodes ["neighbour_label0":1] - ["neighbour_label1":2] - ["neighbour_label2":5]:
        neighbour_label0 neighbour_label1
        neighbour_label1 neighbour_label2
        NOTE: Each pair is only mentioned once!
              Order is arbitrary.
Output(1 line):
    2 ints, separated by space:
    min_dangpath_cost max_dangpath_cost

Limitations:
    1 <= N <= 10^6
    0 <= any_key_val <= 10^3
"""

# TODO's:
"""
    1) Node class fully with all necessary methods
    2) Failsafe cases
    3) Think of a solution method
        - Identify binary tree graph structure
        - Find method to identify a dangling path
        - Use recursion(go deep, then return from the bottom iteratively)
"""

def sortnodes_bychildren(R: int, neighbours_list: list, sorted_dict=None) -> dict:
    """
    Given a root(parent) node label and a list of tuples with 2 neighbouring node labels,
     creates dict of form {node:str : tuple(child1, child2)}
    """
    # Root is needed, to know we are assigning parent -> children, not the other way around

    if sorted_dict is None:
        sorted_dict = {}

    children = 0
    children_list = []
    # Iterating over a copy, removal works unpredictably otherwise
    for pair in neighbours_list[:]:
        if R in pair:
            neighbours_list.remove(pair)
            children += 1
            child = pair[1] if pair[0] == R else pair[0]
            children_list.append(child)
        if children == 2: break

    sorted_dict[str(R)] = tuple(children_list)
    for c in children_list:
        sortnodes_bychildren(c, neighbours_list, sorted_dict)

    return sorted_dict

def is_regular(children: tuple) -> bool:
    if len(children) == 1: return False
    return True

def binary_recursion(node:int, nodes_dict:dict, nodechildren_dict:dict,
                     optmin_dangscore=float('inf'), optmax_dangscore=float('-inf')) -> tuple:
    """
    Given dictonary of label:key type and dictionary of parent:children type, find min and max cost from all dangling paths
    """
    key = nodes_dict[str(node)]
    children = nodechildren_dict[str(node)]

    if not children:  # leaf node
        return optmin_dangscore, optmax_dangscore, key  # inf, -inf, 16


    if not is_regular(children):    # stop path here
        optmin_dangscore, optmax_dangscore, child_sum = binary_recursion(children[0], nodes_dict, nodechildren_dict, optmin_dangscore, optmax_dangscore)

        # So that dangling path doesn't end in a regular node
        if child_sum is None:
            return optmin_dangscore, optmax_dangscore, None

        total = key + child_sum  # 15+16=31
        return optmin_dangscore, optmax_dangscore, total   # inf, -inf, 31

    # Regular node: stop dangling paths here, update min/max from children
    # Traverse children, get dangling sums
    for child in children:
        optmin_dangscore, optmax_dangscore, child_sum = binary_recursion(child, nodes_dict, nodechildren_dict, optmin_dangscore, optmax_dangscore)
        if child_sum is not None:  # only update for valid dangling paths
            optmin_dangscore = min(optmin_dangscore, child_sum)
            optmax_dangscore = max(optmax_dangscore, child_sum)
        # dangling path ends here in the Regular node; update min/max

        # Debugging
        #print(f"For regular nodes we got: {optmin_dangscore} and {optmax_dangscore}")
        #print(f"Child sum is {child_sum} for {child}")

    # None, so we don't propagate anything up from a regular node
    return optmin_dangscore, optmax_dangscore, None



def minmaxcost_dangpath():

    # 1) Read input, init variables
    try:
        N, R = map(int, input().split())
    except ValueError:
        raise ValueError(f"Invalid form of first input line. Should be two integers separated by space.")
    if N not in range(1, 10**6+10**5):
        raise ValueError(f"Invalid N size. Expected within [1, 10^6] range, got {N}.")

    # TODO: Instead of dictionary use nodes class
    # Nodes dict in form "label":key
    try:
        line2 = list(map(int, input().split()))
        nodes_dict = {f"{i}": line2[i] for i in range(N)}
    except ValueError:
        raise ValueError(f"Invalid form of second input line. Values should be integers separated by space.")
    if not len(line2) == N:
        raise ValueError(f"Invalid form of second input line. Should be N({N}) integer(s) separated by space.")

    # M inputs stored into a list of tuples, each with a pair of neighbours:
    # TODO: Think whether to leave int and use str() everywhere OR use str here and ignore failsafe
    try:
        neighbours_list = [tuple(map(int, input().split())) for _ in range(N-1)]
    except ValueError:
        raise ValueError(f"Invalid form of third input.\nShould be M lines, each with a pair of integers separated by space.")

    print(f"{N} and {R}")
    print(nodes_dict)
    print(neighbours_list)

    # 2) What the hecc do I do now?
    # IDEA: Look through tuples in neighbours_list, find the same nodes in nodes_dict and pop value from neighbours_list
    # for tuple in neighbours_list: if R in tuple, then we just found the root! That means values next to the root are left/right
    # which one if left and which one is right is unclear for now

    nodechildren_dict = sortnodes_bychildren(R, neighbours_list)

    print(nodechildren_dict)


    # Dict -> node_labl: (child_labl1, child_labl2) or (child_labl)
    # {"7": (6, 8), "6":(2), "2":(1,3), ..., "8":(15), ..., }
    # BETTER IDEA: Go deep, until leaf. If self.is_leaf(): return key of this leaf and go up by recursion.
    # Return sum of all keys(values) from leaf up, and if not node.is_Regular() stop summing and add final result to some list.
    # E.G.:
    # 1) going down: 7 -> 6 -> 2 -> 1 -> 0
    # 2) 0 is leaf, so we get its value of 16
    # 3) We start going up now: 0 -> 1 ...
    # 4) We check if 1 is not regular(has only 1 child). It does, so we accumulate: 16+15=31
    # 5) We go up: 1 -> 2. We check if 2 is not regular. It is regular, so we stop accumulating here and just add the
    #       value either to list all_danglpath_costs OR just
    #       min(optmin_dangscore, value) AND max(value, optmax_dangscore),
    #       which at the start should be set to optmin_dangscore = float('inf') and optmax_dangscore = float('-inf')
    # 6)

    mindangcost, maxdangcost, f = binary_recursion(R, nodes_dict, nodechildren_dict)
    return mindangcost, maxdangcost

if __name__ == '__main__':
    print(minmaxcost_dangpath())


'''
E.g.:

In:
20 9
5 4 6 9 3 1 2 8 7 9 9 9 9 9 9 9 9 9 9 9
0 1
2 0
3 2
3 7
7 4
4 6
6 5
7 8
9 3
9 10
10 13
12 11
13 12
13 14
14 19
16 15
16 17
18 16
19 18

Out:
6 18
'''