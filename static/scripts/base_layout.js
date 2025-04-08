const html = document.querySelector("html")
const bd = document.querySelector("body")
const darkModeOnIcon =  document.getElementsByClassName("bi-brightness-high-fill")[0]
const darkModeOffIcon = document.getElementsByClassName("bi-brightness-high")[0]

var timer = null
function doneScrolling(){
    navBar.style.opacity=1   

}

function setBgImg(isDark){
    let bgImage = document.getElementById("heroImg")

    if(bgImage != null){
        if(isDark)
            bgImage.src="../static/assets/heroSectionBgImgDark.jpg"
        else
            bgImage.src="../static/assets/heroSectionBgImgLight.jpg"

    }
}




window.onload = function(){
    if(localStorage.getItem("theme") === "dark-mode"){

        html.classList.add("dark-mode")
        darkModeOnIcon.style.display = "block"
        darkModeOffIcon.style.display = "none" 
        setBgImg(true)

    }else{
        setBgImg(false)
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

        setBgImg(false)


    }else{

        html.classList.add("dark-mode")

        localStorage.setItem("theme","dark-mode")

        darkModeOnIcon.style.display = "block"
        darkModeOffIcon.style.display = "none" 

        setBgImg(true)

    }

}