import datetime
import base64
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
import model
import os
import pytesser
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps, ImageFilter
from urllib import urlopen


UPLOAD_FOLDER = "./image_files"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "superdupersecretish"

# Specify the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def auth():
    return session.get("user_id")

def allowed_file(filename):
    """Check if the filename ends in one of the allowed extensions"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def prepare_image(im):
    """Prepare the image by smoothing it and converting to grayscale."""
    im = im.filter(ImageFilter.SMOOTH_MORE)
    im = im.filter(ImageFilter.SMOOTH_MORE)
    if 'L' != im.mode:
        im = im.convert('L')

    return im

def remove_noise_by_pixel(im, column, line, pass_factor):
    """Change a certain pixel to white or black depending on how it compares to threshold."""
    if im.getpixel((column, line)) < pass_factor:
        # If the color value of an image is less than the pass factor, make it black.
        return (0)
    # Otherwise, make it white.
    return (255)

def remove_noise(im, pass_factor):
    """Go through every pixel and convert to white or black based on a threshold pixel."""
    # for every pixel in the image
    for column in range(im.size[0]):
        for line in range(im.size[1]):
            # if it's darker than a certain value, replace with black.
            # otherwise, replace with white.
            value = remove_noise_by_pixel(im, column, line, pass_factor)
            im.putpixel((column, line), value)
    return im

def normalize_image(image_path):
    """Convert image to grayscale and heighten contrast to optimize for Tesseract."""
    
    # open the image from the path
    im = Image.open(image_path)

    # smooth image (get rid of little lines, dots) and convert to grayscale
    im = prepare_image(im)

    # remove noise in the image by converting everything to black or white
    # pass factor is the color threshold for determining whether a pixel becomes 
    # black or white
    # TODO: Calculate pass factor based on darkest color value in image somehow?
    pass_factor = 150
    im = remove_noise(im, pass_factor)

    im.save(image_path)

    return im


def process_image(path):
    """Run the image through Tesseract and get text."""

    normalize_image(path)
    print "converted im"

    text = pytesser.image_file_to_string(path, lang='chi_sim', graceful_errors=True)
    print text

    # Text is in utf-8. Decode to Unicode, and strip extra newline character.
    return text.decode('utf-8').rstrip('\n')

def lookup_text(text):
    """Find likely words in the text and look them up in the database.
    Returns a list of Entry objects."""

    # Get all combinations of sequential characters in the string.
    combinations = model.find_combinations(text)

    # Look them up until you've found a complete definition.
    chars = model.search(combinations)
    return chars

def get_route(image_path):
    """Return the appropriate route for an image uploaded by a user.
    Run the image through Tesseract and get text,
    Look up the text in the dishes table,
    If it's not there, then look up individual words in the dictionary."""

    print image_path
    # send the image to tesseract for processing    
    text = process_image(image_path)
    print text

    if text:

        # Look up the dish in the dishes table, if it exists.
        dish = model.session.query(model.Dish).filter_by(chin_name=text).first()
        print dish

        # if the dish is already in the table, return the view for that dish.
        if dish:
            return redirect(url_for("view_dish", id=dish.id))

        # otherwise, send text to translate_text to look it up in the dictionary.
        else:
            return redirect(url_for("translate_text", text=text))

    else:
        flash("I'm sorry, I couldn't find any text in that image. Please try again.")
        return redirect(url_for("index"))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", authenticate=auth())

@app.route("/", methods=["POST"])
def upload_image():
    """Get uploaded image, process, and redirect to appropriate page."""

    # Get the file from the request object
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # file.save actually saves it on the system
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        #print image_path
        return get_route(image_path)

    else:
        flash("No file, or bad image filename.")
        return redirect(url_for("index"))

@app.route("/upload/webcam", methods=["POST"])
def upload_webcam():
    dataURL = request.form.get('dataURL')
    imgURL = dataURL.rsplit(',')[1]
    print len(imgURL)

    if imgURL:
        now = datetime.datetime.utcnow()
        filename = now.strftime('%Y%m%d%M%S') + '.png'
        print filename

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print image_path

        # img = Image.open(StringIO(urlopen(imgURL).read()))

        with open(image_path, 'wb') as f:
            decoded_image = base64.b64decode(imgURL + '=' * (4 - len(imgURL) % 4))
            print len(decoded_image)
            print len(decoded_image) % 4
            f.write(decoded_image)

        # urllib.urlretrieve(imgURL, image_path)
        # img = Image(image_path)
        # img.save(image_path)

        return get_route(image_path)

    else:
        # Add a flash message with an error if Tesseract doesn't return anything.
        flash("Bad request: no file object on request.")
        return redirect(url_for("index"))

@app.route("/dish/<int:id>", methods=["GET"])
def view_dish(id):
    dish = model.session.query(model.Dish).get(id)
    return render_template("dish.html", dish=dish)

@app.route("/dish/search/<string:text>", methods=["GET"])
def translate_text(text):

    # It looks like Safari on iOS automatically encodes and quotes URL strings.
    # Unquoting & decoding to get unicode text.
    if type(text) == unicode:
        #print "already unicode!"
        unitext = text
    else:
        # I'm not sure if this is necessary, actually. Looks like Flask does this for me.
        print "unquoting and decoding url"
        unquoted_chars = urllib.unquote(text)
        unitext = unquoted_chars.decode('utf-8')

    chars = lookup_text(unitext)

    if chars:
        #authenticated = session.get("user_id")
        authenticated = True
        return render_template("search.html", dish=chars, searchstring=text, authenticated=authenticated)
    else:
        # redirect to search instead?
        flash("I couldn't read that, sorry! Try again?")
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if user exists. 
        user = model.session.query(model.User).filter_by(username=username).first()
        print user

        if user:
            # check if password matches.
            if user.authenticate(password):
                flash("Logged in!")
                session['user_id'] = user.id
                # is this where we want to redirect them? 
                return redirect(url_for('index'))
            else:
                flash("Username and password don't match.") 
                return render_template("login.html")
        else: 
            flash("Username and password don't match.")
            return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password_verify = request.form.get("password_verify")

        if password == password_verify:
            user = model.session.query(model.User).filter_by(username=username).all()
            if user == []:
               new_user = model.User(username=username, password="temp", salt="temp")
               new_user.set_password(password)
               model.session.add(new_user)
               model.session.commit()

               flash("New user created. Please log in.")
               return render_template("login.html")
            else:
                flash("Username already taken.")
                return render_template("signup.html") 
        else:
            flash("Passwords don't match.")
            return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Change debug to False when deploying, probably.
    app.run(debug = True)

