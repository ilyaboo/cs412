import yfinance as yf

def get_latest_stock_price(ticker: str) -> float:
    """ returns latest stock price """

    try:
        stock = yf.Ticker(ticker)
        return stock.fast_info['lastPrice']
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e} (stock)")
        return None
    
def get_latest_crypto_price(ticker: str) -> float:
    """ returns latest crypto price """

    try:
        crypto = yf.Ticker(ticker + "-USD")
        return crypto.fast_info['lastPrice']
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e} (crypto)")
        return None