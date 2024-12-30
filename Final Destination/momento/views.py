from flask import Blueprint, redirect, render_template, request, Flask, session, url_for, flash, send_file
import io, time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from . import db
from .models import *
from sqlalchemy import desc, asc, and_
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/')
def index_page(): 
     return render_template('index.html')

@views.route('/homepage')
@login_required
def homepage():
     current_user_id = current_user.id
     user_comrades = Comrades.query.filter_by(owner_id = current_user_id).all()

     comrades = [comrade for comrade in user_comrades]
     comrades_id = [comrade.comrade_id for comrade in user_comrades]

    

     comrades_id = comrades_id + [current_user_id]


     posts = Posts.query.filter(Posts.user_id.in_(comrades_id)).order_by(desc(Posts.id)).all()
     liked_posts = [like.post_id for like in UserLikedPosts.query.filter_by(user_id = current_user_id).all()]

     
     notifications = Notifications.query.filter_by(target_id = current_user_id).order_by(desc(Notifications.id)).all()     
     notificationCount = Notifications.query.filter_by(owner_id = current_user_id).first()

     try:
          notificationCount = notificationCount.unread_notification_count
     except:
          print('new account created')

     activeUsers =  ActiveUsers.query.all()
         
     searchHistory = SearchHistory.query.filter_by(owner_id = current_user_id).order_by(desc(SearchHistory.id)).all()

     allUsers = User.query.filter(User.id != current_user_id).all()
     currentUser = User.query.filter_by(id = current_user_id).first()

     ALLUSERS = User.query.filter(User.highscore != 0).order_by(desc(User.highscore)).all()

  
     firstName = current_user.firstName
     lastName = current_user.lastName
     name = firstName + ' ' + lastName

          
     return render_template('homepage.html',
                              ALLUSERS = ALLUSERS,
                              users = allUsers,
                              currentUser = currentUser,
                              comrades = comrades,
                              name = name,
                              posts = posts,
                              time = time,
                              liked_posts = liked_posts,
                              notifications = notifications,
                              notificationCount = notificationCount,
                              activeUsers = activeUsers,
                              searchHistory = searchHistory
                      
                              )

@views.route('/userprofile')
@login_required
def user_profile_page():
     current_user_id = current_user.id
     liked_posts = [like.post_id for like in UserLikedPosts.query.filter_by(user_id = current_user_id).all()]
     searchHistory = SearchHistory.query.filter_by(owner_id = current_user_id).order_by(desc(SearchHistory.id)).all()

     posts = Posts.query.filter_by(user_id = current_user_id).order_by(desc(Posts.id)).all()
     
     notifications = Notifications.query.filter_by(target_id = current_user_id).order_by(desc(Notifications.id)).all()     
     notificationCount = Notifications.query.filter_by(owner_id = current_user_id).first()
     notificationCount = notificationCount.unread_notification_count
     

     bio = current_user.bio
     firstName = current_user.firstName
     lastName = current_user.lastName
     name = firstName + ' ' + lastName

     activeUsers =  ActiveUsers.query.all()

     address = current_user.address
     birthday = current_user.birthday

     followersId = [follower for follower in Followers.query.filter_by(owner_id = current_user_id).order_by(desc(Followers.id)).all()]
     followingsId = [following for following in Following.query.filter_by(owner_id = current_user_id).order_by(desc(Following.id)).all()]

     followersCount = len(followersId)
     followingCount = len(followingsId)
     postCount = len(posts)

     user_comrades = Comrades.query.filter_by(owner_id = current_user_id).all()
     comrades = [comrade for comrade in user_comrades]

     return render_template('profile_page.html', 
                              name = name,
                              address = address,
                              birthday = birthday,
                              posts = posts,
                              bio = bio,
                              liked_posts = liked_posts,
                              followersId = followersId,
                              followingsId = followingsId,
                              notifications = notifications,
                              notificationCount = notificationCount,
                              followingCount = followingCount,
                              followersCount = followersCount,
                              postCount = postCount,
                              searchHistory = searchHistory,
                              activeUsers = activeUsers,
                              comrades = comrades)

