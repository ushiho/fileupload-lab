'''
    solution proposed:
    generate a filename string by calculate
    the md5 hash of the current time
'''

import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import time
from hashlib import md5

app = Flask(__name__, template_folder='.',static_url_path='/static', static_folder='static')
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'html'])
app.config['DEBUG'] = True



def generate_filename(old_filename):
    # file extension
    ext = old_filename.split('.')[-1]
    now = str(time.time())
    hashed = md5(now.encode())
    new_filename = hashed.hexdigest() + '.' + ext
    print(new_filename)
    return new_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    res = {'success': False, 'message': ''}
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = generate_filename(file.filename)
            full_path = os.path.join(os.getcwd(), 'solution/uploads')
            file.save(os.path.join(full_path, filename))
            res['success'] = True
            res['message'] = "File was uploaded"
            return render_template("./index.html", res = res)
        res['success'] = False
        res['message'] = "something went wrong!"
        return render_template("./index.html", res = res)
    
    return render_template("./index.html", res=res)

@app.route("/clear", methods=['GET'])
def clear():
    upload_dir = os.path.join(os.getcwd(), 'solution/uploads')
    res = {}
    try:
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            os.unlink(file_path)
        res['success'] = True
        res['message'] = "Upload directory is clean"
    except Exception as e:
        print("Exception occured\n", e)
        res['success'] = False
        res['message'] = "An exception is occured!"
    return render_template("./index.html", res=res)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("./404.html"), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)