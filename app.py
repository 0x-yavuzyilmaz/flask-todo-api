from flask import Flask, jsonify, abort, request

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


# Rota: Yeni bir yapılacak iş oluştur
@app.route('/api/todos', methods=['POST'])
def create_todo():
    # 1. Gelen isteğin JSON formatında olup olmadığını kontrol et.
    #    Eğer değilse veya veri yoksa, 400 Bad Request (Kötü İstek) hatası ver.
    if not request.json or not 'task' in request.json:
        abort(400)

    # 2. Yeni todo için ID belirle. Listenin son elemanının ID'sini alıp 1 artır.
    #    Eğer liste boşsa, ID'yi 1 olarak başlat.
    new_id = todos[-1]['id'] + 1 if todos else 1

    # 3. Gelen JSON verisinden yeni bir todo sözlüğü oluştur.
    #    'done' durumu varsayılan olarak False olsun.
    new_todo = {
        'id': new_id,
        'task': request.json['task'],
        'done': False
    }

    # 4. Yeni oluşturulan todo'yu "veritabanımıza" (listemize) ekle.
    todos.append(new_todo)

    # 5. Başarılı bir oluşturma işleminin ardından, REST standardı gereği
    #    oluşturulan yeni nesneyi ve 201 Created (Oluşturuldu) durum kodunu döndür.
    return jsonify(new_todo), 201



@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    # 1. Güncellenecek 'todo'yu ID'sine göre bul. (GET'ten tanıdık)
    found_todo = [todo for todo in todos if todo['id'] == todo_id]
    if len(found_todo) == 0:
        abort(404)  # Bulamazsak 404 hatası ver.

    # 2. Gelen isteğin JSON olup olmadığını ve gerekli alanları içerip içermediğini kontrol et. (POST'tan tanıdık)
    if not request.json:
        abort(400, description="Request must be JSON")
    if 'task' not in request.json or 'done' not in request.json:
        abort(400, description="Missing 'task' or 'done' in request body")
    if not isinstance(request.json['done'], bool):
        abort(400, description="'done' must be a boolean (true/false)")

    # 3. Bulduğumuz 'todo'nun verilerini güncelle.
    #    found_todo bir liste olduğu için ilk elemanını ([0]) alıyoruz.
    todo_to_update = found_todo[0]
    todo_to_update['task'] = request.json['task']
    todo_to_update['done'] = request.json['done']

    # 4. Güncellenmiş nesneyi ve 200 OK durum kodunu döndür.
    return jsonify(todo_to_update)

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
