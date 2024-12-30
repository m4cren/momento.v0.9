from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
     __tablename__ = 'User Database'
     id = db.Column(db.Integer, primary_key = True)
     email = db.Column(db.String(6969), unique = True)
     firstName = db.Column(db.String(69))
     lastName = db.Column(db.String(69))
     birthday = db.Column(db.Date, nullable=False)
     address = db.Column(db.String(6969))
     bio = db.Column(db.String(126), nullable = True)
     password = db.Column(db.String(126))
     profilePic = db.relationship('profilePicture', backref='user')
     coverPic = db.relationship('coverPicture', backref='user')
     posts = db.relationship('Posts', backref = 'user' )
     comments = db.relationship('Comments', backref = 'user')
     userWhoLiked = db.relationship('UserLikedPosts', backref = 'user')
     followers = db.relationship('Followers', backref = 'user')
     following = db.relationship('Following', backref = 'user')
     notificationOwner = db.relationship('Notifications', backref = 'user')
     isActive = db.relationship('ActiveUsers', backref = 'user')
     searchHistory = db.relationship('SearchHistory', backref = 'user')
     comrades = db.relationship('Comrades', backref = 'user')
     highscore = db.Column(db.Integer, default = 0, nullable = True)
     

class Followers(db.Model):
     __tablename__ = 'Followers'
     id = db.Column(db.Integer, primary_key = True)
     owner_id = db.Column(db.Integer, db.ForeignKey('Following.user_id'))
     user_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     name = db.Column(db.String(6969))
     follower_name = db.Column(db.String(6969))
     

class Following(db.Model):
     __tablename__ = 'Following'
     id = db.Column(db.Integer, primary_key = True)
     owner_id = db.Column(db.Integer, db.ForeignKey('Followers.owner_id'))
     user_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     name = db.Column(db.String(6969))
     following_name = db.Column(db.String(6969))

class Comrades(db.Model):
     __tablename__ = 'Comrades'
     id = db.Column(db.Integer, primary_key = True)
     owner_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     comrade_id = db.Column(db.Integer)
     comrade_name = db.Column(db.String(6969))
     



class profilePicture(db.Model):
     __tablename__ = 'Profile Pictures'
     id = db.Column(db.Integer, primary_key = True)
     img = db.Column(db.Text, nullable = False)
     name = db.Column(db.Text, nullable = False)
     mimetype = db.Column(db.Text, nullable = False)
     user_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))

class coverPicture(db.Model):
     __tablename__ = 'Cover Pictures'
     id = db.Column(db.Integer, primary_key = True)
     img = db.Column(db.Text, nullable = False)
     name = db.Column(db.Text, nullable = False)
     mimetype = db.Column(db.Text, nullable = False)
     user_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))

class Posts(db.Model):
     __tablename__ = 'Posts'
     id = db.Column(db.Integer, primary_key = True)
     caption = db.Column(db.String(569))
     nameWhoPost = db.Column(db.String(121))
     img = db.Column(db.LargeBinary, nullable = False)
     name = db.Column(db.Text, nullable = False)
     mimetype = db.Column(db.Text, nullable = False)
     like_count = db.Column(db.Integer)
     comment_count = db.Column(db.Integer)
     datePost= db.Column(db.Date, default = func.current_date())
     user_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     comments = db.relationship('Comments', backref = 'posts')
     userWhoLiked = db.relationship('UserLikedPosts', backref = 'posts')


class Comments(db.Model):
     __tablename__ = 'Comments'
     id = db.Column(db.Integer, primary_key = True)
     comment = db.Column(db.String(6969))
     dateComment= db.Column(db.Date, default = func.current_date())
     user_who_comment = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'))

class UserLikedPosts(db.Model):
     __tablename__ = 'User Liked Posts'
     id = db.Column(db.Integer, primary_key = True)
     post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'))
     user_id = db.Column(db.Integer, db.ForeignKey ('User Database.id'))
     name = db.Column(db.String(69), nullable = True)

class Notifications(db.Model):
     __tablename__ = 'Notifications'
     id = db.Column(db.Integer, primary_key = True)
     owner_id = db.Column(db.Integer)
     target_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     context_type = db.Column(db.String(6969), nullable = False)
     unread_notification_count = db.Column(db.Integer, default = 0, nullable = False)
     date = db.Column(db.Date, default = func.current_date())

class ActiveUsers(db.Model):
     __tablename__ = 'Active users'
     id = db.Column(db.Integer, primary_key = True)
     active_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     name = db.Column(db.String(6969))

class SearchHistory(db.Model):
     __tablename__ = 'Search History'
     id = db.Column(db.Integer, primary_key = True)
     owner_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     searched_id = db.Column(db.Integer)
     seached_name = db.Column(db.String(6969))
     

class Messages(db.Model):
     __tablename__ = 'Messages'
     id = db.Column(db.Integer, primary_key = True)
     from_id = db.Column(db.Integer, db.ForeignKey('User Database.id'))
     to_id = db.Column(db.Integer)
     message_text = db.Column(db.String(696969), nullable = True)
     img = db.Column(db.LargeBinary, nullable = True)
     name = db.Column(db.Text, nullable = True)
     mimetype = db.Column(db.Text, nullable = True)
     date_sent = db.Column(db.Date, default = func.current_date())
