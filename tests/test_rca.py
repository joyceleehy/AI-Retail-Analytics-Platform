from modules.root_cause import load_orders_for_rca, get_available_months, analyze_period_change

df = load_orders_for_rca()
months = get_available_months(df)
print(f"✅ Available months (first 5): {months[:5]}")
print(f"✅ Total months available: {len(months)}")

# Compare two consecutive months as a test
period_a = months[-3]  # third-to-last month
period_b = months[-2]  # second-to-last month

result = analyze_period_change(df, period_a, period_b, metric="Sales")

print(f"\n✅ Comparing {period_a} vs {period_b}")
print(f"Total {period_a}: ${result['total_a']:,.0f}")
print(f"Total {period_b}: ${result['total_b']:,.0f}")
print(f"Change: ${result['overall_change']:,.0f} ({result['overall_pct_change']:.1f}%)")

print(f"\n✅ Category Breakdown:")
print(result["breakdowns"]["Category"])