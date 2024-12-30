
const likeBtn = document.getElementById('like')
const unlikeBtn = document.getElementById('unlike')
const closeCommentBtn = document.querySelector('.close-comment-box')
const socket = io.connect('http://192.168.1.23:5000');

const searchInput = document.querySelector('.search-input')

let activeConversation = null

socket.on('notify-my-comrade', (data)=>{
     const messageData = data.messageData
     const message_notify = document.querySelector('.message-notify')
     message_notify.style.display = 'block'
     const last_message_container = document.querySelector(`.last-message-${messageData.from_id}`)

     last_message_container.innerHTML = messageData.message_text

})

function viewConversation(comrade_id){
     const contactList = document.querySelectorAll('.contact-listt')
     const sendBtnContainer = document.querySelector('.message-conversation-action-send')
     const last_message = document.querySelector(`.last-message-${comrade_id}`)
     last_message.style = 'font-weight: 300'

     activeConversation = comrade_id
     const messageContent = document.querySelector('.message-conversation-container')
     messageContent.scrollTop = messageContent.scrollHeight;
   

     sendBtnContainer.innerHTML = ""


     const sendButton = document.createElement('button')

          const i = document.createElement('i')
          
          sendButton.appendChild(i)
          i.classList.add('fa-solid')
          i.classList.add('fa-paper-plane')
         
          sendButton.onclick = () => sendMessage(comrade_id)

          sendBtnContainer.appendChild(sendButton)


     contactList.forEach(item =>{
          item.classList.remove('selected-comrade')
     })
     
     const selectedList = document.getElementById(`contactList-${comrade_id}`)

   
     selectedList.classList.add('selected-comrade')
   
     const messageConversationContainer = document.querySelector('.message-other-container')
     const chatContainer = document.querySelector('.message-conversation-container')
     

     

     
     messageConversationContainer.style.display = 'flex'
     messageConversationContainer.classList.add('like-animation')
     chatContainer.scrollTop = chatContainer.scrollHeight
     to_id = comrade_id
     socket.emit('request-comrade-info', {comrade_id})
     socket.emit('load-message-history', {to_id})

     
     socket.on('comrade-info-feedback', (data)=>{

          
          const comrade_info = data.comrade_info
          const head = document.querySelector('.profile-name-conversation')
          const img = document.createElement('img')
          
             
     
          head.innerHTML = `
                
                <h4>${comrade_info.comrade_name}</h4>
          `
          head.prepend(img)
          
          img.src = comrade_info.profile_pic

          if(comrade_info.active_status == 'Online'){
               
               img.classList.add('online')
          }else{
               img.classList.add('offline')
          } 
     })
     
     socket.on('message-history', (data)=>{
          const message_history = data.messages
          

          messageContent.innerHTML = ""
          message_history.forEach((msg)=>{



             

               if( String(msg.from_id) === String(CURRENT_USER_ID)){

                    const div = document.createElement('div')
                    div.classList.add('self-message-all')

                    if(msg.message_text != null){
                         div.innerHTML = `
                         <p class="message-text">${msg.message_text}</p>
                    `
                    }else{
                         div.innerHTML = `
                         <img class="send-img" src="${msg.file}" alt="">
                         `
                    }
                    
          
                    messageContent.appendChild(div)
                    messageContent.scrollTop = messageContent.scrollHeight;
               }else{
                    
                    const div = document.createElement('div')
                    div.classList.add('other-message-all')

                    if(msg.message_text){
                         div.innerHTML = `
                         <img class="profile-other" src="${msg.profile_pic}" alt="">
                         <p class="message-text">${msg.message_text}</p>
                    `
                    }else{
                         div.innerHTML = `
                         <img class="profile-other" src="${msg.profile_pic}" alt="">
                         <img class="send-img" src="${msg.file}" alt="">
               
                         `
                    }
                    
          
                    messageContent.appendChild(div)
                    messageContent.scrollTop = messageContent.scrollHeight;
               }
               
          })
     })
     
}


// for sending message

