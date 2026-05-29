#!/usr/bin/env python
# coding: utf-8

#Library

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

#Processing 

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

#Excution 

@click.command()
@click.option('--chunksize', default='100000', type=int, help='Chunksize')
@click.option('--year', default='2021', help='Year')
@click.option('--month', default='1', type=int, help='Month')
@click.option('--pg-user', default='thaivo', help='PostgreSQL user')
@click.option('--pg-pass', default='02072007', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, month, year, chunksize):
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url= prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz'
    
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )


    first = True

    for df_chunk in tqdm(df_iter):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))


# Xóa chữ pass cũ đi và thêm đoạn này vào cuối file:
if __name__ == '__main__':
    run()