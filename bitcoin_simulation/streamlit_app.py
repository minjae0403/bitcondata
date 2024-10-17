import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings
import django
import os

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitcoin_simulation.settings")
django.setup()

from prices.models import BitcoinPrice

# 데이터베이스에서 데이터 가져오기
def get_data():
    prices = BitcoinPrice.objects.all().values()
    return pd.DataFrame(list(prices))

# Streamlit 앱 구성
st.title('비트코인 가격 및 거래량 시뮬레이션')

# 데이터 가져오기
data = get_data()
data['Open_time'] = pd.to_datetime(data['Open_time'])

# 1번 그래프: 주식 차트
st.subheader('비트코인 가격 차트')
fig, ax = plt.subplots()
ax.plot(data['Open_time'], data['Close'], label='Close Price', color='blue')
ax.set_xlabel('Open Time')
ax.set_ylabel('Price (USD)')
ax.set_title('비트코인 가격')
ax.legend()
st.pyplot(fig)

# 2번 그래프: 거래량 차트
st.subheader('비트코인 거래량 차트')
fig, ax = plt.subplots()
ax.bar(data['Open_time'], data['trades'], label='Trading Volume', color='orange')
ax.set_xlabel('Open Time')
ax.set_ylabel('Trades')
ax.set_title('비트코인 거래량')
ax.legend()
st.pyplot(fig)
