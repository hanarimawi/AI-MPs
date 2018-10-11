import numpy as np
from copy import deepcopy

def solve(constraints):
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


"""
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
"""
def is_consecutive(col, quantity):
	space = 0
	quantity_count = 0
	pos = 0
	while pos < len(col) and col[pos] == space:
		pos += 1
	while pos < len(col) and col[pos] != space:
		quantity_count += 1
		pos += 1
	if quantity_count != quantity:
		return False
	return True

def row_checker(cols, constraints):
	"""
	assume cols is 2d array and constraints is list([[1, 1], [1, 1], [1, 1]])
	return whether the columns are viable given the row constraints
	NEEDS CONSECUTIVE CHEKKECEKKEKKCKEKCECCECKC
	"""
	constraints = deepcopy(constraints)
	space = 0
	num_cols = len(cols)
	row_pos = 0
	for row in constraints:
		if len(row) == 1:
			constraint = row[0]
			quantity = constraint[0]
			val = constraint[1]
			quantity_count = 0
			for col_pos in range(num_cols):
				if cols[row_pos][col_pos] == val:
					quantity_count += 1
				if quantity_count > quantity:
					return False
			if quantity_count != quantity or not is_consecutive([ cols[row_pos][y] for y in range(num_cols) ], quantity):
				return False 
		else:
			for constraint in row:
				space_checked = False
				quantity = constraint[0]
				val = constraint[1]
				quantity_count = 0
				for col_pos in range(num_cols):
					if cols[row_pos][col_pos] == val:
						quantity_count += 1
					if quantity_count > quantity:
						return False
					#if we haven't checked for the space in between yet and we've reached the end of the block
					if not space_checked and quantity == quantity_count:
						space_checked = True
						#check if the next col over is not the end and is not a space
						if col_pos + 1 >= num_cols and cols[row_pos][col_pos+1] != space:
							return False
						else:
							break
				if quantity_count != quantity:
					return False 
		row_pos += 1
	return True
		

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
				if cols[row_pos][col_pos] == val:
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

print(row_checker(cols, constraints))
# print(partial_row_checker(cols, constraints))
