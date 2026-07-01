from modules.rfm import get_full_rfm_analysis
from modules.recommendations import recommendations_from_rfm

result = get_full_rfm_analysis()
summary = result["summary"]

print("✅ Segment Summary:")
print(summary)

print("\n🤖 Generating AI Recommendations...")
recommendations = recommendations_from_rfm(summary)
print(f"\n✅ Recommendations:\n{recommendations}")