from yahoo_functions_revamp import YahooTicker
import os

def tickers_to_raw(ticker_list: list, key_list: list, file_path: str, downloads_directory_path: str):
    file = open(file_path,"a+")
    available_html_files = os.listdir(downloads_directory_path)
    header_str = "\"ticker\""
    for key in key_list:
        header_str += f",\"{key}\""
    file.write(header_str+"\n")
    for ticker in ticker_list:
        try:
            ticker = ticker.strip()
            fin_name = f"{ticker}_fin.html"
            bal_name = f"{ticker}_bal.html"
            if (fin_name in available_html_files) and (bal_name in available_html_files):
                read_file = open(downloads_directory_path+fin_name,"r")
                fin_txt = "".join(read_file.readlines())
                read_file.close()

                read_file = open(downloads_directory_path+bal_name,"r")
                bal_txt = "".join(read_file.readlines())
                read_file.close()

                y_ticker = YahooTicker(ticker = ticker,htmls = {"fin": fin_txt,"bal": bal_txt})
                next_line = ""
                vals = y_ticker.tuple_get(key_list)
                for val in vals:
                    next_line+=f"\"{val}\","
                next_line = next_line[:-1] #to remove last comma
                file.write(next_line+"\n")
        except BaseException as e:
            print(ticker)
            print(e.with_traceback())
    file.close()
if __name__ == "__main__":
    main1()
def main1():
    file = open("../all_tickers.txt", "r")
    lines = file.readlines()
    all_tickers = list(map(lambda x : x.replace("\n",""),lines))

    key_list = ["Total Assets","Total Liabilities","Gross Profit"]

    new_csv_path = "./results_.csv"
    downloads_path = "./downloads/"

    tickers_to_raw(all_tickers, key_list, new_csv_path, downloads_path)
