import pandas as pd


def _trim_dates(data, start_date, end_date):
    if start_date is not None and end_date is not None:
        return data.loc[(data['expiration'] >= start_date) & (data['expiration'] <= end_date)]
    elif start_date is None and end_date is not None:
        return data.loc[data['expiration'] <= end_date]
    elif start_date is not None and end_date is None:
        return data.loc[data['expiration'] >= start_date]
    else:
        return data


def _trim_cols(data, column_mapping):
    cols = [c for c, _ in column_mapping if c is not None]
    return data.iloc[:, cols]


def _standardize_cols(data, column_mapping):
    col_names = list(data.columns)
    cols = {col_names[idx]: label for idx, label in column_mapping if idx is not None}
    return data.rename(columns=cols)


def _infer_date_cols(data):
    data["expiration"] = pd.to_datetime(data.expiration, infer_datetime_format=True)
    data["quote_date"] = pd.to_datetime(data.quote_date, infer_datetime_format=True)
    return data


def csv_data(
    file_path,
    start_date=None,
    end_date=None,
    underlying_symbol=0,
    underlying_price=1,
    option_type=2,
    expiration=3,
    quote_date=4,
    strike=5,
    bid=6,
    ask=7,
):
    """
    Uses pandas DataFrame.read_csv function to import data from CSV files.
    It will automatically generate standardized headers for this library to use.

    Args:
        file_path: str, path to csv file
        start_date: datetime, start date of data set to consider, date is inclusive
        end_date: datetime, end date of data set to consider, date is inclusive
        underlying_symbol: int, index of column containing underlying symbol of option chain
        underlying_price: int, index of column containing underlying stock price
        quote_date: int, index of column containing quote date of option chain
        expiration: int, index of column containing expiration of option chain
        strike: int, index of column containing strike price of option chain
        option_type: int, index of column containing option type of option chain
        bid: int, index of column containing bid price of option chain
        ask: int, index of column containing ask price of option chain

    Returns:
        DataFrame: A dataframe of option chains with standardized columns

    """

    column_mapping = [
        (underlying_symbol, "underlying_symbol"),
        (underlying_price, "underlying_price"),
        (option_type, "option_type"),
        (expiration, "expiration"),
        (quote_date, "quote_date"),
        (strike, "strike"),
        (bid, "bid"),
        (ask, "ask"),
    ]

    return (
        pd.read_csv(file_path)
        .pipe(_standardize_cols, column_mapping)
        .pipe(_trim_cols, column_mapping)
        .pipe(_infer_date_cols)
        .pipe(_trim_dates, start_date, end_date)
    )
