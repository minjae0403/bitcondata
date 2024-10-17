import websocket
import json
import mysql.connector
from datetime import datetime
import time

# 바이낸스에서 실시간 가격 스트림을 받을 URL (BTC/USDT 예시)
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host="localhost",  # DB 호스트 주소
    user="root",       # MySQL 사용자 이름
    password="12345",  # MySQL 비밀번호
    database="crypto_db"  # 사용할 데이터베이스 이름
)

cursor = db.cursor()

# MySQL에 데이터를 저장하는 함수
def save_to_db(symbol, price):
    query = "INSERT INTO crypto_prices (symbol, price, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (symbol, price, datetime.now()))
    db.commit()

# WebSocket으로 수신한 메시지를 처리하는 함수
def on_message(ws, message):
    json_message = json.loads(message)
    price = float(json_message['p'])  # 거래된 가격
    symbol = json_message['s']        # 코인 심볼 (BTCUSDT)
    print(f"현재 {symbol} 가격: {price}")

    # DB에 저장
    save_to_db(symbol, price)

    # 1초 대기
    time.sleep(1)

def on_error(ws, error):
    print(f"에러 발생: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket 연결이 닫혔습니다.")
    cursor.close()
    db.close()

def on_open(ws):
    print("WebSocket 연결이 열렸습니다.")

# WebSocket 연결 설정
ws = websocket.WebSocketApp(SOCKET,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# WebSocket 연결 시작
ws.run_forever()
