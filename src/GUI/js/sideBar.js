'use strict';

import { FS, fsFind, fsGetFile, fsAllFiles } from './file_system.js';
import { actualizarNumeroLinhas } from './editor.js';
import { limparResultados } from './ui.js';
import { tokenizar } from './lexer.js';
import { mostrarMenuContexto } from './contextMenu.js';


let idFicheiroActivo = FS.activeId;

export function obterFicheiroActivo() { return idFicheiroActivo; }
export function definirFicheiroActivo(id) { idFicheiroActivo = id; }

function obterIconeFicheiro(nome) {
  if (nome.endsWith('.pas') || nome.endsWith('.pp')) return '📄';
  if (nome.endsWith('.md')) return '📝';
  if (nome.endsWith('.txt')) return '🗒️';
  return '📃';
}

function renderizarArvoreLegado(nos = FS.tree, contentor = document.getElementById('file-tree'), profundidade = 0) {
  if (profundidade === 0) contentor.innerHTML = '';

  for (const no of nos) {
    const item = document.createElement('div');
    item.className = [
      'tree-item',
      no.type === 'folder' ? 'folder' : '',
      no.id === idFicheiroActivo ? 'active' : '',
    ].join(' ').trim();

    // Define o recuo visual (padding-left)
    item.style.paddingLeft = `${(profundidade * 12) + 12}px`;
    item.dataset.id = no.id;

    const icone = no.type === 'folder'
      ? (no.open ? '▼' : '▶')
      : obterIconeFicheiro(no.name);

    const iconePasta = no.type === 'folder' ? (no.open ? '📂' : '📁') : '';

    item.innerHTML = `
      <span class="item-icon-arrow">${no.type === 'folder' ? icone : ''}</span>
      <span class="item-icon">${no.type === 'folder' ? iconePasta : icone}</span>
      <span class="item-name">${escaparHtml(no.name)}</span>`;

    item.addEventListener('click', () => aoClicarArvore(no));
    item.addEventListener('contextmenu', e => mostrarMenuContexto(e, no.id));
    contentor.appendChild(item);

    if (no.type === 'folder' && no.open && no.children) {
      // Cria um container para o grupo de filhos para poder desenhar a linha vertical
      const childrenContainer = document.createElement('div');
      childrenContainer.className = 'tree-children';
      // A linha vertical fica posicionada com base na profundidade
      childrenContainer.style.marginLeft = `${(profundidade * 12) + 18}px`;
      childrenContainer.style.borderLeft = '1px solid var(--border)';
      contentor.appendChild(childrenContainer);

      renderizarArvore(no.children, childrenContainer, 0.5);
    }
  }
}

export function renderizarArvoreVSCode(nos = FS.tree, contentor = document.getElementById('file-tree'), profundidade = 0) {
  if (profundidade === 0) contentor.innerHTML = '';

  for (const no of nos) {
    const item = document.createElement('div');
    item.className = [
      'tree-item',
      no.type === 'folder' ? 'folder' : '',
      no.id === idFicheiroActivo ? 'active' : '',
    ].join(' ').trim();

    item.style.paddingLeft = `${(profundidade * 16) + 10}px`;
    item.dataset.id = no.id;

    const seta = no.type === 'folder' ? (no.open ? '▼' : '▶') : '';
    const icone = no.type === 'folder' ? (no.open ? '📂' : '📁') : obterIconeFicheiro(no.name);

    item.innerHTML = `
      <span class="item-arrow">${seta}</span>
      <span class="item-icon">${icone}</span>
      <span class="item-name">${escaparHtml(no.name)}</span>`;

    item.addEventListener('click', () => aoClicarArvore(no));
    item.addEventListener('contextmenu', e => mostrarMenuContexto(e, no.id));
    contentor.appendChild(item);

    if (no.type === 'folder' && no.open && no.children) {
      // No estilo VS Code, a linha vertical é desenhada por um container
      const childrenGroup = document.createElement('div');
      childrenGroup.className = 'tree-group';
      // O segredo das linhas verticais do VS Code
      childrenGroup.style.borderLeft = '1px solid #ffffff15';
      childrenGroup.style.marginLeft = `${(profundidade * 16) + 16}px`;
      contentor.appendChild(childrenGroup);

      renderizarFilhos(no.children, childrenGroup, 0);
    }
  }
}

function renderizarFilhos(nos, contentor, profundidade) {
  for (const no of nos) {
    const item = document.createElement('div');
    item.className = ['tree-item', no.type === 'folder' ? 'folder' : '', no.id === idFicheiroActivo ? 'active' : ''].join(' ').trim();
    item.style.paddingLeft = `12px`; // Padding fixo relativo à linha vertical

    const seta = no.type === 'folder' ? (no.open ? '▼' : '▶') : '';
    const icone = no.type === 'folder' ? (no.open ? '📂' : '📁') : obterIconeFicheiro(no.name);

    item.innerHTML = `
          <span class="item-arrow">${seta}</span>
          <span class="item-icon">${icone}</span>
          <span class="item-name">${escaparHtml(no.name)}</span>`;

    item.addEventListener('click', () => aoClicarArvore(no));
    item.addEventListener('contextmenu', e => mostrarMenuContexto(e, no.id));
    contentor.appendChild(item);

    if (no.type === 'folder' && no.open && no.children) {
      const subGroup = document.createElement('div');
      subGroup.className = 'tree-group';
      subGroup.style.borderLeft = '1px solid #ffffff15';
      subGroup.style.marginLeft = `18px`;
      contentor.appendChild(subGroup);
      renderizarFilhos(no.children, subGroup, 0);
    }
  }
}

// Substituir a original pela versão VS Code
export const renderizarArvoreOriginal = renderizarArvoreLegado;
export { renderizarArvoreVSCode as renderizarArvore };

export function aoClicarArvore(no) {
  if (no.type === 'folder') {
    no.open = !no.open;
    renderizarArvoreVSCode();
    return;
  }

  const ficheiroActual = fsGetFile(idFicheiroActivo);
  if (ficheiroActual) ficheiroActual.content = document.getElementById('code-input').value;

  idFicheiroActivo = no.id;
  document.getElementById('code-input').value = no.content || '';
  document.getElementById('active-file-label').textContent = no.name;
  actualizarNumeroLinhas();
  limparResultados();
  renderizarArvoreVSCode();
}

export function obterIdAlvoContexto() {
  return window.ctxTargetId;
}

function escaparHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}
