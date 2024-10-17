from django.urls import path
from .views import bitcoin_prices_view  # 비트코인 가격 뷰를 임포트합니다.

urlpatterns = [
    path('bitcoin-prices/', bitcoin_prices_view, name='bitcoin_prices'),  # URL과 뷰를 매핑
]
