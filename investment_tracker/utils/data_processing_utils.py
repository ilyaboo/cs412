import pandas as pd
from ..models import PurchasedAsset
from .yfinance_utils import get_historical_prices

def set_historical_values(df: pd.DataFrame, quantity: float) -> None:
    """ helper function that takes df with historical prices 
        of an asset, quantity and modifies it to get historical values """
    
    df["Close"] = df["Close"] * quantity
    return

def combine_historical_closes(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """ helper function that combines the Close values of two DataFrames and 
    return the result as a new dataset """

    # ensuring both DataFrames have the same index type
    df1.index = pd.to_datetime(df1.index).tz_localize(None)
    df2.index = pd.to_datetime(df2.index).tz_localize(None)

    # rounding to the nearest even hour for consistency
    df1.index = df1.index.round("1h")
    df2.index = df2.index.round("1h")

    merged_df = pd.merge(df1, df2, left_index = True, right_index = True, suffixes = ("_1", "_2"), how = "inner")

    merged_df["Close"] = merged_df["Close_1"] + merged_df["Close_2"]  
    merged_df = merged_df[~merged_df.index.duplicated(keep = "first")]

    # returning only the Datetime index and the Combined_Close column
    return merged_df[["Close"]]

def get_historical_total_values(portfolios_assets_objects: list[PurchasedAsset], period: str, interval: str) -> pd.DataFrame:
    """ function that iterates over passed portfolio asset objects and combines historical data to total values """

    first_asset = True
    for portfolio_assets_object in portfolios_assets_objects:
        
        if first_asset:
            first_asset = False
            asset_historical_prices = get_historical_prices(portfolio_assets_object.asset.ticker, period = period, interval = interval, type = portfolio_assets_object.asset.asset_type)
            set_historical_values(asset_historical_prices, float(portfolio_assets_object.purchase_quantity))
            historical_total_values = asset_historical_prices
        
        else:
            asset_historical_prices = get_historical_prices(portfolio_assets_object.asset.ticker, period = period, interval = interval, type = portfolio_assets_object.asset.asset_type)
            set_historical_values(asset_historical_prices, float(portfolio_assets_object.purchase_quantity))
            historical_total_values = combine_historical_closes(historical_total_values, asset_historical_prices)

    print(historical_total_values)
    return historical_total_values