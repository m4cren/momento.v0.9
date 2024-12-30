let passwordInput = document.getElementById('passwordInput');
let passwordInput1 = document.getElementById('passwordInput1');
let passwordInput2 = document.getElementById('passwordInput2');
let showPassword = document.getElementById('showPassword');
let showPassword1 = document.getElementById('showPassword1');
let showPassword2 = document.getElementById('showPassword2');
let warningText = document.querySelector('.warning-text');

const privacyPopup = document.querySelector('.privacy-policy-container')
const privContainer = document.querySelector('.priv-container')
const privacyBtn = document.getElementById('privacyBtn')
const exitPrivacyContainer = document.querySelector('.exit-privacy-container')

privacyBtn.addEventListener('click', function(){
     privacyPopup.style.display = " block"
     privContainer.classList.add('fromTop-animation')
})

exitPrivacyContainer.addEventListener('click', function(){
     privacyPopup.style.display = 'none'
})

passwordInput2.addEventListener('input', function(){
     if(passwordInput1.value == passwordInput2.value){
          warningText.innerHTML = 'Password match'
          warningText.style = 'background-color: green'
     }else{
          warningText.innerHTML = 'Password do not match'
          warningText.style = 'background-color: red'
     }
});


showPassword.onclick = function(){
     if(passwordInput.type == "password"){
          passwordInput.type = "text";
     }else{
          passwordInput.type = "password";
     }
};
showPassword1.onclick = function(){
     if(passwordInput1.type == "password"){
          passwordInput1.type = "text";
     }else{
          passwordInput1.type = "password";
     }
};
showPassword2.onclick = function(){
     if(passwordInput2.type == "password"){
          passwordInput2.type = "text";
     }else{
          passwordInput2.type = "password";
     }
};





document.getElementById('aboutUsBtn').addEventListener('click',function(){

     document.querySelector('.about-us-pop').style.display = 'block';
     document.querySelector('.about-us-container').classList.add('fromTop-animation')
     
});
document.getElementById('exit-about-us').addEventListener('click',function(){

     document.querySelector('.about-us-pop').style.display = 'none';
     
});

document.getElementById('login-btn').addEventListener('click',function(){
     document.querySelector('.login-pop').style.display = 'block';
});


document.querySelector('.exit-login').addEventListener('click',function(){
     var content = document.querySelector('.login-pop').style.display = 'none';
     let loginCont = document.getElementById('login-container')

     if(content == 'none'){
          content = 'block';
     }else{
          loginCont.classList.add('toBottom-animation')
          content = 'none';
     };
});
document.getElementById('signup-btn').addEventListener('click',function(){
     document.querySelector('.signup-pop').style.display = 'block';
});
document.querySelector('.exit-signup').addEventListener('click',function(){
     var content = document.querySelector('.signup-pop').style.display = 'none';

     if(content == 'none'){
          content = 'block';
     }else{
          content = 'none';
     };
});

const promptContainer = document.querySelector('.prompt-container')
const exitPrompt = document.querySelector('.exit-prompt')

exitPrompt.addEventListener('click', function(){
     promptContainer.classList.add("hidden");
});



