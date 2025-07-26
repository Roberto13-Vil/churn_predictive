# 📉 Churn Prediction in Telecom Customers (Iranian Dataset)

A complete churn prediction project using a telecom dataset from the UC Irvine Machine Learning Repository.  
Includes data preprocessing, model training, and an interactive Streamlit dashboard with storytelling-driven visualizations.

---

## 📌 Project Overview

Churn — when a customer stops using a service — is a major concern in the telecom industry.  
This project explores customer behavior using a real-world dataset from an Iranian telecom company to predict churn and extract actionable insights.

---

## 📊 Dataset Information

- **Source**: [UC Irvine Machine Learning Repository – Iranian Churn Dataset](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset)
- **Rows**: 3,150 customers  
- **Features**:
  - `Call Failures`, `Frequency of SMS`, `Number of Complaints`, `Subscription Length`
  - `Distinct Calls`, `Charge Amount`, `Seconds of Use`
  - `Type of Service`, `Age Group`, `Customer Status`, etc.
- **Target**: `Churn` (1 = Yes, 0 = No)

⏳ **Temporal setup**:
- All features are aggregated over the **first 9 months**.
- The churn label reflects customer status at **month 12** (3-month planning gap).

---

## 🎯 Objectives

1. **Understand key drivers** of churn through EDA.
2. **Train and evaluate** multiple classification models.
3. Apply **feature importance and explainable AI** tools (e.g., SHAP).
4. Deploy an **interactive Streamlit dashboard** to explore results and segment customer behavior.

---

## 🧰 Tech Stack