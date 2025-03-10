
function onClick(event) {
  if (event.target === dialog) {
    dialog.close() 
  }
}



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

const dialog = document.querySelector("dialog")
const logInBtnFrm = document.getElementById("logInFrmBtn") 
const signUpBtnFrm = document.getElementById("signUpFrmBtn") 
const logInFrm = document.getElementById("logInFrm") 
const signUpFrm = document.getElementById("signUpFrm") 

dialog.addEventListener("click", onClick)
logInBtnFrm.classList.add("ls-button-activated") 
signUpFrm.style.visibility = "collapse"  