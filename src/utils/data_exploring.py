import pandas as pd
from IPython.display import display

def show_basic_df_info(df: pd.DataFrame) -> None:
    """
    Display basic information and summary statistics of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Prints:
        - DataFrame info including data types and memory usage.
        - Count of missing values per column.
        - Summary statistics for numeric columns.
    """
    print("Dataset Info:")
    display(df.info())

    print("\nMissing Values:")
    display(df.isna().sum())

    print("\nBasic Statistics:")
    print(df.describe())


def get_categorical_counts(df: pd.DataFrame, cat_cols: list[str] = []) -> None:
    """
    Print value counts for specified or inferred categorical columns.

    Args:
        df (pd.DataFrame): The DataFrame containing categorical data.
        cat_cols (list[str], optional): List of categorical column names. 
            If empty, all object-type columns are used.

    Prints:
        Value counts for each categorical column.
    """
    if len(cat_cols) == 0:
        cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        print(f"\n{col} distribution:")
        print(df[col].value_counts())