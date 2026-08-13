from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "training_demo.db"


# ==========================================
# Database
# ==========================================

def init_db():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS demo_data (
            id INTEGER PRIMARY KEY,
            username TEXT,
            training_secret TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_demo_data(username, secret):
    conn = sqlite3.connect(DB_FILE)

    conn.execute("DELETE FROM demo_data")

    conn.execute(
        """
        INSERT INTO demo_data
        (username, training_secret)
        VALUES (?, ?)
        """,
        (username, secret)
    )

    conn.commit()
    conn.close()


def get_demo_data():
    conn = sqlite3.connect(DB_FILE)

    result = conn.execute(
        """
        SELECT username, training_secret
        FROM demo_data
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    if result:
        return result[0], result[1]

    return "لا يوجد", "لا يوجد Training Secret"


# ==========================================
# Student 1 Page
# ==========================================

student_page = """
<!DOCTYPE html>

<html lang="ar" dir="rtl">

<head>

<meta charset="UTF-8">

<title>Security Awareness Demo</title>

<style>

body {
    font-family: Arial;
    background: #f2f2f2;
    text-align: center;
    padding-top: 70px;
}

.box {
    background: white;
    width: 350px;
    margin: auto;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 0 15px #aaa;
}

input {
    width: 90%;
    padding: 12px;
    margin: 8px;
    font-size: 16px;
    box-sizing: border-box;
}

button {
    padding: 12px 30px;
    font-size: 17px;
    cursor: pointer;
    border: none;
    border-radius: 8px;
}

.warning {
    color: red;
    margin-top: 20px;
}

</style>

</head>

<body>

<div class="box">

<h1>🔐 Login Demo</h1>

<form method="POST">

<input
    type="text"
    name="username"
    placeholder="Username"
    required
>

<input
    type="text"
    name="secret"
    placeholder="Training Secret"
    required
>

<button type="submit">
    Login
</button>

</form>

<p class="warning">
ادخل كلمة مرورك مطمئن
</p>

</div>

</body>

</html>
"""


# ==========================================
# Student 2 / Receiver Page
# ==========================================

receiver_page = """
<!DOCTYPE html>

<html lang="ar" dir="rtl">

<head>

<meta charset="UTF-8">

<meta http-equiv="refresh" content="2">

<title>Receiver</title>

<style>

body {
    font-family: Arial;
    background: #111;
    color: white;
    text-align: center;
    padding-top: 70px;
}

.box {
    width: 500px;
    max-width: 90%;
    margin: auto;
    padding: 40px;
    background: #222;
    border-radius: 20px;
}

.data {
    background: white;
    color: #111;
    padding: 20px;
    margin: 15px 0;
    font-size: 24px;
    border-radius: 10px;
    font-weight: bold;
    word-break: break-word;
}

.secret {
    color: red;
}

.warning {
    color: orange;
    margin-top: 30px;
}

</style>

</head>

<body>

<div class="box">

<h1>📡 Receiver</h1>

<h2>البيانات التدريبية المستلمة</h2>

<p>👤 Username:</p>

<div class="data">
    {{ username }}
</div>

<p>🔐 Training Secret:</p>

<div class="data secret">
    {{ secret }}
</div>

<p class="warning">
أخلاقي ☠️ 
</p>

</div>

</body>

</html>
"""


# ==========================================
# Student 1
# ==========================================

@app.route("/", methods=["GET", "POST"])
def student():

    if request.method == "POST":

        username = request.form.get("username", "")
        secret = request.form.get("secret", "")

        # السماح فقط بالـTraining Secret
        if secret:

            save_demo_data(username, secret)

            print("\n" + "=" * 60)
            print("🚨 PHISHING AWARENESS DEMONSTRATION")
            print("=" * 60)
            print(f"👤 Username: {username}")
            print(f"🔐 Training Secret: {secret}")
            print("=" * 60)
            print("⚠️ Training Secret فقط")
            print("=" * 60 + "\n")

        else:

            print("\n⚠️ تم رفض الإدخال.")
            print("استخدم Training Secret يبدأ بـ TRAINING-\n")

    return render_template_string(student_page)


# ==========================================
# Receiver
# ==========================================

@app.route("/receiver")
def receiver():

    username, secret = get_demo_data()

    return render_template_string(
        receiver_page,
        username=username,
        secret=secret
    )


# ==========================================
# Start Application
# ==========================================

init_db()


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    ) 
