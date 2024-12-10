import yfinance as yf

def get_latest_stock_price(ticker: str) -> float:
    """ returns latest stock price """

    # to address heroku not being able to get a response from API call
    for _ in range(50):
        try:
            stock = yf.Ticker(ticker)
            return stock.fast_info['lastPrice']
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e} (stock)")
    return None
    
def get_latest_crypto_price(ticker: str) -> float:
    """ returns latest crypto price """

    # to address heroku not being able to get a response from API call
    for _ in range(50):
        try:
            crypto = yf.Ticker(ticker + "-USD")
            return crypto.fast_info['lastPrice']
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e} (crypto)")
    return None
    
def get_historical_prices(ticker: str, period: str = "3mo", interval: str = "1d", type: str = "stock"):
    """ fethcing historical prices for the given ticker """

    if type == "stock":
        ticker = yf.Ticker(ticker)
    else:
        ticker = yf.Ticker(ticker + "-USD")
        
    data = ticker.history(period = period, interval = interval)
    return data[['Close']]