from sqlalchemy import create_engine

def get_db_engine():
    db_user = "root"
    db_password = "admin123"
    db_host = "localhost"
    db_name = "document_db"
    return create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
