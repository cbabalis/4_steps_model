#!/usr/bin/env python
""" Module to run 4 Step Model to given arrays. """
import sys
import pandas as pd
import numpy as np

import pdb


def read_user_input(prod_cons_tn_fpath, movement_fpath, crit):
    prod_cons_tn = pd.read_csv(prod_cons_tn_fpath, delimiter='\t')
    movement = pd.read_csv(movement_fpath, delimiter='\t')
    crit_percentage = float(crit)
    return prod_cons_tn, movement, crit_percentage


def is_input_valid(prod_cons_tn, movement, crit_percentage):
    if not isinstance(prod_cons_tn, pd.DataFrame):
        return False
    if not isinstance(crit_percentage, float):
        return False
    return True


def compute_4_step_model(prod_cons_tn, movement, crit_percentage, B_j, A_i=[], curr_matrix=[]):
    """ documentation here.
    """
    # if B_j == 1: then it is the first step. begin.
    if len(set(B_j)) == 1:
        curr_matrix = pd.DataFrame(np.ones((len(movement), len(movement))))
        cons = prod_cons_tn['Κατανάλωση'].tolist()
        pdb.set_trace()
        A_i = compute_coefficient(cons, movement.values.tolist(), B_j)
        pdb.set_trace()
        #compute_T_i_j(A_i, prod_cons_tn[], B_j, prod_cons_tn['Κατανάλωση'], movement)
    pdb.set_trace()
    # if crit_percentage is satsified, then exit
    # call again compute_4_step_model with different B_j, A_j, curr_matrix


def compute_coefficient(tn, movement, existing_coef):
    coef = []
    for mv_line in movement:
        coef.append(sumprod(tn, mv_line, existing_coef))
    pdb.set_trace()
    coef = [1/x for x in coef]
    return coef


def sumprod(li1, li2, l3):
    """ sumproduct between two lists."""
    sumproduct = 0
    for l1, l2, l3 in zip(li1, li2, l3):
        sumproduct += l1 * l2 * l3
    return sumproduct


def compute_threshold(df):
    """TODO: need to implement the following line"""
    df['R7'] = (df.R3 - df.R4) / df.R3 * 100


def test_print(a_word):
    print(a_word)


def main():
    # read input arrays
    prod_cons_fp, mv_fp, pcnt = sys.argv[1], sys.argv[2], sys.argv[3]
    prod_cons_tn, movement, crit_percentage = read_user_input(prod_cons_fp, mv_fp, pcnt)
    test_print([prod_cons_tn, movement, crit_percentage])
    # check if arrays are ok (same length)
    assert is_input_valid(prod_cons_tn, movement, crit_percentage)
    # do some preliminary work
    B_j = [1 for i in range(0, len(prod_cons_tn))]
    compute_4_step_model(prod_cons_tn, movement, crit_percentage, B_j)
    # run main algorithm


if __name__ == '__main__':
    main()