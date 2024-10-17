import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import test_streamlit as st
import mysql.connector
import pandas as pd
import dash
import plotly.graph_objects as go

# MySQL 데이터베이스 연결 함수
def get_data_from_db():
    # MySQL 연결 설정
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="crypto_oneday_db",
        port=3306
    )
    cursor = db.cursor()

    # 데이터 가져오기
    query = "SELECT Open_time, Open, High, Low, Close, trades FROM btcusdt ORDER BY Open_time ASC"
    cursor.execute(query)
    result = cursor.fetchall()

    # 데이터프레임으로 변환
    df = pd.DataFrame(result, columns=["Open_time", "Open", "High", "Low", "Close", "trades"])

    # 연결 종료
    cursor.close()
    db.close()

    return df

# Dash 애플리케이션 생성
app = dash.Dash(__name__)

# # Streamlit 페이지 설정
# st.title("실시간 코인 가격 데이터 시각화")
# st.write("MySQL 데이터베이스에서 가져온 실시간 BTC/USDT 가격 데이터를 시각화합니다.")

# 데이터 가져오기
df = get_data_from_db()
df['Open_time'] = pd.to_datetime(df['Open_time'])

# 데이터가 없을 경우 경고 메시지
if df.empty:
    st.warning("데이터베이스에 데이터가 없습니다.")

else:
    # 레이아웃 설정
    app.layout = html.Div([
        dcc.Graph(id='line-graph'),
        dcc.Input(id='y-value', type='number', value=10000, placeholder='직선 Y값'),
        html.Button('직선 추가', id='add-line', n_clicks=0)
    ])

    @app.callback(
        Output('line-graph', 'figure'),
        Input('add-line', 'n_clicks'),
        Input('y-value', 'value')
    )

    def update_graph(n_clicks, y_value):
        # 그래프 데이터 생성
        fig = go.Figure()

        # 가격 데이터 추가
        fig.add_trace(go.Scatter(x=df['Open_time'], y=df['Close'], mode='lines', name='Price'))

        # 직선 추가
        if n_clicks > 0:
            fig.add_shape(
                type="line",
                x0=df['Open_time'].min(), y0=y_value,
                x1=df['Open_time'].max(), y1=y_value,
                line=dict(color="Red", width=2, dash="dash")  # 점선 형태로
            )

        fig.update_layout(title='BTC/USDT 가격 변화', xaxis_title='시간', yaxis_title='가격')
        
        return fig

# 애플리케이션 실행
if __name__ == '__main__':
    app.run_server(debug=True)

    # df = df.sort_values(by="timestamp")
    # df['timestamp'] = pd.to_datetime(df['timestamp'])

    # # 사용자가 원하는 시간 범위 선택 (시간 슬라이더)
    # start_time = st.date_input(
    #     "시작 날짜를 선택하세요",
    #     value=df['timestamp'].min().date(),
    #     min_value=df['timestamp'].min().date(),
    #     max_value=df['timestamp'].max().date()
    # )

    # end_time = st.date_input(
    #     "끝 날짜를 선택하세요",
    #     value=df['timestamp'].max().date(),
    #     min_value=df['timestamp'].min().date(),
    #     max_value=df['timestamp'].max().date()
    # )

    # # Timestamp와 datetime.date 비교를 위해 .date() 사용
    # filtered_df = df[(df['timestamp'].dt.date >= start_time) & (df['timestamp'].dt.date <= end_time)]

    # # Y축 단위 선택 (셀렉트 박스)
    # interval = st.selectbox(
    #     "Y축 단위 선택:",
    #     ('1초', '5초', '10초', '30초')
    # )

    # # 단위에 따른 시간 간격 설정 (대문자 'S' -> 소문자 's')
    # if interval == '1초':
    #     resample_rule = '1s'
    # elif interval == '5초':
    #     resample_rule = '5s'
    # elif interval == '10초':
    #     resample_rule = '10s'
    # elif interval == '30초':
    #     resample_rule = '30s'

    # # 데이터 리샘플링 (평균값으로 계산)
    # df_resampled = filtered_df.resample(resample_rule, on='timestamp').mean().dropna()

    # # 가격을 콤마로 표시하고 소수 첫째 자리까지만 출력
    # df_resampled['price'] = df_resampled['price'].apply(lambda x: f"{x:,.1f}")

    # # 사용자 직선 그리기 기능 활성화 여부
    # enable_drawing = st.checkbox("직선 그리기 활성화", value=False)

    # # plotly로 그래프 그리기
    # fig = go.Figure()

    # # 가격 데이터 추가
    # fig.add_trace(go.Scatter(x=df_resampled.index, y=df_resampled['price'], mode='lines', name='Price'))

    # # 직선 그리기 기능 활성화 시 (임의로 y=10000에 직선 추가)
    # if enable_drawing:
    #     fig.add_shape(
    #         type="line",
    #         x0=df_resampled.index.min(), y0=10000,
    #         x1=df_resampled.index.max(), y1=10000,
    #         line=dict(color="Red", width=2)
    #     )

    # fig.update_layout(
    #     title="BTC/USDT 가격 변화",
    #     xaxis_title="시간",
    #     yaxis_title="가격",
    #     showlegend=True
    # )

    # # 그래프 출력
    # st.plotly_chart(fig)

    # # 최근 데이터 출력
    # num_records = st.slider("표시할 데이터 개수를 선택하세요", min_value=1, max_value=len(filtered_df), value=100)
    # st.write(f"선택된 시간 범위 내 최근 {num_records}개의 데이터:")
    # st.dataframe(filtered_df.tail(num_records))


# 애플리케이션 실행 명령 (명령줄에서 실행)
# streamlit run app.py