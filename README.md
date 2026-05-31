# Payment Exception & Fraud Monitoring Dashboard

## 1. Project Overview

This project simulates a payment exception and fraud monitoring workflow for finance, treasury and risk operations teams. It uses simulated payment transaction data to identify unusual payment patterns, missing documentation, duplicate payments, large-value outliers, high-risk transfer activities and unresolved review items.

The project is inspired by my professional experience in treasury operations, voucher verification, payment discrepancy investigation, audit support and internal controls.

All data used in this project is simulated. No confidential, real government, bank, audit, voucher, department, account or transaction data is used.

## 2. Business Problem

Finance and risk operations teams need to monitor payment transactions for potential exceptions and control risks. Common issues include duplicate payments, missing supporting documents, abnormal transaction amounts, unusual transfer patterns and unresolved investigation items.

A structured payment monitoring workflow can help prioritise high-risk items, support investigation queues and improve internal control follow-up.

## 3. Tools Used

- Python
- pandas
- SQL
- SQLite
- Tableau Public
- Excel / CSV files
- VS Code

## 4. Planned Workflow

1. Prepare simulated payment transaction data.
2. Define rule-based risk indicators.
3. Flag payment exceptions using Python and SQL.
4. Build an investigation queue with risk scores and priority levels.
5. Create Tableau dashboards for payment risk monitoring and exception follow-up.

## 5. Planned Exception Rules

The project will identify rule-based payment exceptions, including:

- Duplicate payment patterns
- Missing voucher or supporting document indicators
- Unusually large payment amounts
- High-risk fund transfer patterns
- Transactions requiring second-level review
- Repeated exceptions by department
- Unresolved or pending review items

## 6. Planned Dashboard Outputs

The final dashboard will include:

- Payment risk overview
- Exception count by risk rule
- High-risk transaction queue
- Exception amount by department
- Recommended investigation actions
- Interactive filters by risk type, department and priority

## 7. Dashboard Outputs

### Payment Risk Overview

![Payment Risk Overview](tableau/dashboard_payment_risk_overview.png)

### High-Risk Investigation Queue

![High-Risk Investigation Queue](tableau/dashboard_investigation_queue.png)


## 8. Confidentiality Statement

This project does not use any real government, bank, audit, voucher, account, department or transaction data. All datasets are simulated for portfolio purposes. The project is designed to demonstrate payment exception monitoring, fraud-risk thinking, internal control analytics and dashboard reporting skills without disclosing any confidential information.

## 9. Project Development Log

### Day 1 Log

Created the project folder structure, prepared the README file, copied simulated payment transaction data from the treasury reconciliation project and tested the Python environment.

### Day 2 Log

Created the first version of rule-based payment risk flags using Python and pandas. The rules identify large-amount transactions, high-risk transaction types, duplicate payment patterns, year-end transactions and high-activity departments.

A risk score and risk level were created for each transaction, along with a recommended investigation action and a readable risk flag summary. The output file is saved as `data/payment_risk_flags.csv`.

### Day 3 Log

Created an investigation queue based on the payment risk flags generated on Day 2. Transactions with medium or high risk levels, large amount flags, duplicate patterns or high-risk transaction types were selected for follow-up review.

The investigation queue includes case IDs, case owners, case status, days open, overdue flags, second-review indicators, investigation priority levels, investigation notes and follow-up actions.

The output file is saved as `data/payment_investigation_queue.csv`. This dataset will be used to build Tableau dashboards for payment risk monitoring and investigation queue management.

### Day 4 Log

Generated payment monitoring summary datasets for dashboard preparation. The summaries include management-level overview metrics, department-level risk summaries, transaction-type risk summaries, high-priority case lists and overdue case summaries.

These outputs were created from `payment_risk_flags.csv` and `payment_investigation_queue.csv`. The summary tables will be used as Tableau data sources for the payment exception and fraud monitoring dashboard.

The output files include `payment_monitoring_overview.csv`, `department_risk_summary.csv`, `transaction_type_risk_summary.csv`, `high_priority_case_list.csv` and `overdue_case_summary.csv`.

### Day 5 Log

Created the first Tableau dashboard page for the payment exception and fraud monitoring project: Payment Risk Monitoring Overview.

The dashboard includes KPI cards for total transactions, investigation cases, critical cases and overdue cases. It also includes charts showing investigation cases by department, investigation cases by transaction type and case counts by investigation priority.

This dashboard page is designed to provide a management-level overview of payment risk monitoring results and support prioritisation of investigation resources.

### Day 6 Log

Created the second Tableau dashboard page for the payment exception and fraud monitoring project: High-Risk Payment Investigation Queue.

This dashboard focuses on critical, high-priority and overdue payment exception cases. It includes a high-priority case list, overdue cases by department, investigation case workload by owner, average days open by priority and case status breakdown.

The purpose of this dashboard page is to support investigation queue management, escalation review and follow-up prioritisation for payment risk monitoring.

The dashboard screenshot is saved as `tableau/dashboard_investigation_queue.png`.