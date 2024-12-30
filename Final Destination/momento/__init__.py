from flask import Flask
from .extensions import db, DB_NAME
from .sockets import socketio
from os import path
from flask_login import LoginManager







def create_website():
     website = Flask(__name__)
     website.config['SECRET_KEY'] = 'aki7-29-05_kyle3-01-05_mika6-10-05_anne9-8-04_ren10-27-04'
     website.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
     

     db.init_app(website)
     socketio.init_app(website)


     from .views import views
     from .auth import auth

     from .models import Posts, User, Comments, UserLikedPosts

     create_database(website)

     website.register_blueprint(views, url_prefix = '/')
     website.register_blueprint(auth, url_prefix = '/')

     login_manager = LoginManager()
     login_manager.login_view = 'views.index_page'
     login_manager.init_app(website)

     @login_manager.user_loader
     def load_user(id):
          return User.query.get(int(id))
     
     
     return website

def create_database(website):
     if not path.exists('website' + DB_NAME):
          with website.app_context():
               db.create_all()
               print("Created Database!")