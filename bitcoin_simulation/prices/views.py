from django.shortcuts import render
from .models import BitcoinPrice  # BitcoinPrice 모델을 임포트합니다.

def bitcoin_prices_view(request):
    prices = BitcoinPrice.objects.all()  # 데이터베이스에서 모든 데이터를 가져옵니다.
    
    # 데이터 준비
    open_times = [price.Open_time for price in prices]
    opens = [price.Open for price in prices]
    highs = [price.High for price in prices]
    lows = [price.Low for price in prices]
    closes = [price.Close for price in prices]

    # 캔들스틱 차트 생성
    fig = go.Figure(data=[go.Candlestick(x=open_times,
                                          open=opens,
                                          high=highs,
                                          low=lows,
                                          close=closes)])

    # 차트 제목과 레이아웃 설정
    fig.update_layout(title='Bitcoin Prices',
                      xaxis_title='Open Time',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)

    # HTML로 차트 렌더링
    graph_html = pio.to_html(fig, full_html=False)

    return render(request, 'bitcoin_prices.html', {'graph_html': graph_html}) # 템플릿에 데이터를 전달합니다.
    
    # return render(request, 'bitcoin_prices.html', {'prices': prices})  


# Create your views here.
