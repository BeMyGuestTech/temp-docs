import os
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection string
# DATABASE_URL = 'postgresql+psycopg2://postgres:password@localhost:5432/RAG_DB_UPLOADS' #Local DB
DATABASE_URL = 'postgresql+psycopg2://postgres:password@localhost:5433/RAG_DB_UPLOADS' #Docker DB
# DATABASE_URL = "postgresql+psycopg2://postgres:mmd7j9Gd3xgjMCmMZoMN@bct-data-symphony-dev-01.chcvz661tzog.us-east-1.rds.amazonaws.com:5432/datasymphony_tables" # AWS KV
# Target folder with Excel and CSV files
TARGET_FOLDER = r'/home/ec2-user/DataSymphony_POC/Document/Tabular Data'

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Supported file extensions
SUPPORTED_EXTENSIONS = ['.csv', '.xlsx', '.xls']

# Iterate through files in the folder
for filename in os.listdir(TARGET_FOLDER):
    file_path = os.path.join(TARGET_FOLDER, filename)
    name, ext = os.path.splitext(filename)

    if ext.lower() not in SUPPORTED_EXTENSIONS:
        continue

    try:
        # Load data using pandas
        if ext.lower() == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Upload to PostgreSQL
        df.to_sql(name=name.lower(), con=engine, if_exists='replace', index=False)
        print(f"Uploaded {filename} to table '{name.lower()}' successfully.")

    except Exception as e:
        print(f"Failed to upload {filename}: {e}")