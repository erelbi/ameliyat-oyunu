from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__, static_url_path='/static')
CORS(app)

SKOR_DOSYA = 'skorlar.json'

def skor_yukle():
    if not os.path.exists(SKOR_DOSYA):
        return []
    with open(SKOR_DOSYA, 'r') as f:
        return json.load(f)

def skor_kaydet(skor):
    tum_skorlar = skor_yukle()
    tum_skorlar.append(skor)
    with open(SKOR_DOSYA, 'w') as f:
        json.dump(tum_skorlar, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ameliyat')
def oyun():
    return render_template('ameliyat.html')

@app.route('/skorlar')
def skor_sayfasi():
    return render_template('skorlar.html')

@app.route('/api/skor', methods=['POST'])
def skor_ekle():
    veri = request.json
    veri['tarih'] = datetime.utcnow().isoformat()
    skor_kaydet(veri)
    return jsonify({"durum": "ok", "skor": veri}), 201

@app.route('/api/skorlar', methods=['GET'])
def skor_listesi():
    return jsonify(skor_yukle())

if __name__ == '__main__':
    app.run(debug=True)
