"""
Input: a csv file containing disease-disease similarity
    # Fields:
    # disease1, disease2, similarity
Output: a csv file containing clustering matrix, a csv file containing disease-index pairs
"""
import sys
import numpy as np
import random
from scipy import linalg
import matplotlib.pyplot as plt
import math
import pandas as pd


def l_matrix(s=np.zeros((1, 1)), threshold=0.0):
    sim_matrix = np.array(s)
    r, c = sim_matrix.shape
    for i in range(0, r):
        for j in range(0, c):
            if sim_matrix[i, j] < threshold:
                sim_matrix[i, j] = 0.0
        sim_matrix[i, i] = - np.sum(sim_matrix[i, :])
    lap = - np.array(sim_matrix)
    return lap


def sp_clustering_points(l_matrix=np.zeros((1,1))):
    w, v = linalg.eigh(l_matrix)
    i = 0
    while w[i] < 1e-3:
        i += 1
    return v[:, i:i+10]


def vis2D(cluster_points):
    plt.scatter(cluster_points[:, 1], cluster_points[:, 2], color='blue')
    plt.ylabel('v1')
    plt.xlabel('v2')
    plt.legend()
    plt.show()


def vis3D(cluster_points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = cluster_points[:, 1]
    y = cluster_points[:, 2]
    z = cluster_points[:, 4]
    ax.scatter(x, y, z, c='r', marker='o')
    plt.show()


def read_matrix(file):
    df = pd.read_csv(file, sep=',', header=None)
    return np.array(df)


def save_matrix(matrix, file):
    np.savetxt(file, matrix, delimiter=',')


def main():
    sim_matrix = read_matrix('o2_reduced_similarity_matrix_fixed.csv')
    lmatrix = l_matrix(sim_matrix)
    cluster_points = sp_clustering_points(lmatrix)
    # vis2D(cluster_points)
    # vis3D(cluster_points)
    save_matrix(cluster_points, 'o3_cluster_points.csv')


if __name__ == '__main__':
    main()
