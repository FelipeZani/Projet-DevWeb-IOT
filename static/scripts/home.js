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

