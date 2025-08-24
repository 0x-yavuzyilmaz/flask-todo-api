from flask import Flask, jsonify, abort

# --- Uygulama Kurulumu ve Konfigürasyon ---

app = Flask(__name__)

# JSON çıktılarında Türkçe gibi Unicode karakterlerin doğru görüntülenmesini sağla.
# Bu, senin bulduğun daha modern ve doğrudan bir yoldur.
app.json.ensure_ascii = False

# --- "Veritabanı" ve Yardımcı Fonksiyonlar ---

# Başlangıç için sahte veritabanımız (İngilizce anahtarlar ve verilerle)
todos = [
    {"id": 1, "task": "Start Python REST API Project", "done": True},
    {"id": 2, "task": "List all todos (GET)", "done": False},
    {"id": 3, "task": "Show a single todo (GET)", "done": False},
]


# Bu decorator, her cevaba UTF-8 karakter setini ekleyerek
# istemcilerin (tarayıcıların) cevabı doğru okumasını garanti eder.
@app.after_request
def set_charset(response):
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


# --- API Rotaları (Endpoints) ---

# Rota: Tüm yapılacakları listele
@app.route('/api/todos', methods=['GET'])
def get_all_todos():  # Fonksiyon adı İngilizce'ye çevrildi
    return jsonify(todos)


# Rota: Sadece ID'si belirtilen tek bir yapılacak işi getir
@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_single_todo(todo_id):  # Fonksiyon adı İngilizce'ye çevrildi
    # List comprehension ile aradığımız ID'ye sahip todo'yu bulalım
    found_todo = [todo for todo in todos if todo['id'] == todo_id]  # Değişken adı İngilizce'ye çevrildi

    # Eğer o ID'ye sahip bir todo bulunamazsa, 404 hatası döndür
    if len(found_todo) == 0:
        abort(404)

    # List comprehension bir liste döndürdüğü için, ilk elemanını alıyoruz.
    return jsonify(found_todo[0])


# --- Ana Çalıştırma Bloğu ---

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
