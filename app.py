from flask import Flask, jsonify, abort, request

# --- Uygulama Kurulumu ---
app = Flask(__name__)
app.json.ensure_ascii = False

# --- "Veritabanı" ---
todos = [
    {"id": 1, "task": "Start Python REST API Project", "done": True},
    {"id": 2, "task": "List all todos (GET)", "done": False},
    {"id": 3, "task": "Show a single todo (GET)", "done": False},
]


# --- Karakter Seti Yardımcısı ---
@app.after_request
def set_charset(response):
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


# --- API Rotaları (Endpoints) ---

# /api/todos adresine gelen GET ve POST isteklerini yönetir
@app.route('/api/todos', methods=['GET', 'POST'])
def handle_todos():
    if request.method == 'GET':
        # Tüm yapılacakları listele
        return jsonify(todos)

    if request.method == 'POST':
        # Yeni bir yapılacak iş oluştur
        if not request.json or 'task' not in request.json:
            abort(400, description="Request must be JSON and contain a 'task' field.")

        new_id = todos[-1]['id'] + 1 if todos else 1
        new_todo = {
            'id': new_id,
            'task': request.json['task'],
            'done': False
        }
        todos.append(new_todo)
        return jsonify(new_todo), 201


# /api/todos/<id> adresine gelen GET, PUT, DELETE isteklerini yönetir
@app.route('/api/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_todo(todo_id):
    # Önce, istenen 'todo'yu bulalım. Bu, tüm metotlar için ortak.
    found_todo_list = [todo for todo in todos if todo['id'] == todo_id]
    if not found_todo_list:
        abort(404)

    todo = found_todo_list[0]

    if request.method == 'GET':
        return jsonify(todo)

    if request.method == 'PUT':
        # Gelen veriyi kontrol et
        if not request.json:
            abort(400, description="Request must be JSON.")
        if 'task' not in request.json or 'done' not in request.json:
            abort(400, description="Missing 'task' or 'done' fields.")
        if not isinstance(request.json.get('done'), bool):
            abort(400, description="'done' field must be a boolean.")

        # Veriyi güncelle
        todo['task'] = request.json.get('task', todo['task'])  # .get() daha güvenli
        todo['done'] = request.json.get('done', todo['done'])
        return jsonify(todo)

    if request.method == 'DELETE':
        todos.remove(todo)
        return jsonify({'result': True, 'message': f'Todo with ID {todo_id} has been deleted.'})


# --- Ana Çalıştırma Bloğu ---
if __name__ == '__main__':
    app.run(debug=True)