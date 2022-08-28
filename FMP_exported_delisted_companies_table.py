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
    FROM fmp.delisted_companies;
"""
cursor.execute(sql)
delisted_companies = cursor.fetchall()

for p in delisted_companies:
    print(p)

# Excel
workbook = Workbook()
sheet = workbook.active
sheet.append(["ID", "symbol", "companyName", "dex", "ipoDate", "delistedDate"])

for p in delisted_companies:
    print(p)
    sheet.append(p)

workbook.save(filename="exported_delisted_companies.xlsx")
