import pandas as pd 
import numpy as np 
from app.utils.logger import get_logger

logger = get_logger(__name__)


#function for missing values
def detect_missing_values(df: pd.DataFrame) -> dict:
   
    missing={}
    for column in df.columns:
        missing[column]=df[column].isnull().sum()

    return missing 

# function for duplicate values in dataset
def detect_duplicate(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())


# function for datatype for each columns
def detect_datatypes(df: pd.DataFrame) -> dict :
    data_types = {}

    for col, dtype in df.dtypes.items():

        dtype_str = str(dtype)
        data_types[col] = dtype_str

    return data_types


# function for outliers
def detect_outlier(df: pd.DataFrame) -> dict :

    res ={}

    numeric_cols = df.select_dtypes(include=['number']).columns

    for col in numeric_cols :
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].qunatile(0.75)
        IQR = Q3 - Q1

        lb = Q1 - 1.5 *IQR
        ub = Q3 + 1.5* IQR

        outliers =len( df[(df[col] < lb) | (df[col] > ub)] )

        res[col] = outliers

    return res

# function for the metadata of dataset
 def generate_stats(df: pd.DataFrame) -> dict :
     return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list( df.columns),
        "numeric_columns": list(df.select_dtypes(include=['number']).columns),
        "categorical_columns": list(df.select_dtypes(exclude=['number']).columns)
     }

def run_data_quality_checks(df : pd.DataFrame) -> dict:
    logger.info("data quality service done successfully  ")
    return{
        "metadata" : generate_stats(df),
        "data_types" : detect_datatypes(df),
        "missing_values" : detect_missing_values(df),
        "duplicates" : detect_duplicate(df),
        "outliers" : detect_outlier(df)
    }

        

    

