from sqlalchemy import create_engine, Table, Column, Integer, Float, String, Text, MetaData
import pandas as pd
import os

# Path to the data folder
data_folder = os.path.join('Paris_Olympics_2024', 'data')
db_uri = 'postgresql://postgres:Toogaz5me@localhost:5432/Paris_Olympics_2024'
engine = create_engine(db_uri)
metadata = MetaData()

# Define schema
general_schema = 'General'
results_schema = 'Results'

def infer_sqlalchemy_type(series):
    """ Map pandas dtype to SQLAlchemy's types with dynamic length adjustment for String columns """
    dtype = series.dtype

    if "int" in dtype.name:
        return Integer
    elif "float" in dtype.name:
        return Float
    elif "object" in dtype.name:
        # Determine the maximum length of the strings in the column
        max_length = series.astype(str).apply(len).max()
        if max_length > 255:
            return Text()  # For very long text, use Text()
        else:
            return String(max_length)
    else:
        return String(255)  # Default fallback

def create_table_from_csv(csv_path, engine, metadata, schema=None):
    """ Create a table from a CSV file and load data into it """
    df = pd.read_csv(csv_path)
    
    # Determine the table name from the CSV filename (capitalize first letter)
    table_name = os.path.splitext(os.path.basename(csv_path))[0].capitalize()
    
    # Define columns dynamically
    columns = [Column(name, infer_sqlalchemy_type(df[name])) for name in df.columns]
    
    # Create table with schema if provided
    table = Table(table_name, metadata, *columns, schema=schema)
    
    # Create the table
    metadata.create_all(engine)
    
    # Insert data into the table
    df.to_sql(table_name, con=engine, schema=schema, if_exists='append', index=False)
    
    print(f"Table '{schema}.{table_name}' created and data loaded.")

# Process CSV files in the main data folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        csv_path = os.path.join(data_folder, file_name)
        create_table_from_csv(csv_path, engine, metadata, schema=general_schema)

# Process CSV files in the results folder (use the results schema)
results_folder = os.path.join(data_folder, 'results')
for file_name in os.listdir(results_folder):
    if file_name.endswith('.csv'):
        csv_path = os.path.join(results_folder, file_name)
        create_table_from_csv(csv_path, engine, metadata, schema=results_schema)