# __init__.py
from flask import Flask
app = Flask(__name__)
app.secret_key = "askfkas2131akldjfaks@fda"
DATABASE = "magazine_schema"
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)    # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument
