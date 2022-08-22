"""
Input: a pre-filtered csv file containing disease-phenotype relationship
    # Fields:
    # GOName,GOID,DiseaseName,DiseaseID,InferenceChemicalQty,InferenceChemicalNames,InferenceGeneQty,InferenceGeneSymbols
Output: a csv file containing disease similarity pairs
"""
import numpy as np
from scipy import linalg
import math
import pandas as pd


def generate_matrix(inputfile):
    phe_dis_dict = {}
    disease_list = []
    disease_dict = {}
    with open('o1_COVID_disease_sim.csv', 'r') as f:
        line = f.readline()
        index = 0
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            disease_list.append(line.split(',')[0])
            disease_dict[line.split(',')[0]] = index
            index += 1
            line = f.readline()
    with open(inputfile, 'r') as f:
        line = f.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            words = line.split(',')
            if words[0] in phe_dis_dict:
                phe_dis_dict[words[0]].add(words[2])
            else:
                phe_dis_dict[words[0]] = {words[2]}
            line = f.readline()
    i = 0
    pheno_dict = {}
    all_disease = set()
    for phenotype in phe_dis_dict:
        pheno_dict[phenotype] = i
        all_disease = all_disease.union(phe_dis_dict[phenotype])
        i += 1
    i = 0
    sim_matrix = np.zeros((len(pheno_dict), len(disease_list)))
    for phenotype in phe_dis_dict:
        for disease in phe_dis_dict[phenotype]:
            sim_matrix[pheno_dict[phenotype]][disease_dict[disease]] = 1
    return sim_matrix, disease_list, pheno_dict


def jaccard_sim(v1=None, v2=None):
    if v2 is None:
        v2 = [0]
    if v1 is None:
        v1 = [0]
    inter_ = np.dot(v1, v2)
    union_ = sum(v1) + sum(v2) - inter_
    return inter_ / union_


def similarity_dic(rela_matrix=np.zeros((2, 2)), disease_list=None):
    if disease_list is None:
        disease_list = []
    r, c = rela_matrix.shape
    sim_matrix = np.zeros((len(disease_list), len(disease_list)))
    for i in range(0, c):
        for j in range(i + 1, c):
            sim_matrix[i, j] = jaccard_sim(rela_matrix[:, i], rela_matrix[:, j])
            sim_matrix[j, i] = jaccard_sim(rela_matrix[:, i], rela_matrix[:, j])
        print("similarity ", i, "done!")
    return sim_matrix


def fix_helper(v1, v2):
    n = linalg.norm(v1 - v2)
    return math.exp(- n * n)


def similarity_fix(sim_matrix=np.zeros((1, 1))):
    r, c = sim_matrix.shape
    fixed = np.zeros((r, c))
    for i in range(0, r):
        for j in range(0, c):
            fixed[i, j] = fix_helper(sim_matrix[:, i], sim_matrix[:, j])
        fixed[i, i] = 0.0
    return fixed


def write_result(outfile="out", sim_dict=None):
    if sim_dict is None:
        sim_dict = {1: {1}}
    res = ''
    for key in sim_dict:
        res += key
        res += ','
        res += str(sim_dict[key])
        res += '\n'
    res = res[: -1]
    with open(outfile, "w") as f:
        f.write(res)


def save_matrix(matrix, file):
    np.savetxt(file, matrix, delimiter=',')


def read_matrix(file):
    df = pd.read_csv(file, sep=',', header=None)
    return np.array(df)


def main():
    inputfile = 'o1_filtered_p_d.csv'
    outputfile = 'o2_reduced_similarity_matrix_fixed.csv'
    print("done1")
    rela_matrix, disease_list, _ = generate_matrix(inputfile)
    print("done2")
    sim_matrix = similarity_dic(rela_matrix, disease_list)
    save_matrix(sim_matrix, 'o2_reduced_similarity_matrix.csv')
    print("done3")
    fixed_matrix = similarity_fix(sim_matrix)
    save_matrix(fixed_matrix, outputfile)



if __name__ == '__main__':
    main()