function uploadFile(){
     const toggle = document.getElementById('toggle-file-text')
     const textarea = document.querySelector('.text-area')
     const upload_file_input = document.querySelector('.upload-file')

     const computedStyle = window.getComputedStyle(toggle).display

     if(toggle.classList.contains('fa-upload')){
          toggle.classList.remove('fa-upload')
          toggle.classList.add('fa-comments')
          textarea.style.display = 'none'
          upload_file_input.style.display = 'flex'
     }else{
          toggle.classList.remove('fa-comments')
          toggle.classList.add('fa-upload')
          upload_file_input.style.display = 'none'
          textarea.style.display = 'block'
     }
}

function sendMessage(target_comrade_id){
     const to_id = target_comrade_id
    
     const message_text = document.getElementById('messageText').value
     const upload_file_input = document.querySelector('.upload-file')
     const textarea = document.querySelector('.text-area')
     const computedStyle = window.getComputedStyle(textarea).display

     

     if(computedStyle == 'none'){
   
          if(upload_file_input.length != 0){

               console.log(upload_file_input)

               const file = upload_file_input.files[0]

               const reader = new FileReader();
               reader.onload = function(e){
                    socket.emit('send-file', {
                         to_id,
                         file: e.target.result,
                         fileName: file.name,
                         fileType: file.type, 
                    });
               };
               reader.readAsDataURL(file)
      
          }
     }else{
        
          if(message_text.length != 0){
               socket.emit('send-message', {to_id, message_text})
          }
     }


     document.getElementById('messageText').value = ""
     document.querySelector('.upload-file').value = ""
}

socket.on('recieve-message', (data)=>{
     const messageData = data.messageData
     const messageContainer = document.querySelector('.message-conversation-container')

     if(messageData.from_id === activeConversation || messageData.to_id === activeConversation){

          if( String(messageData.from_id) === String(CURRENT_USER_ID)){

               const div = document.createElement('div')
               div.classList.add('self-message-all')
     
      
                div.innerHTML = `
                    <p class="message-text">${messageData.message_text}</p>
               `
              
               
     
               messageContainer.appendChild(div)
               messageContainer.scrollTop = messageContainer.scrollHeight;
          }else{
               
               const div = document.createElement('div')
               div.classList.add('other-message-all')
     
              
               div.innerHTML = `
                    <img class="profile-other" src="${messageData.profile_pic}" alt="">
                    <p class="message-text">${messageData.message_text}</p>
               `

     
               messageContainer.appendChild(div)
               messageContainer.scrollTop = messageContainer.scrollHeight;
          }

     }else{
          return
     }
   

})
socket.on('recieve-file', (data)=>{
     const fileData = data.fileData
     const messageContainer = document.querySelector('.message-conversation-container')
  
     if(!fileData || !fileData.from_id || !fileData.file){
          console.error("Invalid fileData received:", fileData);
          return
     }
     if (!messageContainer) {
          console.error("Message container not found.");
          return;
     }
     
     
     
     if( String(fileData.from_id) === String(CURRENT_USER_ID)){

          const div = document.createElement('div')
          div.classList.add('self-message-all')
          div.innerHTML = `
               <img class="send-img" src="${fileData.file}" alt="">
          `

          messageContainer.appendChild(div)
          messageContainer.scrollTop = messageContainer.scrollHeight;
     }else{
          
          const div = document.createElement('div')
          div.classList.add('other-message-all')
          div.innerHTML = `
               <img class="profile-other" src="${fileData.profile_pic}" alt="">
               <img class="send-img" src="${fileData.file}" alt="">
               
          `

          messageContainer.appendChild(div)
          messageContainer.scrollTop = messageContainer.scrollHeight;
     }
     messageContainer.scrollTop = messageContainer.scrollHeight;
})
     



