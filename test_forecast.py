from modules.forecasting import get_full_forecast

result = get_full_forecast(months_ahead=3, sales_growth_pct=10)

print("✅ Historical (last 5 months):")
print(result["historical"].tail(5))

print("\n✅ Base Forecast (next 3 months):")
print(result["base_forecast"])

print("\n✅ Adjusted Forecast (+10% growth scenario):")
print(result["adjusted_forecast"])