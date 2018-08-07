import requests#导入requests库
from cryptocmd import CmcScraper#从cryptocmd库中导入CmcScraper方法
import warnings#导入warning库
import numpy as np#导入numpy库并改名为np
import pandas as pd#导入pandas库并改名为pd
import time#导入time库
from time import strftime, localtime#从time库中导入strftime,localtime方法
from datetime import timedelta, date#从datetime库中导入timedelta,date方法
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt#导入matplotlib.pyplot库并改名为plt
pd.set_option('display.max_rows',None)#设置输出行数无限,为了显示全部数据
pd.set_option("display.max_colwidth",1000)#增加宽度,输出所有完整数据
warnings.filterwarnings('ignore')#忽略警告
now=time.strftime('%d-%m-%Y', time.localtime())
def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        return date.today() - timedelta(days=n)
    else:
        return date.today() + timedelta(days=n)
'''
Code By Coel
Copy right 2018 (c) Coel

'''
columns=['Symbol','Market cap','Price($)','Volume(24h)','Circulating Supply','% 1h','% 24h','% 7d']
url='https://coinmarketcap.com/all/views/all/'#需要爬的网址
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
r=requests.get(url,headers=header)
print('Stats:',r)
bsobj=BeautifulSoup(r.text)#传入BeautifulSoup,有内建函数更方便取数据
#-----------------------------------------------------------------------------------------------------------------------------------
data_name=bsobj.find_all('a',{'class':'currency-name-container link-secondary'})#获取所有货币名称
coinname=[]
for each in data_name:
    coinname.append(each.text)#存入所有货币名称
#-----------------------------------------------------------------------------------------------------------------------------------
data_symbol=bsobj.find_all('td',{'class':'text-left col-symbol'})
symbol=[]
for each in data_symbol:
    symbol.append(each.text)
#-----------------------------------------------------------------------------------------------------------------------------------
data_cap=bsobj.find_all('td',{'class':'no-wrap market-cap text-right'})
market_cap=[]
for each in data_cap:
    market_cap.append(each.text)#存入market_cap
	#market_cap
market_cap=map(lambda x:x.replace("\n$",""),market_cap)#过滤\n\$
market_cap=map(lambda x:x.replace("\n $",""),market_cap)#过滤\n \$
market_cap=map(lambda x:x.replace("\n",""),market_cap)#过滤\n
market_cap=list(market_cap)#转换为数组
#-----------------------------------------------------------------------------------------------------------------------------------
data_price=bsobj.find_all('a',{'class':'price'})
price=[]
for each in data_price:
    price.append(each.text)
price=map(lambda x:x.replace("$",""),price)#过滤$
price=list(price)#转换为数组
#-----------------------------------------------------------------------------------------------------------------------------------
data_volume=bsobj.find_all('a',{'class':'volume'})
volume=[]
for each in data_volume:
    volume.append(each.text)
volume=map(lambda x:x.replace("$",""),volume)#过滤$
volume=list(volume)#转换为数组
#-----------------------------------------------------------------------------------------------------------------------------------
data_cs=bsobj.find_all('td',{"class":"no-wrap text-right circulating-supply"})
cs=[]
for each in data_cs:
    cs.append(each.text)
cs=map(lambda x:x.replace("\n\n",""),cs)#过滤$
cs=map(lambda x:x.replace("\n",""),cs)#过滤$
cs=map(lambda x:x.replace("*",""),cs)#过滤$
cs=list(cs)#转换为数组
#-----------------------------------------------------------------------------------------------------------------------------------
data_hour1=bsobj.find_all('td',{'data-timespan':'1h'})
hour1=[]
for each in data_hour1:
    hour1.append(each.text)
#-----------------------------------------------------------------------------------------------------------------------------------
data_hour24=bsobj.find_all('td',{'data-timespan':"24h"})
hour24=[]
for each in data_hour24:
    hour24.append(each.text)
#-----------------------------------------------------------------------------------------------------------------------------------
data_day7=bsobj.find_all('td',{'data-timespan':"7d"})
day7=[]
for each in data_day7:
    day7.append(each.text)
#-----------------------------------------------------------------------------------------------------------------------------------
df = pd.DataFrame([symbol,market_cap,price,volume,cs,hour1,hour24,day7])
df =df.T
df.index=coinname
df.columns=columns
df.index.name="    Coin    "
print(df)
df.to_html('coinmarketcap.html')
print("All data has been write to coinmarketcap.html")