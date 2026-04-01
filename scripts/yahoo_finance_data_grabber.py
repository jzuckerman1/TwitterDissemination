import yfinance as yf
import pandas as pd
import argparse
import datetime as dt


def main(start_date, end_date, ticker):
    print(f"Fetching {ticker} from {start_date} to {end_date}...")

    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        print(f"No data returned for ticker '{ticker}'. Check the symbol or date range.")
        return

    print(data)

    output_file = f"data/{ticker}_{start_date}_{end_date}.csv" # SAVE LOCATION
    data.to_csv(output_file)
    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    # FOR COMMAND LINE RUNNING::
    # parser = argparse.ArgumentParser(description="A script to fetch data from the Yahoo Finance API")
    # parser.add_argument('sd', type=str, help="The start date (YYYY-MM-DD)")
    # parser.add_argument('ed', type=str, help="The end date (YYYY-MM-DD)")
    # parser.add_argument('tick', type=str, help="The ticker")

    # args = parser.parse_args()

    # # Validate and parse dates
    # try:
    #     start_date = dt.date.fromisoformat(args.sd)
    #     end_date   = dt.date.fromisoformat(args.ed)
    # except ValueError as e:
    #     raise SystemExit(f"Invalid date format: {e}. Use YYYY-MM-DD.")

    # if end_date <= start_date:
    #     raise SystemExit("End date must be after start date.")

    # main(
    #     start_date=start_date.isoformat(),
    #     end_date=end_date.isoformat(),
    #     ticker=args.tick.upper(),
    # )
    
    main(
        start_date=dt.date.fromisoformat("YYYY-MM-DD"),
        end_date=dt.date.fromisoformat("YYYY-MM-DD"),
        ticker="SNP",
    )