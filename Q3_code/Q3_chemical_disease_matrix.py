"""
Input: a csv file containing diseaseid-clusterid relationship
        a csv file containing drugid-cluster relationship
        a csv file containing drugid-disease relationship
    # Fields:
    # ChemicalName,ChemicalID,CasRN,DiseaseName,DiseaseID,DirectEvidence,InferenceGeneSymbol,InferenceScore,OmimIDs,PubMedIDs
Output: a csv file containing disease-drug weight matrix
"""
import sys
import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

random.seed(3)

def disease_cluster_dict(pointfile):
    di_c_dict = {}
    with open(pointfile, 'r') as f:
        line = f.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            di_c_dict[line.split(',')[0]] = int(line.split(',')[1])
            line = f.readline()
    return di_c_dict # index: point


def generate_matrix(disease_dict, drug_dict): # row: disease; column: drug
    row_id = sorted(list(set(disease_dict.values())))
    column_id = sorted(list(set(drug_dict.values())))
    return np.zeros((len(row_id), len(column_id)))


def update_matrix(adj_matrix, drug_disease_file, drug_dict, disease_dict):
    with open(drug_disease_file, 'r') as f:
        line = f.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            words = line.split(',')
            if words[1] in drug_dict and words[4] in disease_dict:
                adj_matrix[disease_dict[words[4]], drug_dict[words[1]]] += 1
            line = f.readline()
    return adj_matrix


def write_result(outfile="out", disease_cluster_dict=None):
    if disease_cluster_dict is None:
        disease_cluster_dict = {1: {1}}
    sorted_dcd = {k: v for k, v in sorted(disease_cluster_dict.items(), key=lambda item: item[1])}
    res = ''
    for disease in sorted_dcd:
        res += disease
        res += ','
        res += str(sorted_dcd[disease])
        res += '\n'
    res = res[: -1]
    print(res)
    with open(outfile, "w") as f:
        f.write(res)


def expand(m):
    r, c = m.shape
    adj_matrix = np.zeros((r + c, r + c))
    adj_matrix[0:r, r:] = m
    adj_matrix[r:, 0:r] = np.transpose(m)
    return adj_matrix


def nxplot(adj_matrix):
    G = nx.from_numpy_matrix(adj_matrix)
    edge_labels = nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))
    nx.draw(G)
    plt.show()


def save_matrix(matrix, file):
    np.savetxt(file, matrix, delimiter=',')


def main():
    disease_dict = disease_cluster_dict('data/disease_cluster_withid.csv')
    print("done1")
    drug_dict = disease_cluster_dict('data/drugid_cluster.csv')
    print("done2")
    adj_matrix = generate_matrix(disease_dict, drug_dict)
    print(adj_matrix.shape)
    print("done3")
    adj_matrix = update_matrix(adj_matrix, 'data/drug_disease.csv', drug_dict, disease_dict)
    adj_matrix = expand(adj_matrix)
    save_matrix(adj_matrix, 'q3_adj_matrix.csv')


if __name__ == '__main__':
    main()


