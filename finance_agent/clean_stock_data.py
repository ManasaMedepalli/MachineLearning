import pandas as pd
import sys
from datetime import datetime

def convert_volume(vol):
    if isinstance(vol, str) and 'M' in vol:
        return int(float(vol.replace('M', '')) * 1_000_000)
    elif isinstance(vol, str) and 'B' in vol:
        return int(float(vol.replace('B', '')) * 1_000_000_000)
    return int(vol)

def clean_and_append(filename, ticker, output="mag7_cleaned.csv"):
    # Load raw CSV
    df = pd.read_csv(filename)

    # Rename columns for clarity
    df.columns = ['date', 'close', 'open', 'high', 'low', 'volume', 'change_percent']

    # Add ticker
    df['ticker'] = ticker.upper()

    # Clean volume and change %
    df['volume'] = df['volume'].apply(convert_volume)
    df['change_percent'] = df['change_percent'].str.replace('%', '').astype(float)

    # Format date to YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date'], dayfirst=False, errors='coerce').dt.date

    # Reorder columns to match DB schema
    df = df[['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'change_percent']]

    # Append to master file
    df.to_csv(output, mode='a', header=not pd.io.common.file_exists(output), index=False)
    print(f"✅ Appended {len(df)} rows for {ticker} to {output}")

# Example usage:
# clean_and_append("AAPL_raw.csv", "AAPL")
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_stock_csv.py <input_csv> <TICKER>")
    else:
        clean_and_append(sys.argv[1], sys.argv[2])
