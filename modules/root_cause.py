import pandas as pd
import sqlite3

def load_orders_for_rca():
    """Pull order data needed for root cause analysis"""
    conn = sqlite3.connect("superstore.db")
    df = pd.read_sql("""
        SELECT Order_Date, Category, Sub_Category, Region, Segment, 
               Sales, Profit, Order_ID
        FROM orders
    """, conn)
    conn.close()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

def get_available_months(df):
    """Return a sorted list of all Year-Month periods available in the data"""
    months = df["Order_Date"].dt.to_period("M").unique()
    months = sorted(months)
    return [str(m) for m in months]

def analyze_period_change(df, period_a, period_b, metric="Sales"):
    """
    Compare two time periods (format: 'YYYY-MM') and break down
    the change by Category, Region, and Segment.

    metric: 'Sales', 'Profit', or 'Order_ID' (count of orders)
    """
    df = df.copy()
    df["Period"] = df["Order_Date"].dt.to_period("M").astype(str)

    df_a = df[df["Period"] == period_a]
    df_b = df[df["Period"] == period_b]

    # Overall totals
    if metric == "Order_ID":
        total_a = df_a["Order_ID"].nunique()
        total_b = df_b["Order_ID"].nunique()
    else:
        total_a = df_a[metric].sum()
        total_b = df_b[metric].sum()

    overall_change = total_b - total_a
    overall_pct_change = (overall_change / total_a * 100) if total_a != 0 else 0

    # Breakdown by each dimension
    breakdowns = {}
    for dimension in ["Category", "Region", "Segment"]:
        if metric == "Order_ID":
            agg_a = df_a.groupby(dimension)["Order_ID"].nunique()
            agg_b = df_b.groupby(dimension)["Order_ID"].nunique()
        else:
            agg_a = df_a.groupby(dimension)[metric].sum()
            agg_b = df_b.groupby(dimension)[metric].sum()

        combined = pd.DataFrame({
            f"{period_a}": agg_a,
            f"{period_b}": agg_b
        }).fillna(0)

        combined["Change"] = combined[f"{period_b}"] - combined[f"{period_a}"]
        combined["Contribution_to_Change"] = combined["Change"]
        combined = combined.sort_values("Change")

        breakdowns[dimension] = combined.reset_index()

    return {
        "period_a": period_a,
        "period_b": period_b,
        "metric": metric,
        "total_a": total_a,
        "total_b": total_b,
        "overall_change": overall_change,
        "overall_pct_change": overall_pct_change,
        "breakdowns": breakdowns
    }

def get_top_contributors(rca_result, dimension="Category", top_n=3):
    """
    Returns the top N positive and negative contributors
    for a given dimension (used for AI recommendation prompts later)
    """
    df = rca_result["breakdowns"][dimension]
    biggest_decline = df.nsmallest(top_n, "Change")
    biggest_growth = df.nlargest(top_n, "Change")
    return biggest_decline, biggest_growth
