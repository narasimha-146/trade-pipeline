import re
import pandas as pd

def parse_goods_description(df: pd.DataFrame):

    # ------------ REGEX PATTERNS ------------
    material_pattern = r'(STEEL|PLASTIC|WOOD|WOODEN|GLASS|ALUMINIUM|COPPER|MILD STEEL|SS|HOUSEHOLD)'
    MODEL_TOKEN_RE = re.compile(r'[A-Z0-9]+(?:-[A-Z0-9]+)*', re.IGNORECASE)
    INSIDE_PAREN_RE = re.compile(r'\(([^)]+)\)')
    START_MODEL_RE = re.compile(r"^\s*([A-Z0-9]+(?:-[A-Z0-9]+)*)")
    NON_MODEL_WORDS = {"QTY", "PCS", "SET", "SETS", "NOS", "PER", "USD", "CNY"}
    model_name_pattern = r'^[A-Z0-9]+(?:-[A-Z0-9]+)?'

    # new capacity pattern
    capacity_pattern = r'(\d+\s*(?:PCS|NOS|SET)(?:\s*SET)?)'

    qty_pattern = r'QTY[:\s]*([\d,]+)'
    uom_after_qty_pattern = r'QTY[:\s]*\d+[, ]*\s*(PCS|SET|NOS)'
    price_pattern = r'(USD|CNY|EUR|HKD|JPY)[\s/:]*([\d\.]+)'


    # ------------ MASTER CATEGORY ------------
    df['Master category'] = df['GOODS DESCRIPTION'].str.extract(material_pattern, expand=False)


    # ------------ MODEL NUMBER LOGIC ------------
    def extract_model_number(text):
        if pd.isna(text):
            return None
        t = text

        # A) Block inside brackets
        for block in INSIDE_PAREN_RE.findall(t):
            block_up = block.upper().strip()
            m = MODEL_TOKEN_RE.search(block_up)
            if m:
                tok = m.group(0)
                if tok not in NON_MODEL_WORDS:
                    return tok

        # B) Start of string
        m = START_MODEL_RE.match(t.strip())
        if m:
            tok = m.group(1).upper()
            if tok not in NON_MODEL_WORDS and not tok.isnumeric():
                return tok

        # C) Anywhere in string
        for m in MODEL_TOKEN_RE.finditer(t):
            tok = m.group(0).upper()
            if tok not in NON_MODEL_WORDS:
                return tok

        return None

    df["Model Number"] = df["GOODS DESCRIPTION"].apply(extract_model_number)


    # ------------ PRICE ------------
    df[['Unit of measure.1', 'Price']] = df['GOODS DESCRIPTION'].str.extract(price_pattern)
    df['Price'] = df['Price'].astype(float)


    # ------------ CAPACITY (CORRECTED) ------------

    # Extract only the part before QTY
    df['Before_QTY'] = df['GOODS DESCRIPTION'].str.split(r"QTY", n=1).str[0]

    # Extract capacity ONLY from before QTY
    df['Capacity'] = df['Before_QTY'].str.extract(capacity_pattern)[0]


    # ------------ UNIT OF MEASURE (AFTER QTY) ------------
    df['Unit of measure'] = df['GOODS DESCRIPTION'].str.extract(uom_after_qty_pattern)

    # If missing, fallback to unit found inside capacity
    df['Unit of measure'] = df['Unit of measure'].fillna(
        df['Capacity'].str.extract(r'(PCS|SET|NOS)', expand=False)
    )

    # Default unit
    df['Unit of measure'] = df['Unit of measure'].fillna("PCS")


    # Default capacity: "1 <Unit>"
    df['Capacity'] = df.apply(
        lambda row: f"1 {row['Unit of measure']}" if pd.isna(row['Capacity']) else row['Capacity'],
        axis=1
    )


    # ------------ QTY ------------
    df['Qty'] = (
        df['GOODS DESCRIPTION']
        .str.extract(qty_pattern)[0]
        .str.replace(",", "")
        .astype(float)
    )

    # infer qty from capacity if missing
    df.loc[df['Qty'].isna(), 'Qty'] = (
        df.loc[df['Qty'].isna(), 'Capacity'].str.extract(r'(\d+)').astype(float)
    )


    # ------------ CLEANUP TEMP COLUMN ------------
    df.drop(columns=['Before_QTY'], inplace=True)


    # ------------ MODEL NAME CLEANING ------------
    def clean_model_name(desc):
        if pd.isna(desc):
            return None

        original = desc

        # remove anything after (QTY...)
        desc = re.split(r"\(QTY[:\s]", desc, maxsplit=1)[0]

        # remove content inside brackets
        desc = re.sub(r"\([^)]+\)", "", desc)

        # remove model number at start
        desc = re.sub(model_name_pattern + r"\s+", "", desc)

        # clean spaces
        desc = " ".join(desc.split()).strip()

        return desc if desc else original

    df["Model Name"] = df["GOODS DESCRIPTION"].apply(clean_model_name)

    return df
