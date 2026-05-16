'use strict';

export function actualizarNumeroLinhas() {
  const editor = document.getElementById('code-input');
  const numeros = document.getElementById('line-numbers');
  const total = editor.value.split('\n').length;
  numeros.innerHTML = Array.from({ length: total }, (_, i) => i + 1).join('<br>');
}

export function sincronizarScroll() {
  const editor = document.getElementById('code-input');
  const numeros = document.getElementById('line-numbers');
  numeros.scrollTop = editor.scrollTop;
}

export function tratarTab(evento) {
  if (evento.key !== 'Tab') return;
  evento.preventDefault();
  const editor = evento.target;
  const inicio = editor.selectionStart;
  const fim = editor.selectionEnd;
  editor.value = editor.value.substring(0, inicio) + '    ' + editor.value.substring(fim);
  editor.selectionStart = editor.selectionEnd = inicio + 4;
  actualizarNumeroLinhas();
}

export function actualizarPosicaoCursor(evento) {
  const editor = evento.target;
  const textoAtesCursor = editor.value.substring(0, editor.selectionStart);
  const linha = textoAtesCursor.split('\n').length;
  const coluna = editor.selectionStart - textoAtesCursor.lastIndexOf('\n');
  document.getElementById('cursor-pos').textContent = `Ln ${linha}, Col ${coluna}`;
}

export function iniciarEditor() {
  const editor = document.getElementById('code-input');
  editor.addEventListener('keydown', tratarTab);
  editor.addEventListener('keyup', actualizarPosicaoCursor);
  editor.addEventListener('scroll', sincronizarScroll);
}