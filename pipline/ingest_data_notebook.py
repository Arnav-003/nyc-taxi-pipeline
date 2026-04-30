#!/usr/bin/env python
# coding: utf-8

# In[4]:


from calendar import month

import pandas as pd
from sqlalchemy import create_engine
from time import time
import click  



dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]
@click.command()
@click.option('--user', default='root', help='Username for postgres')
@click.option('--password', default='root', help='Password for postgres')
@click.option('--host', default='localhost', help='Host for postgres')
@click.option('--port', default='5432', help='Port for postgres')
@click.option('--db', default='ny_taxi', help='Database name for postgres')
@click.option('--table_name', default='yellow_taxi_data', help='Name of the destination table')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
def run(user, password, host, port, db, table_name, year, month):
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f"{prefix}yellow_tripdata_{year}-{month:02d}.csv.gz"

  



    engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}:{port}/{db}')

    print(f"Starting ingestion for {year}-{month:02d}...")
 
    df_itr = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,    
        iterator=True, 
        chunksize=100000
    )

    try:

        first_chunk = next(df_itr)


        first_chunk.tpep_pickup_datetime = pd.to_datetime(first_chunk.tpep_pickup_datetime)
        first_chunk.tpep_dropoff_datetime = pd.to_datetime(first_chunk.tpep_dropoff_datetime)

        first_chunk.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')


        first_chunk.to_sql(name=table_name, con=engine, if_exists='append')
        print("First chunk inserted... row count should now be 100,000")


        for df_chunk in df_itr:
            t_start = time()

            df_chunk.tpep_pickup_datetime = pd.to_datetime(df_chunk.tpep_pickup_datetime)
            df_chunk.tpep_dropoff_datetime = pd.to_datetime(df_chunk.tpep_dropoff_datetime)

            df_chunk.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()
            print(f"Inserted another chunk, took {t_end - t_start:.3f} seconds")

        print("Finished all ingestion!")
    except StopIteration:     
        print("Finished all ingestion!")        
    except Exception as e:
        print(f"An error occurred: {e}") 

if __name__ == "__main__":
    run()       
