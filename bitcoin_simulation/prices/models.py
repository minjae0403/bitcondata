from django.db import models

class BitcoinPrice(models.Model):
    Open_time = models.DateTimeField(primary_key=True)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    Close = models.FloatField()
    trades = models.IntegerField()

    class Meta:
        db_table = 'btcusdt'  # MySQL 테이블 이름
        managed = False
