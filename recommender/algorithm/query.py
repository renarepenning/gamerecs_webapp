"""https://towardsdatascience.com/set-up-heroku-postgresql-for-your-app-in-python-7dad9ceb0f92"""
import os 
import psycopg2
import pandas as pd
# WHITE DB
DATABASE_URL = "postgres://jfqbocymbesqkd:b0bdc1a7ecbf26b512954e7620a57c186be91d88ef9aee30a6ae12913b986d00@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d6ula8hn40666q"

con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()
"""This code reads the database url from your environment variables and uses it to establish a connection to the server."""
# query 
query = f"""SELECT name FROM "Games";"""

# return results as a dataframe
results = pd.read_sql(query, con)
print(results)