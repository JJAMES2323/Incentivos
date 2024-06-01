const navbarMenu = document.querySelector(".navbar .links");
const hamburgerBtn = document.querySelector(".hamburger-btn");
const hideMenuBtn = navbarMenu.querySelector(".close-btn");
const showPopupBtn = document.querySelector(".login-btn");
const formPopup = document.querySelector(".form-popup");
const hidePopupBtn = formPopup.querySelector(".close-btn");
const signupLoginLink = formPopup.querySelectorAll(".bottom-link a");
 
hamburgerBtn.addEventListener("click", () => {
navbarMenu.classList.toggle("show-menu");
});

 
hideMenuBtn.addEventListener("click", () =>  hamburgerBtn.click());
 
showPopupBtn.addEventListener("click", () => {
    document.body.classList.toggle("show-popup");
});


hidePopupBtn.addEventListener("click", () => showPopupBtn.click());


signupLoginLink.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        formPopup.classList[link.id === 'signup-link' ? 'add' : 'remove']("show-signup");
    });
});



document.getElementById("btn_open").addEventListener("click", open_close_menu);


var side_menu = document.getElementById("menu_side");
var btn_open = document.getElementById("btn_open");
var body = document.getElementById("body");


    function open_close_menu(){
        body.classList.toggle("body_move");
        side_menu.classList.toggle("menu__side_move");
    }



if (window.innerWidth < 760){

    body.classList.add("body_move");
    side_menu.classList.add("menu__side_move");
}



window.addEventListener("resize", function(){

    if (window.innerWidth > 760){

        body.classList.remove("body_move");
        side_menu.classList.remove("menu__side_move");
    }

    if (window.innerWidth < 760){

        body.classList.add("body_move");
        side_menu.classList.add("menu__side_move");
    }

});

document.addEventListener("DOMContentLoaded", function () {
    const registroForm = document.getElementById("registroForm");
    const registrarOption = document.getElementById("registrarOption");
    const cerrarForm = document.getElementById("cerrarForm");
  
    registrarOption.addEventListener("click", function (e) {
      e.preventDefault();
      registroForm.style.display = "block";
    });
  
    cerrarForm.addEventListener("click", function () {
      registroForm.style.display = "none";
    });
  });