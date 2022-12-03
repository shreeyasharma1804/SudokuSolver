from typing import List


def solveSudoku(board: List[List[int]]) -> List[List[int]]:

    # board = [[int(val) if val.isdigit() else 0 for val in row]
    #          for row in board]

    def is_valid(i, j, val):
        if val in board[i]:
            return False
        if val in [board[r][j] for r in range(9)]:
            return False
        grp_r, grp_c = i//3, j//3
        for r in range(3):
            for c in range(3):
                if board[grp_r*3 + r][grp_c*3 + c] == val:
                    return False
        return True

    def backtrack(pos=0):
        if pos == len(need):
            return True
        i, j = need[pos]
        for num in range(1, 10):
            if is_valid(i, j, num):
                board[i][j] = num
                if backtrack(pos+1):
                    return True
        board[i][j] = 0

    need = [(i, j) for i in range(9) for j in range(9) if not board[i][j]]
    backtrack()
    return board
