from flask import Flask, render_template, request, session, redirect, url_for
import functools
import numpy as np
import os

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

filepath = 'C:/Users/HP/Documents/Plant-Leaf-Disease-Prediction-main/model.h5'
model = load_model(filepath)
print(model)

print("Model Loaded Successfully")
# Create a Flask application instance
app = Flask(__name__)

# Set a secret key for the Flask application
app.secret_key = "abc"

# Enable auto-reloading of templates
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Define a dictionary of users (for demonstration purposes)
users = {"abc": ("abc", "1234")}


# Define a function to be called after each request is processed
@app.after_request
def after_request(response):
    # Set response headers to disable caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate,post-check=0, pre-check=0"
    print(response)
    return response


# Define a route for the home page
@app.route("/", methods=['GET', 'POST'])
def home():
    # Render the home page template with the current username (if available) and session data
    return render_template("home.html", name=session.get("username", None), s=session)


# Define a function that can be used as a decorator to require login for certain routes
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        # If the user is not logged in, redirect them to the login page
        if "username" not in session:
            return redirect(url_for("login", next=request.url))
        # Otherwise, allow them to access the requested route
        return func()

    return secure_function

def pred_tomato_dieas(tomato_plant):
  test_image = load_img(tomato_plant, target_size = (128, 128)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image) # predict diseased palnt or not
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
      return "Tomato - Bacteria Spot Disease", 'Tomato-Bacteria Spot.html'
       
  elif pred==1:
      return "Tomato - Early Blight Disease", 'Tomato-Early_Blight.html'
        
  elif pred==2:
      return "Tomato - Healthy and Fresh", 'Tomato-Healthy.html'
        
  elif pred==3:
      return "Tomato - Late Blight Disease", 'Tomato - Late_blight.html'
       
  elif pred==4:
      return "Tomato - Leaf Mold Disease", 'Tomato - Leaf_Mold.html'
        
  elif pred==5:
      return "Tomato - Septoria Leaf Spot Disease", 'Tomato - Septoria_leaf_spot.html'
        
  elif pred==6:
      return "Tomato - Target Spot Disease", 'Tomato - Target_Spot.html'
        
  elif pred==7:
      return "Tomato - Tomoato Yellow Leaf Curl Virus Disease", 'Tomato - Tomato_Yellow_Leaf_Curl_Virus.html'
  elif pred==8:
      return "Tomato - Tomato Mosaic Virus Disease", 'Tomato - Tomato_mosaic_virus.html'
        
  elif pred==9:
      return "Tomato - Two Spotted Spider Mite Disease", 'Tomato - Two-spotted_spider_mite.html'


# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        file_path = os.path.join('C:/Users/HP/Documents/Plant-Leaf-Disease-Prediction-main/static/upload/', filename)
        file.save(file_path)
        print("@@ Predicting class......")
        pred, output_page = pred_tomato_dieas(tomato_plant=file_path)
        return render_template(output_page, pred_output = pred, user_image = file_path)

# Define a route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get the username and password from the submitted form data
        username = request.form.get("username")
        password = request.form.get("password")
        next_url = request.form.get("next")
        print(username, password, next_url)

        # If the username and password are valid, store the username in the session and redirect to the profile page
        if username in users and users[username][1] == password:
            #@app.route("/", methods=['GET', 'POST'])
            return render_template("index.html")
            #home1()


    # If the request method is GET or the login was unsuccessful, render the login page template
    return render_template("login.html")

@app.route("/", methods=['GET', 'POST'])
def home1():
        return render_template('index.html')

# Define a route for the registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get the username and password from the submitted form data
        username = request.form.get("username")
        password = request.form.get("password")

        # If the username is not already in the users dictionary, add it with the provided password and redirect to the home page
        if username not in users:
            users[username] = (username, password)
            return redirect(url_for("home"))

    # If the request method is GET or the registration was unsuccessful, render the registration page template
    return render_template("register.html")


# Define a route for the logout function
@app.route("/logout")
def logout():
    # Clear the user's session data and redirect to the home page
    session.clear()
    return redirect(url_for("home"))


# Define a route for the profile page that requires login
@app.route("/profile")
@login_required
def profile_page():
    # Render the profile page template with the current username
    return render_template("profile.html", name=session["username"])


# If the script is executed as the main program, run the Flask application
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(threaded=False,port=8000)
