import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

print("Project 2 environment is ready.")
print("Base directory:", BASE_DIR)
print("Data directory:", DATA_DIR)
print("pandas version:", pd.__version__)
print("numpy version:", np.__version__)

input_path = DATA_DIR / "payment_transactions.csv"

if input_path.exists():
    df = pd.read_csv(input_path)
    print("payment_transactions.csv loaded successfully.")
    print("Number of rows:", len(df))
    print("Columns:", list(df.columns))
    print(df.head())
else:
    print("payment_transactions.csv not found. Please copy transactions.csv from Project 1 and rename it.")