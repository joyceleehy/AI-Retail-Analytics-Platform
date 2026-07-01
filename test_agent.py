from modules.ai_agent import ask_question

question = "What are the top 5 products by total sales?"
result = ask_question(question)

print(f"Question: {question}\n")
print(f"Generated SQL:\n{result['sql']}\n")

if result['error']:
    print(f"❌ Error: {result['error']}")
else:
    print(f"✅ Data Result:\n{result['result_df']}\n")
    print(f"🤖 Insight:\n{result['insight']}")