import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

app = Flask(__name__, template_folder='.',static_url_path='/static', static_folder='static')
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'html'])
app.config['DEBUG'] = True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    res = {'success': False, 'message': ''}
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename and allowed_file(file.filename):
            filename = file.filename
            full_path = os.path.join(os.getcwd(), 'app/uploads')
            file.save(os.path.join(full_path, filename))
            res['success'] = True
            res['message'] = "File was uploaded"
            return render_template("./index.html", res = res)
        res['success'] = False
        res['message'] = "something went wrong!"
        return render_template("./index.html", res = res)

    return render_template("./index.html", res=res)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("./404.html"), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)