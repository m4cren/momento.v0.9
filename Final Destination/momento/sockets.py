from .extensions import socketio, emit, send
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask import url_for
from flask_login import current_user
from sqlalchemy import desc, asc
from .models import *
from werkzeug.utils import secure_filename
import base64
import time

@socketio.on('connect')
def user_connect():

     name = f'{current_user.firstName} {current_user.lastName}'

     print(f'Client Connected: {name}')

     activeUser = ActiveUsers(active_id = current_user.id, name = name)
     db.session.add(activeUser)
     db.session.commit()

     emit('online', {'user':current_user.id, 'username':name}, broadcast=True)

     target_id = current_user.id
     room = f'target_{current_user.id}'
     join_room(room)

     checkNotification = Notifications.query.filter_by(target_id = current_user.id).all()

     if not checkNotification:
         
          context_type = f'Welcome {current_user.firstName}, Enjoy your remaining days using our website :>'

          welcome_notification = Notifications(owner_id = current_user.id, target_id = current_user.id, unread_notification_count = 1, context_type = context_type)

          db.session.add(welcome_notification)
          db.session.commit()
          
          unread_count = 1
          welcomeNotification = {
               'from': 'Momento',
               'to': current_user.firstName,
               'context_type': context_type,
               'profile_pic': url_for('static', filename = 'icons/iconNamin.png')
          }
          emit('listen_for_like_welcome_notification', {'welcomeNotification':welcomeNotification,'unread_notification_count': unread_count}, to=f'target_{target_id}')
     else:
          print('There is item in Notification database')




@socketio.on('disconnect')
def user_disconnect():

     user_to_disconnect = ActiveUsers.query.filter_by(active_id = current_user.id).all()

     for user in user_to_disconnect:
          db.session.delete(user)
          db.session.commit()
     
     

     name = f'{current_user.firstName} {current_user.lastName}'
     print(f'Client disconnected: {name}')
     emit('offline', {'user':current_user.id, 'username':name}, broadcast=True)

@socketio.on('request_active_users')
def send_active_users():
     active_users = ActiveUsers.query.all()
     user_list = [{'user': user.active_id, 'username': user.name} for user in active_users]
     emit('active_users_list', user_list)


