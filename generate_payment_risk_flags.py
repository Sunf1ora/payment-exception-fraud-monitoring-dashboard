import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------------------------
# Project 2 Day 2
# Generate rule-based payment risk flags
# All data is simulated and used for portfolio practice only.
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

input_path = DATA_DIR / "payment_transactions.csv"
output_path = DATA_DIR / "payment_risk_flags.csv"

# Read simulated payment transactions
transactions = pd.read_csv(input_path)

# Make a working copy
df = transactions.copy()

# Ensure amount is numeric
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Ensure date is datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ------------------------------------------------------------
# Rule 1: Large amount flag
# A transaction is flagged if its amount is above the 90th percentile
# within the same transaction type.
# ------------------------------------------------------------

type_thresholds = (
    df.groupby("transaction_type")["amount"]
    .quantile(0.90)
    .reset_index()
    .rename(columns={"amount": "type_amount_90th_percentile"})
)

df = df.merge(type_thresholds, on="transaction_type", how="left")

df["large_amount_flag"] = np.where(
    df["amount"] > df["type_amount_90th_percentile"],
    1,
    0
)

# ------------------------------------------------------------
# Rule 2: High-risk transaction type flag
# These transaction types normally require closer review.
# ------------------------------------------------------------

high_risk_transaction_types = [
    "off_budget_fund_transfer",
    "temporary_holding",
    "inter_fund_transfer",
    "audit_adjustment",
    "year_end_settlement"
]

df["high_risk_type_flag"] = np.where(
    df["transaction_type"].isin(high_risk_transaction_types),
    1,
    0
)

# ------------------------------------------------------------
# Rule 3: Duplicate pattern flag
# Same department + transaction type + amount appearing more than once.
# This is a simplified duplicate payment risk rule.
# ------------------------------------------------------------

duplicate_keys = [
    "department",
    "transaction_type",
    "amount"
]

duplicate_counts = (
    df.groupby(duplicate_keys)
    .size()
    .reset_index(name="duplicate_group_count")
)

df = df.merge(duplicate_counts, on=duplicate_keys, how="left")

df["duplicate_pattern_flag"] = np.where(
    df["duplicate_group_count"] > 1,
    1,
    0
)

# ------------------------------------------------------------
# Rule 4: Year-end transaction flag
# December transactions may require additional review because of
# year-end settlement and reporting pressure.
# ------------------------------------------------------------

df["year_end_flag"] = np.where(
    df["month"] == 12,
    1,
    0
)

# ------------------------------------------------------------
# Rule 5: Department activity risk flag
# Departments with transaction count above the 75th percentile are flagged.
# ------------------------------------------------------------

department_counts = (
    df.groupby("department")
    .size()
    .reset_index(name="department_transaction_count")
)

department_threshold = department_counts["department_transaction_count"].quantile(0.75)

department_counts["department_risk_flag"] = np.where(
    department_counts["department_transaction_count"] > department_threshold,
    1,
    0
)

df = df.merge(
    department_counts[["department", "department_transaction_count", "department_risk_flag"]],
    on="department",
    how="left"
)

# ------------------------------------------------------------
# Create total risk score
# ------------------------------------------------------------

df["risk_score"] = (
    df["large_amount_flag"] * 3
    + df["high_risk_type_flag"] * 2
    + df["duplicate_pattern_flag"] * 3
    + df["year_end_flag"] * 1
    + df["department_risk_flag"] * 1
)

# ------------------------------------------------------------
# Assign risk level
# ------------------------------------------------------------

def assign_risk_level(score):
    if score >= 6:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"

df["risk_level"] = df["risk_score"].apply(assign_risk_level)

# ------------------------------------------------------------
# Recommended action
# ------------------------------------------------------------

def recommend_action(row):
    if row["risk_level"] == "High":
        return "Immediate review required"
    elif row["large_amount_flag"] == 1:
        return "Review transaction amount and supporting documents"
    elif row["duplicate_pattern_flag"] == 1:
        return "Check potential duplicate payment pattern"
    elif row["high_risk_type_flag"] == 1:
        return "Second-level review recommended"
    elif row["year_end_flag"] == 1:
        return "Check year-end classification and approval"
    else:
        return "Routine monitoring"

df["recommended_action"] = df.apply(recommend_action, axis=1)

# ------------------------------------------------------------
# Create readable risk flag summary
# ------------------------------------------------------------

def build_flag_summary(row):
    flags = []

    if row["large_amount_flag"] == 1:
        flags.append("large_amount")
    if row["high_risk_type_flag"] == 1:
        flags.append("high_risk_type")
    if row["duplicate_pattern_flag"] == 1:
        flags.append("duplicate_pattern")
    if row["year_end_flag"] == 1:
        flags.append("year_end")
    if row["department_risk_flag"] == 1:
        flags.append("high_activity_department")

    if not flags:
        return "no_major_flag"

    return "; ".join(flags)

df["risk_flag_summary"] = df.apply(build_flag_summary, axis=1)

# ------------------------------------------------------------
# Export result
# ------------------------------------------------------------

df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("payment_risk_flags.csv has been created successfully.")
print(f"File saved to: {output_path}")
print()

print("Number of transactions:", len(df))
print()

print("Risk level summary:")
print(df["risk_level"].value_counts())
print()

print("Risk flag summary:")
print(df[[
    "large_amount_flag",
    "high_risk_type_flag",
    "duplicate_pattern_flag",
    "year_end_flag",
    "department_risk_flag"
]].sum())
print()

print("Preview:")
print(df[[
    "transaction_id",
    "date",
    "department",
    "transaction_type",
    "amount",
    "risk_score",
    "risk_level",
    "risk_flag_summary",
    "recommended_action"
]].head(10))