@views.route('/view-other-profile/<int:id>')
@login_required
def viewOtherProfile(id):

     user_comrades = Comrades.query.filter_by(owner_id = current_user.id).all()
     comrades = [comrade for comrade in user_comrades]

     activeUsers =  ActiveUsers.query.all()
     searchHistory = SearchHistory.query.filter_by(owner_id = current_user.id).order_by(desc(SearchHistory.id)).all()
     current_user_id = current_user.id
     userToView = User.query.get_or_404(id)
     posts = Posts.query.filter_by(user_id = id).order_by(desc(Posts.id)).all()
     liked_posts = [like.post_id for like in UserLikedPosts.query.filter_by(user_id = current_user_id).all()]

     do_i_follow_this_user = Following.query.filter_by(owner_id = current_user_id, user_id = id).first()

     respone = False

     notifications = Notifications.query.filter_by(target_id = current_user_id).order_by(desc(Notifications.id)).all()     
     notificationCount = Notifications.query.filter_by(owner_id = current_user_id).first()
     notificationCount = notificationCount.unread_notification_count
     

     if do_i_follow_this_user:
          response = True
     else:
          response = False

     followers = [follower.follower_name for follower in Followers.query.filter_by(owner_id = id).all()]
     followings = [following.following_name for following in Following.query.filter_by(owner_id = id).all()]

     followersCount = len(followers)
     followingCount = len(followings)
     postCount = len(posts)


     return render_template('other_user_page.html',
                              user = userToView,
                              posts = posts,
                              liked_posts = liked_posts,
                              do_i_follow_this = response,
                              followers = followers,
                              followings = followings,
                              followingCount = followingCount,
                              notifications = notifications,
                              notificationCount = notificationCount,
                              followersCount = followersCount,
                              postCount = postCount,
                              searchHistory = searchHistory,
                              activeUsers = activeUsers,
                              comrades = comrades)







@views.route('/upload-profile', methods =['POST'])
def uploadProfilePicture():
     picture = request.files['profile-pic']

     if not picture:
          flash('No image selected', category="error")
          return redirect('/userprofile')
     
     filename = secure_filename(picture.filename)
     mimetype = picture.mimetype

     profilePic = profilePicture(img = picture.read(), mimetype = mimetype, name = filename, user_id = current_user.id)

     db.session.query(profilePicture).filter_by(user_id = current_user.id).delete()

     db.session.add(profilePic)
     db.session.commit()


     return redirect('/userprofile')

@views.route('/profile-picture/<int:user_id>')
def get_profile_picture(user_id):

     profile_pic = db.session.query(profilePicture).filter_by(user_id = user_id).first()

     if not profile_pic:
          return redirect('/static/defaultImages/default.jpg')

     return send_file(
          io.BytesIO(profile_pic.img),
          mimetype= profile_pic.mimetype,
          as_attachment = False,
          download_name = profile_pic.name
     )

@views.route('/upload-cover', methods = ['POST'])
def uploadCoverPicture():
     coverPictureUploaded = request.files['cover-pic']

     if not coverPictureUploaded:
          flash('No image selected', category="error")
          return redirect('/userprofile')
     
     filename = secure_filename(coverPictureUploaded.filename)
     mimetype = coverPictureUploaded.mimetype

     coverPic = coverPicture(img = coverPictureUploaded.read(), mimetype = mimetype, name = filename, user_id = current_user.id)

     db.session.query(coverPicture).filter_by(user_id = current_user.id).delete()

     db.session.add(coverPic)
     db.session.commit()

     return redirect('/userprofile')

@views.route('/cover-picture/<int:user_id>')
def get_cover_picture(user_id):

     cover_pic = db.session.query(coverPicture).filter_by(user_id = user_id).first()

     if not cover_pic:
          return redirect('/static/defaultImages/defaultPhoto.jpg')

     return send_file(
          io.BytesIO(cover_pic.img),
          mimetype= cover_pic.mimetype,
          as_attachment = False,
          download_name = cover_pic.name
     )


@views.route('/upload-post', methods = ['POST'])
def uploadPost():
     if request.method == 'POST':
          postPicture = request.files['post-picture']
          caption = request.form['caption']

          name = current_user.firstName + " " + current_user.lastName

          filename = secure_filename(postPicture.filename)
          mimetype = postPicture.mimetype

          like_count = 0
          comment_count = 0

          postPic = Posts(comment_count = comment_count, nameWhoPost = name, img = postPicture.read(), mimetype = mimetype, name = filename, user_id = current_user.id, caption = caption, like_count = like_count)
          db.session.add(postPic)
          db.session.commit()

          return redirect(url_for('views.homepage'))
     
@views.route('/post-picture/<int:user_id>')
def get_post_picture(user_id):

     post_pic = db.session.query(Posts).filter_by(id = user_id).first()

     return send_file(
          io.BytesIO(post_pic.img),
          mimetype= post_pic.mimetype,
          as_attachment = False,
          download_name = post_pic.name
     )

     
@views.route('/delete-post/<int:id>', methods = ['POST','GET'])
def deletePost(id):

     postToDelete = Posts.query.filter_by(id = id).first()
     db.session.delete(postToDelete)
     db.session.commit()

     return redirect('/userprofile')

@views.route('/like/<int:postId>/<int:userId>', methods = ['POST','GET'])
def like(postId, userId):

     userWhoLike = User.query.filter_by(id = userId).first()
     name = userWhoLike.firstName + " " + userWhoLike.lastName;

     post = Posts.query.filter_by(id = postId).first()
     post.like_count += 1;


     print(post.like_count)

     db.session.commit()

     if request.path == '/view-other-profile/<int:id>':
          return redirect('/view-other-profile/<int:id>')
     elif request.path == '/userprofile':
          return redirect('/userprofile')
     else:
          return redirect(url_for('views.homepage'))
     
