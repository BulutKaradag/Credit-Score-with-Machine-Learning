import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("modelcatb.pkl", "rb"))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    skor_text =""
    skor = ""
    skor_aciklama = ""
    float_features = [float(x) for x in request.form.values()]
    features = (float_features)
    prediction = model.predict(features)
    if prediction[0] == "0":
        skor_text = "Az Riskli" 
        skor_aciklama = "Kredi oranı çok yüksek tutulur ve çok düşük limitli kredi kartı verilebilir."
        skor = "D"
    if prediction[0] == 1:
        skor_text = "Orta Riskli" 
        skor_aciklama = "Kredi oranlarında bir ayrıcalık yapılmaz, belirlenecek tahsis limiti yüksek olmaz."
        skor = "C"
    if prediction[0]  == 2:
        skor_text = "Çok Riskli" 
        skor_aciklama = "Çoğu kredi ve kredi kartı başvurusu reddedilir."
        skor = "E"
    if prediction[0] == 3:
        skor_text = "Çok İyi" 
        skor_aciklama = "En iyi kredi kartı segmentine sahip bir kart verilebilir, ev ve araç kredisi kullandırılır."
        skor = "A"
    if prediction[0] == 4:
        skor_text = "İyi" 
        skor_aciklama = "Çoğu kredi kartı ve kredi verilebilir, ancak en iyi fırsatlar verilmeyebilir."
        skor = "B"

    return render_template("index.html", prediction_text = "Müşterinin Kredi Durumu:"  + skor_text, prediction_aciklama = "Skor Açıklaması:"+ skor_aciklama,  score = "Müşterinin Kredi Skoru:" + skor)

if __name__ == "__main__":
    flask_app.run(debug=True)