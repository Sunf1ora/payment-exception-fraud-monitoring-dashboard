import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# Project 2 Day 4
# Generate payment monitoring summary datasets
# All data is simulated and used for portfolio practice only.
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

risk_flags_path = DATA_DIR / "payment_risk_flags.csv"
queue_path = DATA_DIR / "payment_investigation_queue.csv"

risk_df = pd.read_csv(risk_flags_path)
queue_df = pd.read_csv(queue_path)

# Ensure numeric fields
risk_df["amount"] = pd.to_numeric(risk_df["amount"], errors="coerce")
risk_df["risk_score"] = pd.to_numeric(risk_df["risk_score"], errors="coerce")

queue_df["amount"] = pd.to_numeric(queue_df["amount"], errors="coerce")
queue_df["risk_score"] = pd.to_numeric(queue_df["risk_score"], errors="coerce")
queue_df["days_open"] = pd.to_numeric(queue_df["days_open"], errors="coerce")
queue_df["overdue_flag"] = pd.to_numeric(queue_df["overdue_flag"], errors="coerce")
queue_df["second_review_required"] = pd.to_numeric(queue_df["second_review_required"], errors="coerce")

# ------------------------------------------------------------
# 1. Monitoring overview KPI table
# ------------------------------------------------------------

overview = pd.DataFrame([{
    "total_transactions": len(risk_df),
    "total_investigation_cases": len(queue_df),
    "high_risk_transactions": (risk_df["risk_level"] == "High").sum(),
    "medium_risk_transactions": (risk_df["risk_level"] == "Medium").sum(),
    "low_risk_transactions": (risk_df["risk_level"] == "Low").sum(),
    "critical_cases": (queue_df["investigation_priority"] == "Critical").sum(),
    "high_priority_cases": (queue_df["investigation_priority"] == "High").sum(),
    "overdue_cases": queue_df["overdue_flag"].sum(),
    "second_review_required_cases": queue_df["second_review_required"].sum(),
    "total_payment_amount": risk_df["amount"].sum(),
    "investigation_case_amount": queue_df["amount"].sum(),
    "average_risk_score": risk_df["risk_score"].mean(),
    "average_days_open": queue_df["days_open"].mean()
}])

overview_path = DATA_DIR / "payment_monitoring_overview.csv"
overview.to_csv(overview_path, index=False, encoding="utf-8-sig")

# ------------------------------------------------------------
# 2. Department risk summary
# ------------------------------------------------------------

department_summary = (
    risk_df
    .groupby("department")
    .agg(
        total_transactions=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean"),
        average_risk_score=("risk_score", "mean"),
        high_risk_transactions=("risk_level", lambda x: (x == "High").sum()),
        medium_risk_transactions=("risk_level", lambda x: (x == "Medium").sum()),
        large_amount_flags=("large_amount_flag", "sum"),
        high_risk_type_flags=("high_risk_type_flag", "sum"),
        duplicate_pattern_flags=("duplicate_pattern_flag", "sum"),
        year_end_flags=("year_end_flag", "sum")
    )
    .reset_index()
)

# Add investigation queue metrics by department
queue_department_summary = (
    queue_df
    .groupby("department")
    .agg(
        investigation_cases=("case_id", "count"),
        critical_cases=("investigation_priority", lambda x: (x == "Critical").sum()),
        high_priority_cases=("investigation_priority", lambda x: (x == "High").sum()),
        overdue_cases=("overdue_flag", "sum"),
        second_review_required_cases=("second_review_required", "sum"),
        average_days_open=("days_open", "mean")
    )
    .reset_index()
)

department_summary = department_summary.merge(
    queue_department_summary,
    on="department",
    how="left"
)

department_summary = department_summary.fillna(0)

department_summary["case_rate"] = (
    department_summary["investigation_cases"]
    / department_summary["total_transactions"]
)

department_summary = department_summary.sort_values(
    by=["critical_cases", "high_priority_cases", "average_risk_score", "total_amount"],
    ascending=[False, False, False, False]
)

department_summary_path = DATA_DIR / "department_risk_summary.csv"
department_summary.to_csv(department_summary_path, index=False, encoding="utf-8-sig")

# ------------------------------------------------------------
# 3. Transaction type risk summary
# ------------------------------------------------------------

