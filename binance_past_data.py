import requests
import pandas as pd
import time
import os
from datetime import datetime
import mysql.connector

# MySQL Database Connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',  # Replace with your host
        user='root',  # Replace with your username
        password='12345',  # Replace with your password
        database='crypto_db'  # Replace with your database name
    )

# Create table if it doesn't exist
def create_table(cursor, symbol):
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS `{symbol}` (
        Open_time DATETIME,
        Open FLOAT,
        High FLOAT,
        Low FLOAT,
        Close FLOAT,
        Volume FLOAT,
        quote_av FLOAT,
        trades INT,
        tb_base_av FLOAT,
        tb_quote_av FLOAT
    )
    """)

# Fetch symbols
result = requests.get('https://api.binance.com/api/v3/ticker/price')
symbols = [x['symbol'] for x in result.json() if 'USDT' in x['symbol']]

# Data columns
COLUMNS = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av']

# URL for fetching data
URL = 'https://api.binance.com/api/v3/klines'

def get_data(start_date, end_date, symbol):
    data = []
    start = int(time.mktime(datetime.strptime(start_date + ' 00:00', '%Y-%m-%d %H:%M').timetuple())) * 1000
    end = int(time.mktime(datetime.strptime(end_date + ' 23:59', '%Y-%m-%d %H:%M').timetuple())) * 1000
    
    params = {
        'symbol': symbol,
        'interval': '1d',
        'limit': 1000,
        'startTime': start,
        'endTime': end
    }

    while start < end:
        print(datetime.fromtimestamp(start // 1000))
        params['startTime'] = start
        response = requests.get(URL, params=params)
        js = response.json()
        if not js:
            break
        data.extend(js)
        start = js[-1][0] + 60000

    if not data:
        print('해당 기간에 데이터가 없습니다.')
        return None

    # 필요한 열만 선택
    df = pd.DataFrame(data)
    df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
    df = df.drop(columns=['quote_av'])  # 불필요한 열 삭제
    df.loc[:, 'Open':'tb_quote_av'] = df.loc[:, 'Open':'tb_quote_av'].astype(float)
    df['trades'] = df['trades'].astype(int)
    
    # MySQL 테이블에 필요한 열만 선택
    df = df[['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'trades', 'tb_base_av', 'tb_quote_av']]
    
    return df

# Start and end dates
years = range(2018, 2023)
interval = '1d'

# Fetch data for each symbol and store it in MySQL
for symbol in symbols[:10]:
    conn = create_connection()
    cursor = conn.cursor()
    
    create_table(cursor, symbol)

    for year in years:
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        
        df = get_data(start_date, end_date, symbol)
        
        if df is not None:
            for _, row in df.iterrows():
                cursor.execute(f"""
                INSERT INTO `{symbol}` (Open_time, Open, High, Low, Close, Volume, trades, tb_base_av, tb_quote_av)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, tuple(row))
            conn.commit()
            time.sleep(1)  # Rate limiting to avoid API bans

    cursor.close()
    conn.close()

print("Data has been successfully stored in MySQL.")
