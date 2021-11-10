# -*- coding: utf-8 -*-

import business_day as bd
import pandas as pd
from datetime import datetime,date,timedelta
import os
import time

urls={}
urls["000905"]="http://quotes.money.163.com/service/chddata.html?code=0000905&start=20041231&end={0}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER"
# urls["000016"]="http://quotes.money.163.com/service/chddata.html?code=0000016&start=20040102&end={0}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER"
# urls["399006"]="http://quotes.money.163.com/service/chddata.html?code=1399006&start=20100601&end={0}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER"
# urls["000300"]="http://quotes.money.163.com/service/chddata.html?code=0000300&start=20020104&end={0}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER"

def update_prices_to_date():
    end_da=date.today()+timedelta(days=-1)
    last_trade_day=pd.date_range(end=end_da, periods=1, freq=bd.get_business_day_cn("all"))[0]
    last_day_str=str(last_trade_day)[:10].replace("-","")
    
    
    for k,v in urls.items():
        url=str.format(v, last_day_str)
        print("downloading price data for",k,"from",url)
        df=pd.read_csv(url,encoding="gbk")
        df.to_csv(os.path.join(k,k+".csv"),index=False)
        time.sleep(3)
        
    

    
if __name__=="__main__":
    print(update_prices_to_date())
    