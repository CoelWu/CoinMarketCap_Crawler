import os
import datetime
from threading import Timer
def Crawler():
	os.system("cls")
	os.system("python CoinMarketCap_Crawler.py")
	t=Timer(10800,Crawler)
	t.start()

if  __name__=="__main__":
	Crawler()