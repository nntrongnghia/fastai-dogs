from fastai.vision import open_image, load_learner
from base64 import b64encode
from io import BytesIO
from flask import Flask, render_template, flash, request, redirect,\
    url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
print('Packages loaded!')

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.secret_key = b'_5#y32L"F#^8z\n\xec]/'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            im = BytesIO(file.read())
            img_tag = "data:image/png;base64," + \
                b64encode(im.getvalue()).decode('UTF-8')
            # === PREDICTION
            # - open image fastai from BytesIO im
            im_fast = open_image(im)
            # - predict
            pred = model.predict(im_fast)[0]
            print(pred)
            # - change template html to display the predicted class
            return render_template('show_image.html', img_tag=img_tag, pred = pred)
    return render_template('upload.html')


if __name__ == '__main__':
    print("Loading model...")
    try:
        print(os.listdir('.'))
        model = load_learner('./models', fname='export.pkl')
        print('Model loaded')
    except:
        print('Fail to load the model. Kill the program')
    app.run(debug=True)
