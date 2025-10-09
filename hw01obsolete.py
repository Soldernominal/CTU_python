"""
Code for splitting a square tile input of different tiles with qualities into 4 squares with 1 horizontal line and 2 vertical ones, 
s.t. there is minimal difference between the smallest sum of qualities of 1/4 part of the square and the largest. 
Input:
    N - Number of rows and columns NxN
    NxN orchard - square grid of tiles as their qualities
Output:
    n(int) - Minimum possible difference between lowest sum(q) and highest sum(q)
"""

def read_pubdata(path_to_file: str) -> tuple[int, list]:
    """
    Reads data from file

    Input:
        Full path to the file (/home/.../pub)
    Output:
        N, orchard(same as input for the task)
    """
    with open(path_to_file) as f:
        tokens = f.read().strip().split()

    clean = [t for t in tokens if t != '-']  # remove bad standalone dashes
    N = int(clean[0])
    values = list(map(int, clean[1:]))
    orchard = [values[i*N:(i+1)*N] for i in range(N)]

    return N, orchard


def prefix_sum(N: int, list_to_prefixsum: list) -> list:
    """
    Creates prefix sum lists from the NxN list of qualities given

    Input:
        N(int) - size of the orchard
        list_to_prefixsum(list) - self-explanatory
    Output:
        prefixsum_list(list) - resulting list of the nesting sum of qualities
        prefixsumbyrow_list(list) - resulting list of the nesting sum of qualities, but only accumulated each row
    """

    # .copy() doesn't work, lists are NOT immutable
    prefixsum_list = list()
    prefixsumbyrow_list = list()

    for i in range(N):
        prefixsum_list.append([])
        prefixsumbyrow_list.append([])
        for j in range(N):
            if j-1 >= 0:
                prefixsum_list[i].append(list_to_prefixsum[i][j] + prefixsum_list[i][j-1])
                prefixsumbyrow_list[i].append(list_to_prefixsum[i][j] + prefixsumbyrow_list[i][j-1])
            elif i-1 >= 0:
                prefixsum_list[i].append(list_to_prefixsum[i][j] + prefixsum_list[i-1][-1]) 
                prefixsumbyrow_list[i].append(list_to_prefixsum[i][j]) 
            else:
                prefixsum_list[i].append(list_to_prefixsum[0][0])    
                prefixsumbyrow_list[i].append(list_to_prefixsum[0][0])    

    return prefixsum_list, prefixsumbyrow_list


def orchard_div():
    """
    Get the smallest quality difference between 4 resulting orchard parts

    Input:
        User input(None to function)
    Output:
        n(int) - Minimum possible difference between lowest sum(q) and highest sum(q)
    """


    # 1) Get inputs
    N = int(input())
    orchard = [list(map(int, input().split())) for _ in range(N)]

    # Or pull from public data
    #N, orchard = read_pubdata("/home/user/Documents/ALG/hw01/datapub/pub04.in")

    # Failsafe cases
    if N <= 0 or N > 3025: raise ValueError("N(size of orchard) has an invalid size")
    if N == 1: return orchard[0][0]


    # 2) Make prefixsum list for easier computation and memory efficiency(One full prefix sum and One by rows)
    prefsum_list, prefixsumbyrow_list = prefix_sum(N, orchard)


    # 3) Fix horizontal line(divide N and S)
    min_NSquality = float('inf')
    hi = 0              # Where to cut horizontally, a.k.a last row of North part
    for i in range(N-1):
        qN = prefsum_list[i][-1]
        qS = prefsum_list[N-1][-1] - prefsum_list[i][-1]
        NSdiff = abs(qN - qS)
        if NSdiff < min_NSquality: 
            min_NSquality = NSdiff
            #min_qN = qN
            min_qS = qS
            hi = i
    
    # Debugging: Shows the horizontal line(numbers don't look ordered visually though)
    '''
    row = str()
    for i in range(N):
        for j in range(N):
            if j == N-1:  
                row += str(orchard[i][j])
            else:
                row += str(orchard[i][j]) + " "
        print(row)
        row = str()
        if i == hi: print("---" * N)
    '''


    # 4) Fix vertical lines

    # North split
    min_NEWquality = float('inf')
    vNj = 0              # Where to cut vertically, a.k.a. last column of North-West part
    for j in range(N-1):
        qNW, qNE = 0, 0
        for i in range(hi+1):
            qNW += prefixsumbyrow_list[i][j]
            qNE += prefixsumbyrow_list[i][-1] - prefixsumbyrow_list[i][j]
        NEWdiff = max(abs(qNW - qNE), abs(min_qS - qNE), abs(min_qS - qNW))
        if NEWdiff < min_NEWquality: 
            min_NEWquality = NEWdiff
            min_qNE = qNE
            min_qNW = qNW
            vNj = j   


    # Debugging: Shows the horizontal line(numbers don't look ordered visually though) AND vertical line of North part
    '''
    row = str()
    for i in range(N):
        for j in range(N):
            if j == N-1:  
                row += str(orchard[i][j])
            else:
                row += str(orchard[i][j]) + " "
            if j == vNj and i <= hi: row += "| "
        print(row)
        row = str()
        if i == hi: print("---" * N)
    '''
    

    # East split
    min_SNEWquality = float('inf')
    vSj = 0              # Where to cut vertically, a.k.a. last column of South-West part
    for j in range(N-1):
        qSW, qSE = 0, 0
        for i in range(hi+1, N):
            qSW += prefixsumbyrow_list[i][j]
            qSE += prefixsumbyrow_list[i][-1] - prefixsumbyrow_list[i][j]
        SNEWdiff = max(abs(min_qNW - min_qNE), abs(qSE - qSW), abs(qSE - min_qNW), abs(qSE - min_qNE), abs(qSW - min_qNW), abs(qSW - min_qNE))
        if SNEWdiff < min_SNEWquality: 
            min_SNEWquality = SNEWdiff
            #min_qSE = qSE
            #min_qSW = qSW
            vSj = j  

    # Debugging: Shows the horizontal line(numbers don't look ordered visually though) AND vertical line of both North and South parts
    '''    
    row = str()
    for i in range(N):
        for j in range(N):
            if j == N-1:  
                row += str(orchard[i][j])
            else:
                row += str(orchard[i][j]) + " "
            if (j == vNj and i <= hi) or (j == vSj and i > hi): row += "| "
        print(row)
        row = str()
        if i == hi: print("---" * N)
    '''

    return min_SNEWquality



if __name__ == "__main__":
    #orchard_div()
    print(orchard_div())


'''
Example input:

5
 3   0   2  -8  -8
 5   3   2   2   3
 2   5   2   1   4
 3   4  -1   4   2
-3   6   2   4   3

Output:
5
'''