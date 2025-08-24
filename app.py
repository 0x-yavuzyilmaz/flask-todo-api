from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def merhaba_dunya():
    return "Merhaba, Web Dünyası!"


@app.route('/hakkimda')
def hakkimda_sayfasi():
    return "Ben bir yazilim mimarıyım!"


@app.route('/api/kisiler')
def kisileri_getir():
    rehber = [
        {'isim': 'Walter White', 'telefon': '555-1234'},
        {'isim': 'Jesse Pinkman', 'telefon': '555-5678'},
    ]
    return jsonify(rehber)


if __name__ == '__main__':
    app.run(debug=True)
