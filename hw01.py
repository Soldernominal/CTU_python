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
    orchard = [values[i * N:(i + 1) * N] for i in range(N)]

    return N, orchard


def prefix_sum(N: int, list_to_prefixsum: list) -> list:
    """
    Creates 2D prefix sum lists from the NxN list of qualities given

    Input:
        N(int) - size of the orchard
        list_to_prefixsum(list) - self-explanatory
    Output:
        prefixsum2D_list(list) - resulting list of the nesting^2 sum of qualities
    """

    # .copy() doesn't work, lists are NOT immutable
    prefixsum2D_list = list()

    for i in range(N):
        prefixsum2D_list.append([])
        for j in range(N):
            if (j - 1 >= 0) and (i - 1 >= 0):   # Case for inner tiles(for non-corners)
                prefixsum2D_list[i].append(prefixsum2D_list[i-1][j]
                                          + prefixsum2D_list[i][j-1]
                                          + list_to_prefixsum[i][j]
                                          - prefixsum2D_list[i-1][j-1])
            elif (i - 1 < 0) and (j - 1 < 0):   # First element, a.k.a. list[0][0]
                prefixsum2D_list[i].append(list_to_prefixsum[i][j])
            else:
                if i - 1 < 0:  # No row above
                    prefixsum2D_list[i].append(prefixsum2D_list[i][j-1]
                                              + list_to_prefixsum[i][j])
                if j - 1 < 0:  # No column to the left
                    prefixsum2D_list[i].append(prefixsum2D_list[i-1][j]
                                              + list_to_prefixsum[i][j])

    return prefixsum2D_list


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
    # N, orchard = read_pubdata("/home/user/Documents/ALG/hw01/datapub/pub04.in")

    # Failsafe cases
    if N <= 0 or N > 3025: raise ValueError("N(size of orchard) has an invalid size")
    if N == 1: return orchard[0][0]

    # 2) Make prefixsum list for easier computation and memory efficiency(One full prefix sum and One by rows)
    prefixsum2D_list = prefix_sum(N, orchard)

    # Debugging: Show prefixsum rows
    #for row in prefixsum2D_list: print(row)

    # 3) Iterate and find optimal SNEW(South-West, South-East, North-West, North-East) difference a.k.a. smallest cost
    optNEW_qdiff, optSEW_qdiff, optSNEW_qdiff = float('inf'), float('inf'), float('inf')
    # N-1, so it won't reach last row/column
    for i in range(N-1):
        for j in range(N-1):
            # We find optimal pair of NW and NE...
            NW = prefixsum2D_list[i][j]
            NE = prefixsum2D_list[i][-1] - prefixsum2D_list[i][j]
            if abs(NW - NE) < optNEW_qdiff:
                optNW = NW
                optNE = NE
                optNEW_qdiff = abs(NW - NE)

            # ...and meanwhile, also find the optimal pair of SW and SE
            SW = prefixsum2D_list[-1][j] - prefixsum2D_list[i][j]
            SE = (prefixsum2D_list[-1][-1]
                  - prefixsum2D_list[-1][j]
                  - prefixsum2D_list[i][-1]
                  + prefixsum2D_list[i][j])
            if abs(SW - SE) < optSEW_qdiff:
                optSW = SW
                optSE = SE
                optSEW_qdiff = abs(SW - SE)

        # Find overall maximum quality difference between 4 optimal quadrants for a given row
        SNEW_qdiff = max(abs(optSW - optSE), abs(optSW - optNW), abs(optSW - optNW),
                         abs(optNW - optNE), abs(optNW - optSE),
                         abs(optSE - optNE))

        # Update optimal value if it is smaller
        optSNEW_qdiff = min(SNEW_qdiff, optSNEW_qdiff)

        # Set optimal back to infinity for next row
        optNEW_qdiff, optSEW_qdiff = float('inf'), float('inf')



    return optSNEW_qdiff


if __name__ == "__main__":
    # orchard_div()
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