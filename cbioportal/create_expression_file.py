########################################################
#### File to create expression data synthetic data  ####
########################################################

import polars as pl
import numpy as np
from utils import get_patient_identifiers, combine_dataframes_horizontal
import yaml

def create_expression_matrix(column_list, patient_id_col, min_value, max_value, number_of_entries):
    names = column_list[patient_id_col].to_list()
    data = {
        name: np.random.randint(low=min_value, high=max_value, size=number_of_entries)
        for name in names
    }
    df = pl.DataFrame(data)
    return df

def read_gene_json(input_json):
    df = pl.read_json(input_json)
    return df.select(["entrezGeneId","hugoGeneSymbol"])




if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    gene_identifiers = read_gene_json(config["GENE_IDENTIFIERS_JSON"])
    gene_identifiers_subset = gene_identifiers[config["GENE_IDENTIFIERS_SUBSET_START"]:config["GENE_IDENTIFIERS_SUBSET_STOP"], :]
    patient_identifiers = get_patient_identifiers(config["DATA_CLINICAL_PATIENT_TXT"], '\t')
    number_of_genes = gene_identifiers_subset.shape[0]
    print(number_of_genes)
    gene_expression_median = create_expression_matrix(
        patient_identifiers,
        config["PATIENT_ID_COL"],
        config["GENE_EXPRESSION_MIN"],
        config["GENE_EXPRESSION_MAX"],
        number_of_genes
    )
    gene_expression_df = combine_dataframes_horizontal(gene_identifiers_subset, gene_expression_median)
    print(gene_expression_df.head())
    gene_expression_df.write_csv(config["DATA_GENE_EXPRESSION_TXT"], separator='\t')