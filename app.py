from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

DB_FILE = "users.json"


# создать файл если нет
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


# загрузить пользователей
def load_users():
    if not os.path.exists(DB_FILE):
        return []

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# сохранить пользователей
def save_users(users):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


# открыть index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# регистрация
@app.route("/api/register", methods=["POST"])
def register():

    data = request.json

    if not data:
        return jsonify({
            "status": "error",
            "message": "Нет данных"
        })

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Нет email или пароля"
        })

    users = load_users()

    # проверка существует ли пользователь
    for user in users:
        if user["email"] == email:
            return jsonify({
                "status": "error",
                "message": "Пользователь уже существует"
            })

    # сохранить пользователя
    users.append({
        "email": email,
        "password": password,
        "firstName": data.get("firstName"),
        "lastName": data.get("lastName"),
        "birth": data.get("birth"),
        "card": data.get("card"),
        "exp": data.get("exp"),
        "cvv": data.get("cvv")
    })

    save_users(users)

    return jsonify({
        "status": "ok"
    })


# вход
@app.route("/api/login", methods=["POST"])
def login():

    data = request.json

    if not data:
        return jsonify({
            "status": "error",
            "message": "Нет данных"
        })

    email = data.get("email")
    password = data.get("password")

    users = load_users()

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({
                "status": "ok"
            })

    return jsonify({
        "status": "error",
        "message": "Неверный email или пароль"
    })


# запуск
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
