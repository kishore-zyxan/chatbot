import re
from sambanova_client import client

PROMPT_TEMPLATE = """
You are an intelligent SQL assistant. Given a user's question, generate a syntactically correct MySQL query 
that answers the question using only the tables and data present in the database.

Question: {question}

Respond ONLY with the SQL query. Do not include explanations or any other text.
"""

def extract_sql(text):
    # Remove any <think>...</think> or similar explanations
    cleaned = re.sub(r"<.*?>.*?</.*?>", "", text, flags=re.DOTALL)

    # Extract first valid SQL query
    for line in cleaned.strip().splitlines():
        line = line.strip().rstrip(";")
        if line.upper().startswith(("SELECT", "INSERT", "UPDATE", "DELETE")):
            return line + ";"  # Append semicolon
    return ""

def generate_sql_from_question(question: str) -> str:
    prompt = PROMPT_TEMPLATE.format(question=question)
    response = client.chat.completions.create(
        model="DeepSeek-R1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    raw_output = response.choices[0].message.content.strip()
    return extract_sql(raw_output)
