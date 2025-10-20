
import polars as pl
import yaml

def get_patient_identifiers(input_file, sep):
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    df = pl.read_csv(input_file, separator=sep).select(config["PATIENT_ID_COL"])
    return df

def get_patient_ids_from_file(input_file, sep):
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    data = pl.read_csv(input_file, separator=sep)
    return data[config["PATIENT_ID_COL"]]

def combine_dataframes_horizontal(df1,df2):
    new_df  = pl.concat([df1, df2],how='horizontal')
    return new_df