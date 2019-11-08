from flask import Flask,request
from workflow import get_values
app = Flask(__name__)

@app.route("/predict")
def predict():
    ticker = request.args.get('ticker')
    predicted,actual = get_values(ticker)
    return f"Prediction: {predicted}\nActual: {actual}"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
