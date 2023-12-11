from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
from common.models import curd
from controllers import manage_password
import os
import random
import string
import datetime
from controllers import encode
import io
from helpers import apology, login_required

app = Flask(__name__)

with open('secret_key.txt') as f:
    app.secret_key = f.read().strip()


# 暗号化キーの生成
def generate_key(length=20):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


# メインページ
@app.route('/')
def index():
    return render_template('index.html')


# ファイルアップロードと暗号化
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('ファイルが選択されていません。', 'error')
        return redirect(request.url)
    file = request.files['file']
    key = request.form['key']
    if not key:
        flash('キーが入力されていません。', 'error')
        return redirect(request.url)
    
    try:
        encrypted_data = encode.encrypt_decrypt(file.read(), key.encode())
        file_stream = io.BytesIO(encrypted_data)
        file_stream.seek(0)
        # 'download_name' パラメータを設定
        download_name = 'encrypted_' + file.filename
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=download_name,
            mimetype='application/octet-stream'  # MIMEタイプの設定
        )
    except Exception as e:
        flash(str(e), 'error')
        return redirect(request.url)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    # ユーザーidをクリアする
    session.clear()
    # POSTの場合
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = manage_password.password_hash(password)

        if curd.check_login_attempts(username):
            return "複数回のログイン試行が検出されました。しばらくお待ちください。", 403

        
        if not username:
            return apology("ユーザーネームを入力してください", 403)
        elif not password:
            return apology("パスワードを入力してください", 403)

        user = curd.check_user(username)
        print(user)

        # ユーザーネームとパスワードが正しいか確認
        if user[3] == hashed_password:
            session["user_id"] = user[0]
            # flash("ログインしました")
            return redirect("/")
        else:
            return apology("ユーザネームが無効です", 403)

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    #　ユーザーidをクリアする
    session.clear()
    # ログインページに送る
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        password_hash = manage_password.password_hash(password)

        if not username:
            return apology("ユーザーネームを入力してください", 400)
        elif not password:
            return apology("パスワードを入力してください", 400)
        elif password != confirmation:
            return apology("パスワードが一致しません", 400)

        user = curd.check_user(username)
        if user:
            return apology("このユーザーネームは既に使われています", 400)

        curd.register_user(username, password_hash)
        flash("登録が完了しました")
        return redirect("/login")
    else:
        return render_template("register.html")


# 他のルートと機能をここに追加

if __name__ == '__main__':
    app.run(debug=True)