@socketio.on('follow_user')
def follow_user(data):
     ownerId = data['ownerId']
     userId = data['userId']

     userWhoFollow = User.query.filter_by(id = ownerId).first()
     userToFollow = User.query.filter_by(id = userId).first()

     follower_name = f'{userWhoFollow.firstName} {userWhoFollow.lastName}'
     following_name = f'{userToFollow.firstName} {userToFollow.lastName}'
     target_id = userId


     
     context_type = f'{follower_name} follows you'
     

     if str(ownerId) == str(target_id):
         pass
     else:

          newNotification = Notifications(owner_id = ownerId, target_id = target_id, context_type = context_type)

          db.session.add(newNotification)
          db.session.commit()
          print(newNotification)
     
          
          
          updateCount = Notifications.query.filter_by(owner_id = target_id).first()

        
          updateCount.unread_notification_count += 1

          update_count =  updateCount.unread_notification_count
         
          profile_pic = profilePicture.query.filter_by(id = current_user.id).first()
         
          recentNotification = {
               'from': f'{userWhoFollow.firstName} {userWhoFollow.lastName}',
               'to': f'{userToFollow.firstName} {userToFollow.lastName}',
               'context_type': context_type,
               'profile_pic': url_for('views.get_profile_picture', user_id=profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')
          }
          emit('listen_for_like_notification', {'recentNotification':recentNotification,'unread_notification_count': update_count}, to=f'target_{target_id}')

     print(f'{userWhoFollow.firstName} {userWhoFollow.lastName} follows {userToFollow.firstName} {userToFollow.lastName}')

     newFollower = Followers(owner_id = userId, user_id = ownerId, name = following_name, follower_name = follower_name)
     newFollowing = Following(owner_id = ownerId, user_id = userId, name = follower_name, following_name = following_name)

     
     db.session.add(newFollower)
     db.session.add(newFollowing)
     db.session.commit()
     
     try:

          user_followings = Following.query.filter_by(owner_id = current_user.id).all()
          user_followers = Followers.query.filter_by(owner_id = current_user.id).all()
          user_comrades = Comrades.query.filter_by(owner_id = current_user.id).all()

        

          if len(user_comrades) == 0:

               for following in user_followings:
                    for follower in user_followers:
                         if following.following_name == follower.follower_name:
                                           
                              new_comradeSelf = Comrades(owner_id = current_user.id, comrade_id = follower.user_id, comrade_name = follower.follower_name)
                              new_comradeOther = Comrades(owner_id = follower.user_id, comrade_id = current_user.id, comrade_name = f'{current_user.firstName} {current_user.lastName}')
                              db.session.add(new_comradeSelf)
                              db.session.add(new_comradeOther)
                              db.session.commit()
                              print('comrade addeddddddddddddddddddd')
          else:
               for following in user_followings:
                    for follower in user_followers:
                         if following.following_name == follower.follower_name:
                              for comrade in user_comrades:
                                   if comrade.comrade_name == following.following_name: 
                                        print('aldready comrades')
                                   else:
                                        new_comradeSelf = Comrades(owner_id = current_user.id, comrade_id = follower.user_id, comrade_name = follower.follower_name)
                                        new_comradeOther = Comrades(owner_id = follower.user_id, comrade_id = current_user.id, comrade_name = f'{current_user.firstName} {current_user.lastName}')
                                        db.session.add(new_comradeSelf)
                                        db.session.add(new_comradeOther)
                                        db.session.commit()
                                        print('comrade addeddddddddddddddddddd')
                              
          
          for item in user_comrades:
               print(item.comrade_name)
     except:
          pass

     emit('reload')
     

     

@socketio.on('unfollow_user')
def unfollow_user(data):
     ownerId = data['ownerId']
     userId = data['userId']

     userWhoUnfollow = User.query.filter_by(id = ownerId).first()
     userToUnfollow = User.query.filter_by(id = userId).first()

     context_type = f'{userWhoUnfollow.firstName} {userWhoUnfollow.lastName} unfollow you'
     target_id = userId

     if str(ownerId) == str(target_id):
         pass
     else:

          newNotification = Notifications(owner_id = ownerId, target_id = target_id, context_type = context_type)

        
          updateCount = Notifications.query.filter_by(owner_id = target_id).first()

         
          updateCount.unread_notification_count += 1

          update_count =  updateCount.unread_notification_count
 
          db.session.add(newNotification)
          db.session.commit()
          
       
          profile_pic = profilePicture.query.filter_by(id = current_user.id).first()
      
          recentNotification = {
               'from': f'{userWhoUnfollow.firstName} {userWhoUnfollow.lastName}',
               'to': f'{userToUnfollow.firstName} {userToUnfollow.lastName}',
               'context_type': context_type,
               'profile_pic': url_for('views.get_profile_picture', user_id=profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')
          }
          emit('listen_for_like_notification', {'recentNotification':recentNotification,'unread_notification_count': update_count}, to=f'target_{target_id}')

     print(f'{userWhoUnfollow.firstName} {userWhoUnfollow.lastName} unfollows {userToUnfollow.firstName} {userToUnfollow.lastName}')

     removeFollower = Followers.query.filter_by(owner_id = userId, user_id = ownerId).first()
     removeFollowing = Following.query.filter_by(owner_id = ownerId, user_id = userId).first()
     
     
     try:
          removeComradeSelf = Comrades.query.filter_by(owner_id = current_user.id, comrade_id = userId).all()
          removeComradeOther = Comrades.query.filter_by(owner_id = userId, comrade_id = current_user.id).all()

          for user in removeComradeSelf:
               db.session.delete(user)
               db.session.commit()
          for user in removeComradeOther:
               db.session.delete(user)
               db.session.commit()

          print(f'{removeComradeSelf.comrade_name} and {removeComradeOther.comrade_name} become enemies')
     except:
          print('already enemies')

     db.session.delete(removeFollower)
     
     db.session.delete(removeFollowing)
     db.session.commit()

     emit('reload')

     


@socketio.on('like_post')
def handle_like(data):
     postId = data['postId']
     userId = data['userId']
     

     userThatLike = User.query.filter_by(id = userId).first()
     nameWHoLikes = f'{userThatLike.firstName} {userThatLike.lastName}'
  
     post = Posts.query.filter_by(id = postId).first()

     context_type = f'{nameWHoLikes} loved your post'
     target_id = post.user_id
   
     if str(userId) == str(target_id):
          print(f'{nameWHoLikes} liked his/her own post')

          updateCount = Notifications.query.filter_by(owner_id = target_id).first()
          updateCount.unread_notification_count += 0
          

          
     else:
          newNotification = Notifications(owner_id = userId, target_id = target_id, context_type = context_type)
          db.session.add(newNotification)
          db.session.commit()

          updateCount = Notifications.query.filter_by(owner_id = target_id).first()
          updateCount.unread_notification_count += 1
         

          profile_pic = profilePicture.query.filter_by(id = userId).first()

          recentNotification = {
               'from': nameWHoLikes,
               'to': post.nameWhoPost,
               'context_type': context_type,
               'profile_pic': url_for('views.get_profile_picture', user_id=profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')
          }
          emit('listen_for_like_notification', {'recentNotification':recentNotification,'unread_notification_count': updateCount.unread_notification_count}, to=f'target_{target_id}')
       

          
     print(f'{nameWHoLikes} like {post.nameWhoPost} post')
     

     post.like_count += 1
     userLikeThisPost = UserLikedPosts(user_id = userId, post_id = postId, name = nameWHoLikes)
     
     
     db.session.add(userLikeThisPost)

     

   
     db.session.commit()
     
     

     emit('update_like', {'postId': postId, 'like_count': post.like_count}, broadcast = True);
    
@socketio.on('clear_notifications')
def clearNotifications(data):
     userId = data['userId']

     notificationToReset = Notifications.query.filter_by(owner_id = userId).first()
     notificationToReset.unread_notification_count = 0
     db.session.commit()

@socketio.on('unlike_post')
def handle_unlike(data):
     postId = data['postId']
     userId = data['userId']

 



     userThatUnlike = User.query.filter_by(id = userId).first()
     nameWhoUnlikes = f'{userThatUnlike.firstName} {userThatUnlike.lastName}'

     postToUnlike = Posts.query.filter_by(id = postId).first()
     postToUnlike.like_count -= 1

     userUnlikeThisPost = UserLikedPosts.query.filter_by(post_id = postId, user_id = userId).first()
     db.session.delete(userUnlikeThisPost)
     post = Posts.query.filter_by(id = postId).first()

     context_type = f'{nameWhoUnlikes} hated your post'
     target_id = post.user_id

     if str(userId) == str(target_id):
          print(f'{nameWhoUnlikes} unliked his/her own post')
          updateCount = Notifications.query.filter_by(owner_id = target_id).first()
          updateCount.unread_notification_count += 0
     else:

          newNotification = Notifications(owner_id = userId, target_id = target_id, context_type = context_type)
          db.session.add(newNotification)
          db.session.commit()
          updateCount = Notifications.query.filter_by(owner_id = target_id).first()
          updateCount.unread_notification_count += 1
    
          
          
          profile_pic = profilePicture.query.filter_by(id = userId).first()

          recentNotification = {
               'from': nameWhoUnlikes,
               'to': post.nameWhoPost,
               'context_type': context_type,
               'profile_pic': url_for('views.get_profile_picture', user_id=profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')
          }
          emit('listen_for_like_notification', {'recentNotification':recentNotification,'unread_notification_count': updateCount.unread_notification_count}, to=f'target_{target_id}')

     print(f'{nameWhoUnlikes} unlike {post.nameWhoPost} post')
     db.session.commit()
     emit('update_unlike', {'postId': postId, 'like_count': postToUnlike.like_count}, broadcast = True)
    
@socketio.on('view_comments')
def load_comments(data):
     postId = data['postId']
     comments_to_load = Comments.query.filter_by(post_id = postId).all()
     room = f'post_{current_user.id}'
     post = Posts.query.filter_by(id = postId).first()
     name = post.nameWhoPost
     join_room(room)
     

     user_ids = [comment.user_who_comment for comment in comments_to_load]
     users = {user.id: user for user in User.query.filter(User.id.in_(user_ids)).all()}
    
     comments_data = []
     for comment in comments_to_load:
        user = users.get(comment.user_who_comment)
        if user:
            comments_data.append({
                'name': f'{user.firstName} {user.lastName}',
                'comment': comment.comment,
                'date': comment.dateComment.strftime('%Y-%m-%d'),
                'profile_pic': url_for('views.get_profile_picture', user_id=user.id)
            })
    
     

     emit('load_comments', {'comments': comments_data, 'userId': user_ids, 'name':name}, to = room)
          

     

     # emit('load_comments', {'comments': comments_to_load.comment, 'userWhoComment': comments_to_load.user_who_comment, 'dateComment': comments_to_load.dateComment}, broadcast=True)

@socketio.on('view_likes')
def load_likes_in_post(data):
     postId = data['postId']
     room = f'post_{postId}'
     join_room(room)

     post_to_load_likes = UserLikedPosts.query.filter_by(post_id = postId).all()

     likers = [liker.name for liker in post_to_load_likes]

     emit('load_likers', {'likers':likers, 'postId': postId}, to=room)

@socketio.on('handle_comment')
def handle_comment(data):
     postId = data['postId']
     comment = data['comment']

     user = User.query.filter_by(id = current_user.id).first()

     nameWhoComment = f'{user.firstName} {user.lastName}'

     newComment = Comments(comment = comment, post_id = postId, user_who_comment = current_user.id)
     post = Posts.query.filter_by(id = postId).first()

     target_id = post.user_id

     context_type = f'{nameWhoComment} trashtalk your post'

     print(context_type)

     if str(current_user.id) == str(target_id):
          print(f'{nameWhoComment} comment on his/her own post')
          updateCount = Notifications.query.filter_by(owner_id = target_id).first()
          updateCount.unread_notification_count += 0
     else:
          newNotification = Notifications(owner_id = current_user.id, target_id = target_id, context_type = context_type)
          db.session.add(newNotification)
          db.session.commit()
          updateCount = Notifications.query.filter_by(owner_id = target_id).first()
          updateCount.unread_notification_count += 1
    
          
          profile_pic = profilePicture.query.filter_by(id = current_user.id).first()

          recentNotification = {
               'from': nameWhoComment,
               'to': post.nameWhoPost,
               'context_type': context_type,
               'profile_pic': url_for('views.get_profile_picture', user_id=profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')
          }

          print(recentNotification)
          emit('listen_for_like_notification', {'recentNotification':recentNotification,'unread_notification_count': updateCount.unread_notification_count}, to=f'target_{target_id}')



     post.comment_count += 1
     db.session.add(newComment)
     db.session.commit()

     commentCount = post.comment_count;

     room = f'post_{postId}'

     emit('load_comment_counts', {'commentCount':commentCount, 'postId':postId}, to=room);

@socketio.on('do_nothing')
def do_nothing():
     pass

@socketio.on('listen-to-search-input')
def listenToSearchInput(data):
     search_text = data['search_text']
     owner = current_user
     room = f'my_{owner.id}'
     join_room(room)
     
     user_to_search = User.query.filter(User.firstName.ilike(f'%{search_text}%') | User.lastName.ilike(f'%{search_text}%')).all()

    
     user_results = [{
          'id': user.id ,
          'name': f'{user.firstName} {user.lastName}',
          'profile_pic': url_for('views.get_profile_picture', user_id=user.id) if user.id else url_for('static', filename = 'defaultImages/nothing.gif')
     } for user in user_to_search]
    

     emit('search-results', {'users':user_results, 'owner':owner.id}, to = room )

     print(user_results)

     
@socketio.on('add-to-search-history')
def addToSearchHistory(data):
     userId = data['id']
     name = data['name']
     room = f'target_{userId}'
     join_room(room)

     history = SearchHistory.query.filter_by(owner_id = current_user.id).first()

     context_type = f"{current_user.firstName} {current_user.lastName} visited your profile"
     target_id = userId
     owner_id = current_user.id

   
     newNotification = Notifications(owner_id = current_user.id, target_id = target_id, context_type = context_type)
     db.session.add(newNotification)
     db.session.commit()
     updateCount = Notifications.query.filter_by(owner_id = target_id).first()
     updateCount.unread_notification_count += 1

     profile_pic = profilePicture.query.filter_by(id = current_user.id).first()

     user = User.query.filter_by(id = userId).first()
         
     recentNotification = {
          'from': f'{current_user.firstName} {current_user.lastName}',
          'to': f'{user.firstName} {user.lastName}',
          'context_type': context_type,
          'profile_pic': url_for('views.get_profile_picture', user_id=profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')
     }
     
     emit('listen_for_like_notification', {'recentNotification':recentNotification,'unread_notification_count': updateCount.unread_notification_count}, to=f'target_{userId}')

     print(recentNotification)
     



   

     if not history:
          newSearched = SearchHistory(owner_id = current_user.id, searched_id = userId, seached_name = name)
          db.session.add(newSearched)
          db.session.commit()
     else:
          if history.searched_id == userId:
               pass
          else:
               newSearched = SearchHistory(owner_id = current_user.id, searched_id = userId, seached_name = name)
               db.session.add(newSearched)
               db.session.commit()

          
               
          
@socketio.on('delete-search-history')
def deleteSearchHistory(data):
     userId = data['id']

    

     
     history = SearchHistory.query.filter_by(owner_id = current_user.id).filter_by(searched_id = userId).first()
     

     db.session.delete(history)
     db.session.commit()
     
     emit('reload-page')

@socketio.on('send-message')
def sendMessage(data):
     message_text = data['message_text']
  
     from_id = current_user.id
     to_id = data['to_id']

 

     newMessage = Messages(message_text = message_text, from_id = from_id, to_id = to_id)
     db.session.add(newMessage)
     db.session.commit()

     profile_pic = profilePicture.query.filter_by(id = current_user.id).first()

     


     messageData = {
          'from_id': from_id,
          'to_id': to_id,
          'message_text': message_text,
          'profile_pic': url_for('views.get_profile_picture', user_id=profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')
     }
     print(to_id)
     emit('recieve-message', {'messageData':messageData, 'CURRENT_USER_ID': current_user.id}, to = f'target_{to_id}')
     emit('recieve-message', {'messageData':messageData, 'CURRENT_USER_ID': current_user.id}, to = f'target_{current_user.id}')

     emit('notify-my-comrade', {'messageData': messageData}, to = f'target_{to_id}')

     
@socketio.on('load-message-history')
def loadMessageHistory(data):
     to_id = data['to_id']
     from_id = current_user.id
     
     messageHistory = Messages.query.filter(
        ((Messages.from_id == current_user.id) & (Messages.to_id == to_id))|
        ((Messages.from_id == to_id) & (Messages.to_id == current_user.id)) 
    
    ).order_by(Messages.date_sent).all()
     
     for i in messageHistory:
          print(str(i.message_text))
     profile_pic = profilePicture.query.filter_by(id = to_id).first()

     messages =[{
          'from_id': msg.from_id,
          'to_id': msg.to_id,
          'message_text': msg.message_text,
          'file': url_for('views.get_message_file', sender_id=from_id, receiver_id=to_id, _external=True) + f"?t={int(time.time())}",
          'profile_pic': url_for('views.get_profile_picture', user_id = profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')

     }for msg in messageHistory]

     for i in messages:
          print(i)

     emit('message-history', {'messages': messages}, to = f'target_{current_user.id}')

@socketio.on('send-file')
def sendFile(data):
     to_id = data['to_id']
     from_id = current_user.id
     file_data = data['file']
     file_name = data['fileName']
     file_type = data['fileType']

     file_bytes = base64.b64decode(file_data.split(",")[1])
     

     newFileMessage = Messages(from_id = from_id, to_id = to_id, img = file_bytes, name = file_name, mimetype = file_type)
     db.session.add(newFileMessage)
     db.session.commit()
     profile_pic = profilePicture.query.filter_by(id = current_user.id).first()
     fileData = {
          'from_id': from_id,
          'to_id': to_id,
          'profile_pic': url_for('views.get_profile_picture', user_id = profile_pic.id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg'),
          'file': url_for('views.get_message_file', sender_id = from_id, receiver_id = to_id)
     }

     print(fileData)

     emit('recieve-file', {'fileData':fileData, 'CURRENT_USER_ID': current_user.id}, to = f'target_{to_id}')
     emit('recieve-file', {'fileData':fileData, 'CURRENT_USER_ID': current_user.id}, to = f'target_{current_user.id}')
     

     
@socketio.on('request-comrade-info')
def requestComradeInfo(data):
     comrade_id = data['comrade_id']

     isActive = ActiveUsers.query.filter_by(active_id = comrade_id).first()

     

     comrade = Comrades.query.filter_by(comrade_id = comrade_id).first()
     profile_pic = profilePicture.query.filter_by(user_id = comrade_id).first()
     comrade_info = {
          'owner_id': current_user.id,
          'comrade_id':comrade.comrade_id,
          'comrade_name':comrade.comrade_name,
          'active_status': 'Online' if isActive else 'Offline',
          'profile_pic': url_for('views.get_profile_picture', user_id = comrade_id) if profile_pic else url_for('static', filename = 'defaultImages/default.jpg')
     }

     emit('comrade-info-feedback', {'comrade_info':comrade_info}, to = f'target_{current_user.id}')
     
     
@socketio.on('update-highscore') 
def updateHighscore(data):
     score = data['score']


     newHighscore = User.query.filter_by(id = current_user.id).first()

     newHighscore.highscore += score

     db.session.commit()

     user = User.query.filter_by(id = current_user.id).first()

     print(user.highscore)