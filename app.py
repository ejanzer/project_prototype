from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import model
import os
import pytesser
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "./image_files"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

# Specify the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # Checks if the filename ends in one of the allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_image(path):
    text = pytesser.image_file_to_string(path, lang='chi_sim', graceful_errors=True)
    return text.decode('utf-8')

def lookup_text(text):
    session = model.connect()
    entry = session.query(model.Entry).filter_by(simplified=text).first()
    return entry.definition

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def upload_image():
    # Get the file from the request object
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save actually saves it on the system
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        text = process_image(image_path)
        dish_name = lookup_text(text)
        # TODO: Have it look up dish in database, find id, etc.
        return dish_name

@app.route("/image/<filename>", methods=["GET"])
def uploaded_file(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/dish/<int:id>", methods=["GET"])
def view_dish(id):
    # TODO: Have this find the name of the dish in the database.
    dish_name = ""
    return render_template("dish.html", name=dish_name)

if __name__ == "__main__":
    app.run(debug = True)