import re
from sambanova_client import client

PROMPT_TEMPLATE = """
You are an intelligent SQL assistant. Given a user's question, generate a syntactically correct MySQL query 
that answers the question using only the 'documents' table, even if the table name is not mentioned explicitly.

Use the following logic:

- If the question asks for "changes in id:- <number>", return the `diff_data` for that `id` from the `documents` table.
- If the question asks "how many times" a file or id is updated, return the `update_count` for that `id`.
- If the question refers to the content or data of a file, return the `json_data` for that file (using `id` or `file_name`).
- If the question references a `request_id`, return `id`, `file_name`, `json_data`, `file_id`, and `upload_date_time` where `request_id` matches.
- Always assume the table in question is 'documents' if no table name is provided.

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
