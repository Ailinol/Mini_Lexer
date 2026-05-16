'use strict';

console.log('[Main] Carregando módulos...');

import { FS, fsFind, fsGetFile, fsCreateFile } from './file_system.js';
import { iniciarEditor, actualizarNumeroLinhas, sincronizarScroll, tratarTab } from './editor.js';
import { definirEstado, limparResultados, limparTudo, actualizarEstatisticas } from './ui.js';
import { tokenizar, renderizarTokens, renderizarErros } from './lexer.js';
import { renderizarArvore, aoClicarArvore, obterFicheiroActivo } from './sideBar.js';
import { iniciarMenuContexto, renomear, novoFicheiro, criarNovaPasta, eliminar, mostrarMenuContexto, obterIdAlvoContexto } from './contextMenu.js';
import { abrirModal, confirmarModal, cancelarModal } from './modal.js';
import { iniciarAssistente, enviarPergunta, definirUltimosTokens, definirUltimosErros } from './ai.js';

async function novoProjecto() {
  abrirModal('Nome do Novo Projecto', 'MeuNovoProjecto', nome => {
    if (!nome.trim()) return;
    FS.newProject(nome);
    limparTudo();
    renderizarArvore();
    definirEstado(`Projecto "${nome}" criado`);
  });
}

async function abrirProjecto(ficheiros) {
  if (!ficheiros || ficheiros.length === 0) return;

  const pathParts = ficheiros[0].webkitRelativePath.split('/');
  const rootName = pathParts[0];

  FS.newProject(rootName);
  limparResultados();

  let primeiroFicheiroCarregado = null;

  for (const f of ficheiros) {
    if (f.name.startsWith('.') || f.webkitRelativePath.includes('/.')) continue;

    const reader = new FileReader();
    reader.onload = (e) => {
      const conteudo = e.target.result;
      const novoNo = fsCreateFile('root', f.name);
      if (novoNo) {
        novoNo.content = conteudo;
        if (!primeiroFicheiroCarregado) {
          primeiroFicheiroCarregado = novoNo;
          document.getElementById('code-input').value = conteudo;
          document.getElementById('active-file-label').textContent = f.name;
          window.FS.activeId = novoNo.id;
          actualizarNumeroLinhas();
        }
        renderizarArvore();
      }
    };
    reader.readAsText(f);
  }

  definirEstado(`Projecto "${rootName}" carregado`);
}

async function analisar() {
  console.log('Botão Analisar clicado!');
  const codigo = document.getElementById('code-input').value;

  const idActivo = obterFicheiroActivo();
  const ficheiroActual = fsGetFile(idActivo);
  if (ficheiroActual) ficheiroActual.content = codigo;

  if (!codigo.trim()) {
    definirEstado('Nenhum código para analisar', 'aviso');
    return;
  }

  definirEstado('A analisar...', 'aviso');
  try {
    const { tokens, errors } = await tokenizar(codigo);

    if (!tokens) { definirEstado('Resposta inválida do servidor', 'err'); return; }
    const erros = Array.isArray(errors) ? errors : [{ msg: 'Formato de erro inesperado', lexeme: '', linha: 0, coluna: 0 }];

    definirUltimosTokens(tokens);
    definirUltimosErros(erros);

    renderizarTokens(tokens);
    renderizarErros(erros);
    actualizarEstatisticas(tokens, erros, codigo);

    if (erros.length > 0) {
      const abaErros = document.querySelector('.tab[onclick*="errors"]');
      if (abaErros) trocarAba('errors', abaErros);
    }

    definirEstado(
      erros.length ? `Análise completa — ${erros.length} erro(s)` : 'Análise completa — sem erros',
      erros.length ? 'err' : 'ok'
    );

    renderizarArvore();
  } catch (err) {
    console.error('Erro durante a análise:', err);
    definirEstado('Erro na análise. Verifique o console.', 'err');
  }
}


function carregarAmostra(chave) {
  const AMOSTRAS = {
    basic: `program OlaMundo;\nvar\n  nome : string;\n  idade : integer;\nbegin\n  nome := 'João';\n  idade := 20;\n  writeln('Olá, ', nome);\nend.`,
    loop: `program CicloExemplo;\nvar\n  i : integer;\n  soma : real;\nbegin\n  soma := 0.0;\n  for i := 1 to 10 do\n  begin\n    soma := soma + i;\n  end;\n  writeln('Total: ', soma);\nend.`,
    errors: `program ComErros;\nvar\n  x : integer;\nbegin\n  x := 3.14@;\n  { comentário não fechado\nend.`,
  };
  if (!chave) return;
  document.getElementById('code-input').value = AMOSTRAS[chave] || '';
  actualizarNumeroLinhas();
  analisar();
  document.querySelector('.sample-select').value = '';
}

function trocarAba(id, elemento) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  elemento.classList.add('active');
  const alvo = document.getElementById('tab-' + id);
  if (alvo) alvo.classList.add('active');
}

window.FS = FS;
window.analisar = analisar;
window.carregarAmostra = carregarAmostra;
window.loadSample = carregarAmostra;
window.novoFicheiro = (id = 'root') => novoFicheiro(id);
window.newFile = (id = 'root') => novoFicheiro(id);
window.trocarAba = trocarAba;
window.switchTab = trocarAba;
window.confirmarModal = confirmarModal;
window.confirmModal = confirmarModal;
window.cancelarModal = cancelarModal;
window.cancelModal = cancelarModal;
window.askAI = enviarPergunta;
window.enviarPergunta = enviarPergunta;
window.limparTudo = () => limparTudo(obterFicheiroActivo());
window.updateLineNumbers = actualizarNumeroLinhas;
window.syncScroll = sincronizarScroll;
window.handleTab = tratarTab;
window.renderTree = renderizarArvore;
window.newFolder = (id = 'root') => criarNovaPasta(id);
window.ctxNewFolder = (id = obterIdAlvoContexto()) => criarNovaPasta(id);
window.novoProjecto = novoProjecto;
window.abrirProjecto = abrirProjecto;


window.debugApp = function () {
  console.log('Sistema de Debug activo!');
  alert('O JavaScript está a funcionar!');
};

(function iniciar() {
  console.log('[Main] Iniciando aplicação...');
  try {
    const primeirFicheiro = fsGetFile(FS.activeId);
    if (primeirFicheiro) {
      document.getElementById('code-input').value = primeirFicheiro.content || '';
      document.getElementById('active-file-label').textContent = primeirFicheiro.name;
    }

    iniciarEditor();
    iniciarMenuContexto();
    iniciarAssistente();
    renderizarArvore();
    actualizarNumeroLinhas();
    definirEstado('Pronto');
    console.log('[Main] Aplicação iniciada com sucesso!');
  } catch (erro) {
    console.error('[Main] Erro na inicialização:', erro);
  }
})();