function message(id){
     const comrade_id = id

     

     const messageActionContainer = document.querySelector('.message-action-send-message')

     messageActionContainer.innerHTML = ""


     const sendButton = document.createElement('button')
     



          const i = document.createElement('i')
          
          sendButton.appendChild(i)
          i.classList.add('fa-solid')
          i.classList.add('fa-paper-plane')
         
          sendButton.onclick = () => sendMessage(comrade_id)

          messageActionContainer.appendChild(sendButton)

     const messagePopup = document.querySelector('.message-popup')
     const messageContainer = document.querySelector('.message-container')
     messageContainer.classList.add('like-animation')
     messagePopup.style.display = 'block'
 
 
     
     socket.emit('request-comrade-info', {comrade_id})
     socket.on('comrade-info-feedback', (data)=>{
          const comrade_info = data.comrade_info
          const chatHeadContainer = document.querySelector('.profile-name')
          

          
          

          if(comrade_info.active_status == 'Online'){
               chatHeadContainer.innerHTML =`
                    <img class="online"src="${comrade_info.profile_pic}" alt="">                  
                    <p>${comrade_info.comrade_name}</p>
               `
          }else{
               chatHeadContainer.innerHTML =`
                    <img class="offline"src="${comrade_info.profile_pic}" alt="">                  
                    <p>${comrade_info.comrade_name}</p>
               `
          }

          
     })
     
     const messageContent = document.querySelector('.message-content')
     messageContent.scrollTop = messageContent.scrollHeight;

     socket.emit('load-message-history', {comrade_id})
     messageContent.innerHTML = ""


     socket.on('message-history', (data)=>{
          const message_history = data.messages

          message_history.forEach((msg)=>{

             

               if( String(msg.from_id) === String(CURRENT_USER_ID)){

                    const div = document.createElement('div')
                    div.classList.add('self-message')

                    if(msg.message_text != null){
                         div.innerHTML = `
                         <p class="message-text">${msg.message_text}</p>
                    `
                    }else{
                         div.innerHTML = `
                         <img class="send-img" src="${msg.file}" alt="">
                         `
                    }
                    
          
                    messageContent.appendChild(div)
                    messageContent.scrollTop = messageContent.scrollHeight;
               }else{
                    
                    const div = document.createElement('div')
                    div.classList.add('other-message')

                    if(msg.message_text){
                         div.innerHTML = `
                         <img class="profile-other" src="${msg.profile_pic}" alt="">
                         <p class="message-text">${msg.message_text}</p>
                    `
                    }else{
                         div.innerHTML = `
                         <img class="profile-other" src="${msg.profile_pic}" alt="">
                         <img class="send-img" src="${msg.file}" alt="">
               
                         `
                    }
                    
          
                    messageContent.appendChild(div)
                    messageContent.scrollTop = messageContent.scrollHeight;
               }
               
          })
     })
     messageContent.scrollTop = messageContent.scrollHeight;

}

function openMessageAll(id){
     const message_notify = document.querySelector('.message-notify')
     message_notify.style.display = 'none'
     
     const messageAllPopup = document.querySelector('.message-all-popup')
     const messageCont = document.querySelector('.message-conversation-container')
     const messageContainer = document.querySelector('.message-all-container')

     messageContainer.classList.add('like-animation')
     messageAllPopup.style.display = 'block'

     messageCont.scrollTop = messageCont.scrollHeight;

     const exitBtn = document.querySelector('.exit-message-all')

     exitBtn.addEventListener('click', function(){
          messageAllPopup.style.display = 'none'
     })
}

function exitMessage(){
     const messagePopup = document.querySelector('.message-popup')
     messagePopup.style.display = 'none'
}
socket.on('search-results', (data)=>{
     const results = data.users
     const owner = data.owner
     const results_container = document.querySelector('.search-results')
     const div = document.querySelector('.cont')

     div.innerHTML = ""

     console.log(results.length)

     if(results && results.length > 0){
          results.forEach((result)=>{

               if(owner != result.id){
                    const a = document.createElement('a')
               const img = document.createElement('img')
               const name = document.createElement('p')
     
               name.textContent = result.name
               img.src = result.profile_pic
               a.href = `/view-other-profile/${result.id}`
               a.onclick = () => addToSearchHistory(result.id, result.name)
               a.appendChild(img)
               a.appendChild(name)
               div.appendChild(a)
               results_container.appendChild(div)
               }

          })
     }else if( results.length === 0){
  
          const ehh = document.createElement('div')
          const img = document.createElement('img')
          const name = document.createElement('p')
          
          img.src = '/static/defaultImages/nothing.gif'

          ehh.classList.add('wala-dito')
     
          ehh.appendChild(img)
          div.appendChild(ehh)
          results_container.appendChild(div)
     }
  
})

    
     
