// var section
const dialog = document.querySelector("dialog")
const logInBtnFrm = document.getElementById("logInFrmBtn") 
const signUpBtnFrm = document.getElementById("signUpFrmBtn")
const signUpSubFrm = document.getElementById("sub-btn") 
const logInFrm = document.getElementById("logInFrm") 
const signUpFrm = document.getElementById("signUpFrm")

let strength = checkStrength(signUpFrm['password'].value)
let password = document.getElementById("signup-password")
let power = document.getElementById("contet-load")
let invalidInputs = document.getElementsByClassName("incorect-input-field")


//Dialog
dialog.addEventListener("click", onClick)
function onClick(event) {
  if (event.target === dialog) {
    dialog.close() 
  }
}

function openDiag(shownUpForm){
  handleDiagFormOptions(shownUpForm)
  document.querySelector('dialog').showModal()
}

//LS Form
function handleDiagFormOptions(isLoginSelected) {
  if (isLoginSelected) {

    logInBtnFrm.classList.add("ls-button-activated") 
    signUpBtnFrm.classList.remove("ls-button-activated") 
    
    signUpFrm.reset()
    logInFrm.style.display = "flex"   
    signUpFrm.style.display = "none"  

  } else {
    
    logInBtnFrm.classList.remove("ls-button-activated") 
    signUpBtnFrm.classList.add("ls-button-activated") 
    
    logInFrm.reset()
    logInFrm.style.display = "none"   
    signUpFrm.style.display = "flex"

  }
}


//password Verification
function checkStrength(value){
  let newStregthValue = 0
  if (value.length > 6) newStregthValue += 10
  if (value.match(/[a-z]+/)) newStregthValue += 15
  if (value.match(/[A-Z]+/)) newStregthValue += 25
  if (value.match(/[0-9]+/)) newStregthValue += 25
  if (value.match(/[$@#&!€]+/)) newStregthValue += 25
  return newStregthValue
}
password.oninput = function () {
  
  let value = password.value

  let colorPower = {
      0: "#c4c4c4",
      10: "#D73F40",
      25: "#DC6551",
      50: "#F2B84F",
      75: "#BDE952",
      100: "#3ba62f"
  }

  // Case: Empty password
  if (value.length === 0) {
      strength = 0
  } else {
      strength = checkStrength(value)
  }

  if(strength != 100){
    signUpSubFrm.classList.add("disabled")
  }else{
    signUpSubFrm.classList.remove("disabled")

  }

  // Ensure max strength is 100%
  strength = Math.min(strength, 100)

  // Apply styles
  power.style.width = strength>0? strength + "%" : (strength+1)+"%"
  power.style.backgroundColor = colorPower[strength]
}

//check Login/signup and submiting through http request
function checkLogIn(){
  let userNameLength = logInFrm["username"].value.length
  let passWordLength = logInFrm["password"].value.length
  let isOperationValid = true
  
  if( userNameLength <= 0){
    
    logInFrm["username"].classList.add('incorect-input-field')
    isOperationValid = false
  }
  if( passWordLength <= 0){
    
    logInFrm["password"].classList.add('incorect-input-field')
    isOperationValid = false
  
  }

  if(isOperationValid){ 
    sendLoginRequest(logInFrm["username"],logInFrm["password"])

  }else{
    return;
  }
  
}

function checkSignUp(){
 
  let signupInputList = document.getElementsByClassName("sup-form") 
  let isOperationValid = true
  
  for (let i = 0; i < signupInputList.length; i++){ //look for an empty input field
    
    

    if(signupInputList[i].value.length <= 0){
      
      signupInputList[i].classList.add("incorect-input-field")

      isOperationValid = false
    }
      
  }
  if(isOperationValid){
    sendSignUpRequest(signUpFrm["susername"].value,signUpFrm["signup-password"].value, signUpFrm["fname"].value, signUpFrm["lname"].value
      ,signUpFrm["email"].value, signUpFrm["gender"].value,signUpFrm["role"].value,signUpFrm["birthdate"].value)

  }


}


function sendSignUpRequest(  username,password,fname,lname,email,gender,role,birthdate){

  fetch("/login",{
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username :   username,
      password:password,
      fname:fname,
      lname:lname,
      email:email,
      gender:gender,
      role:role,
      birthdate:birthdate,
      action:"signup"
    })
  })
  .then(response=>response.json())
  .then(data => {
    if (data.success) {
      alert("Your account was successfully created, you shall wait for an admin to add you to the family")
      signUpFrm.reset()
    } else {
      // Display error messages
      data.messages.forEach(message => {
      for (let key in message) {     
          document.getElementById(key).classList.add("incorect-input-field")
          alert(message[key])
        }
      })
    }
  })
  .catch(error => {
      console.error("Error:", error);
  })

}

function sendLoginRequest(username, password) {

  fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        username: username.value,
        password: password.value,
        action: "signin"
    })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Successful login, redirect the user to the dashboard
          window.location.href = data.redirect;
      } else {
          // Display error messages
          data.messages.forEach(message => {
            
            for (let key in message) {
                
              alert(message[key]);
            
            }

          });
          
          username.classList.add('incorect-input-field')
          password.classList.add('incorect-input-field')
      }
  })
  .catch(error => {
      
    console.error("Error:", error);
  
  });

}

//Login Signup Input eventListeners

document.addEventListener("click", function(event) {
  if (event.target.classList.contains("incorect-input-field")) {
    event.target.classList.remove("incorect-input-field");
  }
});