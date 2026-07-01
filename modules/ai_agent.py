import pandas as pd
import sqlite3
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Schema description — tells the AI exactly what columns exist
# so it generates correct SQL instead of guessing column names
TABLE_SCHEMA = """
Table: orders
Columns:
- Order_ID, Order_Date, Ship_Date, Ship_Mode
- Customer_ID, Customer_Name, Segment
- Country, City, State, Postal_Code, Region
- Product_ID, Category, Sub_Category, Product_Name
- Sales (revenue), Quantity, Discount, Profit
"""

def generate_sql(question):
    """
    Takes a natural language question, asks Groq to convert it
    into a valid SQLite query based on our table schema.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    You are a SQL expert. Convert this question into a valid SQLite query.

    {TABLE_SCHEMA}

    Question: {question}

    Rules:
    - Return ONLY the SQL query, no explanation, no markdown formatting
    - Use the exact column names shown above
    - Always use proper SQLite syntax
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    
    # Clean up in case the AI wraps it in markdown code blocks
    sql = sql.replace("```sql", "").replace("```", "").strip()
    
    return sql

def run_query(sql):
    """Executes the generated SQL against superstore.db and returns a DataFrame"""
    conn = sqlite3.connect("superstore.db")
    try:
        result_df = pd.read_sql(sql, conn)
        conn.close()
        return result_df, None
    except Exception as e:
        conn.close()
        return None, str(e)

def generate_insight(question, result_df):
    """
    Takes the query result and asks Groq to explain it
    in plain, business-friendly language.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Convert result to readable text for the AI to interpret
    data_summary = result_df.to_string(index=False, max_rows=20)

    prompt = f"""
    A user asked: "{question}"

    The data result is:
    {data_summary}

    Write a clear, 2-3 sentence business insight answering their question.
    Be specific with numbers from the data.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

def ask_question(question):
    """
    Main function that ties everything together:
    question -> SQL -> data -> insight
    """
    sql = generate_sql(question)
    result_df, error = run_query(sql)

    if error:
        return {
            "sql": sql,
            "error": error,
            "result_df": None,
            "insight": None
        }

    insight = generate_insight(question, result_df)

    return {
        "sql": sql,
        "error": None,
        "result_df": result_df,
        "insight": insight
    }