from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
import random
import string
import datetime
from controllers import encode
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理用の秘密鍵
app.config['UPLOAD_FOLDER'] = 'uploads'  # ファイルアップロード用のフォルダ

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

# 他のルートと機能をここに追加

if __name__ == '__main__':
    app.run(debug=True)
