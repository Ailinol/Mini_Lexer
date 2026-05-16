'use strict';

const overlay = document.getElementById('modal-overlay');
const titulo = document.getElementById('modal-title');
const input = document.getElementById('modal-input');
let callbackConfirmacao = null;

export function abrirModal(textoTitulo, valorInicial, callback) {
  titulo.textContent = textoTitulo;
  input.value = valorInicial;
  callbackConfirmacao = callback;
  overlay.classList.add('open'); // Sincronizado com styles.css (.open)
  setTimeout(() => input.select(), 50);
}

export function confirmarModal() {
  if (callbackConfirmacao) callbackConfirmacao(input.value);
  fecharModal();
}

export function cancelarModal() {
  fecharModal();
}

function fecharModal() {
  overlay.classList.remove('open');
  callbackConfirmacao = null;
}
