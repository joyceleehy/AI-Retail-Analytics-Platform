import pandas as pd
import sqlite3
from datetime import datetime

def load_customer_orders():
    """Pull order-level data needed for RFM calculation"""
    conn = sqlite3.connect("superstore.db")
    df = pd.read_sql("""
        SELECT Customer_ID, Customer_Name, Order_ID, Order_Date, Sales
        FROM orders
    """, conn)
    conn.close()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

def calculate_rfm(df):
    """
    Calculate Recency, Frequency, Monetary value per customer,
    then score each on a 1-4 scale and assign a segment label.
    """
    # Reference date = one day after the most recent order in the dataset
    # (simulates "today" for recency calculation)
    snapshot_date = df["Order_Date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby(["Customer_ID", "Customer_Name"]).agg(
        Recency=("Order_Date", lambda x: (snapshot_date - x.max()).days),
        Frequency=("Order_ID", "nunique"),
        Monetary=("Sales", "sum")
    ).reset_index()

    # Score each metric 1-4 using quartiles
    # Recency: lower days = better, so we reverse the scoring (4 = most recent)
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1, 2, 3, 4]).astype(int)

    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

    def assign_segment(row):
        if row["R_Score"] >= 3 and row["F_Score"] >= 3 and row["M_Score"] >= 3:
            return "Champion"
        elif row["R_Score"] >= 3 and row["F_Score"] >= 2:
            return "Loyal"
        elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
            return "At Risk"
        elif row["R_Score"] <= 2 and row["F_Score"] <= 2:
            return "Lost"
        else:
            return "Needs Attention"

    rfm["Segment"] = rfm.apply(assign_segment, axis=1)

    return rfm

def calculate_clv(rfm_df, df, estimated_lifespan_years=3):
    """
    Estimate Customer Lifetime Value using:
    CLV = Average Order Value x Purchase Frequency per Year x Estimated Lifespan

    Then tag each customer as High Value / Growth Potential / High Risk
    based on combined CLV and RFM segment.
    """
    rfm_df = rfm_df.copy()

    # Average order value per customer
    avg_order_value = rfm_df["Monetary"] / rfm_df["Frequency"]

    # Estimate how many orders per year based on their actual history span
    customer_span = df.groupby("Customer_ID")["Order_Date"].agg(
        first_order="min", last_order="max"
    )
    customer_span["Years_Active"] = (
        (customer_span["last_order"] - customer_span["first_order"]).dt.days / 365
    ).clip(lower=0.5)  # minimum 0.5 years to avoid divide-by-zero issues

    rfm_df = rfm_df.merge(customer_span[["Years_Active"]], on="Customer_ID")
    purchase_freq_per_year = rfm_df["Frequency"] / rfm_df["Years_Active"]

    rfm_df["CLV"] = avg_order_value * purchase_freq_per_year * estimated_lifespan_years

    def value_tier(row):
        if row["CLV"] >= rfm_df["CLV"].quantile(0.75) and row["Segment"] in ["Champion", "Loyal"]:
            return "High Value"
        elif row["Segment"] in ["At Risk", "Lost"]:
            return "High Risk"
        else:
            return "Growth Potential"

    rfm_df["Value_Tier"] = rfm_df.apply(value_tier, axis=1)

    return rfm_df

def get_segmentation_summary(rfm_df):
    """Aggregate segment counts and average CLV for dashboard display"""
    summary = rfm_df.groupby("Segment").agg(
        Customer_Count=("Customer_ID", "count"),
        Avg_CLV=("CLV", "mean"),
        Avg_Monetary=("Monetary", "mean")
    ).reset_index().sort_values("Avg_CLV", ascending=False)

    return summary

def get_full_rfm_analysis():
    """Main function tying everything together"""
    df = load_customer_orders()
    rfm = calculate_rfm(df)
    rfm_with_clv = calculate_clv(rfm, df)
    summary = get_segmentation_summary(rfm_with_clv)

    return {
        "rfm_data": rfm_with_clv,
        "summary": summary
    }