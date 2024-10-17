from django.shortcuts import render
from .models import BitcoinPrice  # BitcoinPrice 모델을 임포트합니다.

def bitcoin_prices_view(request):
    prices = BitcoinPrice.objects.all()  # 데이터베이스에서 모든 데이터를 가져옵니다.
    return render(request, 'bitcoin_prices.html', {'prices': prices})  # 템플릿에 데이터를 전달합니다.


# Create your views here.
