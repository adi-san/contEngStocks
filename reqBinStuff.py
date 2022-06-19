import yahooquery as yq
from forex_python.converter import CurrencyRates
from yahooquery import Ticker
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly
import plotly.graph_objects as go
import kaleido
import os


industrial_automation_portfolio=np.array(['siegy','rok','miely','sbgsy','abb', 'hon', 'omrny', 'hthiy','tosyy','yokey','etn','kyccf','pcrfy','emr', 'ge', 'avevf', 'dhr', 'ftv','yasky','voyjf','ptc','adsk','azpn','ame', 'fss', 'msa','mtd', 'bmi', 'fti', 'ldos','tmo', 'tdy', 'fls', 'rtoxf', 'slb', 'ph','nvt', 'wegzy','csco','bdc', 'nexny', 'skfry', 'itw', 'dov'])
# industrial_automation_portfolio=np.array(['dhr'])
len_iap=len(industrial_automation_portfolio)
cur_rates=CurrencyRates()
share_price_list=np.empty(len_iap)
mkt_cap_list=np.empty(len_iap)
percent_error_list=np.empty(len_iap)
company_name_list=np.empty(len_iap,dtype='str')
posted_mkt_cap_list=np.empty(len_iap)
ind=0

for company in industrial_automation_portfolio:
    tick_symb = Ticker(company, asynchronous=True)
    financial_data = tick_symb.financial_data
    summary_detail = tick_symb.summary_detail
    price_class=tick_symb.price
    key_stats = tick_symb.key_stats
    current_share_price = financial_data[company]["currentPrice"]
    shares_outstanding = key_stats[company]["sharesOutstanding"]
    currency = summary_detail[company]["currency"]
    posted_mkt_cap = summary_detail[company]["marketCap"]
    company_name=price_class[company]["longName"]
    if currency != "USD":
        usd_factor = cur_rates.get_rate(currency, 'USD')
        current_share_price = current_share_price * usd_factor
        posted_mkt_cap= posted_mkt_cap * usd_factor
    precise_mkt_cap = current_share_price * shares_outstanding
    share_price_list[ind]=current_share_price
    mkt_cap_list[ind]= precise_mkt_cap
    percent_error_mkt_cap= (abs(posted_mkt_cap-precise_mkt_cap)/precise_mkt_cap)*100
    percent_error_list[ind]= percent_error_mkt_cap
    company_name_list[ind]= company_name
    posted_mkt_cap_list[ind]=posted_mkt_cap
    period_list = np.array(['max', '5y', '1y', '1mo', '7d', '1d'])
    interval_list = np.array(['1mo', '1wk', '1d', '1h', '15m', '2m'])
    for i in range(0,len(period_list)):
        df = tick_symb.history(period=period_list[i], interval=interval_list[i])
        print(type(df))
        df.head()
        fig = go.Figure(data=[go.Candlestick(x=df.index.get_level_values('date'), open=df['open'],
                                             high=df['high'], low=df['low'], close=df['close'])])
        fig.update_layout(
            title = company_name+' '+period_list[i],
            yaxis_title = company_name +' Share Price (USD)')
        fig.update_xaxes(title='datetime')
        if not os.path.exists("iap_files"):
            os.mkdir("iap_files")
        fig.write_html("iap_files/"+company_name+"_"+period_list[i]+"candlestick.html")
    ind+=1
print(share_price_list)
print(mkt_cap_list)
total_mkt_cap=np.sum(mkt_cap_list)
mkt_share_list=np.divide(mkt_cap_list,total_mkt_cap)
mkt_cap_weighted_shares=np.multiply(share_price_list,mkt_share_list)
iap_mkt_cap_index=np.sum(mkt_cap_weighted_shares)
print(total_mkt_cap)
print(iap_mkt_cap_index)






