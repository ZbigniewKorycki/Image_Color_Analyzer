from flask import Flask, flash, render_template, url_for, redirect
import os
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField, FileField
import secrets
from colorthief import ColorThief
import matplotlib.pyplot as plt

UPLOAD_FOLDER = r".\static\uploads"
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


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=("GET", "POST"))
def upload_image():
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.image.data
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File updated correctly")
            return render_template("home.html", filename=filename, form=form)
        else:
            flash("Incorrect file type")
    return render_template("home.html", form=form)


@app.route("/display/<filename>", methods=["GET", "POST"])
def display_image(filename):
    return redirect(url_for('static', filename="uploads/" + filename))


@app.route("/palette/<filename>", methods=["GET", "POST"])
def color_analyzer(filename):
    ct = ColorThief("static/uploads/" + filename)
    palette = ct.get_palette(color_count=5)
    plt.imshow([[palette[i] for i in range(5)]])
    plt.savefig("static/palette/" + filename)
    return redirect(url_for('static', filename="palette/" + filename))


if __name__ == "__main__":
    app.run(debug=True)
