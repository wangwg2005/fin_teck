# -*- coding: utf-8 -*-

import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.offsets import BusinessDay

holidays_2021=["2021-01-01","2021-02-11","2021-02-12","2021-02-15","2021-02-16","2021-02-17","2021-04-05","2021-05-03","2021-05-04","2021-05-05",
               "2021-06-14","2021-09-20","2021-09-21","2021-10-01","2021-09-04","2021-10-05","2021-10-06","2021-10-07",]



def get_business_day_cn(year):
    if year=="2021":
        return CustomBusinessDay(holidays=holidays_2021)
    else:
        return BusinessDay()
    
def test():
    hodiday_cn=pd.date_range(start='2/01/2021', end='3/01/2021',freq= get_business_day_cn('2021'))
    print(hodiday_cn)
    
# test()
