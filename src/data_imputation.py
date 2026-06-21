import pandas as pd

def fill_missing_values_by_id(df: pd.DataFrame, 
                              id_col: str, 
                              value_col: str) -> pd.DataFrame:
    """Fills null fields by mapping the most frequent valid value (mode) of the same id.

    This function optimizes data completeness within a DataFrame. It groups rows
    by a unique identifier and propagates existing, non-null textual
    values to rows missing that information. It leaves the column null
    only if no reference text exists for that specific id.

    Args:
        df: The pandas DataFrame containing product transactions or catalog records.
        id_col: The name of the column identifying the id.
        value_col: The name of the column containing the text value to complete.

    Returns:
        A shallow copy of the input DataFrame with missing values filled in the 
        target description column where applicable.

    Raises:
        ValueError: If either `id_col` or `value_col` are not present in the 
            provided DataFrame's columns.
    """
    # Validate column schema
    required_cols = {id_col, value_col}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"DataFrame is missing required columns: {missing_cols}")
        
    df_clean = df.copy()

    id_to_value_map = (
        df_clean.dropna(subset=[value_col])
            .groupby(id_col)[value_col]
            .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
            .dropna()
            .to_dict()
    )
    # 2. Fill missing values using the map dictionary
    df_clean[value_col] = df_clean[value_col].fillna(df_clean[id_col].map(id_to_value_map))
    
    return df_clean
