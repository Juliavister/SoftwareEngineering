import pyodbc


server = 'dogakserver.database.windows.net'
database = 'Currency'
username = 'doga123'
password = 'Ed44ha03'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
cursor = cnxn.cursor()