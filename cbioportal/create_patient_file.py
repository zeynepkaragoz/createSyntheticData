##########################################################################
#### Python script to create clinical data on patient and sample level ###
##########################################################################
# Author: T.J.M. Kuijpers

# Columns in patient file:
# Patient Identifier
# Overall Survival
# Status Overall Survival (Months)
# Disease Free Status Disease Free (Months)

import random
import polars as pl
import polars.selectors as cs
import yaml


def create_patient_identifier(patient_size, prefix):
    identifier_list = []
    for x in range(1, patient_size + 1):
        identifier_list.append(prefix + str(x))
    return identifier_list


def create_categorical_list_patients(patient_size, option_list):
    return [random.choice(option_list) for i in range(patient_size)]

def create_numerical_list_patients(patient_size, min_value, max_value, number_of_decimals):
    return [round(random.uniform(min_value, max_value), number_of_decimals) for i in range(patient_size)]

def create_sample_identifier(patient_id, sample_per_patient=1):
    sample_ids = []
    for pid in patient_id:
        for i in range(1, sample_per_patient + 1):
            sample_ids.append(f"{pid}_SAMPLE{i}")
    return sample_ids

def create_sample_data(patient_id, cancer_types, cancer_type_detailed, sample_per_patient=1):
    # Expand patient_id and cancer_types for multiple samples per patient
    expanded_patient_id = []
    expanded_cancer_type = []
    expanded_cancer_type_detailed = []
    sample_display_names = []
    sample_classes = []
    primary_sites = []
    sample_types = []
    for idx, pid in enumerate(patient_id):
        for i in range(1, sample_per_patient + 1):
            expanded_patient_id.append(pid)
            expanded_cancer_type.append(cancer_types[idx])
            expanded_cancer_type_detailed.append(cancer_type_detailed[idx])
            sample_display_names.append(f"Sample {i} of {pid}")
            sample_classes.append(random.choice(["Primary", "Metastatic", "Recurrence"]))
            primary_sites.append(random.choice(["Lung", "Liver", "Breast", "Prostate"]))
            sample_types.append(random.choice(["primary", "metastatic", "recurrence"]))
    sample_ids = create_sample_identifier(patient_id, sample_per_patient)
    return {
        "PATIENT_ID": expanded_patient_id,
        "SAMPLE_ID": sample_ids,
        "CANCER_TYPE": expanded_cancer_type,
        "CANCER_TYPE_DETAILED": expanded_cancer_type_detailed,
        "SAMPLE_DISPLAY_NAME": sample_display_names,
        "SAMPLE_CLASS": sample_classes,
        "PRIMARY_SITE": primary_sites,
        "SAMPLE_TYPE": sample_types
    }

def write_sample_clinical_file(sample_data, filename, sep="\t"):
    import polars as pl
    df = pl.DataFrame(sample_data)
    df.write_csv(filename, separator=sep)

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    patient_id = create_patient_identifier(config["PATIENT_SIZE"], config["FAKE_PATIENT_PREFIX"])
    os_status = create_categorical_list_patients(config["PATIENT_SIZE"], config["OS_OPTIONS"])
    dfs_status = create_categorical_list_patients(config["PATIENT_SIZE"], config["DFS_OPTIONS"])
    os_months = create_numerical_list_patients(config["PATIENT_SIZE"], config["OS_MONTHS_MIN"], config["OS_MONTHS_MAX"], config["OS_MONTHS_DECIMALS"])
    dfs_months = create_numerical_list_patients(config["PATIENT_SIZE"], config["DFS_MONTHS_MIN"], config["DFS_MONTHS_MAX"], config["DFS_MONTHS_DECIMALS"])
    age = create_numerical_list_patients(config["PATIENT_SIZE"], config["AGE_MIN"], config["AGE_MAX"], config["AGE_DECIMALS"])
    sex = create_categorical_list_patients(config["PATIENT_SIZE"], config["SEX_OPTIONS"])
    data_frame = pl.DataFrame({
        config["PATIENT_ID_COL"]: patient_id,
        'AGE': age,
        'OS_STATUS': os_status,
        'OS_MONTHS': os_months,
        'DFS_STATUS': dfs_status,
        'DFS_MONTHS': dfs_months
    })

    data_frame.with_columns((~cs.string()).cast(pl.String))
    data_frame.write_csv(config["DATA_CLINICAL_PATIENT_TXT"], separator="\t")

    sample_per_patient = 2
    cancer_type = create_categorical_list_patients(config["PATIENT_SIZE"], config["CANCER_TYPE_OPTIONS"])
    cancer_type_detailed = create_categorical_list_patients(config["PATIENT_SIZE"], config["CANCER_TYPE_OPTIONS"])
    sample_data = create_sample_data(
        patient_id,
        cancer_type,
        cancer_type_detailed,
        sample_per_patient=sample_per_patient
    )
    write_sample_clinical_file(sample_data, "data_clinical_sample.txt", sep="\t")