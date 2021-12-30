# -*- coding: utf-8 -*-

from study.datasource import qq
from study.datasource import neteasy
from study.realtime import price_query


print(qq.get_kline_day("sh600010",days=5))
print(neteasy.get_kline_day("600010.sh")[-6:])
print(price_query.get_history_price("sh600010", 5))