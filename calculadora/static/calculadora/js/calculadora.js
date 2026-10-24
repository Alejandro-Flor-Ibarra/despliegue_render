const pantalla = document.getElementById('pantalla');
const teclas = document.querySelector('.calculator__keys');
const historialBody = document.getElementById('historial-body');
const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]')?.value;
const guardarUrl = document.querySelector('.calculator')?.dataset.saveUrl;

function presionar(valor) {
    if (pantalla.value === 'Error' || (pantalla.value === '0' && /\d/.test(valor))) {
        pantalla.value = valor;
        return;
    }

    pantalla.value += valor;
}

function limpiar() {
    pantalla.value = '0';
}

function calcular() {
    const operacion = pantalla.value;

    try {
        const resultado = Function(`"use strict"; return (${operacion})`)();
        if (!Number.isFinite(resultado)) {
            throw new Error('El resultado no es un número finito.');
        }

        pantalla.value = String(resultado);
        if (operacion !== String(resultado)) {
            guardar(operacion, resultado);
        }
    } catch {
        pantalla.value = 'Error';
    }
}

async function guardar(operacion, resultado) {
    try {
        const respuesta = await fetch(guardarUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ operacion, resultado }),
        });
        const datos = await respuesta.json();

        if (respuesta.ok && datos.ok) {
            agregarFila(datos);
        }
    } catch (error) {
        console.error('No se pudo guardar el resultado:', error);
    }
}

function agregarFila(datos) {
    document.getElementById('sin-datos')?.remove();

    const fila = historialBody.insertRow(0);
    fila.insertCell().textContent = datos.fecha;
    fila.insertCell().textContent = datos.operacion;
    fila.insertCell().textContent = datos.resultado;
}

teclas?.addEventListener('click', (evento) => {
    const boton = evento.target.closest('button');
    if (!boton) return;

    if (boton.dataset.action === 'clear') {
        limpiar();
    } else if (boton.dataset.action === 'calculate') {
        calcular();
    } else if (boton.dataset.value) {
        presionar(boton.dataset.value);
    }
});
