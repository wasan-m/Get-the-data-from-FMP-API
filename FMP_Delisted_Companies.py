import pandas as pd
import requests
import mysql.connector
import json

# Import any secret key
import fmp_secret as fs

# Get response
API_key = fs.APPL
url = (
    "https://financialmodelingprep.com/api/v3/delisted-companies?page=0&apikey="
    + API_key
)


def get_api_result(url):
    r = requests.get(url)
    return json.loads(r.text)


# Create dataframe
JL = get_api_result(url)
df = pd.DataFrame(JL)

# Convert datafram to list
lldf = df.values.tolist()

# MySQL database
db = mysql.connector.connect(
    host=fs.host, port=fs.port, user=fs.user, password=fs.password, database=fs.database
)

# Insert data to MySQL database
cursor = db.cursor()
sql = """
    INSERT INTO delisted_companies (symbol, companyName, dex, ipoDate, delistedDate)
    VALUES (%s, %s, %s, STR_TO_DATE(%s, '%Y-%m-%D'), STR_TO_DATE(%s, '%Y-%m-%D'));
"""

cursor.executemany(sql, lldf)
db.commit()

print("Insert data " + str(cursor.rowcount) + " rows to delisted_companies table")
