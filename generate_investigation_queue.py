import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------------------------
# Project 2 Day 3
# Generate investigation queue for payment exception monitoring
# All data is simulated and used for portfolio practice only.
# ------------------------------------------------------------

np.random.seed(52)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

input_path = DATA_DIR / "payment_risk_flags.csv"
output_path = DATA_DIR / "payment_investigation_queue.csv"

# Read risk-flagged payment transactions from Day 2
df = pd.read_csv(input_path)

# Ensure date is datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ------------------------------------------------------------
# Select transactions for investigation
# We include:
# - High risk transactions
# - Medium risk transactions
# - Any large amount transactions
# - Any duplicate pattern transactions
# - Any high-risk type transactions
# ------------------------------------------------------------

investigation_df = df[
    (df["risk_level"].isin(["High", "Medium"]))
    | (df["large_amount_flag"] == 1)
    | (df["duplicate_pattern_flag"] == 1)
    | (df["high_risk_type_flag"] == 1)
].copy()

investigation_df = investigation_df.reset_index(drop=True)

# ------------------------------------------------------------
# Create investigation case IDs
# ------------------------------------------------------------

investigation_df.insert(
    0,
    "case_id",
    [f"CASE{i + 1:05d}" for i in range(len(investigation_df))]
)

# ------------------------------------------------------------
# Assign case owners
# ------------------------------------------------------------

case_owners = [
    "Risk Analyst A",
    "Risk Analyst B",
    "Controls Reviewer",
    "Finance Operations Reviewer",
    "Senior Review Officer"
]

investigation_df["case_owner"] = np.random.choice(
    case_owners,
    size=len(investigation_df),
    p=[0.25, 0.25, 0.20, 0.20, 0.10]
)

# ------------------------------------------------------------
# Assign investigation status
# ------------------------------------------------------------

def assign_case_status(risk_level):
    if risk_level == "High":
        return np.random.choice(
            ["open", "investigating", "escalated", "closed"],
            p=[0.30, 0.40, 0.20, 0.10]
        )
    elif risk_level == "Medium":
        return np.random.choice(
            ["open", "investigating", "closed"],
            p=[0.35, 0.35, 0.30]
        )
    else:
        return np.random.choice(
            ["open", "closed"],
            p=[0.40, 0.60]
        )

investigation_df["case_status"] = investigation_df["risk_level"].apply(assign_case_status)

# ------------------------------------------------------------
# Create days open
# High-risk cases tend to stay open longer.
# Closed cases have fewer days open.
# ------------------------------------------------------------

def assign_days_open(row):
    if row["case_status"] == "closed":
        return np.random.randint(1, 8)
    if row["risk_level"] == "High":
        return np.random.randint(3, 31)
    if row["risk_level"] == "Medium":
        return np.random.randint(2, 21)
    return np.random.randint(1, 14)

investigation_df["days_open"] = investigation_df.apply(assign_days_open, axis=1)

# ------------------------------------------------------------
# Overdue flag
# A case is overdue if:
# - High risk and open more than 7 days
# - Medium risk and open more than 14 days
# ------------------------------------------------------------

investigation_df["overdue_flag"] = np.where(
    (
        (investigation_df["risk_level"] == "High")
        & (investigation_df["case_status"] != "closed")
        & (investigation_df["days_open"] > 7)
    )
    | (
        (investigation_df["risk_level"] == "Medium")
        & (investigation_df["case_status"] != "closed")
        & (investigation_df["days_open"] > 14)
    ),
    1,
    0
)

# ------------------------------------------------------------
# Second review required
# ------------------------------------------------------------

investigation_df["second_review_required"] = np.where(
    (investigation_df["risk_level"] == "High")
    | (investigation_df["risk_score"] >= 6)
    | (investigation_df["overdue_flag"] == 1),
    1,
    0
)

# ------------------------------------------------------------
# Investigation priority
# ------------------------------------------------------------

def assign_investigation_priority(row):
    if row["risk_level"] == "High" and row["overdue_flag"] == 1:
        return "Critical"
    if row["risk_level"] == "High":
        return "High"
    if row["risk_level"] == "Medium" and row["overdue_flag"] == 1:
        return "High"
    if row["risk_level"] == "Medium":
        return "Medium"
    return "Low"

investigation_df["investigation_priority"] = investigation_df.apply(
    assign_investigation_priority,
    axis=1
)

# ------------------------------------------------------------
# Investigation note
# ------------------------------------------------------------

def build_investigation_note(row):
    notes = []

    if row["large_amount_flag"] == 1:
        notes.append("large amount transaction")
    if row["duplicate_pattern_flag"] == 1:
        notes.append("possible duplicate payment pattern")
    if row["high_risk_type_flag"] == 1:
        notes.append("high-risk transaction type")
    if row["year_end_flag"] == 1:
        notes.append("year-end transaction")
    if row["department_risk_flag"] == 1:
        notes.append("high-activity department")
    if row["overdue_flag"] == 1:
        notes.append("overdue review item")

    if not notes:
        return "Routine review case"

    return "; ".join(notes)

investigation_df["investigation_note"] = investigation_df.apply(
    build_investigation_note,
    axis=1
)

# ------------------------------------------------------------
# Follow-up action
# ------------------------------------------------------------

def assign_follow_up_action(row):
    if row["investigation_priority"] == "Critical":
        return "Escalate to senior reviewer immediately"
    if row["second_review_required"] == 1:
        return "Send for second-level review"
    if row["duplicate_pattern_flag"] == 1:
        return "Check duplicate payment evidence"
    if row["large_amount_flag"] == 1:
        return "Request supporting documents for large payment"
    if row["high_risk_type_flag"] == 1:
        return "Review approval workflow and transaction purpose"
    return "Continue routine monitoring"

investigation_df["follow_up_action"] = investigation_df.apply(
    assign_follow_up_action,
    axis=1
)

# ------------------------------------------------------------
# Sort queue: Critical / High first, then risk score and amount
# ------------------------------------------------------------

priority_order = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}

investigation_df["investigation_priority_score"] = investigation_df[
    "investigation_priority"
].map(priority_order)

investigation_df = investigation_df.sort_values(
    by=["investigation_priority_score", "risk_score", "amount", "days_open"],
    ascending=[False, False, False, False]
).reset_index(drop=True)

# Reassign case IDs after sorting
investigation_df["case_id"] = [
    f"CASE{i + 1:05d}" for i in range(len(investigation_df))
]

# Export
investigation_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("payment_investigation_queue.csv has been created successfully.")
print(f"File saved to: {output_path}")
print()

print("Number of investigation cases:", len(investigation_df))
print()

print("Investigation priority summary:")
print(investigation_df["investigation_priority"].value_counts())
print()

print("Case status summary:")
print(investigation_df["case_status"].value_counts())
print()

print("Overdue cases:", investigation_df["overdue_flag"].sum())
print("Second review required:", investigation_df["second_review_required"].sum())
print()

print("Preview:")
print(investigation_df[[
    "case_id",
    "transaction_id",
    "date",
    "department",
    "transaction_type",
    "amount",
    "risk_score",
    "risk_level",
    "investigation_priority",
    "case_status",
    "days_open",
    "overdue_flag",
    "follow_up_action"
]].head(10))