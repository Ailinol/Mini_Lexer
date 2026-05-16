'use strict';

import { fsFind, fsDelete, fsCreateFile, fsCreateFolder, fsRename, fsAllFiles } from './file_system.js';
import { abrirModal } from './modal.js';
import { renderizarArvore, definirFicheiroActivo } from './sideBar.js';
import { actualizarNumeroLinhas, } from './editor.js';
import { limparResultados } from './ui.js';

export function obterIdAlvoContexto() { return window.ctxTargetId; }

/* ══════════════════════════════════════
   MENU DE CONTEXTO
   ══════════════════════════════════════ */

const menu = document.getElementById('ctx-menu');

export function mostrarMenuContexto(evento, id) {
  evento.preventDefault();
  evento.stopPropagation();
  window.ctxTargetId = id;

  const menuElement = document.getElementById('ctx-menu');
  menuElement.style.left = evento.clientX + 'px';
  menuElement.style.top  = evento.clientY + 'px';
  menuElement.classList.add('open');

  const resultado = fsFind(id);
  const ehPasta = resultado?.node?.type === 'folder';
  document.getElementById('ctx-new-file').style.display   = ehPasta ? '' : 'none';
  document.getElementById('ctx-new-folder').style.display = ehPasta ? '' : 'none';
  document.getElementById('ctx-sep1').style.display       = ehPasta ? '' : 'none';
}

export function iniciarMenuContexto() {
  document.addEventListener('click', () => menu.classList.remove('open'));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') menu.classList.remove('open');
  });
}

/* ══════════════════════════════════════
   ACÇÕES DO MENU
   ══════════════════════════════════════ */

export function renomear() {
  menu.classList.remove('open');
  const id = obterIdAlvoContexto();
  const resultado = fsFind(id);
  if (!resultado) return;

  abrirModal(`Renomear "${resultado.node.name}"`, resultado.node.name, novoNome => {
    fsRename(id, novoNome);
    renderizarArvore();
  });
}

export function novoFicheiro(targetId = null) {
  menu.classList.remove('open');
  const id = targetId || obterIdAlvoContexto();
  if (!id) return;

  abrirModal('Novo ficheiro', 'novo.pas', nome => {
    if (!nome.trim()) return;
    const novoNo = fsCreateFile(id, nome);
    if (novoNo) {
      renderizarArvore();
    }
  });
}

export function criarNovaPasta(targetId = null) {
  menu.classList.remove('open');
  const id = targetId || obterIdAlvoContexto();
  if (!id) return;

  abrirModal('Nova pasta', 'novaPasta', nome => {
    if (!nome.trim()) return;
    const novoNo = fsCreateFolder(id, nome);
    if (novoNo) {
      renderizarArvore();
    }
  });
}

export function eliminar(idFicheiroActivo) {
  menu.classList.remove('open');
  const id = obterIdAlvoContexto();
  const resultado = fsFind(id);
  if (!resultado) return;
  if (!confirm(`Eliminar "${resultado.node.name}"?`)) return;

  fsDelete(id);

  if (idFicheiroActivo === id) {
    const ficheiros = fsAllFiles();
    const proximo = ficheiros[0];
    if (proximo) {
      definirFicheiroActivo(proximo.id);
      document.getElementById('code-input').value = proximo.content || '';
      document.getElementById('active-file-label').textContent = proximo.name;
    } else {
      document.getElementById('code-input').value = '';
      document.getElementById('active-file-label').textContent = 'sem ficheiro';
    }
    actualizarNumeroLinhas();
    limparResultados();
  }

  renderizarArvore();
}
