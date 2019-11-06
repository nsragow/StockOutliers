#from yahoo_functions_revamp import YahooTicker
import os

def tickers_to_raw(ticker_list: list, key_list: list, file_path: str, downloads_directory_path: str):
    file = open(file_path,"a+")
    available_html_files = os.listdir(downloads_directory_path)
    for ticker in ticker_list:
        ticker = ticker.strip()
        fin_name = f"{ticker}_fin.html"
        bal_name = f"{ticker}_bal.html"
        if (fin_name in available_html_files) and (bal_name in available_html_files):
            file = open(downloads_directory_path+fin_name,"r")
            fin_txt = file.readlines()
            file.close()

            file = open(downloads_directory_path+bal_name,"r")
            bal_txt = file.readlines()
            file.close()

            
