document.getElementById("btn_open").addEventListener("click", open_close_menu);

var side_menu = document.getElementById("menu_side");
var btn_open = document.getElementById("btn_open");
var body = document.getElementById("body");

function open_close_menu() {
    body.classList.toggle("body_move");
    side_menu.classList.toggle("menu__side_move");
}

if (window.innerWidth < 760) {
    body.classList.add("body_move");
    side_menu.classList.add("menu__side_move");
}

window.addEventListener("resize", function () {
    if (window.innerWidth > 760) {
        body.classList.remove("body_move");
        side_menu.classList.remove("menu__side_move");
    }
    if (window.innerWidth < 760) {
        body.classList.add("body_move");
        side_menu.classList.add("menu__side_move");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const registroForm = document.getElementById("registroForm");
    const gestionForm = document.getElementById("gestionForm");
    const editarForm = document.getElementById("editarForm");
    const registrarOption = document.getElementById("registrarOption");
    const gestionOption = document.getElementById("gestionOption");
    const editarOption = document.getElementById("editarOption");

    registrarOption.addEventListener("click", function (e) {
        e.preventDefault();
        registroForm.style.display = "block";
        gestionForm.style.display = "none"; // Asegurarse de ocultar el otro formulario si está visible
        editarForm.style.display = "none"; // Asegurarse de ocultar el otro formulario si está visible
    });

    gestionOption.addEventListener("click", function (e) {
        e.preventDefault();
        gestionForm.style.display = "block";
        registroForm.style.display = "none"; // Asegurarse de ocultar el otro formulario si está visible
        editarForm.style.display = "none"; // Asegurarse de ocultar el otro formulario si está visible
    });
    editarOption.addEventListener("click", function (e) {
        e.preventDefault();
        editarForm.style.display = "block";
        registroForm.style.display = "none"; // Asegurarse de ocultar el otro formulario si está visible
        gestionForm.style.display = "none"; // Asegurarse de ocultar el otro formulario si está visible
    });
});