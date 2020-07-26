import yfinance as yf
from newscatcher import Newscatcher
from newscatcher import describe_url
from newscatcher import urls
import matplotlib.pyplot as plt
from datetime import date
import mplfinance as mpf
from yahoo_fin import stock_info as si
from datetime import datetime 
import time
import holidays
import datetime
import pandas as np
import numpy as np
import pytz



tz = pytz.timezone('US/Eastern')
us_holidays = holidays.US()

majorSites = ["seekingalpha.com", "marketwatch.com", "nytimes.com", "wsj.com", "bloomberg.com", "investopedia.com", "finance.yahoo.com", "money.cnn.com", "reuters.com", "forbes.com"]
topTickers = ["AMD", "INTC", "ROKU", "AAPL", "ABBV", "ABT", "ACN", "ADBE", "AIG", "ALL", "AMGN", "AMT", "AMZN", "AXP", "BA", "BAC", "BIIB", "BK", "BKNG", "BLK", "BMY", "C", "CAT", "CHTR", "CL", "CMCSA", "COF", "COP", "COST", "CRM", "CSCO", "CVS", "CVX", "DD", "DHR", "DIS", "DOW", "DUK", "EMR", "EXC", "F", "FB", "FDX", "GD", "GE", "GILD", "GM", "GOOG", "GOOGL", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KHC", "KMI", "KO", "LLY", "LMT", "LOW", "MA", "MCD", "MDLZ", "MDT", "MET", "MMM", "MO"
, "MRK", "MS", "MSFT", "NEE", "NFLX", "NKE", "NVDA", "ORCL", "OXY", "PEP", "PFE", "PG", "PM", "PYPL", "QCOM", "RTX", "SBUX", "SLB", "SO", "SPG", "T", "TGT", "TMO", "TXN", "UNH", "UNP", "UPS", "USB", "V", "VZ", "WBA", "WFC", "WMT", "XOM"]

class stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.movingaverage50 = 0
        self.averageVolume10Days = 0
        self.averageVolume24HR = 0
        self.lastDividend = 0
        self.dividendYield = 0
        self.volumeToday = 0
        self.previousClose = 0
        self.open = 0
        self.nextDividendDate = "00:00:00"
        self.lastSR = 0
        self.market = ""
        self.yearperformance = 0
        self.lastSplitDate = "00:00:00"
        self.lastSplitYield = "0:0"
        self.todayClose = 0

def latestNews(source):
    try:
        nc = Newscatcher(website = source, topic = 'finance')
        for k in nc.get_headlines():
            print(k + "\n")
    except:
        print("unable to retrieve data from: " + source)

def initTicker(ticker):
    #print(ticker)
    
    i = datetime.datetime.now()
    date = ("%s-%s-%s" % (i.year, i.month, i.day))
    s = stock(ticker)
    gTicker = yf.Ticker(ticker)
    try:
        inf = gTicker.info
        s.movingaverage50 = inf['fiftyDayAverage']
        s.averageVolume10Days = inf['averageDailyVolume10Day']
        s.averageVolume24HR = inf['volume24Hr']
        s.dividendYield = inf['dividendYield'] 
        s.nextDividendDate =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inf['exDividendDate']))
        divs = gTicker.history(period="5y")['Dividends']
        divs = [i for i in divs if i > 0]
        s.dividendRate = inf['dividendRate']
        s.yearperformance = inf['52WeekChange']
        s.lastDividend = divs.pop()
        s.market = inf['market']
        s.open = inf['open']
        s.previousClose = inf['previousClose']
        s.lastSplitDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inf['lastSplitDate']))
        s.lastSplitYield = inf['lastSplitFactor']
        s.volumeToday = inf['volume']
        s.todayClose = priceHistory(ticker,date,date)['Close'][0]
        return s
    except:
        print(ticker + " did not succeed")
    
def createMajorTickers():
    list = []
    for k in topTickers:
        list.append(initTicker(k))
    return list
def latestMajorNews():
    list = []
    for k in majorSites:
        list.append(latestNews(k))
    return list

def recommendations(ticker, limit, pref):
    share = yf.Ticker(ticker).recommendations
    for i in range(limit):
        if not pref == "":
            if share.values[i] == pref:
                print(share.values[i][1])
        else:
            print(share.values[i][0] + ": " + share.values[i][1])
        
