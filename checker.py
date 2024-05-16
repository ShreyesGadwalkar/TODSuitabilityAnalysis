import pandas as pd
import ssl
import certifi
import urllib.request

# Function to download and inspect CSV columns
def inspect_csv_columns(url):
    context = ssl.create_default_context(cafile=certifi.where())
    response = urllib.request.urlopen(url, context=context)
    df = pd.read_csv(response)
    print(df.columns)

# Inspect column names
inspect_csv_columns('https://data.sfgov.org/resource/acdm-wktn.csv')
inspect_csv_columns('https://data.sfgov.org/resource/gtr9-ntp6.csv')
inspect_csv_columns('https://data.sfgov.org/resource/tpp3-epx2.csv')
inspect_csv_columns('https://data.sfgov.org/resource/i28k-bkz6.csv')
