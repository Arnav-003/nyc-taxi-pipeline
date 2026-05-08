# NYC Taxi Data Pipeline — Docker + PostgreSQL

An end-to-end data ingestion pipeline built as part of the 
Data Engineering Zoomcamp (DataTalksClub).

## What this does
- Pulls NYC Green Taxi trip data from a public dataset
- Runs a Dockerised PostgreSQL database locally
- Ingests and validates the data using Python + pandas
- Queries the data using SQL for basic analysis

## Tech Stack
- Python (pandas, SQLAlchemy)
- PostgreSQL
- Docker + Docker Compose
- Jupyter Notebook

## How to run
1. Clone the repo
   git clone https://github.com/Arnav-003/Docker_Workshop
   cd Docker_Workshop

2. Start the database
   docker-compose up -d

3. Run the pipeline
   jupyter notebook pipeline/ingest_data.ipynb

## What I learned
- Containerising data pipelines with Docker
- Loading large CSVs into PostgreSQL efficiently
- Writing SQL queries for data validation and analysis
