import numpy as np
'''
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
'''

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

    '''colSums = {}
    for key in sums.keys():
        colSums[key] = 0
    for val in col:
        if val in colSums.keys():
            colSums[val]+=1
    print (sums)
    print (colSums)
    for val in sums:
        if sums[val]!=colSums[val]:
            return False
    print(36)
    needzero = False
    for i in range(len(col)):
        if col[i] == 0:
            needzero = False
            continue
        if col[i] == constraint[0][1] and not needzero:
            constraint[0][0]-=1
            if constraint[0][0]==0:
                constraint.pop(0)
        else:
            return False
    if len(constraint) == 0:
        print (sums)
        print (colSums)
        print (col)
        print(constraint)
        return True
    else:
        return False
    '''
def getCols(constraints):
    vals = [0]
    colCons = constraints[1]
    rowCons = constraints[0]
    for c in rowCons+colCons:
        for l in c:
            if l[1] not in vals:
                vals.append(l[1])
    print(len(colCons), len(rowCons))
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
    print(constraints)
    return legitCols
def genCols(l, d):
    if l == 1:
        return [[x] for x in d]
    else:
        sub = genCols(l-1, d)
        ret = [y + [x] for x in d for y in sub]
        return ret


def solve(constraints):
    cons = getCols(constraints)
    for i in cons:
        print(i)
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
