import yfinance as yf
from newscatcher import Newscatcher
from newscatcher import describe_url
from newscatcher import urls
import time
import datetime

majorSites = ["seekingalpha.com", "marketwatch.com", "nytimes.com", "wsj.com", "bloomberg.com", "investopedia.com", "finance.yahoo.com", "money.cnn.com", "reuters.com", "forbes.com"]
topTickers = ["AAPL", "ABBV", "ABT", "ACN", "ADBE", "AIG", "ALL", "AMGN", "AMT", "AMZN", "AXP", "BA", "BAC", "BIIB", "BK", "BKNG", "BLK", "BMY", "C", "CAT", "CHTR", "CL", "CMCSA", "COF", "COP", "COST", "CRM", "CSCO", "CVS", "CVX", "DD", "DHR", "DIS", "DOW", "DUK", "EMR", "EXC", "F", "FB", "FDX", "GD", "GE", "GILD", "GM", "GOOG", "GOOGL", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KHC", "KMI", "KO", "LLY", "LMT", "LOW", "MA", "MCD", "MDLZ", "MDT", "MET", "MMM", "MO"
, "MRK", "MS", "MSFT", "NEE", "NFLX", "NKE", "NVDA", "ORCL", "OXY", "PEP", "PFE", "PG", "PM", "PYPL", "QCOM", "RTX", "SBUX", "SLB", "SO", "SPG", "T", "TGT", "TMO", "TXN", "UNH", "UNP", "UPS", "USB", "V", "VZ", "WBA", "WFC", "WMT", "XOM","BRK.B"]

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

def latestNews(source):
    try:
        nc = Newscatcher(website = source, topic = 'finance')
        for k in nc.get_headlines():
            print(k + "\n")
    except:
        print("unable to retrieve data from: " + source)

def initTicker(ticker):
    print(ticker)
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
        print(divs)
        s.lastDividend = divs.pop()
        s.market = inf['market']
        s.open = inf['open']
        s.previousClose = inf['previousClose']
        s.lastSplitDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inf['lastSplitDate']))
        s.lastSplitYield = inf['lastSplitFactor']
        s.volumeToday = inf['volume']
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
print(yf.Ticker("MSFT").info)

#majorTickers = createMajorTickers()
#majorNewsSites = latestMajorNews()

