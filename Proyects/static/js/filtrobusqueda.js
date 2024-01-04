function filtrarPlantas() {
    let filtro = document.getElementById("filtroNombre").value.toLowerCase();
    let cartas = document.querySelectorAll(".plant-card");
    let mensaje = document.getElementById("mensajeNoResultados");

    let encontrados = 0;

    cartas.forEach(cart => {
        let nombre = cart.querySelector("h2").textContent.toLowerCase(); // Busca en el nombre en lugar del comentario

        if (nombre.includes(filtro) || filtro === "") {
            cart.style.display = "block";
            encontrados++;
        } else {
            cart.style.display = "none";
        }
    });

    if (encontrados === 0) {
        mensaje.style.display = "block";
    } else {
        mensaje.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    cargarOpcionesDropdown();
});