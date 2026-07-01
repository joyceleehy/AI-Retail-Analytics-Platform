# 🛒 AI-Powered Retail Analytics Platform

> **Transforming raw sales data into actionable business intelligence** — featuring a natural language SQL agent, sales forecasting, customer segmentation, root cause analysis, AI recommendations, and one-click Excel reporting.

[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange)](https://groq.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-green)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)

---

## 🌐 Live Demo

👉 **[Launch Live App](https://ai-retail-analytics-platform-ykxfx2b7gzabgt388ijvpg.streamlit.app/)**

> App may take 30-60 seconds to wake up on first visit (Streamlit Cloud free tier)

---

## ⚡ Quick Summary

| | |
|---|---|
| **Dataset** | Kaggle Superstore Sales — 9,994 orders, 4 years (2014–2017) |
| **Stack** | Python · Streamlit · Groq LLM · LangChain · scikit-learn · Pandas · Plotly · SQLite · openpyxl |
| **Modules** | 7 analytics modules covering descriptive → diagnostic → predictive → prescriptive analytics |
| **AI Features** | Natural language to SQL, AI executive summaries, AI business recommendations |

---

## 🎯 Why I Built This

Most dashboards stop at describing what happened — leaving business teams to figure out the "why" and "what next" on their own.

I built this platform to show what modern business intelligence looks like when you combine traditional analytics with AI:

- Not just "revenue dropped" — but **which category, region, or segment caused it**
- Not just "here are your customers" — but **which ones are at risk of leaving and what they're worth**
- Not just "here's last quarter" — but **what next quarter looks like and what to do about it**

This project reflects how I think about analytics: as a tool for driving decisions, not just reporting numbers.

This project covers the **full analytical cycle**:

| Question | Module |
|---|---|
| What's happening? | Executive Dashboard |
| Why is it happening? | Root Cause Analysis |
| What will happen next? | Sales Forecasting |
| Who are our customers? | RFM + CLV Segmentation |
| What should we do? | AI Recommendation Engine |

---

## 📊 Project Metrics

```
📦 9,994 orders analyzed          👥 793 customers segmented
🧩 7 analytics modules             🤖 3 AI-powered features
🗄️ 1 SQLite database               📥 1-click Excel report (4 sheets)
📈 3-month sales forecast          🔍 Natural language → SQL pipeline
```

---

## 📸 Screenshots

### Executive Dashboard
![Executive Dashboard](Screenshots/01_executive_dashboard.png)

### AI Insights Agent
![AI Insights Agent](Screenshots/02_ai_insights_agent.png)

### Sales Forecasting
![Sales Forecasting](Screenshots/03_sales_forecasting.png)

### Customer Segmentation
![Customer Segmentation](Screenshots/04_customer_segmentation.png)

### Root Cause Analysis
![Root Cause Analysis](Screenshots/05_root_cause_analysis.png)

---

## 🚀 Modules

### 📊 Module 0: Executive Dashboard
**Business Problem:** Leadership needs a single-screen view of business health without digging through raw data.

**Solution:** Auto-calculated KPI scorecards (Revenue, Profit, YoY Growth, Active Customers, Average Order Value) with a revenue trend chart and an AI-generated executive summary.

**Business Impact:** Reduces time-to-insight for leadership from hours to seconds. The AI summary surfaces the most important business trend in plain English automatically on load.

---

### 🤖 Module 1: AI Insights Agent
**Business Problem:** Analysts spend significant time writing ad-hoc SQL queries to answer one-off business questions from stakeholders.

**Solution:** A natural language interface that converts plain English questions to SQL, runs them against the database, and returns AI-written business insights with supporting data tables. Sample question buttons make demos effortless.

**Business Impact:** Democratises data access — non-technical stakeholders can get answers directly without waiting for an analyst to write a query.

---

### 📈 Module 2: Sales Forecasting + Scenario Simulator
**Business Problem:** Planning teams need revenue projections for budgeting, and need to test assumptions before committing to targets.

**Solution:** A forecasting model trained on 48 months of historical data predicts the next 3 months of revenue. Interactive "what if" sliders let users model scenarios like "what if sales grow by 20%?" and instantly see the impact on the forecast.

**Business Impact:** Gives planning teams a data-backed baseline forecast with instant scenario modeling — no manual Excel work required.

---

### 👥 Module 3: Customer Segmentation (RFM + CLV)
**Business Problem:** Marketing teams often treat all customers the same, wasting budget on low-value customers while under-investing in high-value ones.

**Solution:** Every customer is scored on Recency (how recently they bought), Frequency (how often they buy), and Monetary value (how much they spend). This segments all 793 customers into Champion, Loyal, At Risk, Lost, and Needs Attention groups. Customer Lifetime Value (CLV) adds a long-term revenue estimate per customer.

**Business Impact:** At Risk customers have nearly identical average CLV ($4,219) to Champions ($4,330) — making them a high-priority retention target with significant recoverable revenue potential.

---

### 🔍 Module 4: Root Cause Analysis
**Business Problem:** When revenue changes month-to-month, it's rarely obvious which product category, region, or customer segment caused the shift.

**Solution:** A period-over-period comparison tool that automatically breaks down changes in Revenue, Profit, or Orders across Category, Region, and Segment dimensions. Color-coded charts make it instantly clear what's growing (green) and what's declining (red).

**Business Impact:** Turns "revenue dropped 15% last month" from a vague concern into a specific, actionable finding — with the exact category and region driving the change identified in seconds.

---

### 💡 Module 5: AI Recommendation Engine
**Business Problem:** Data findings often stay in dashboards and don't translate into concrete actions for business teams.

**Solution:** After each analysis (RFM segmentation or Root Cause), a Groq-powered AI engine reads the actual results and generates 3-4 specific, numbered business recommendations — referencing real numbers from the data, not generic advice.

**Business Impact:** Bridges the gap between analysis and action, giving business teams clear next steps grounded in their own data.

---

### 📥 Module 6: Auto Report Generator
**Business Problem:** Compiling analysis results into a shareable report is time-consuming and prone to copy-paste errors.

**Solution:** One click generates a formatted Excel workbook with 4 sheets: Executive Summary (KPIs), Customer Segmentation, Sales Forecast, and Root Cause Analysis (automatically included if run during the session).

**Business Impact:** Stakeholders get a clean, professional, shareable report in seconds — ready for a business review meeting.

---

## 🤖 How the AI Agent Works

The AI Insights Agent accepts questions in plain English, automatically converts them to SQL using Groq's LLM, runs the query against the Superstore database, and returns a human-readable business insight with a supporting data table. No SQL knowledge required from the user — and sample question buttons make it easy to demo instantly.

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

## 🧠 Skills Demonstrated

`Python` `SQL` `Streamlit` `Pandas` `Data Cleaning` `Data Modeling`
`Machine Learning` `Forecasting` `Business Intelligence` `Data Visualisation`
`RFM Analysis` `Customer Lifetime Value (CLV)` `Root Cause Analysis`
`Prompt Engineering` `LLM Integration` `Excel Automation` `SQLite`
`LangChain` `Groq API` `Modular Architecture`

---

## 📈 Project Highlights

- ✅ Built a **complete prescriptive analytics platform** covering all 4 levels of analytics: descriptive, diagnostic, predictive, and prescriptive
- ✅ Implemented a **natural language to SQL pipeline** that lets non-technical users query data in plain English
- ✅ Discovered that **At Risk customers ($4,219 avg CLV)** represent nearly the same value as Champions — making retention a higher business priority than acquisition
- ✅ Built an **AI recommendation engine** that generates specific, number-backed business actions — not generic advice
- ✅ Delivered a **one-click Excel report** combining 4 modules into a polished, stakeholder-ready document
- ✅ Deployed as a **live interactive web app** accessible without any local setup

---

## 💡 Business Insights from the Data

- **At Risk customers** ($4,219 avg CLV) are nearly as valuable as Champions ($4,330) — meaning a targeted retention campaign has higher ROI than acquiring new customers
- **Consumer segment** drives ~62% of total sales — but Corporate customers have higher average order values, suggesting a different pricing or upsell strategy for each segment
- **Technology sales spike in November and December** — consistent with holiday demand, making Q4 inventory and staffing planning critical
- **20.4% YoY revenue growth** in the final year signals strong business momentum, but with only 793 active customers, growth is concentrated in a relatively small base

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

## 📁 Project Structure

```
ai-retail-analytics/
│
├── app.py                     # Streamlit entry point, module navigation
├── data_loader.py             # CSV → SQLite pipeline (run once)
├── requirements.txt
│
├── data/
│   └── superstore.csv         # Kaggle Superstore Sales dataset
│
├── modules/
│   ├── kpi_dashboard.py       # Module 0: Executive KPIs + AI summary
│   ├── ai_agent.py            # Module 1: NL → SQL → Insight
│   ├── forecasting.py         # Module 2: Sales Forecasting
│   ├── rfm.py                 # Module 3: RFM + CLV Segmentation
│   ├── root_cause.py          # Module 4: Root Cause Analysis
│   ├── recommendations.py     # Module 5: AI Recommendations
│   └── report_generator.py    # Module 6: Excel Report Generator
│
└── tests/                     # Standalone test scripts for each module
```
---

## 📊 Dataset

**Kaggle Superstore Sales Dataset**
- 9,994 orders across 4 years (2014–2017)
- 21 columns: order details, customer info, product categories, sales, profit
- Source: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

---

## 👩‍💼 Author

**Joyce Lee** | Data & BI Analyst | PL-300 Certified

With 10 years of experience in HR and People Analytics, I'm passionate about building analytics tools that go beyond reporting — turning data into decisions.

- 🔗 LinkedIn: [linkedin.com/in/joyceleehy](https://linkedin.com/in/joyceleehy)
- 💻 GitHub: [github.com/joyceleehy](https://github.com/joyceleehy)
- 📊 More Projects: [github.com/joyceleehy](https://github.com/joyceleehy)

  
