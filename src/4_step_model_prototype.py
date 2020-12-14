import pandas as pd



def compute_sumproduct_of_b(B_j, D, F):
    """ Compute the sumproduct.
    - B_j: just a value
    - D: dataframe of consumption
    - F: dataframe of gravity.
    """
    val_by_val_product = []
    for i, j in (D, F):
        val_by_val_product.append(i * j)
    return sum(val_by_val_product) * B_j



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
distm = pd.read_csv('distm.xlsx', engine='openpyxl')
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



#################################

def select(choice):
    if choice == 1:
        print(region_consumption)
    leif choice == 2:
        print(runit_merge)
