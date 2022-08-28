import pandas as pd
import requests
import mysql.connector
import json

# Import any secret key
import fmp_secret as fs

# Get response
API_key = fs.APPL
url = (
    "https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/AAPL?apikey="
    + API_key
)


def get_api_result(url):
    r = requests.get(url)
    return json.loads(r.text)


# Create dataframe 1
jl = get_api_result(url)
df1 = pd.DataFrame(jl)

# Create dataframe 2
historical = df1.historical.values.tolist()
df2 = pd.DataFrame(historical)

# Adjust dataframe 1
df1 = df1.pop("symbol")

# Combine dataframe 1, 2
result = pd.concat([df1, df2], axis=1)

# Convert datafram to list
lldf = result.values.tolist()

# MySQL database
db = mysql.connector.connect(
    host=fs.host, port=fs.port, user=fs.user, password=fs.password, database=fs.database
)

# Insert data to MySQL database
cursor = db.cursor()
sql = """
    INSERT INTO historical_dividends (symbol, historicalDate, labelDate, adjDividend, dividend, recordDate, paymentDate, declarationDate)
    VALUES (%s, STR_TO_DATE(%s, '%Y-%m-%D'), %s, %s, %s, STR_TO_DATE(%s, '%Y-%m-%D'), STR_TO_DATE(%s, '%Y-%m-%D'), STR_TO_DATE(%s, '%Y-%m-%D'));
"""

cursor.executemany(sql, lldf)
db.commit()

print("Insert data " + str(cursor.rowcount) + " rows to delisted_companies table")
