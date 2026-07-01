from modules.rfm import get_full_rfm_analysis

result = get_full_rfm_analysis()

print("✅ Segment Summary:")
print(result["summary"])

print("\n✅ Sample Customer Data (first 10):")
print(result["rfm_data"][["Customer_Name", "Recency", "Frequency", "Monetary", "Segment", "CLV", "Value_Tier"]].head(10))