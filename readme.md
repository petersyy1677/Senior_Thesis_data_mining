# EECS476 W20 final project
# Exploring potentially effective chemical for COVID-19: similarity-based network analysis and predictive analysis
This is the capstone design project that I completed for Data Science Bachelors at the University Of Michigan (April 2020).
![Alt text](https://github.com/petersyy1677/Senior_Thesis_data_mining/blob/main/drug_tan_5.png)



# Instructions
 
## Q1: chemical chemical community detection

## Q2: disease disease community detection
	step1: 
		input: 
			a csv file in data/ directory, containing phenotype_disease pairs
		output: 
			1. a csv file named o1_filtered_p_d.csv, containing filtered input file based on the disease that similar to COVID-19
			2. a csv file named o1_COVID_disease_sim.csv, containing similarity between COVID-19 and filtered disease.
	step2:
		input:
			output from step1
		output:
			1. a csv file named o2_reduced_similarity_matrix.csv containing similarity matrix of filtered disease
			2. a csv file named o2_reduced_similarity_matrix_fixed.csv containing similarity matrix fixed by Gaussian distance measure
	step3:
		input:
			output from step2
		output:
			1. a csv file named o3_cluster_points.csv, containing the eigenvectors of the Laplcian matrix.
	step4:
		input:
			output from step3
		output:
			a csv file containing assigned cluster index and points
		Note that the code for this step is the same as the code for K-mean in project 2. We use random initialization.
	step5:
		input:
			1. a csv file in disease_cluster_data/ containing the <disease, MESHID>(disease_id.csv)
			2. a csv file in disease_cluster_data/ containing the <index, disease>(disease_index.csv)
			3. a csv file in disease_cluster_data/ containing the points for clustering, the row number of each point is the disease index of the corresponding disease
			4. a csv file in disease_cluster_data/ containing the <cluster, point>
		output:
			1. a csv file named o5_disease_cluster.csv, containing <disease name, cluster> pairs
			2. a csv file named o5_diseaseID_cluster.csv, containing <disease MESHID, cluster> pairs
		Note that some of the input data for this part comes from hadoop, we simply include the input file in disease_cluster_data/ directory.

## Q3: chemical disease relationship graph
	step1:
		input:
			1. a csv file named data/disease_cluster_withid.csv containing <disease MESHID, cluster>
			2. a csv file named data/drug_disease.csv containing <drug, disease> 
			3. a csv file named data/drugid_cluster.csv containing <drug ID, cluster>
		output:
			a csv file named q_3_adj_matrix.csv, containing the weight between drug clusters and disease clusters. the 0-4 rows and columns represent the cluster for disease and other rows and columns represent the clusters of drugs.
		Since some of the data for this part comes from Q1, which is shown in Jupter notebook, we simply include some data for this part, in the data/ directory.

## MAKEFILE
	To run the make file, you should first download the data from google drive. The link is as follows. 

	Google link for the data:
		https://drive.google.com/drive/folders/1LB41o7M8h1zVR2elmq4GR7thCtqE61u0?usp=sharing

	Put the all_data/ directory in the code/ directory and run the bash script or just make. 
  
## Code Structure	
  The structure should look like this:
  
	code--all_data------Phenotype-Disease.csv
		| 			|---disease_id.csv
		|-Q1_code	|---disease_index.csv
		|			|---index_point.csv
		|-Q2_code	|---point_cluster.csv
		|			|---disease_cluster_withid.csv
		|-Q3_code	|---drug_disease.csv
		|			+---drugid_cluster.csv
		|-makefile
		|
		+-run.sh

	Notice that the makefile runs a bash script whose name is run.sh, so I used chmod command in the makefile to ensure the permission of the bash script though I'm not sure whether it can successfully change the permission.


