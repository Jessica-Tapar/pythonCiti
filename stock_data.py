from datetime import date, datetime, timedelta

import yfinance as yf
import math


def get_stock_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def collect_data():
    COMPANY = ["TCS", "INDUSINDBK", "MARUTI", "RELIANCE", "HDFCBANK", "INFY", "ICICIBANK"]
    NSE = ["TCS.NS", "INDUSINDBK.NS", "MARUTI.NS", "RELIANCE.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS"]
    BSE = ["TCS.BO", "INDUSINDBK.BO", "MARUTI.BO", "RELIANCE.BO", "HDFCBANK.BO", "INFY.BO", "ICICIBANK.BO "]
    list = []
    for x in range(len(NSE)):
        stock_symbol_nse = NSE[x]  # Replace this with the NSE symbol you want to fetch data for
        stock_symbol_bse = BSE[x]  # Replace this with the BSE symbol you want to fetch data for
        start_date = datetime.now() - timedelta(days=1)
        end_date = date.today()

        sub_list = []
        nse_data = get_stock_data(stock_symbol_nse, start_date, end_date)
        bse_data = get_stock_data(stock_symbol_bse, start_date, end_date)

        nse_close_prices = nse_data['Close'].to_list()
        bse_close_prices = bse_data['Close'].to_list()
        sub_list.append(COMPANY[x])

        sub_list.append(round(nse_close_prices[0], 2))
        sub_list.append(round(bse_close_prices[0], 2))

        if (nse_close_prices > bse_close_prices):
            sub_list.append('NSE')
            sub_list.append('BSE')
        else:
            sub_list.append('BSE')
            sub_list.append('NSE')

        profit = abs(round(bse_close_prices[0], 2) - round(nse_close_prices[0], 2)) / max(round(bse_close_prices[0], 2),
                                                                                          round(nse_close_prices[0],
                                                                                                2)) * 100
        sub_list.append(round(profit, 3))
        sub_list.append(end_date)
        # sub_list.append(math.floor(nse_close_prices))
        # sub_list.append(math.floor(bse_close_prices))
        list.append(sub_list)
    return list
