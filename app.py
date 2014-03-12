from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import model
import os
import pytesser
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "./image_files"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "superdupersecretish"

# Specify the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if the filename ends in one of the allowed extensions"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_image(path):
    """Run the image through Tesseract and get text."""
    # TODO: Add an image processing step.
    text = pytesser.image_file_to_string(path, lang='chi_sim', graceful_errors=True)

    # Text is in utf-8. Decode to Unicode, and strip extra newline character.
    return text.decode('utf-8').rstrip('\n')

def lookup_text(text):
    combinations = model.find_combinations(text)
    chars = model.search(combinations)
    return chars


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def upload_image():
    """Get uploaded image, process, and redirect to appropriate page."""

    print "Entered route."
    print request
    # Get the file from the request object
    file = request.files['file']
    print file.filename;

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # file.save actually saves it on the system
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        # send the image to tesseract for processing
        text = process_image(image_path)

        # Look up the dish in the dishes table.
        dish = model.session.query(model.Dish).filter_by(chin_name=text).first()

        if dish:
            return redirect(url_for("view_dish", id=dish.id))
        else:
            return redirect(url_for("translate_text", text=text))
    else:
        flash("Bad image filename.")
        return redirect(url_for("index"))

@app.route("/dish/<int:id>", methods=["GET"])
def view_dish(id):
    dish = model.session.query(model.Dish).get(id)
    return render_template("dish.html", dish=dish)

@app.route("/dish/search/<string:text>", methods=["GET"])
def translate_text(text):
    chars = lookup_text(text)
    if chars:
        #authenticated = session.get("user_id")
        authenticated = True
        return render_template("search.html", dish=chars, searchstring=text, authenticated=authenticated)
    else:
        # redirect to search instead?
        return redirect(url_for("index"))

@app.route("/dish/new", methods=["POST"])
def add_dish():
    chin_name = request.form.get("chin_name")
    eng_name = request.form.get("eng_name")
    pinyin = request.form.get("pinyin")
    desc = request.form.get("desc")
    dish = model.Dish(chin_name=chin_name, eng_name=eng_name, pinyin=pinyin, desc=desc)
    model.session.add(dish)
    model.session.commit()
    return redirect(url_for("view_dish", id=dish.id))

if __name__ == "__main__":
    # Change debug to False when deploying, probably.
    app.run(debug = True)

