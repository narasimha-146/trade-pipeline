import pandas as pd

def clean_base(df: pd.DataFrame):
    
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

    
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month
    df['QUARTER'] = df['DATE'].dt.quarter

    
    df = df.dropna(subset=['TOTAL VALUE_INR', 'DUTY PAID_INR', 'QUANTITY'])

    return df

def standardize_units(df: pd.DataFrame):
    unit_map = {
        'nos': 'PCS',
        'pcs': 'PCS',
        'pieces': 'PCS',
        'piece': 'PCS',
        'kg': 'KG',
        'kgs': 'KG',
        'gms': 'GM',
        'gm': 'GM',
        'units': 'PCS'
    }

    df['unit_standardized'] = df['UNIT'].str.lower().map(unit_map)

    return df
