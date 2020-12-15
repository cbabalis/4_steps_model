""" Module to execute a minimum path to given array.

INPUT:
    - a csv file containing an adjacency list of connected vertices
    - a csv file with costs from vertex to vertex

OUTPUT:
    - Dijkstra to the input graph.
    - minimum path
    - a map with connections with line width compared to load.
"""

import pandas as pd
import numpy as np
import sys
import pdb


def read_from_cmd(connections_csv, t_csv):
    conns = pd.read_csv(connections_csv, delimiter=';')
    t_matrix = pd.read_csv(t_csv)
    return (conns, t_matrix)


def replace_val_with_header(conns_df):
    # read a file as dataframe
    conns_df = conns_df.fillna(0)
    conns_df = conns_df.iloc[1:]
    cols = (conns_df.columns).to_list()
    # remove first element as it is of no use
    cols.pop(0)
    conns_df[list(cols)] = conns_df[list(cols)].astype(int)
    # replace all '1's with column's name
    for col in cols:
        conns_df[col] = conns_df[col].replace(1, col)
    # return dataframe
    return conns_df


def convert_to_adj_dict(conns_df):
    conns_df = conns_df.transpose()
    cols = (conns_df.columns).to_list()
    adj_dict = {}
    for col in cols:
        list_row = conns_df[col].to_list()
        key = list_row.pop(0)
        adj_dict[key] = list_row
    return adj_dict


def remove_val_from_dict_of_lists(a_dict, val):
    """ Remove the value val from the dictionary
    with form <key: list>.
    param d: dictionary
    param val: value (int)
    """
    for key in a_dict:
        a_list = a_dict[key]
        a_dict[key] = [i for i in a_list if i != val]
    return a_dict


def get_adjacency_from_file(conns_df):
    # prepare conns_df data form
    conns_df = replace_val_with_header(conns_df)
    # create a dictionary with <key, val> pairs being
    # FROM => TO.
    adj_dict = convert_to_adj_dict(conns_df)
    # remove zeros from adjacency dictionary
    adj_dict = remove_val_from_dict_of_lists(adj_dict, 0)
    return adj_dict
    #TODO: maybe it should be a dictionary


def main():
    # read input files given from the command line
    conns, t_matrix = read_from_cmd(sys.argv[1], sys.argv[2])
    # create adjacency list from csv file
    adj_conns = get_adjacency_from_file(conns)
    pdb.set_trace()
    # run a dijkstra in the given adjacency list
    # create loads graph (csv file) according to the file with the loads (second file)
    # plot results to map
    pass


if __name__ == '__main__':
    main()