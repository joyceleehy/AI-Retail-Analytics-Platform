import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
import subprocess
from modules.kpi_dashboard import load_data, calculate_kpis, generate_ai_summary
from modules.ai_agent import ask_question
from modules.forecasting import get_full_forecast
from modules.rfm import get_full_rfm_analysis
from modules.root_cause import load_orders_for_rca, get_available_months, analyze_period_change
from modules.recommendations import recommendations_from_rfm, recommendations_from_rca
from modules.report_generator import generate_excel_report

# Auto-create database if it doesn't exist (e.g. on Streamlit Cloud)
if not os.path.exists("superstore.db"):
    subprocess.run(["python", "data_loader.py"], check=True)

st.set_page_config(
    page_title="AI Retail Analytics Platform",
    page_icon="📊",
    layout="wide"
)


st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["Executive Dashboard", "AI Insights Agent", "Sales Forecasting", "Customer Segmentation (RFM)", "Root Cause Analysis"]
)

@st.cache_data
def get_data():
    return load_data()

@st.cache_data
def get_rfm_data():
    return get_full_rfm_analysis()

@st.cache_data
def get_rca_data():
    return load_orders_for_rca()

# ============================================
# PAGE 1: Executive Dashboard
# ============================================
if page == "Executive Dashboard":
    st.title("📊 AI-Powered Retail Analytics Platform")
    st.caption("Executive Dashboard — Superstore Sales Performance")

    df = get_data()
    kpis = calculate_kpis(df)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Revenue", f"${kpis['total_revenue']:,.0f}")
    col2.metric("Total Profit", f"${kpis['total_profit']:,.0f}")
    col3.metric("YoY Growth", f"{kpis['growth_rate']:.1f}%")
    col4.metric("Active Customers", f"{kpis['active_customers']:,}")
    col5.metric("Avg Order Value", f"${kpis['avg_order_value']:,.2f}")

    st.divider()
    st.subheader("Revenue by Year")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=kpis['yearly_revenue'].index.astype(str),
        y=kpis['yearly_revenue'].values,
        marker_color="#2E86AB"
    ))
    fig.update_layout(xaxis_title="Year", yaxis_title="Revenue ($)", height=400)
    st.plotly_chart(fig, width='stretch')

    st.divider()
    st.subheader("🤖 AI Executive Summary")

    if st.button("Generate Summary"):
        with st.spinner("Analyzing business performance..."):
            summary = generate_ai_summary(kpis)
            st.success(summary)

    st.divider()
    st.subheader("📥 Download Full Report")
    st.write("Generate a multi-sheet Excel report with KPIs, customer segmentation, sales forecast, and root cause analysis (if available).")

    if st.button("Generate Excel Report"):
        with st.spinner("Building report..."):
            rfm_result = get_rfm_data()
            forecast_result = get_full_forecast(months_ahead=3)

            rca_breakdown = None
            if "rca_result" in st.session_state:
                rca_breakdown = st.session_state.rca_result["breakdowns"]["Category"]

            excel_buffer = generate_excel_report(
                kpis=kpis,
                rfm_summary=rfm_result["summary"],
                forecast_df=forecast_result["base_forecast"],
                rca_category_breakdown=rca_breakdown
            )

            st.download_button(
                label="📥 Download Excel Report",
                data=excel_buffer,
                file_name="retail_analytics_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# ============================================
# PAGE 2: AI Insights Agent
# ============================================
elif page == "AI Insights Agent":
    st.title("🤖 AI Insights Agent")
    st.caption("Ask questions about your sales data in plain English")

    if "question_input" not in st.session_state:
        st.session_state.question_input = ""

    st.write("**Try a sample question:**")
    sample_col1, sample_col2, sample_col3 = st.columns(3)

    if sample_col1.button("Top 5 products by sales"):
        st.session_state.question_input = "What are the top 5 products by total sales?"
        st.rerun()
    if sample_col2.button("Which region has highest profit?"):
        st.session_state.question_input = "Which region has the highest total profit?"
        st.rerun()
    if sample_col3.button("Sales by customer segment"):
        st.session_state.question_input = "What is the total sales by customer segment?"
        st.rerun()

    question = st.text_input(
        "Or type your own question:",
        key="question_input"
    )

    if st.button("Ask") and question:
        with st.spinner("Thinking..."):
            result = ask_question(question)

        if result["error"]:
            st.error(f"Something went wrong: {result['error']}")
        else:
            st.subheader("🤖 Insight")
            st.success(result["insight"])

            with st.expander("📊 View Data"):
                st.dataframe(result["result_df"], width='stretch')

            with st.expander("🔍 View Generated SQL"):
                st.code(result["sql"], language="sql")

# ============================================
# PAGE 3: Sales Forecasting
# ============================================
elif page == "Sales Forecasting":
    st.title("📈 Sales Forecasting")
    st.caption("Predicting next 3 months revenue using historical trends")

    st.subheader("🎛️ Scenario Simulator")
    st.write("Adjust the sliders to test 'what if' business assumptions:")

    sim_col1, sim_col2 = st.columns(2)
    sales_growth = sim_col1.slider("What if sales grow by (%)", -20, 50, 0)
    retention_improvement = sim_col2.slider("What if retention improves by (%)", -20, 50, 0)

    result = get_full_forecast(
        months_ahead=3,
        sales_growth_pct=sales_growth,
        retention_improvement_pct=retention_improvement
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=result["historical"]["Month"],
        y=result["historical"]["Sales"],
        mode="lines+markers",
        name="Actual",
        line=dict(color="#2E86AB")
    ))

    fig.add_trace(go.Scatter(
        x=result["base_forecast"]["Month"],
        y=result["base_forecast"]["Sales"],
        mode="lines+markers",
        name="Base Forecast",
        line=dict(color="#F77F00", dash="dash")
    ))

    if result["adjusted_forecast"] is not None:
        fig.add_trace(go.Scatter(
            x=result["adjusted_forecast"]["Month"],
            y=result["adjusted_forecast"]["Sales"],
            mode="lines+markers",
            name="Adjusted Forecast (Scenario)",
            line=dict(color="#06A77D", dash="dot")
        ))

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )

    st.plotly_chart(fig, width='stretch')

    st.divider()
    st.subheader("📋 Forecast Summary")

    display_df = result["base_forecast"][["Month", "Sales"]].copy()
    display_df["Month"] = display_df["Month"].dt.strftime("%B %Y")
    display_df = display_df.rename(columns={"Sales": "Base Forecast ($)"})

    if result["adjusted_forecast"] is not None:
        display_df["Adjusted Forecast ($)"] = result["adjusted_forecast"]["Sales"].values

    st.dataframe(display_df, width='stretch')

