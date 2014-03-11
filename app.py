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
    print text
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
    # Get the file from the request object
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save actually saves it on the system
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        text = process_image(image_path)

        # TODO: This should look up the dish in the dish database.
        dish_id = None

        # TODO: This should return dish_id
        if dish_id:
            return redirect(url_for("view_dish", id=dish_id))
        else:
            # TODO: Look up text.
            dish = lookup_text(text)
            if dish:
                #TODO: Redirect to create new dish.
                #authenticated = session.get("user_id")
                authenticated = False
                return render_template("newdish.html", dish=dish, searchstring=text, authenticated=authenticated)
            else:
                return "Dish not found."

@app.route("/dish/<int:id>", methods=["GET"])
def view_dish(id):
    # TODO: Have this find the name of the dish in the database.
    session = model.connect()
    dish = session.query(model.Entry).get(id)
    return render_template("dish.html", dish=dish)

# @app.route("/dish/add", methods=["GET"])
# def add_dish(dish, searchstring):
#     # TODO - check if logged in first
#     return render_template("newdish.html", dish=dish)

if __name__ == "__main__":
    app.run(debug = True)