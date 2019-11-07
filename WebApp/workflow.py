import pickle
from yahoo_functions_revamp import YahooTicker

model_file = open("./lin_model.pkl","rb")
model = pickle.load(model_file)
model_file.close()


def get_values(ticker: str):
    y_ticker = YahooTicker(ticker)
    to_predict = [(int(y_ticker.get("Total Assets").replace(",","")),int(y_ticker.get("Total Liabilities").replace(",","")))]
    prediction = model.predict(to_predict)
    return (prediction,y_ticker.get_market_cap())

if __name__ == "__main__":
    print(get_values("FANG"))