# ============================================
# PAGE 4: Customer Segmentation (RFM + CLV)
# ============================================
elif page == "Customer Segmentation (RFM)":
    st.title("👥 Customer Segmentation")
    st.caption("RFM Analysis + Customer Lifetime Value Estimation")

    rfm_result = get_rfm_data()
    rfm_data = rfm_result["rfm_data"]
    summary = rfm_result["summary"]

    st.subheader("Segment Distribution")

    col1, col2 = st.columns([1, 1])

    with col1:
        fig_pie = px.pie(
            summary,
            values="Customer_Count",
            names="Segment",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, width='stretch')

    with col2:
        fig_bar = px.bar(
            summary,
            x="Segment",
            y="Avg_CLV",
            color="Segment",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_bar.update_layout(
            height=400,
            yaxis_title="Average CLV ($)",
            showlegend=False
        )
        st.plotly_chart(fig_bar, width='stretch')

    st.divider()
    st.subheader("Customer Distribution: Frequency vs Spending")

    fig_scatter = px.scatter(
        rfm_data,
        x="Frequency",
        y="Monetary",
        color="Segment",
        size="CLV",
        hover_data=["Customer_Name", "Recency", "CLV"],
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_scatter.update_layout(height=450)
    st.plotly_chart(fig_scatter, width='stretch')

    st.divider()
    st.subheader("📋 Customer Details")

    segment_filter = st.multiselect(
        "Filter by Segment",
        options=rfm_data["Segment"].unique(),
        default=rfm_data["Segment"].unique()
    )

    filtered = rfm_data[rfm_data["Segment"].isin(segment_filter)]
    filtered = filtered.sort_values("CLV", ascending=False)

    st.dataframe(
        filtered[["Customer_Name", "Segment", "Value_Tier", "Recency", "Frequency", "Monetary", "CLV"]],
        width='stretch'
    )

    st.divider()
    st.subheader("🤖 AI Recommendations")

    if st.button("Generate Recommendations", key="rfm_recommend"):
        with st.spinner("Generating strategic recommendations..."):
            recs = recommendations_from_rfm(summary)
            st.success(recs)

# ============================================
# PAGE 5: Root Cause Analysis
# ============================================
elif page == "Root Cause Analysis":
    st.title("🔍 Root Cause Analysis")
    st.caption("Investigate what's driving changes in performance between two periods")

    df_rca = get_rca_data()
    months = get_available_months(df_rca)

    col1, col2, col3 = st.columns(3)
    period_a = col1.selectbox("Period A (baseline)", months, index=len(months) - 2)
    period_b = col2.selectbox("Period B (compare to)", months, index=len(months) - 1)
    metric = col3.selectbox("Metric", ["Sales", "Profit", "Order_ID"], 
                              format_func=lambda x: "Orders" if x == "Order_ID" else x)

    if st.button("Analyze"):
        st.session_state.rca_result = analyze_period_change(df_rca, period_a, period_b, metric=metric)

    if "rca_result" in st.session_state:
        result = st.session_state.rca_result

        st.divider()

        metric_label = "Orders" if result["metric"] == "Order_ID" else result["metric"]
        col1, col2, col3 = st.columns(3)
        col1.metric(f"{metric_label} ({result['period_a']})", 
                    f"{result['total_a']:,.0f}" if result["metric"] == "Order_ID" else f"${result['total_a']:,.0f}")
        col2.metric(f"{metric_label} ({result['period_b']})", 
                    f"{result['total_b']:,.0f}" if result["metric"] == "Order_ID" else f"${result['total_b']:,.0f}")
        col3.metric("Change", 
                    f"{result['overall_change']:,.0f}" if result["metric"] == "Order_ID" else f"${result['overall_change']:,.0f}",
                    f"{result['overall_pct_change']:.1f}%")

        st.divider()
        st.subheader("Breakdown by Dimension")

        tab1, tab2, tab3 = st.tabs(["Category", "Region", "Segment"])

        for tab, dimension in zip([tab1, tab2, tab3], ["Category", "Region", "Segment"]):
            with tab:
                breakdown_df = result["breakdowns"][dimension]

                fig = px.bar(
                    breakdown_df,
                    x=dimension,
                    y="Change",
                    color="Change",
                    color_continuous_scale=["#E63946", "#CCCCCC", "#06A77D"],
                    color_continuous_midpoint=0
                )
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, width='stretch')

                st.dataframe(breakdown_df, width='stretch')

        st.divider()
        st.subheader("🤖 AI Recommendations")

        if st.button("Generate Recommendations", key="rca_recommend"):
            with st.spinner("Generating strategic recommendations..."):
                recs = recommendations_from_rca(result)
                st.success(recs)