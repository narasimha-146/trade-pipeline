import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

postgres_url = os.getenv("POSTGRESQL_URL")
engine = create_engine(postgres_url)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
csv_path = os.path.join(BASE_DIR, "data", "processed", "trade_cleaned.csv")

df = pd.read_csv(csv_path)
df.to_sql("shipments", engine, if_exists="replace", index=False)

print("Data loaded successfully!")
