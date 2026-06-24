import pandas as pd

def fill_and_standardize_values_by_id(
        df: pd.DataFrame, 
        id_col: str, 
        value_col: str,
        standardize_existing: bool=False
) -> pd.DataFrame:
    """
    Fill and standardize values using the most frequent value within each ID group.

    For each group defined by `id_col`, this function finds the most frequent
    non-null value in `value_col`. It then assigns that consensus value to all
    rows with the same ID when a consensus exists.

    This means the function does two things:
    1. fills missing values when another row with the same ID has a known value;
    2. standardizes inconsistent values within the same ID group.

    Rows whose ID has no non-null reference value keep their original value.

    Args:
        df: Input DataFrame.
        id_col: Column used to group related records.
        value_col: Column to fill and standardize.

    Returns:
        A copy of the DataFrame with `value_col` filled and standardized by ID.

    Raises:
        ValueError: If `id_col` or `value_col` are missing from the DataFrame.
    """
    # Validate column schema
    required_cols = {id_col, value_col}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"DataFrame is missing required columns: {missing_cols}")
        
    df_clean = df.copy()

    id_to_consensus_map = (
        df_clean.dropna(subset=[value_col])
            .groupby(id_col)[value_col]
            .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
            .dropna()
            .to_dict()
    )

    if standardize_existing:
        # 2. OVERWRITE the column entirely with the dictionary map
        # Using .fillna() at the end acts as a safety backup for IDs with 0 descriptions
        df_clean[value_col] = df_clean[id_col].map(id_to_consensus_map).fillna(df_clean[value_col])
    else:
        missing_mask = df_clean[value_col].isna()
        df_clean.loc[missing_mask, value_col] = df_clean.loc[missing_mask, value_col].map(id_to_consensus_map)
    return df_clean
