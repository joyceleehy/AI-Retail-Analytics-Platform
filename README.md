# 🛒 AI-Powered Retail Analytics Platform

An end-to-end business intelligence platform built with Python and Streamlit, featuring AI-driven insights, sales forecasting, customer segmentation, root cause analysis, and automated reporting — all powered by real Superstore sales data.

---

## 🎯 Project Overview

Most analytics dashboards stop at "what happened." This platform goes further — answering **why it happened**, **what will happen next**, and **what the business should do about it**.

Built to demonstrate full-stack BI thinking: from raw data ingestion to prescriptive AI recommendations.

---

## 🚀 Modules

### 📊 Module 0: Executive Dashboard
- 5 core KPIs: Revenue, Profit, YoY Growth, Active Customers, Avg Order Value
- Revenue trend chart by year
- AI-generated executive summary (Groq LLM)

### 🤖 Module 1: AI Insights Agent
- Natural language → SQL → business insight pipeline
- Ask questions like "Which region has the highest profit?" in plain English
- Auto-generates SQL, runs it, and returns AI-written insights
- Sample question buttons for easy demo

### 📈 Module 2: Sales Forecasting + Scenario Simulator
- Predicts next 3 months revenue using Linear Regression (scikit-learn)
- Interactive "what if" sliders for sales growth and retention scenarios
- Actual vs Forecast vs Adjusted Forecast chart

### 👥 Module 3: Customer Segmentation (RFM + CLV)
- RFM scoring (Recency, Frequency, Monetary) for all 793 customers
- Segments: Champion, Loyal, At Risk, Lost, Needs Attention
- Customer Lifetime Value (CLV) estimation
- Interactive scatter plot and filterable customer table

### 🔍 Module 4: Root Cause Analysis
- Compare any two time periods across Revenue, Profit, or Orders
- Automatic breakdown by Category, Region, and Customer Segment
- Color-coded charts: red = decline, green = growth

### 💡 Module 5: AI Recommendation Engine
- Generates specific, data-driven business recommendations using Groq LLM
- Recommendations reference real numbers from your data (not generic advice)
- Integrated into RFM and Root Cause Analysis modules

### 📥 Module 6: Auto Report Generator
- One-click Excel report with 4 sheets:
  - Executive Summary (KPIs)
  - Customer Segmentation (RFM)
  - Sales Forecast
  - Root Cause Analysis (if run in session)

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.14 |
| Web App | Streamlit |
| AI / LLM | Groq (`llama-3.1-8b-instant`), LangChain |
| Data Processing | Pandas, NumPy |
| Machine Learning | scikit-learn (Linear Regression) |
| Visualisation | Plotly |
| Database | SQLite |
| Reporting | openpyxl |
| Environment | python-dotenv |

---

## 📁 Project Structure

ai-retail-analytics/
│
├── app.py                  # Streamlit entry point, all module navigation
├── data_loader.py          # CSV → SQLite pipeline (run once)
├── requirements.txt
│
├── data/
│   └── superstore.csv      # Kaggle Superstore Sales dataset
│
├── modules/
│   ├── kpi_dashboard.py    # Module 0: Executive KPIs + AI summary
│   ├── ai_agent.py         # Module 1: NL → SQL → Insight
│   ├── forecasting.py      # Module 2: Linear Regression forecast
│   ├── rfm.py              # Module 3: RFM scoring + CLV
│   ├── root_cause.py       # Module 4: Period comparison + breakdown
│   ├── recommendations.py  # Module 5: AI recommendations
│   └── report_generator.py # Module 6: Excel report builder
│
└── tests/                  # Standalone test scripts for each module

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/joyceleehy/AI-Retail-Analytics-Platform.git
cd AI-Retail-Analytics-Platform
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root folder:
GROQ_API_KEY=your_groq_api_key_here
Get a free Groq API key at: https://console.groq.com

### 4. Load the database
```bash
python data_loader.py
```

### 5. Run the app
```bash
python -m streamlit run app.py
```

---

## 📊 Dataset

**Kaggle Superstore Sales Dataset**
- 9,994 orders across 4 years (2014–2017)
- 21 columns: Order details, customer info, product categories, sales, profit
- Source: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

---

## 💡 Key Business Insights (from the data)

- **$2.3M total revenue** with **20.4% YoY growth** in the final year
- **Champion customers** (176) and **At Risk customers** (158) have nearly identical average CLV (~$4,300) — meaning At Risk customers represent significant recoverable revenue
- **Technology** drives the biggest seasonal spikes (Nov/Dec), consistent with holiday demand patterns
- **Consumer segment** accounts for ~62% of total sales across all years

---

## 🔗 Connect

**Joyce Lee** | Data & BI Analyst | PL-300 Certified
- GitHub: [joyceleehy](https://github.com/joyceleehy)
- LinkedIn: [linkedin.com/in/joyce-lee-how-yee](https://linkedin.com/in/joyce-lee-how-yee)