from bs4 import BeautifulSoup

def get_soup(url: str, html: str = None) -> BeautifulSoup:
    if html is None:
        response = re.get(url)
        text = response.text
    else:
        text = html
    return BeautifulSoup(text,features="html.parser")

def get_recent_val(key,yahoo_soup):
    val = yahoo_soup.select(f"div:has(> div[title=\"{key}\" i]) + div > span")
    assert len(val) == 1
    val = val[0]
    return val.text

class YahooTicker:
    def __init__(self, ticker: str, htmls: dict = None):
        self.ticker = ticker.strip()
        base_url = f"https://finance.yahoo.com/quote/{self.ticker}/"
        fin_url = base_url + f"financials?p={self.ticker}"
        bal_sheet_url = base_url + f"balance-sheet?p={self.ticker}"
        if htmls is None:
            htmls = {"fin": None, "bal": None}
        self.fin_soup = get_soup(fin_url, htmls["fin"])
        self.bal_sheet_soup = get_soup(bal_sheet_url,htmls["bal"])
    def get(self,key: str):
        try:
            return get_recent_val(key,self.fin_soup)
        except:
            try:
                return get_recent_val(key,self.bal_sheet_soup)
            except:
                return None
    def tuple_get(self, keys: list) -> tuple:
        """
        Will return a tuple with the first value being the ticker string
        followed by the values returned from self.get for each of
        the keys in keys
        """
        temp_list = [self.ticker]
        for key in keys:
            temp_list.append(self.get(key))
        return tuple(temp_list)
