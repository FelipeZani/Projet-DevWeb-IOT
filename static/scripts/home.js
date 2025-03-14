// var section
const dialog = document.querySelector("dialog")
const logInBtnFrm = document.getElementById("logInFrmBtn") 
const signUpBtnFrm = document.getElementById("signUpFrmBtn") 
const logInFrm = document.getElementById("logInFrm") 
const signUpFrm = document.getElementById("signUpFrm")
 
let strength = 0
let password = document.getElementById("signup-password")
let power = document.getElementById("contet-load")

dialog.addEventListener("click", onClick)

//Dialog
function onClick(event) {
  if (event.target === dialog) {
    dialog.close() 
  }
}

function openDiag(shownUpForm){
  handleDiagFormOptions(shownUpForm)
  document.querySelector('dialog').showModal()
}

//Switching between Login SignUp
function handleDiagFormOptions(isLoginSelected) {
  if (isLoginSelected) {

    logInBtnFrm.classList.add("ls-button-activated") 
    signUpBtnFrm.classList.remove("ls-button-activated") 
    
    logInFrm.style.visibility = "visible"   
    signUpFrm.style.visibility = "collapse"  

  } else {
    
    logInBtnFrm.classList.remove("ls-button-activated") 
    signUpBtnFrm.classList.add("ls-button-activated") 
    
    logInFrm.style.visibility = "collapse"   
    signUpFrm.style.visibility = "visible"

  }
}


//password Verification


password.oninput = function () {
  let strength = 0
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
      if (value.length > 6) strength += 10
      if (value.match(/[a-z]+/)) strength += 15
      if (value.match(/[A-Z]+/)) strength += 25
      if (value.match(/[0-9]+/)) strength += 25
      if (value.match(/[$@#&!€]+/)) strength += 25
  }

  // Ensure max strength is 100%
  strength = Math.min(strength, 100)

  // Apply styles
  power.style.width = strength>0? strength + "%" : (strength+1)+"%"
  power.style.backgroundColor = colorPower[strength]
}









