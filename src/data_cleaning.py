import pandas as pd

def standardize_strs(df: pd.DataFrame, str_cols: list[str]) -> pd.DataFrame:
    """
    Standardize string columns by stripping whitespace and converting to lowercase.

    Args:
        df (pd.DataFrame): The input DataFrame containing string columns.
        str_cols (list[str]): List of column names to standardize.

    Returns:
        pd.DataFrame: A DataFrame with standardized string columns.
    """
    df_copy = df.copy()
    for col in str_cols:
        df_copy.loc[:, col] = df_copy[col].astype(str).str.strip().str.lower()
    return df
