function cargarOpcionesDropdown() {
    let comentarios = new Set();
    let cartas = document.querySelectorAll(".plant-card p");
    
    cartas.forEach(cart => {
        comentarios.add(cart.textContent.trim().toLowerCase());
    });

    let dropdown = document.getElementById("filtroComentarioDropdown");
    dropdown.innerHTML = '<option value="">Clases según su duración</option>';
    
    comentarios.forEach(comentario => {
        dropdown.innerHTML += `<option value="${comentario}">${comentario}</option>`;
    });
}

function filtrarPorDropdown() {
    let seleccion = document.getElementById("filtroComentarioDropdown").value.toLowerCase();
    let cartas = document.querySelectorAll(".plant-card");

    cartas.forEach(cart => {
        let comentario = cart.querySelector("p").textContent.toLowerCase();

        if (seleccion === "" || comentario.includes(seleccion)) {
            cart.style.display = "block";
        } else {
            cart.style.display = "none";
        }
    });
}