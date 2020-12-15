import pandas as pd
import pdb


def compute_sumproduct_of_b(b, D, F):
    """ Compute the sumproduct.
    - b: just a value
    - D: dataframe of consumption
    - F: dataframe of gravity.
    """
    val_by_val_product = []
    for i, j in zip(D, F):
        if (isinstance(i, str) or isinstance(j, str)):
            print("it is string! % %", i, j)
            pdb.set_trace()
        val_by_val_product.append(i * j)
    return sum(val_by_val_product) * b


def compute_B_j(b, D, F, B_j, index):
	"""
	b: a value. in first iteration it should be 1
	D: consumptions matrix
	F: gravity matrix.
	B_j: B_j matrix for costs.
	index: number of iterations
	"""
	# check if iteration is the first one
	if index == 0:
		b = 1
	# create the sumproducts and add them to the array
	cols = F.columns.to_list()
	cols.remove('NUTS_2')
	results = []
	for col in cols:
		result = compute_sumproduct_of_b(b, D, F[col])
		results.append(result)
	B_j[index] = results


def compute_A_j(B_j, A_j, index):
	""" Method to compute A_J
	A_j: dictionary to have A_j
	index: number of iteration.
	bj_list: list of the values of B_j dictionary
	"""
	bj_list = B_j[index]
	# define an empty list to contain the 1/B_j list values
	aj_list = []
	# iterate b_j list and invert its values
	for val in bj_list:
		a = 1/val
		aj_list.append(a)
	# add the values to the dictionary
	A_j[index] = aj_list


def compute_T_j(A, O, b, D, F, iteration):
	""" Method to compute T matrix.
	A: A-help matrix
	O: productions matrix
	b: a value
	D: Consumptions matrix
	F: gravity matrix
	iteration: iteration where we are into
	"""
	# get the lists that correspond to current iteration from A and B matrices
	aj_values_list = A[iteration]
	o_values_list = O.to_list() # O['Production_tn'].to_list()
	d_values_list = D.to_list() # D['Consumption_normalized'].to_list()
	
	# create T matrix according to F and initialize it with 0
	T = F.copy()
	T.loc[:,1:] = 0
	
	# compute the T(i, j) values of the array
	nuts_cols = F.columns.to_list()
	nuts_cols.remove('NUTS_2')
	for i, prod, a in zip(nuts_cols, o_values_list, aj_values_list):
	    for j, cons in zip(F.index, d_values_list):
		    T[i][j] = F[i][j] * prod * cons * b * a
	return T


def get_cons_percentages(T, D, iteration):
	""" Method to get the percentages from each iteration.
	T: T(i, j) matrix.
	D: Consumptions matrix.
	iteration: number of iteration where the program is found.
	
	return: pc_list: list of percentages
	"""
	# percentage list
	pc_list = []
	numerator_matrix = D
	# T is inverted. Hence, we sum the row
	denominator_matrix = T.sum(axis=1)
	for n, d in zip(numerator_matrix, denominator_matrix):
		pc_list.append(n/d)
	return pc_list


def get_prod_percentages(T, O, iteration):
	""" Method to get the percentages from each iteration.
	T: T(i, j) matrix.
	O: Productions matrix.
	iteration: number of iteration where the program is found.
	
	return: percentages_matrix: dictionary
	"""
	pc_list = []
	numerator_matrix = O
	# T is inverted. Hence, we sum the row
	denominator_matrix = T.sum()
	denominator_matrix = denominator_matrix.iloc[1:]
	for n, d in zip(numerator_matrix, denominator_matrix):
		pc_list.append(n/d)
	return pc_list


# read the xlsx file
agro = pd.read_excel("Agro2018.xlsx", engine='openpyxl')

# print all columns of the (previously excel) file
agro.columns

agro.Production_tn = agro.Production_tn.replace('na', 0)

# sum Production_tn column and group sums by Region
# SELECT Region, sum(Production_tn)
# FROM agro
# GROUPBY Region
n_by_region = agro.groupby("Region")["Production_tn"].sum()

# count Production_tn column and group counts by Region
n_by_region = agro.groupby("Region")["Production_tn"].count()

# write results to a csv file WITH column titles
n_by_region.to_csv('results.csv', header=True)

# read another xlsx file, load it, group by consumption
consumption = pd.read_excel("Consumption_NUTS3.xlsx", engine='openpyxl')
n_by_consumption = consumption.groupby("Region")["Consumption"].sum()

# merge the results
region_consumption = pd.merge(left=n_by_region,
                                right=n_by_consumption,
                                left_on='Region',
                                right_on='Region')

# finally write the merged result to a file
region_consumption.to_csv('merged_results.csv', header=True)


# now add another column computing the difference between production and consumption
region_consumption['Difference'] = region_consumption['Production_tn'] - region_consumption['Consumption']

# same as above but by r_unit
n_by_region_runit = agro.groupby("R_unit")["Production_tn"].sum()
n_by_consumption_runit = consumption.groupby("R_unit")["Consumption"].sum()

runit_merge = pd.merge(left=n_by_region_runit, right=n_by_consumption_runit, left_on='R_unit', right_on='R_unit')



##########   Step 1     #########

# Compute the coefficient for normalize the two column values
coeff_1 = region_consumption.Production_tn.sum()/region_consumption.Consumption.sum()

# then create a third column with consumptions and normalize it according to production
region_consumption['Consumption_normalized'] = region_consumption.Consumption * coeff_1
print(region_consumption)

# read xlsx with distances
distm = pd.read_excel('Distm.xlsx', engine='openpyxl')
# fill NaN with very large values
distm = distm.fillna(9999)

# create 1/distm array.
gravity_m = distm.copy()
nuts_cols = gravity_m.columns.to_list()
nuts_cols.remove('NUTS_2')

for i in nuts_cols:
    for j in gravity_m.index:
        gravity_m[i][j] = 1/gravity_m[i][j]

print(gravity_m)


##########   Step 2     #########

# fill the B_j array. Algorithm:
# create a list of column names of gravity_m matrix. It is nuts_cols
# iterate it by filling a list with the sumproduct.
# add it to a new dataframe (each column shoud be the iteration)
B_j = {}
A_j = {}
b =1
index = 0
compute_B_j(b, region_consumption['Consumption_normalized'],
	gravity_m, B_j, index)

compute_A_j(B_j, A_j, index)
T = compute_T_j(A_j, region_consumption['Production_tn'],
		        b, region_consumption['Consumption_normalized'],
		        gravity_m, index)

# compute percentages
cons_pc = get_cons_percentages(T, region_consumption['Consumption_normalized'], index)
prod_pc = get_prod_percentages(T, region_consumption['Production_tn'], index)

print("T is %", T)
print("consumption percentages are % and production percentages are %", cons_pc, prod_pc)

#################################

def select(choice):
    if choice == 1:
        print(region_consumption)
    elif choice == 2:
        print(runit_merge)
