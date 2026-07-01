import pandas as pd
import sqlite3
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def load_data():
    """Pull all order data from SQLite into a DataFrame"""
    conn = sqlite3.connect("superstore.db")
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

def calculate_kpis(df):
    """
    Calculate the 5 core executive KPIs.
    We compare the most recent year vs the previous year for growth rate.
    """
    total_revenue = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    active_customers = df["Customer_ID"].nunique()
    avg_order_value = df.groupby("Order_ID")["Sales"].sum().mean()

    # Growth rate: compare latest year vs previous year revenue
    df["Year"] = df["Order_Date"].dt.year
    yearly_revenue = df.groupby("Year")["Sales"].sum().sort_index()

    if len(yearly_revenue) >= 2:
        latest_year_rev = yearly_revenue.iloc[-1]
        prev_year_rev = yearly_revenue.iloc[-2]
        growth_rate = ((latest_year_rev - prev_year_rev) / prev_year_rev) * 100
    else:
        growth_rate = 0

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "growth_rate": growth_rate,
        "active_customers": active_customers,
        "avg_order_value": avg_order_value,
        "yearly_revenue": yearly_revenue
    }

def generate_ai_summary(kpis):
    """
    Send the KPI numbers to Groq and get back a 3-sentence
    executive summary, written like a business analyst would.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    You are a senior business analyst writing an executive summary.
    Based on these KPIs, write a concise 3-sentence summary of business performance.
    Be specific with numbers. Mention one strength and one area of concern.

    Total Revenue: ${kpis['total_revenue']:,.0f}
    Total Profit: ${kpis['total_profit']:,.0f}
    Year-over-Year Growth Rate: {kpis['growth_rate']:.1f}%
    Active Customers: {kpis['active_customers']:,}
    Average Order Value: ${kpis['avg_order_value']:,.2f}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content