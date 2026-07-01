from modules.kpi_dashboard import load_data, calculate_kpis, generate_ai_summary

# Step 1: Load data
df = load_data()
print(f"✅ Data loaded: {len(df)} rows")

# Step 2: Calculate KPIs
kpis = calculate_kpis(df)
print(f"✅ Total Revenue: ${kpis['total_revenue']:,.0f}")
print(f"✅ Total Profit: ${kpis['total_profit']:,.0f}")
print(f"✅ Growth Rate: {kpis['growth_rate']:.1f}%")
print(f"✅ Active Customers: {kpis['active_customers']:,}")
print(f"✅ Avg Order Value: ${kpis['avg_order_value']:,.2f}")

# Step 3: Generate AI summary
print("\n🤖 Generating AI summary...")
summary = generate_ai_summary(kpis)
print(f"\n✅ AI Summary:\n{summary}")