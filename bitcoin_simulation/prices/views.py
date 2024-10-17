from django.shortcuts import render
from .models import BitcoinPrice  # BitcoinPrice 모델을 임포트합니다.
import plotly.graph_objects as go
import pytz
from plotly.subplots import make_subplots
import plotly.io as pio
from django.utils.timezone import make_aware
from datetime import datetime
from django.db.models import Min, Max

def bitcoin_prices_view(request):
      
    # GET 요청에서 시작 날짜와 끝나는 날짜를 가져옴
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    
    # 데이터베이스에서 가장 이른 날짜와 가장 늦은 날짜 가져오기
    min_date = BitcoinPrice.objects.earliest('Open_time').Open_time
    max_date = BitcoinPrice.objects.latest('Open_time').Open_time
    
    #오류 메세지 기본 값
    error_message = "오류가 있습니다."

    # 날짜가 입력되지 않았을 경우 전체 데이터를 보여줌
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # 현재 시간대 가져오기 (예: 'Asia/Seoul')
        timezone = pytz.timezone('Asia/Seoul')
        
        # naive datetime을 aware datetime으로 변환
        start_date = make_aware(start_date, timezone)
        end_date = make_aware(end_date, timezone)
        
        
        if start_date > end_date:
            error_message = "날짜 설정을 다시 확인해 주세요."
            
            prices = BitcoinPrice.objects.filter(Open_time__range=[start_date, end_date]) 
            
        elif start_date > end_date or  min_date < max_date:
            
            error_message = f"{min_date.date()}부터 {max_date.date()}사이의 날짜로 선택을 해주셔야 합니다."
            
            prices = BitcoinPrice.objects.filter(Open_time__range=[start_date, end_date])  # 에러 발생 시 데이터를 초기 값으로 설정
        else:
            # 날짜 범위에 맞는 데이터 필터링
            prices = BitcoinPrice.objects.filter(Open_time__range=[start_date, end_date])

    else:
        prices = BitcoinPrice.objects.all()

    
    # 데이터 준비
    open_times = [price.Open_time for price in prices] # 시작시간
    opens = [price.Open for price in prices] #시작가
    highs = [price.High for price in prices] # 최고가
    lows = [price.Low for price in prices] # 최저가
    closes = [price.Close for price in prices] # 종가
    trades = [price.trades for price in prices]  # 거래량 데이터
    
    # 서브플롯 생성: 2개의 행(캔들스틱 + 거래량)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1, 
                        row_heights=[0.7, 0.3])

    # 캔들스틱 차트 추가 (첫 번째 플롯)
    fig.add_trace(go.Candlestick(x=open_times,
                                 open=opens,
                                 high=highs,
                                 low=lows,
                                 close=closes,
                                 name='Candlestick'),
                  row=1, col=1)
    
     # 거래량 바 차트 추가 (두 번째 플롯)
    fig.add_trace(go.Bar(x=open_times, y=trades, name='Volume', marker_color='blue'),
                  row=2, col=1)

    # 차트 제목과 레이아웃 설정
    fig.update_layout(title='Bitcoin Prices',
                      xaxis_title='Open Time',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False,
                      dragmode='zoom',  # 확대/축소 모드 설정
                      hovermode='x',  # 마우스 hover 모드
                      margin=dict(l=50, r=50, b=50, t=50, pad=4),  # 여백 설정
                      showlegend=False)
    
    # 서브플롯들의 축 및 레이아웃 세부 설정
    fig.update_xaxes(matches='x', showticklabels=True)  # 두 플롯의 x축을 공유
    fig.update_yaxes(title_text='Price', row=1, col=1)
    fig.update_yaxes(title_text='Volume', row=2, col=1)
    
    config = {'scrollZoom': True}
    # HTML로 차트 렌더링
    graph_html = pio.to_html(fig, full_html=False,include_plotlyjs='cdn', config=config)

    return render(request, 'bitcoin_prices.html', {'graph_html': graph_html, 'error_message': error_message}) # 템플릿에 데이터를 전달합니다.
    
    # return render(request, 'bitcoin_prices.html', {'prices': prices})  


# Create your views here.