function addToSearchHistory(id, name){
     socket.emit('add-to-search-history', {id, name})
}
function deleteHistory(id){
     socket.emit('delete-search-history', {id})
}

function followToggle(userId, ownerId){
     const button = document.getElementById(`follow-${userId}`);
 

     if(button.textContent.trim() == 'Follow'){
          button.textContent = 'Unfollow';
          button.classList.add('unfollow-btn')
          button.classList.remove('follow-btn')
          button.classList.remove('like-animation')

          socket.emit('follow_user', {userId, ownerId})

          
     }else{
          button.textContent = 'Follow';
          button.classList.add('follow-btn')
          button.classList.remove('unfollow-btn')
          button.classList.remove('like-animation')
          
          socket.emit('unfollow_user', {userId, ownerId})
        
     }

     button.classList.add('like-animation');

     socket.on('reload', (data)=>{
          location.reload()
     })
     
}


function toggleLike(postId, userId) {
     const button = document.getElementById(`like-btn-${postId}`);

     const icon = button.querySelector('i'); 
          const isLiked = button.classList.contains('liked');

     button.classList.remove('like-animation');
     void button.offsetWidth; 
     button.classList.add('like-animation');
          
     if (isLiked) {
          socket.emit('unlike_post', { postId, userId });
     } else {
          socket.emit('like_post', { postId, userId }); 
     }
          
     button.classList.toggle('liked');
     if (isLiked) {
          icon.classList.remove('fa-solid');
          icon.classList.add('fa-regular');
     } else {
          icon.classList.remove('fa-regular');
          icon.classList.add('fa-solid');
     };
};


try{
     closeCommentBtn.addEventListener('click', function(){
          const commentBox = document.querySelector('.comment-box-popup');
          commentBox.style.display = 'none';
     });
} catch (e){
     console.log('upload')
}

     
socket.on('update_unlike', (data)=>{
     const { postId, like_count } = data;
     const likeCountSpan = document.getElementById(`like-count-${postId}`);
     likeCountSpan.textContent = like_count;
});
     
socket.on('update_like', (data)=>{
     const { postId, like_count } = data;
     const likeCountSpan = document.getElementById(`like-count-${postId}`);
     likeCountSpan.textContent = like_count;
});








function viewComment(postId){
     const commentBox = document.querySelector('.comment-box-popup')
     socket.emit('view_comments', {postId: postId})

     const currentDisplay = window.getComputedStyle(commentBox).display;


     if(currentDisplay === 'none'){
          commentBox.style.display = 'block';
     }else{
          commentBox.style.display = 'none';
     }
};
socket.on('load_likers', (data)=>{
     const likers = data.likers
     const postId = data.postId
     const likerContainer = document.getElementById(`user-who-likes-${postId}`)
     
     likerContainer.innerHTML = '';

     likers.forEach((liker) => {
          const likerListElement = document.createElement('li');
          likerListElement.textContent = liker;
          likerContainer.appendChild(likerListElement);
     });
});


socket.on('load_comments', (data)=>{
     const comments = data.comments;
     const commentLists = document.querySelector('.comment-list-container')
     console.log(comments)

     commentLists.innerHTML = ''

     comments.forEach((comment) => {
          const commentList = document.createElement('li');
          const imgNameCont = document.createElement('div');
          const profileCont = document.createElement('img');
          const nameCont = document.createElement('p');
          const commentCont = document.createElement('p');
          const dateCont = document.createElement('p');
          commentList.classList.add('comment-list');
          nameCont.classList.add('name');
          commentCont.classList.add('comment-content');
          dateCont.classList.add('date');

          imgNameCont.append(profileCont);
          commentList.appendChild(imgNameCont);
          imgNameCont.appendChild(nameCont);
          commentList.appendChild(dateCont);
          commentList.appendChild(commentCont);
          
          profileCont.src = comment.profile_pic || '/static/defaultImages/default.png';
          nameCont.textContent = `${comment.name}: `;
          commentCont.textContent = comment.comment;
          dateCont.textContent = comment.date;

          commentLists.appendChild(commentList);
          commentLists.scrollTop = commentLists.scrollHeight; 
     });
});

