# -*- coding: utf-8 -*-

import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.offsets import BusinessDay

holidays_2020=["2020-01-01","2020-01-02","2020-01-03","2020-01-24","2020-01-27","2020-01-28","2020-01-29","2020-01-30","2020-01-31",
               "2020-04-06","2020-05-01","2020-05-04","2020-05-05","2020-06-25","2020-06-26","2020-10-01","2020-10-02","2020-10-05","2020-10-06","2020-10-07","2020-10-08"]

holidays_2021=["2021-01-01","2021-02-11","2021-02-12","2021-02-15","2021-02-16","2021-02-17","2021-04-05","2021-05-03","2021-05-04","2021-05-05",
               "2021-06-14","2021-09-20","2021-09-21","2021-10-01","2021-09-04","2021-10-05","2021-10-06","2021-10-07",]

holidays_2019=["2019-01-01","2019-02-04","2019-02-05","2019-02-06","2019-02-07","2019-02-08","2019-04-05","2019-05-01","2019-05-02","2019-05-03","2019-06-07","2019-09-13"
               ,"2019-10-01","2019-10-02","2019-10-03","2019-10-04","2019-10-07"]


def get_business_day_cn(year):
    if year=="2020":
        return CustomBusinessDay(holidays=holidays_2020)
    if year=="2021":
        return CustomBusinessDay(holidays=holidays_2021)
    else:
        return CustomBusinessDay(holidays=[*holidays_2019,*holidays_2020,*holidays_2021])
    
def test():
#     hodiday_cn=pd.date_range(start='2/01/2021', end='3/01/2021',freq= get_business_day_cn('2021'))
    days=pd.date_range(end="2020-09-16", periods=20, freq=get_business_day_cn("2021"))
    print(days)
    
if __name__=="__main__":
    test()
