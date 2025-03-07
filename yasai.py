import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

import numpy as np


classes = ['きゃべつ','じゃがいも','とまと','たまねぎ','かぼちゃ']#表示する回答
#モデルで指定したサイズと同じにする
image_size = 100


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#学習済みモデルをロード
model = load_model('./my_model.h5', compile=False)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':#requestはウェブ上のフォームから送信したデータを扱うための関数。request.method
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)#redirect()は引数に与えられたurlに移動する関数
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)#ファイル名に危険な文字列がある場合に無効化（サニタイズ）する
            file.save(os.path.join(UPLOAD_FOLDER, filename))#os.path.join()で引数に与えられたパスアップロードされた画像を保存。その保存先をfilepathに格納
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            #受け取った画像を読み込み、np形式に変換、#grayscale=False.Trueから変更
            img = image.load_img(filepath, grayscale=False, target_size=(image_size,image_size))
            img = image.img_to_array(img)
            data = np.array([img])
            #変換したデータをモデルに渡して予測する
            result = model.predict(data)[0]
            predicted = result.argmax()
            pred_answer = "これは " + classes[predicted] + " です"

            return render_template("yasai2.html",answer=pred_answer)

    return render_template("yasai2.html",answer="")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)

#if __name__ == "__main__":
#    app.run()