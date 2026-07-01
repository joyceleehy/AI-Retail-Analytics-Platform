from modules.kpi_dashboard import load_data, calculate_kpis
from modules.rfm import get_full_rfm_analysis
from modules.forecasting import get_full_forecast
from modules.report_generator import generate_excel_report

df = load_data()
kpis = calculate_kpis(df)

rfm_result = get_full_rfm_analysis()
rfm_summary = rfm_result["summary"]

forecast_result = get_full_forecast(months_ahead=3)
forecast_df = forecast_result["base_forecast"]

excel_buffer = generate_excel_report(kpis, rfm_summary, forecast_df)

# Save to disk just for this test, to confirm it opens correctly
with open("test_report_output.xlsx", "wb") as f:
    f.write(excel_buffer.getvalue())

print("✅ Excel report generated successfully: test_report_output.xlsx")