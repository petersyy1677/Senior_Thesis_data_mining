#!/bin/sh
mv all_data/Phenotype-Disease.csv Q2_code/data

mv all_data/disease_id.csv Q2_code/disease_cluster_data
mv all_data/disease_index.csv Q2_code/disease_cluster_data
mv all_data/index_point.csv Q2_code/disease_cluster_data
mv all_data/point_cluster.csv Q2_code/disease_cluster_data

mv all_data/disease_cluster_withid.csv Q3_code/data
mv all_data/drug_disease.csv Q3_code/data
mv all_data/drugid_cluster.csv Q3_code/data


cd Q2_code
python3 step1_filter_covid19_related.py
python3 step2_reduced_similarity_matrix.py
python3 step3_spectural_clustering.py
python3 step5_get_disease_cluster.py

cd ../Q3_code
python3 Q3_chemical_disease_matrix.py