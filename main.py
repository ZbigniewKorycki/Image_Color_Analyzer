from flask import Flask, render_template, request, url_for
import os
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField, FileField
import secrets


UPLOAD_FOLDER = ".\static"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
foo = secrets.token_urlsafe(16)
app.secret_key = foo


csrf = CSRFProtect(app)

bootstrap = Bootstrap5(app)


class UploadImageForm(FlaskForm):
    image = FileField('Image', validators=[InputRequired()])
    submit = SubmitField("Submit File")


@app.route("/", methods=("GET", "POST"))
def home():
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.image.data
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return "File updated correctly"
    return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)