transaction_type_summary = (
    risk_df
    .groupby("transaction_type")
    .agg(
        total_transactions=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean"),
        average_risk_score=("risk_score", "mean"),
        high_risk_transactions=("risk_level", lambda x: (x == "High").sum()),
        medium_risk_transactions=("risk_level", lambda x: (x == "Medium").sum()),
        large_amount_flags=("large_amount_flag", "sum"),
        high_risk_type_flags=("high_risk_type_flag", "sum"),
        duplicate_pattern_flags=("duplicate_pattern_flag", "sum"),
        year_end_flags=("year_end_flag", "sum")
    )
    .reset_index()
)

queue_type_summary = (
    queue_df
    .groupby("transaction_type")
    .agg(
        investigation_cases=("case_id", "count"),
        critical_cases=("investigation_priority", lambda x: (x == "Critical").sum()),
        high_priority_cases=("investigation_priority", lambda x: (x == "High").sum()),
        overdue_cases=("overdue_flag", "sum"),
        second_review_required_cases=("second_review_required", "sum"),
        average_days_open=("days_open", "mean")
    )
    .reset_index()
)

transaction_type_summary = transaction_type_summary.merge(
    queue_type_summary,
    on="transaction_type",
    how="left"
)

transaction_type_summary = transaction_type_summary.fillna(0)

transaction_type_summary["case_rate"] = (
    transaction_type_summary["investigation_cases"]
    / transaction_type_summary["total_transactions"]
)

transaction_type_summary = transaction_type_summary.sort_values(
    by=["critical_cases", "high_priority_cases", "average_risk_score", "total_amount"],
    ascending=[False, False, False, False]
)

transaction_type_summary_path = DATA_DIR / "transaction_type_risk_summary.csv"
transaction_type_summary.to_csv(transaction_type_summary_path, index=False, encoding="utf-8-sig")

# ------------------------------------------------------------
# 4. High priority case list
# ------------------------------------------------------------

high_priority_cases = queue_df[
    queue_df["investigation_priority"].isin(["Critical", "High"])
].copy()

high_priority_cases = high_priority_cases.sort_values(
    by=["investigation_priority_score", "risk_score", "amount", "days_open"],
    ascending=[False, False, False, False]
)

high_priority_cases_path = DATA_DIR / "high_priority_case_list.csv"
high_priority_cases.to_csv(high_priority_cases_path, index=False, encoding="utf-8-sig")

# ------------------------------------------------------------
# 5. Overdue case summary
# ------------------------------------------------------------

overdue_cases = queue_df[queue_df["overdue_flag"] == 1].copy()

overdue_summary = (
    overdue_cases
    .groupby(["department", "investigation_priority"])
    .agg(
        overdue_case_count=("case_id", "count"),
        overdue_amount=("amount", "sum"),
        average_days_open=("days_open", "mean"),
        max_days_open=("days_open", "max")
    )
    .reset_index()
    .sort_values(
        by=["overdue_case_count", "overdue_amount", "max_days_open"],
        ascending=[False, False, False]
    )
)

overdue_summary_path = DATA_DIR / "overdue_case_summary.csv"
overdue_summary.to_csv(overdue_summary_path, index=False, encoding="utf-8-sig")

# ------------------------------------------------------------
# Print summaries
# ------------------------------------------------------------

print("Payment monitoring summary datasets created successfully.")
print()

print("Files saved:")
print(f"- {overview_path}")
print(f"- {department_summary_path}")
print(f"- {transaction_type_summary_path}")
print(f"- {high_priority_cases_path}")
print(f"- {overdue_summary_path}")
print()

print("Monitoring overview:")
print(overview.T)
print()

print("Top departments by investigation cases:")
print(department_summary[[
    "department",
    "total_transactions",
    "investigation_cases",
    "critical_cases",
    "high_priority_cases",
    "overdue_cases",
    "average_risk_score"
]].head(10))
print()

print("Top transaction types by investigation cases:")
print(transaction_type_summary[[
    "transaction_type",
    "total_transactions",
    "investigation_cases",
    "critical_cases",
    "high_priority_cases",
    "overdue_cases",
    "average_risk_score"
]].head(10))
print()

print("High priority cases:", len(high_priority_cases))
print("Overdue cases:", len(overdue_cases))