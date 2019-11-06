import requests as re

def download_text(ticker):
    base_url = f"https://finance.yahoo.com/quote/{ticker}/"
    fin_url = base_url + f"financials?p={ticker}"
    bal_sheet_url = base_url + f"balance-sheet?p={ticker}"
    fin_file = open(f"./downloads/{ticker}_fin.html","w+")
    bal_file = open(f"./downloads/{ticker}_bal.html","w+")


    fin_file.write(re.get(fin_url).text)
    bal_file.write(re.get(bal_sheet_url).text)

if __name__ == "__main__":
    file = open("../all_tickers.txt", "r")
    lines = file.readlines()
    all_tickers = list(map(lambda x : x.replace("\n",""),lines))
    for ticker in all_tickers:
        try:
            download_text(ticker)
        except:
            print("failed on ticker "+ ticker)
