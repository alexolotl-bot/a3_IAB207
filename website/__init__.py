#from package import Class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    # Should be set to false in a production environment
    app.debug = True
    app.secret_key = 'somesecretkey'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    #initialize db with flask app
    db.init_app(app)

    # bootstrap = Bootstrap5(app)
    Bootstrap5(app)
    Bcrypt(app)

    
    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    # Importing inside the create_app function avoids circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))
    
 #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import event
    app.register_blueprint(event.event_bp)

    from . import user
    app.register_blueprint(user.user_bp)

   #  Basic 404 Error taken from demo 
    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
      return render_template("404.html", error=e)

    #this creates a dictionary of variables that are available
    #to all html templates
    @app.context_processor
    def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)

    
    return app



