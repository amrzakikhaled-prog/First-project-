from flask import Flask, request, render_template_string

app = Flask(__name__)

last_secret = "لا يوجد Training Secret مستلم حتى الآن"


# ==========================================
# صفحة الطالب الأول
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
        ⚠️ استخدم Training Secret فقط
    </p>

</div>

</body>
</html>
"""


# ==========================================
# صفحة الطالب الثاني
# ==========================================

receiver_page = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
    <meta charset="UTF-8">

    <!-- تحديث الصفحة كل ثانيتين -->
    <meta http-equiv="refresh" content="2">

    <title>Receiver</title>

    <style>

        body {
            font-family: Arial;
            background: #111;
            color: white;
            text-align: center;
            padding-top: 80px;
        }

        .box {
            width: 500px;
            max-width: 90%;
            margin: auto;
            padding: 40px;
            background: #222;
            border-radius: 20px;
        }

        .secret {
            background: white;
            color: red;
            padding: 20px;
            margin-top: 30px;
            font-size: 28px;
            border-radius: 10px;
            font-weight: bold;
            word-break: break-word;
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

    <h2>آخر Training Secret مستلم:</h2>

    <div class="secret">
        {{ secret }}
    </div>

    <p class="warning">
        ⚠️ هذا Demo تعليمي فقط
    </p>

</div>

</body>
</html>
"""


# ==========================================
# استقبال البيانات من الطالب الأول
# ==========================================

@app.route("/", methods=["GET", "POST"])
def student():

    global last_secret

    if request.method == "POST":

        username = request.form.get("username", "")
        secret = request.form.get("secret", "")

        # السماح فقط بالـ Training Secret
        if secret.startswith("TRAINING-"):

            last_secret = secret

            # يظهر في Logs الخاصة بـ Render
            print("\n" + "=" * 60)
            print("🚨 PHISHING AWARENESS DEMONSTRATION")
            print("=" * 60)
            print(f"👤 Username: {username}")
            print(f"🔐 Training Secret: {secret}")
            print("=" * 60)
            print("⚠️ هذا السر تدريبي وليس كلمة مرور حقيقية")
            print("=" * 60 + "\n")

        else:

            print("\n⚠️ تم رفض الإدخال.")
            print("استخدم Training Secret يبدأ بـ TRAINING-\n")

    return render_template_string(student_page)


# ==========================================
# صفحة الطالب الثاني
# ==========================================

@app.route("/receiver")
def receiver():

    return render_template_string(
        receiver_page,
        secret=last_secret
    )


# ==========================================
# تشغيل التطبيق
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
