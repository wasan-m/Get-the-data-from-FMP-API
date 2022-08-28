import mysql.connector
from openpyxl import Workbook

# Import any secret key
import fmp_secret as fs

# MySQL database
db = mysql.connector.connect(
    host=fs.host, port=fs.port, user=fs.user, password=fs.password, database=fs.database
)

# Export historical_dividends table
cursor = db.cursor()
sql = """
    SELECT * 
    FROM fmp.historical_dividends;
"""
cursor.execute(sql)
historical_dividends = cursor.fetchall()

for p in historical_dividends:
    print(p)

# Excel
workbook = Workbook()
sheet = workbook.active
sheet.append(
    [
        "ID",
        " symbol",
        "historicalDate",
        "labelDate",
        "adjDividend",
        "dividend",
        "recordDate",
        "paymentDate",
        "declarationDate",
    ]
)

for p in historical_dividends:
    print(p)
    sheet.append(p)

workbook.save(filename="exported_historical_dividends.xlsx")
