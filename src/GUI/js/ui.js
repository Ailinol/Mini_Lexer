'use strict';

import {abrirModal} from './modal.js';
import { actualizarNumeroLinhas } from './editor.js';

export function definirEstado(msg, tipo=  '') {
    const elemento = document.getElementById('status-msg');
    elemento.textContent = msg;
    elemento.className = tipo;
}


export function actualizarEstatisticas(tokens, erros, codigo) {
    console.log('Actualizando estatísticas:', { tokens: tokens.length, erros: erros.length });
    const totalLinhas = codigo ? codigo.split('\n').length : 0;
    
    const tokenEl = document.getElementById('stat-tokens');
    const errorEl = document.getElementById('stat-errors');
    const linesEl = document.getElementById('stat-lines');

    if (tokenEl) tokenEl.innerHTML = `<strong>${tokens.length}</strong> tokens`;
    if (errorEl) {
        errorEl.innerHTML = `<strong>${erros.length}</strong> erros`;
        errorEl.className = 'stat-chip ' + (erros.length > 0 ? 'chip-erro' : '');
    }
    if (linesEl) linesEl.innerHTML = `<strong>${totalLinhas}</strong> linhas`;
}

export function limparResultados() {
  document.getElementById('token-body').innerHTML = '';
  document.getElementById('tokens-empty').style.display = 'flex';
  document.getElementById('token-table').style.display  = 'none';
  document.getElementById('errors-list').innerHTML = `
    <div class="empty" id="errors-empty">
      <div class="empty-icon">✓</div>
      <div>Nenhum erro detectado</div>
    </div>`;
  actualizarEstatisticas([], [], '\n');
  definirEstado('Pronto');
}

export function limparTudo(idFicheiroActivo) {
  document.getElementById('code-input').value = '';
  actualizarNumeroLinhas();
  limparResultados();
}