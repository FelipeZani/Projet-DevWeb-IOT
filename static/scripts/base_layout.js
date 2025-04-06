const html = document.querySelector("html")
const bd = document.querySelector("body")
const darkModeOnIcon =  document.getElementsByClassName("bi-brightness-high-fill")[0]
const darkModeOffIcon = document.getElementsByClassName("bi-brightness-high")[0]
const navBar = document.querySelector("nav")

var timer = null
function doneScrolling(){
    navBar.style.opacity=1   

}


window.addEventListener('scroll', function() {
    if (timer !== null) {
        clearTimeout(timer);        
        navBar.style.opacity=0.8 

    }

    timer = setTimeout(doneScrolling, 150);
}, false);


window.onload = function(){
    if(localStorage.getItem("theme") === "dark-mode"){

        html.classList.add("dark-mode")
        darkModeOnIcon.style.display = "block"
        darkModeOffIcon.style.display = "none" 

    }
    if(localStorage.getItem("special-font") === "d-font"){
        bd.classList.add("d-font")
    }
}

function toggleFont(){
    if(bd.classList.contains("d-font")){

        bd.classList.remove("d-font")

        localStorage.removeItem("special-font")

    }else{

        bd.classList.add("d-font")

        localStorage.setItem("special-font","d-font")

    }
}
function toggleTheme(){
   
    if(html.classList.contains("dark-mode")){

        html.classList.remove("dark-mode")

        localStorage.removeItem("theme")

        darkModeOnIcon.style.display = "none"
        darkModeOffIcon.style.display = "block"

    }else{

        html.classList.add("dark-mode")

        localStorage.setItem("theme","dark-mode")

        darkModeOnIcon.style.display = "block"
        darkModeOffIcon.style.display = "none" 

    }

}