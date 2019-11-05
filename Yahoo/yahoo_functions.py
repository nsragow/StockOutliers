from bs4 import BeautifulSoup
import requests as re

def ticker_url(ticker: str) -> str:
    ticker = ticker.strip().upper()
    return f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"

def get_soup(url: str) -> BeautifulSoup:
    response = re.get(url)
    return BeautifulSoup(response.text)


def get_fin_data_table(bs: BeautifulSoup):
    table_in_list = bs.select("div.D\\(tbrg\\)")
    assert table_in_list.__len__() == 1, f"selector for fin data table returned list of len {table_in_list.__len__()}"
    return table_in_list[0]

def get_table_rows(table) -> list:
    return table.select("div.rw-expnded > div:nth-child(1)")

def name_and_recent_val(row) -> tuple:
    try:
        title_element = row.select("div[title]")
        assert len(title_element) == 1
        title_element = title_element[0]
        title = title_element.get("title")
        most_recent_val = row.select("div:nth-child(2) > span")
        assert len(most_recent_val) == 1
        val = most_recent_val[0].text
        return (title,val)
    except AssertionError as ae:
        return (ValueError("Formatting error" + str(ae)),row)

class YahooTable:
    def __init__(self, ticker: str):
        self.url = ticker_url(ticker)
        self.soup = get_soup(self.url)
        self.rows = get_table_rows(get_fin_data_table(self.soup))
        self.names_vals = list(map(name_and_recent_val,self.rows))
