from flask import Flask, jsonify, abort

app = Flask(__name__)
#app.config['JSON_AS_ASCII'] = False
app.json.ensure_ascii = False
todos = [
    {"id": 1, "gorev": "Python REST API Projesini Başlatt", "yapildi": True},
    {"id": 2, "gorev": "Tüm yapılacakları listele (GET)", "yapildi": False},
    {"id": 3, "gorev": "Tek bir yapılacak işi göster (GET)", "yapildi": False},
]


@app.route('/api/todos', methods=['GET'])
def tum_todolari_getir():
    return jsonify(todos)

@app.route('/debug/config')
def debug_config():
    # Flask'ın o anki aktif konfigürasyonunu bir sözlük olarak alalım
    config_dict = dict(app.config)
    # Bu sözlüğü JSON olarak döndürelim ki tarayıcıda görebilelim
    return jsonify(config_dict)

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def tek_todoyu_getir(todo_id):
    bulunan_todo = [todo for todo in todos if todo['id'] == todo_id]

    if len(bulunan_todo) == 0:
        abort(404)

    return jsonify(bulunan_todo[0])


if __name__ == '__main__':
    app.run(debug=True)

""" 
#eski çalışmalar
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

"""