@views.route('/update-name', methods=['POST'])
def updateName():
     newFirstName = request.form['updateFirstName']
     newLastName = request.form['updateLastName']

     if newFirstName  and newLastName:

          updateFirstName = User.query.filter_by(id = current_user.id).first()
          updateFirstName.firstName = newFirstName

          updateLastName = User.query.filter_by(id = current_user.id).first()
          updateLastName.lastName = newLastName

          db.session.commit()


          return redirect(url_for('views.homepage'))
     
     else:
          flash('Bawal walang pangalan dito HAHA', category='walangName')
          return redirect(url_for('views.homepage'))
     
@views.route('/update-bio', methods=['POST'])
def updateBio():
     newBio = request.form['updateBio']

     updateBio = User.query.filter_by(id = current_user.id).first()

     updateBio.bio = newBio

     db.session.commit()

     return redirect(url_for('views.homepage'))

@views.route('/update-address', methods = ['POST'])
def updateAddress():
     newAddress = request.form['updateAddress']

     updateAddress = User.query.filter_by(id = current_user.id).first()

     updateAddress.address = newAddress
     db.session.commit()

     return redirect(url_for('views.homepage'))

@views.route('/update-password', methods = ['POST'])
def updatePassword():
     newPassword = request.form['newPassword']
     oldPassword = request.form['oldPassword']


     if check_password_hash(current_user.password, oldPassword):
          updatePassword = User.query.filter_by(id = current_user.id).first()
          password = generate_password_hash(newPassword, method='pbkdf2:sha256')

          updatePassword.password = password
          db.session.commit()

          return redirect(url_for('views.homepage'))
     
     return redirect(url_for('views.homepage'))

@views.route('/delete-account', methods = ['POST'])
def deleteAccount():
    password1 = request.form['password1']
    password2 = request.form['password2']

    accountToDelete = User.query.filter_by(id = current_user.id).first()
    profilePictureToDelete = profilePicture.query.filter_by(id = current_user.id).first()
    coverPictureToDelete = coverPicture.query.filter_by(user_id = current_user.id).first()
    postToDelete = Posts.query.filter_by(user_id = current_user.id).all()
    commentsToDelete = Comments.query.filter_by(user_who_comment = current_user.id).all()
    likesToDelete = UserLikedPosts.query.filter_by(user_id = current_user.id).all()
    notificationsToDelete = Notifications.query.filter_by(target_id = current_user.id).all()
    followersToDelete = Followers.query.filter_by(user_id = current_user.id).all()
    followingsToDelete = Following.query.filter_by(owner_id = current_user.id).all()
    if password1 != password2:
        flash("Password do not match", category='error2')
    else:
        if check_password_hash(accountToDelete.password, password1):
          
          if not profilePictureToDelete:
               pass
          else:
               db.session.delete(profilePictureToDelete)
          
          if not coverPictureToDelete:
               pass
          else:
               db.session.delete(coverPictureToDelete)
          if not notificationsToDelete:
               pass
          else:
               for notif in notificationsToDelete:
                    db.session.delete(notif)
          if not followingsToDelete:
               pass
          else:
               for following in followingsToDelete:
                    db.session.delete(following)
          if not followersToDelete:
               pass
          else:
               for follower in followersToDelete:
                    db.session.delete(follower)


          
           
          for post in postToDelete:
               db.session.delete(post)
          for comment in commentsToDelete:
               db.session.delete(comment)
          for like in likesToDelete:
               db.session.delete(like)
          

          db.session.delete(accountToDelete)
          db.session.commit()
     
         
          return redirect(url_for('views.index_page'))
            
        else:
            flash("Invalid password", category='error2')
    
    return redirect(url_for('views.homepage'))

@views.route('/message-file/<int:sender_id>/<int:receiver_id>')
def get_message_file(sender_id, receiver_id):

     message_file = (db.session.query(Messages).filter(and_(
          Messages.from_id == sender_id,
          Messages.to_id == receiver_id,
          Messages.img != None
     )).order_by(desc(Messages.id)).first())


     return send_file(
          io.BytesIO(message_file.img),
          mimetype= message_file.mimetype,
          as_attachment = False,
          download_name = message_file.name
     )

@views.route('/open-game')
def openGame():
     notifications = Notifications.query.filter_by(target_id = current_user.id).order_by(desc(Notifications.id)).all()     
     notificationCount = Notifications.query.filter_by(owner_id = current_user.id).first()
     user_comrades = Comrades.query.filter_by(owner_id = current_user.id).all()
     comrades = [comrade for comrade in user_comrades]
     activeUsers =  ActiveUsers.query.all()

     try:
          notificationCount = notificationCount.unread_notification_count
     except:
          print('new account created')
     currentUser = User.query.filter_by(id = current_user.id).first()
     return render_template('game.html',
                             currentUser = currentUser,
                             comrades = comrades,
                             notifications = notifications,
                             activeUsers = activeUsers,
                              notificationCount = notificationCount,)