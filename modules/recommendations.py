from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def generate_recommendations(context_type, data_summary):
    """
    Generic function that takes a data summary (as text) and asks Groq
    to generate specific, actionable business recommendations.

    context_type: a label like 'RFM Segmentation', 'Root Cause Analysis', 'KPI Performance'
    data_summary: a text summary of the relevant data/numbers
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    You are a senior business strategy consultant. Based on this {context_type} data,
    generate 3-4 specific, actionable business recommendations.

    Data:
    {data_summary}

    Rules:
    - Each recommendation must reference specific numbers from the data
    - Be concrete and actionable (not generic advice like "improve marketing")
    - Format as a numbered list
    - Each recommendation should be 1-2 sentences
    - Focus on what the business should DO next, not just what happened
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content

def recommendations_from_rfm(summary_df):
    """
    Build a data summary from RFM segment summary and generate recommendations.
    summary_df: the segment summary table from rfm.py (Segment, Customer_Count, Avg_CLV, Avg_Monetary)
    """
    data_summary = summary_df.to_string(index=False)
    return generate_recommendations("Customer RFM Segmentation", data_summary)

def recommendations_from_rca(rca_result):
    """
    Build a data summary from Root Cause Analysis results and generate recommendations.
    rca_result: the dict returned by analyze_period_change() in root_cause.py
    """
    metric = rca_result["metric"]
    metric_label = "Orders" if metric == "Order_ID" else metric

    category_breakdown = rca_result["breakdowns"]["Category"].to_string(index=False)
    region_breakdown = rca_result["breakdowns"]["Region"].to_string(index=False)

    data_summary = f"""
    Comparing {rca_result['period_a']} to {rca_result['period_b']}:
    Overall {metric_label} change: {rca_result['overall_change']:,.0f} ({rca_result['overall_pct_change']:.1f}%)

    Category Breakdown:
    {category_breakdown}

    Region Breakdown:
    {region_breakdown}
    """

    return generate_recommendations("Root Cause Analysis", data_summary)

def recommendations_from_kpis(kpis):
    """
    Build a data summary from Executive KPIs and generate recommendations.
    kpis: the dict returned by calculate_kpis() in kpi_dashboard.py
    """
    data_summary = f"""
    Total Revenue: ${kpis['total_revenue']:,.0f}
    Total Profit: ${kpis['total_profit']:,.0f}
    Year-over-Year Growth Rate: {kpis['growth_rate']:.1f}%
    Active Customers: {kpis['active_customers']:,}
    Average Order Value: ${kpis['avg_order_value']:,.2f}
    """

    return generate_recommendations("Executive KPI Performance", data_summary)