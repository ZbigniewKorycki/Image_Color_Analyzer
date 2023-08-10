from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField, FileField
import secrets


UPLOAD_FOLDER = r"C:\Users\zbign_x5x2ftd\PycharmProjects\DetectingColor\uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
foo = secrets.token_urlsafe(16)
app.secret_key = foo


csrf = CSRFProtect(app)

bootstrap = Bootstrap5(app)


class UploadImageForm(FlaskForm):
    image = FileField('Image')
    submit = SubmitField("Submit File")

def allowed_file(image):
    return "." in image and image.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=("GET", "POST"))
def home():
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.image
    return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)