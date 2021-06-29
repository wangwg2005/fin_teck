# -*- coding: utf-8 -*-
import datetime
from study.leverage import time_util as tutil
from study.leverage import leverage_reader as lreader
import pandas as pd

ttoday=datetime.date.today()

pre_day=tutil.get_prevous_trade_date(ttoday)

pre2_day=tutil.get_prevous_trade_date(pre_day)

df1=lreader.read_detail_sse(tutil.stringfy(pre_day))

df2=lreader.read_detail_sse(tutil.stringfy(pre2_day))

print(df.head())
