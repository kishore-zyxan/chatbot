from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text

def run_query(engine, sql_query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            columns = result.keys()
            rows = result.fetchall()
            return columns, rows
    except ProgrammingError as e:
        return None, f"SQL error: {e}"
    except Exception as e:
        return None, f"Error: {e}"
