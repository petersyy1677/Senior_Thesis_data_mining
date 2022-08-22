"""
Input: a csv file containing disease-phenotype relationship
    # Fields:
    # GOName,GOID,DiseaseName,DiseaseID,InferenceChemicalQty,InferenceChemicalNames,InferenceGeneQty,InferenceGeneSymbols
Output: a csv file containing filtered COVID-19 related rows of the input file
"""
import numpy as np


def generate_matrix(inputfile, target='COVID-19'):
    phe_dis_dict = {}
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
    disea_dict = {}
    all_disease = set()
    for phenotype in phe_dis_dict:
        pheno_dict[phenotype] = i
        all_disease = all_disease.union(phe_dis_dict[phenotype])
        i += 1
    i = 0
    disea_list = []
    target_index = 0
    for disease in all_disease:
        if disease == target:
            target_index = i
        disea_dict[disease] = i
        disea_list.append(disease)
        i += 1
    sim_matrix = np.zeros((len(pheno_dict), len(disea_dict)))
    for phenotype in phe_dis_dict:
        for disease in phe_dis_dict[phenotype]:
            sim_matrix[pheno_dict[phenotype]][disea_dict[disease]] = 1
    return sim_matrix, disea_list, pheno_dict, target_index


def jaccard_sim(v1=None, v2=None):
    if v2 is None:
        v2 = [0]
    if v1 is None:
        v1 = [0]
    inter_ = np.dot(v1, v2)
    union_ = sum(v1) + sum(v2) - inter_
    return inter_ / union_


def similarity_dic(sim_matrix=np.zeros((2, 2)), disease_list=None, target_index=0):
    if disease_list is None:
        disease_list = []
    r, c = sim_matrix.shape
    sim_dict = {}
    for i in range(0, c):
        key = disease_list[i] # key = candidate disease
        sim_dict[key] = jaccard_sim(sim_matrix[:, i], sim_matrix[:, target_index])
        print("done ", i)
    return sim_dict


def write_sim_dict(sim_dict, outputfile, candidate=None):
    if candidate is None:
        candidate = list()
    res = ''
    for i in range(0, len(candidate)):
        res += candidate[i]
        res += ','
        res += str(sim_dict[candidate[i]])
        res += '\n'
    with open(outputfile, 'w') as f:
        f.write(res)


def candidate_list(sim_dict=None, threshold=100):
    sim_sorted = {k: v for k, v in sorted(sim_dict.items(), key=lambda item: item[1])}
    keys = list(sim_sorted.keys())
    return keys[0 - threshold:]


def write_result(outfile="out", inputfile=None, candidate=None):
    if candidate is None:
        candidate = set()
    res = ''
    with open(inputfile, "r") as f:
        line = f.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            words = line.split(',')
            if words[2] in candidate:
                res += line
                res += '\n'
            line = f.readline()
    with open(outfile, "w") as f:
        f.write(res)


def main():
    inputfile = 'data/Phenotype-Disease.csv'
    outputfile = 'o1_filtered_p_d.csv'

    rela_matrix, disease_list, _, target_index = generate_matrix(inputfile)
    print("done2")

    sim_dict = similarity_dic(rela_matrix, disease_list, target_index)

    print("done3")
    candidate = candidate_list(sim_dict, 300)
    write_sim_dict(sim_dict, 'o1_COVID_disease_sim.csv', candidate)
    write_result(outputfile, inputfile, candidate)
    print("done4")



if __name__ == '__main__':
    main()
