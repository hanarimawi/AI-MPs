import numpy as np


def isDank(col, constraint, sums):
    curr = [0,0]
    sol = []
    for i in range(len(col)):
        if col[i] == 0:
            if curr[0] > 0:
                sol.append(curr)
            curr = [0,0]
            continue
        if curr[1] == 0:
            curr[1] = col[i]
            curr[0] = 1
        else:
            curr[0]+=1
    if col[len(col)-1] != 0:
        sol.append(curr)
    if sol == constraint:
        return True
    else:
        return False

def getCols(constraints):
    vals = [0]
    colCons = constraints[1]
    rowCons = constraints[0]
    for c in rowCons+colCons:
        for l in c:
            if l[1] not in vals:
                vals.append(l[1])
    all = genCols(len(rowCons), vals)
    legitCols = []
    for i in range(len(colCons)):
        legitCols.append([])
        for col in all:
            sums = {}
            for v in vals:
                if v > 0:
                    sums[v] = 0
            for l in colCons[i]:
                sums[l[1]]+=l[0]
            if isDank(col, colCons[i], sums):
                legitCols[i].append(col)
    return legitCols

def genCols(l, d):
    if l == 1:
        return [[x] for x in d]
    else:
        sub = genCols(l-1, d)
        ret = [y + [x] for x in d for y in sub]
        return ret



def partial_row_checker(cols, constraints):
    """
    assume cols is 2d array and constraints is list([[1, 1], [1, 1], [1, 1]])
    return whether the columns are viable given the row constraints
    """
    space = 0
    num_cols = len(cols)
    row_pos = 0
    for row in constraints:
        quantity = 0
        val = 1 #change later for colors
        for constraint in row:
            quantity += constraint[0]
        quantity_count = 0
        for col_pos in range(num_cols):
            if len(cols[col_pos]) != 0:
                if cols[col_pos][row_pos] == val:
                    quantity_count += 1
        if quantity_count > quantity:
            return False
        row_pos += 1
    return True


cols = [[0, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 0, 1]]
constraints = [list([[4, 1]]),
         list([[1, 1], [1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]),
         list([[2, 1]]),
         list([[1, 1], [1, 1]])]

def checkAss(constraints, assignment):
    rowCons = constraints[0]
    #print(constraints, assignment)
    for i in range(len(assignment[0])):
        row = []
        for j in range(len(assignment)):
            row.append(assignment[j][i])
        sums = {}
        for l in rowCons[i]:
            if l[1] in sums.keys():
                sums[l[1]]+=l[0]
            else:
                sums[l[1]]=l[0]
        if not isDank(row,rowCons[i],sums):
            return False
    return True

constraints =  [[[1,1],[]],[[1,1],[]]]
arr = [[1,0],[0,0]]
print (checkAss(constraints, arr))


def getLcv(constraints, assignment, cols, coli):
    rowSums = []
    legitVals = []
    rowCons = constraints[0]
    for i in range(len(rowCons)):
        rowSums.append(0)
        for j in rowCons[i]:
            rowSums[i] += j[0]
    colSums = []
    for i in range(len(cols)):
        colSums.append(0)
        for j in range(len(cols[i])):
            if cols[i][j] == 1:
                colSums[i]+=rowSums[j]
    while True:
        if len(colSums) == 0:
            return legitVals
            print(legitVals)
        i = colSums.index(np.max(colSums))
        assignment[coli] = cols[i]
        if partial_row_checker(assignment, rowCons):
            legitVals.append(cols[i])
            colSums.pop(i)
            cols.pop(i)
        else:
            colSums.pop(i)
            cols.pop(i)



def backtracking(constraints, assignment, cols):
    if [] not in assignment:
        if checkAss(constraints, assignment):
            print(assignment)
            return assignment
    mcv = []
    for l in range(len(cols)):
        if assignment[l] == []:
            mcv.append(len(cols[l]))
        else:
            mcv.append(np.inf)
    i = mcv.index(np.min(mcv))
    x = getLcv(constraints.copy(), assignment.copy(), cols[i].copy(), i)
    if x == []:
        return None
    else:
        for val in x:
            assignment[i] = val
            b = backtracking(constraints.copy(), assignment.copy(), cols.copy())
            if b != None:
                return b
    return None

#send copy of cols to recursive
def solve(constraints):
    cols = getCols(constraints)
    colCons = constraints[1]
    rowCons = constraints[0]
    a= []
    for i in range(len(colCons)):
        a.append([])

    return backtracking(constraints, a, cols)



    """
    Implement me!!!!!!!
    This function takes in a set of constraints. The first dimension is the axis
    to which the constraints refer to. The second dimension is the list of constraints
    for some axis index pair. The third demsion is a single constraint of the form
    [i,j] which means a run of i js. For example, [4,1] would correspond to a block
    [1,1,1,1].

    The return value of this function should be a numpy array that satisfies all
    of the constraints.


    A puzzle will have the constraints of the following format:


    array([
        [list([[4, 1]]),
         list([[1, 1], [1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]),
         list([[2, 1]]),
         list([[1, 1], [1, 1]])],
        [list([[2, 1]]),
         list([[1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]),
         list([[1, 1], [1, 1]]),
         list([[5, 1]])]
        ], dtype=object)

    And a corresponding solution may be:

    array([[0, 1, 1, 1, 1],
           [1, 0, 1, 0, 1],
           [1, 1, 1, 0, 1],
           [0, 0, 0, 1, 1],
           [0, 0, 1, 0, 1]])



    Consider a more complicated set of constraints for a colored nonogram.

    array([
       [list([[1, 1], [1, 4], [1, 2], [1, 1], [1, 2], [1, 1]]),
        list([[1, 3], [1, 4], [1, 3]]),
        list([[1, 2]]),
        list([[1, 4], [1, 1]]),
        list([[2, 2], [2, 1], [1, 3]]),
        list([[1, 2], [1, 3], [1, 2]]),
        list([[2, 1]])],
       [list([[1, 3], [1, 4], [1, 2]]),
        list([[1, 1], [1, 4], [1, 2], [1, 2], [1, 1]]),
        list([[1, 4], [1, 1], [1, 2], [1, 1]]),
        list([[1, 2], [1, 1]]),
        list([[1, 1], [2, 3]]),
        list([[1, 2], [1, 3]]),
        list([[1, 1], [1, 1], [1, 2]])]],
        dtype=object)

    And a corresponding solution may be:

    array([
           [0, 1, 4, 2, 1, 2, 1],
           [3, 4, 0, 0, 0, 3, 0],
           [0, 2, 0, 0, 0, 0, 0],
           [4, 0, 0, 0, 0, 0, 1],
           [2, 2, 1, 1, 3, 0, 0],
           [0, 0, 2, 0, 3, 0, 2],
           [0, 1, 1, 0, 0, 0, 0]
         ])


    """
    dim0 = len(constraints[0])
    dim1 = len(constraints[1])
    return np.random.randint(2, size=(dim0, dim1))