const likeCountHover = document.querySelector('.like-count')

function viewLikes(postId){
     const postLikesContainer = document.getElementById(`user-who-likes-${postId}`)
     const likeCounter = document.getElementById(`like-count-${postId}`)
     socket.emit('view_likes', {postId})



     postLikesContainer.style.display = 'block'

     

     likeCounter.addEventListener('mouseout', function(){
          postLikesContainer.style.display = 'none'
     })
};


function sendComment(postId){
     const comment = document.getElementById(`comment-text-${postId}`).value.trim()

     if(comment === ""){
          socket.emit('do_nothing')
     }else{
          socket.emit('handle_comment', {postId, comment})
          document.getElementById(`comment-text-${postId}`).value = ""
     }
};

socket.on('load_comment_counts', (data)=>{
     const postId = data.postId;
     const commentCount = data.commentCount;

     document.getElementById(`comment-section-counter-${postId}`).textContent = commentCount;
});

// <-- for nitifcations -->
socket.on('listen_for_like_welcome_notification', (data)=>{
     const notification = data.welcomeNotification
     const unread_notification = data.unread_notification_count
     const notificationContainer = document.querySelector('.notification-context-unread')
     const notify = document.querySelector('.notify')
     
     notify.style.display = 'flex'
     notify.classList.add('notify-count')
     notify.textContent = unread_notification

     const li = document.createElement('li')
     const img = document.createElement('img')
     const span = document.createElement('span')
     span.textContent = notification.context_type
     img.src = notification.profile_pic || '/static/defaultImages/default.png';     
     li.appendChild(img)
     li.appendChild(span)
     notificationContainer.prepend(li)      
});

socket.on('listen_for_like_notification', (data)=>{
     const notify = document.querySelector('.notify')
     const unread_notification = data.unread_notification_count
     const notifications = data.recentNotification
     const notificationContainer = document.querySelector('.notification-context-unread')
     

     notify.style.display = 'flex'
     notify.classList.add('notify-count')
     notify.textContent = unread_notification

     const li = document.createElement('li')
     const img = document.createElement('img')
     const span = document.createElement('span')
     span.textContent = notifications.context_type
     img.src = notifications.profile_pic || '/static/defaultImages/default.png';     
     li.appendChild(img)
     li.appendChild(span)
     notificationContainer.prepend(li)      

});
const notifBtn = document.querySelector('.menu-btn-text')

     notifBtn.addEventListener('click', function(){
          const notifCon = document.querySelector('.notification-container')
          const computedStyle = window.getComputedStyle(notifCon).display
          const notificationContainer = document.querySelector('.notification-context-unread')

          if(computedStyle == 'flex'){
                console.log('nothing here')
           }else{
                notificationContainer.innerHTML = ''
           }
          

     }) 

function viewNotifications(userId){
     let notificationContainer = document.querySelector('.notification-container')
     const notify = document.querySelector('.notify')
     const notifyParent = document.querySelector('.notify-parent')
     let notifContainer = window.getComputedStyle(notificationContainer).display;

     if(notifContainer == 'none'){
          notificationContainer.style.display = 'flex'
          notify.style.display = 'none'
     }else{
          notificationContainer.style.display = 'none'
     }

     socket.emit('clear_notifications', {userId})
}

const unreadBtn = document.getElementById('unread-notification')
const allBtn = document.getElementById('history-notification')
const unreadContainer = document.querySelector('.notification-context-unread')
const historyContainer = document.querySelector('.notification-context')

unreadBtn.addEventListener('click', function(){
     
     historyContainer.style.display = 'none'
     unreadContainer.style.display = 'flex'
     unreadBtn.classList.add('buttonToggled')
     allBtn.classList.remove('buttonToggled')
     
})
allBtn.addEventListener('click', function(){
     unreadContainer.style.display = 'none'
     historyContainer.style.display = 'flex'
     unreadBtn.classList.remove('buttonToggled')
     allBtn.classList.add('buttonToggled')
     
})