def generalSignal(ticker, limit):
    share = yf.Ticker(ticker).recommendations
    sell = 0
    neutral = 0
    buy = 0
    #market-perform -> average return hence buy,neutral
    k = share.values[::-1]
    for i in range(limit):
        print(k[i])
        if k[i][1] == ("Buy" or "Overweight" or "Market Perform"):
            buy += 1
        elif k[i][1] == ("Sell" or "Underweight"):
            sell += 1
        elif k[i][1] == ("Neutral" or "Equal-Weight" or "Market Perform" or "Hold"):
            neutral += 1
    if sell > neutral and sell > buy:
        return "sell"
    elif buy > neutral and buy > sell:
        return "buy"
    elif buy == neutral or sell == neutral and neutral > sell or neutral > buy:
        return "neutral"
    else:
        print("undecided")

def latestClose(ticker):
    return yf.download(ticker)['Close'][::-1][0]

def priceHistory(ticker, start, end):
    return yf.download(ticker, start, end)

def priceHistoryConfigs(tickerT, periodT, intervalT):
    return yf.download(tickers=tickerT, period=periodT, interval=intervalT)

def latestPrice(ticker):
    return si.get_live_price(ticker)

def getPriceByTime(ticker, time):
    i = datetime.datetime.now()
    date = ("dd/mm/yyyy format =  %s-%s-%s" % (i.day, i.month, i.year))
    return priceHistoryConfigs(ticker,date,time).tail(1)

def candlesticks(ticker, date, interval):
    SPX = priceHistoryConfigs(ticker, date, interval)
    print(SPX)
    mc = mpf.make_marketcolors(up='g',down='r')
    s = mpf.make_mpf_style(marketcolors=mc)
    setup = dict(type='candle',mav=(7,11,20),volume=True,figratio=(11,8),figscale=0.85, style=s)
    mpf.plot(SPX.iloc[0: len(SPX)-1],**setup)
    plt.show()

def pattern(ticker):
    return 0
def entryexit(ticker):
    return 0

#records changes in market by sens (percentage) over a given interval, interval in seconds, sleep 
def priceNotification(interval, sens):
    nyc_datetime = datetime.datetime.now(pytz.timezone('US/Eastern'))
    stocksOfInterest = []
    for stock in topTickers:
        values = getPriceByTime(stock,interval)
        if sens > 0 and values['Close']>values['Open'] and (((values['Close']/values['Open'])-1)*100)[0] > sens:
            if isOpen():
                print(str(stock) + " moved more than " + str(sens) + "% by " + str(nyc_datetime))
                stocksOfInterest.append(stock)
            else:
                print("market closed")
        #decline
        else:
            if (values['Close']<values['Open']) and 0 > sens:
                if isOpen():
                    print(str(stock) + " returned negative sequential result by: -" + str((1-(values['Close']/values['Open']))*100) + "%")
                    stocksOfInterest.append(stock)
                else:
                    print("market closed")
    print("stocks with " + str("positive" if sens > 0 else "negative") + " differentiation returned")
    return stocksOfInterest

def triggerFunction(interval,percent,sleep):
    while True:
        start_time = time.time()
        print(priceNotification(interval,percent))
        end_time = time.time()-start_time
        if sleep < end_time:
            sleep = end_time+0.1
        time.sleep(sleep)

def isOpen(now = None):
        if not now:
            now = datetime.datetime.now(tz)
        openTime = datetime.time(hour = 9, minute = 30, second = 0)
        closeTime = datetime.time(hour = 16, minute = 0, second = 0)
        # If a holiday
        if now.strftime('%Y-%m-%d') in us_holidays:
            return False
        # If before 0930 or after 1600
        if (now.time() < openTime) or (now.time() > closeTime):
            return False
        # If it's a weekend
        if now.date().weekday() > 4:
            return False
        return True
#def supportLevel(ticker, span):
#def resistanceLevel(ticker, span):
def buyOrders():
    list = [("INTC, 46.21$")]
    return list




#format: Stock(s), "date revised-now", "interval"
#candlesticks("AMD", "1mo", "1d")
#triggerFunction("5m",-0.4,15)
#print(initTicker("MSFT"))

