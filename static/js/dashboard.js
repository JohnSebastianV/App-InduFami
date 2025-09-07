let platosSeleccionados = [];
let diasSeleccionados = [];

function cargarPlatos() {
    diasSeleccionados = Array.from(document.querySelectorAll('input[name="dias"]:checked'))
        .map(cb => parseInt(cb.value));

    if (diasSeleccionados.length === 0 || diasSeleccionados.length > 3) {
        Swal.fire({
            icon: 'warning',
            title: 'Selección inválida',
            text: 'Debes seleccionar entre 1 y 3 días',
            confirmButtonColor: '#FF8200' // Naranja Essity
        });
        return;
    }

    axios.post("/get_platos", { dias: diasSeleccionados })
        .then(res => {
            const platos = res.data;
            const cont = document.getElementById("platos-container");
            cont.innerHTML = "";

            // Agrupamos los platos por día
            const grupos = {};
            platos.forEach(p => {
                if (!grupos[p.dia_id]) {
                    grupos[p.dia_id] = { nombre: p.dia_nombre, platos: [] };
                }
                grupos[p.dia_id].platos.push(p);
            });

            // Renderizamos agrupado
            for (const diaId in grupos) {
                const grupo = grupos[diaId];

                const diaTitulo = document.createElement("h3");
                diaTitulo.textContent = grupo.nombre;
                diaTitulo.classList.add("dia-titulo");
                cont.appendChild(diaTitulo);

                grupo.platos.forEach(p => {
                    const label = document.createElement("label");
                    label.classList.add("plato-label");
                    label.innerHTML = `
                        <input type="checkbox" value="${p.id}" onchange="togglePlato(${p.id})">
                        <span>${p.nombre}</span>
                    `;
                    cont.appendChild(label);
                });
            }
        });
}

function togglePlato(id) {
    if (platosSeleccionados.includes(id)) {
        platosSeleccionados = platosSeleccionados.filter(p => p !== id);
    } else {
        platosSeleccionados.push(id);
    }
}

function guardarReserva() {
    if (platosSeleccionados.length === 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Debes seleccionar al menos un plato',
            confirmButtonColor: '#F50082' // Fucsia Essity
        });
        return;
    }

    axios.post("/guardar_reserva", { platos: platosSeleccionados })
        .then(res => {
            if (res.data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Reserva completada',
                    text: res.data.message,
                    confirmButtonColor: '#009A44' // Verde Essity
                }).then(() => {
                    if (res.data.redirect) {
                        window.location.href = res.data.redirect;
                    }
                });
            }
        })
        .catch(err => {
            let msg = "Hubo un error guardando la reserva"; // fallback

            if (err.response && err.response.data && err.response.data.message) {
                msg = err.response.data.message; // 👈 mensaje del backend
            }

            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: msg,
                confirmButtonColor: '#F50082' // Fucsia Essity
            });

            console.error(err);
        });
}

