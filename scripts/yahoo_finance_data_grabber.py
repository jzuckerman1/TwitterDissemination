import yfinance as yf
import pandas as pd
import datetime as dt


def main(start_date, end_date, ticker):
    print(f"Fetching {ticker} from {start_date} to {end_date}...")

    data = yf.download(ticker, start=start_date, end=end_date,auto_adjust=True, timeout=20)

    if data.empty:
        print(f"No data returned for ticker '{ticker}'. Check the symbol or date range.")
        return

    print(data)

    output_file = f"../data/{ticker}_{start_date}_{end_date}.csv" # SAVE LOCATION
    data.to_csv(output_file)
    print(f"\nSaved to {output_file}")


if __name__ == "__main__":    
    main(
        start_date=dt.date.fromisoformat("2007-01-01"),
        end_date=dt.date.fromisoformat("2023-01-01"),
        ticker="^GSPC",
    )