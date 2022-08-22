"""
Input: a csv file containing disease-index relationship
        a csv file containing cluster points(the ith row represents the ith disease)
        a csv file containing cluster id and cluster points
    # Fields:
    # GOName,GOID,DiseaseName,DiseaseID,InferenceChemicalQty,InferenceChemicalNames,InferenceGeneQty,InferenceGeneSymbols
Output: a csv file containing disease-disease-similarity pairs(use Jaccard similarity)
"""
import sys
import numpy as np
import random

random.seed(3)


def point_index_dict(pointfile):
    point_dict = {}
    i = 0
    with open(pointfile, 'r') as f:
        line = f.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            point_dict[i] = line.split(',')[0]
            i += 1
            line = f.readline()
    print("i: ", i)
    return point_dict # index: point


def get_disease_id(didfile):
    did = {}
    with open(didfile, 'r') as f:
        line = f.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            did[line.split(',')[1]] = line.split(',')[0]
            line = f.readline()
    return did # id: disease


def read_point_cluster(clusterfile):
    cluster_dict = {}
    with open(clusterfile, 'r') as f:
        line = f.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            point = line.split(',')[1]
            cluster = line.split(',')[0]
            cluster_dict[point] = int(cluster)
            line = f.readline()
    print(len(cluster_dict))
    return cluster_dict # point: cluster


def disease_index(indexfile):
    index_dict = {}
    with open(indexfile, 'r') as f:
        line = f.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            index_dict[line.split(',')[1]] = int(line.split(',')[0])
            line = f.readline()
    print(len(index_dict))
    return index_dict # disease: index


def disease_cluster(point_dict, cluster_dict, index_dict, did):
    disease_cluster_dict = {}
    for d in did:
        if did[d] in index_dict:
            disease_cluster_dict[d] = cluster_dict[point_dict[index_dict[did[d]]]]
    return disease_cluster_dict


def disease_c(index_point_dict, point_cluster_dict, disease_index_dict):
    dis_c = {}
    for disease in disease_index_dict:
        dis_c[disease] = point_cluster_dict[index_point_dict[disease_index_dict[disease]]]
    return dis_c


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


def main():
    index_point_dict = point_index_dict('disease_cluster_data/index_point.csv')
    point_cluster_dict = read_point_cluster('disease_cluster_data/point_cluster.csv')
    disease_index_dict = disease_index('disease_cluster_data/disease_index.csv')
    did = get_disease_id('disease_cluster_data/disease_id.csv')
    dcd = disease_cluster(index_point_dict, point_cluster_dict, disease_index_dict, did)
    d = disease_c(index_point_dict, point_cluster_dict, disease_index_dict)
    write_result('o5_diseaseID_cluster.csv', dcd)
    write_result('o5_disease_cluster.csv', d)


if __name__ == '__main__':
    main()
