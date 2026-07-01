import pandas as pd
import sqlite3
from sklearn.linear_model import LinearRegression
import numpy as np

def load_monthly_sales():
    """
    Pull all orders and aggregate them into monthly revenue totals.
    This converts daily transaction data into a clean monthly time series.
    """
    conn = sqlite3.connect("superstore.db")
    df = pd.read_sql("SELECT Order_Date, Sales FROM orders", conn)
    conn.close()

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    
    # Create a "Year-Month" period column, then sum sales per month
    df["Month"] = df["Order_Date"].dt.to_period("M")
    monthly = df.groupby("Month")["Sales"].sum().reset_index()
    monthly["Month"] = monthly["Month"].dt.to_timestamp()
    monthly = monthly.sort_values("Month").reset_index(drop=True)

    return monthly

def train_forecast_model(monthly_df):
    """
    Train a simple linear regression model:
    X = month number (0, 1, 2, 3...)
    y = revenue for that month

    The model learns the overall trend line through historical revenue.
    """
    monthly_df = monthly_df.copy()
    monthly_df["Month_Number"] = range(len(monthly_df))

    X = monthly_df[["Month_Number"]]  # must be 2D for scikit-learn
    y = monthly_df["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    return model, monthly_df

def forecast_next_months(model, monthly_df, months_ahead=3):
    """
    Use the trained model to predict revenue for the next N months
    beyond the last month in our historical data.
    """
    last_month_number = monthly_df["Month_Number"].max()
    last_date = monthly_df["Month"].max()

    future_month_numbers = [last_month_number + i for i in range(1, months_ahead + 1)]
    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=months_ahead,
        freq="MS"  # Month Start
    )

    X_future = pd.DataFrame({"Month_Number": future_month_numbers})
    predictions = model.predict(X_future)

    # Predictions shouldn't go negative - floor at 0
    predictions = np.maximum(predictions, 0)

    forecast_df = pd.DataFrame({
        "Month": future_dates,
        "Sales": predictions,
        "Type": "Forecast"
    })

    return forecast_df

def apply_scenario(forecast_df, sales_growth_pct=0, retention_improvement_pct=0):
    """
    Scenario Simulator: applies user-defined 'what if' adjustments
    to the base forecast.

    sales_growth_pct: e.g. 10 means +10% sales growth assumption
    retention_improvement_pct: e.g. 5 means +5% retention improvement,
                                 which we treat as an additional revenue boost
    """
    adjusted_df = forecast_df.copy()
    
    total_multiplier = 1 + (sales_growth_pct / 100) + (retention_improvement_pct / 100)
    adjusted_df["Sales"] = adjusted_df["Sales"] * total_multiplier
    adjusted_df["Type"] = "Adjusted Forecast"

    return adjusted_df

def get_full_forecast(months_ahead=3, sales_growth_pct=0, retention_improvement_pct=0):
    """
    Main function that ties everything together:
    historical data -> trained model -> base forecast -> scenario-adjusted forecast
    """
    monthly_df = load_monthly_sales()
    model, monthly_df = train_forecast_model(monthly_df)
    base_forecast = forecast_next_months(model, monthly_df, months_ahead)

    if sales_growth_pct != 0 or retention_improvement_pct != 0:
        adjusted_forecast = apply_scenario(base_forecast, sales_growth_pct, retention_improvement_pct)
    else:
        adjusted_forecast = None

    # Prepare historical data for charting (mark it as "Actual")
    historical = monthly_df[["Month", "Sales"]].copy()
    historical["Type"] = "Actual"

    return {
        "historical": historical,
        "base_forecast": base_forecast,
        "adjusted_forecast": adjusted_forecast
    }