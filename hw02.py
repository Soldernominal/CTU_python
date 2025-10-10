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

    print(nodes_dict)
    print(neighbours_list)

    # 2) What the hecc do I do now?
    # IDEA: Look through tuples in neighbours_list, find the same nodes in nodes_dict and pop value from neighbours_list
    # for tuple in neighbours_list: if R in tuple, then we just found the root! That means values next to the root are left/right
    # which one if left and which one is right is unclear for now

    return 0

if __name__ == '__main__':
    print(minmaxcost_dangpath())