import pandas as pd


def feature_engineering(df: pd.DataFrame):

    # --------------------------------------------------
    # 1. Correct column names for safe access
    # --------------------------------------------------
    TOTAL_VALUE_COL = "TOTAL VALUE_INR"
    DUTY_PAID_COL = "DUTY PAID_INR"

    # Grand Total = Total Value + Duty Paid
    df["Grand Total (INR)"] = df[TOTAL_VALUE_COL] + df[DUTY_PAID_COL]

    # --------------------------------------------------
    # 2. CATEGORY ASSIGNMENT
    # --------------------------------------------------
    def assign_category(text):
        if pd.isna(text):
            return None

        t = text.upper()

        if "GLASS" in t:
            return "Glass"
        if "STEEL" in t:  # Catch all types of steel under one main category
            return "Steel"
        if "PLASTIC" in t:
            return "Plastic"
        if "WOOD" in t or "WOODEN" in t:
            return "Wooden"
        if "POLYHOUSE" in t:
            return "Polyhouse"
        if "ELECTRONIC" in t:
            return "Electronics"

        return "Others"


    def assign_sub_category(text, category):
        
        if pd.isna(text):
            return None

        t = text.upper()

        if category == "Glass":
            if "BOROSILICATE" in t:
                return "Borosilicate"
            if "OPAL" in t:
                return "Opalware"
            return "General Glass"

        if category == "Steel":
            # Steel subtypes
            if "MILD STEEL" in t:
                return "Mild Steel"
            if "HOUSEHOLD STEEL" in t:
                return "Household Steel"
            if "SS" in t:
                return "Stainless Steel"
            if "SCRUBBER" in t:
                return "Scrubber"
            if "STRAINER" in t:
                return "Strainer"
            if "BASKET" in t:
                return "Basket"
            return "General Steel"

        if category == "Wooden":
            if "SPOON" in t:
                return "Spoon"
            if "FORK" in t:
                return "Fork"
            return "Wooden Item"

        if category == "Plastic":
            if "BOTTLE" in t:
                return "Bottle"
            return "Plastic Item"

        return "Misc"


    df["Sub-Category"] = df.apply(
        lambda row: assign_sub_category(row["GOODS DESCRIPTION"], row["Category"]),
        axis=1
    )

    # --------------------------------------------------
    # 4. LANDED COST PER UNIT
    # --------------------------------------------------
    df["landed_cost_per_unit"] = df["Grand Total (INR)"] / df["Qty"].replace(0, pd.NA)

    return df


def save_processed(df: pd.DataFrame, path="../data/processed/trade_cleaned.csv"):
    df.to_csv(path, index=False)
    print(f"Saved processed file to: {path}")
