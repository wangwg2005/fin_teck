# -*- coding: utf-8 -*-
import pandas_datareader.data as web
import cninfo

start_date="2020-01-01"
end_date="2020-12-31"

print(cninfo.get_by_stock("002118,9900002187", start_date,end_date))
df = web.get_data_yahoo("002118.SZ", start=start_date, end=end_date)
