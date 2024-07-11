#importing necessary libraries
from flask import * # bad practice (import only necessaries)
from werkzeug.utils import secure_filename
import os
import easyocr
import urllib.request
import numpy as np
import cv2

# Flask app instance
app = Flask(__name__)

# # Index page
@app.route('/')
def index():
    return render_template('main.html', title='Project OCR')

pic = {}

# Function for uploading images
@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if request.method == "POST":
            f = request.files['file']


            # this will read the image and process without giving error of location
            #
            screenshot = request.files['file'].read()
            screenshot = np.frombuffer(screenshot, np.uint8)
            screenshot = cv2.imdecode(screenshot, cv2.IMREAD_COLOR)
            
            #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # f.save(secure_filename(f.filename))

            # in this secure_filename, the image should be in the current location to be processes
            # the above screenshot method is more useful to get image from anywhere 
            #
            filename = secure_filename(f.filename)
            print(filename)
            
            reader = easyocr.Reader(['en'], gpu=False)
            # results = reader.readtext(f)

            #results = reader.readtext(filename)
            results = reader.readtext(screenshot)

            text = ""
            for r in results:
                text += r[1]
                print(r)
            print(text)


            return render_template('main.html', result=text)
        else:
            print("UPLOAD FAILED.")
            # return render_template('upload_image.html')
            return redirect(request.url)
    except:
        print("UPLOAD FAILED.")

if __name__ == '__main__':
    app.run(debug=True) # Discard debug=True at production.



