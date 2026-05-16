
'use strict';

export const FS = {
  tree: [
    {
      id: 'root', type: 'folder', name: 'MeuProjeto', open: true,
      children: [
        {
          id: 'src', type: 'folder', name: 'src', open: true,
          children: [
            {
              id: 'f1', type: 'file', name: 'main.pas',
              content: [
                'program OlaMundo;',
                'var',
                '  nome : string;',
                '  idade : integer;',
                'begin',
                "  nome := 'João';",
                '  idade := 20;',
                "  writeln('Olá, ', nome);",
                "  writeln('Idade: ', idade);",
                'end.',
              ].join('\n'),
            },
            {
              id: 'f2', type: 'file', name: 'ciclo.pas',
              content: [
                'program CicloExemplo;',
                'var',
                '  i : integer;',
                '  soma : real;',
                'begin',
                '  soma := 0.0;',
                '  for i := 1 to 10 do',
                '  begin',
                '    soma := soma + i;',
                '    if soma > 20 then',
                "      writeln('Soma ultrapassou 20!')",
                '    else',
                '      writeln(soma);',
                '  end;',
                '  { resultado final }',
                "  writeln('Total: ', soma);",
                'end.',
              ].join('\n'),
            },
            {
              id: 'f3', type: 'file', name: 'erros.pas',
              content: [
                'program ComErros;',
                'var',
                '  x : integer;',
                '  y : real;',
                'begin',
                '  x := 10;',
                '  y := 3.14@;       { @ é símbolo inválido }',
                '  if x > 5 then',
                "    writeln('maior');",
                '  { comentário não fechado',
                '  x := x + 1;',
                "  y := 'string não fechada;",
                'end.',
              ].join('\n'),
            },
          ],
        },
        {
          id: 'utils', type: 'folder', name: 'utils', open: false,
          children: [
            {
              id: 'f4', type: 'file', name: 'helpers.pas',
              content: '{ Utilitários }\nprogram Helpers;\nbegin\nend.',
            },
          ],
        },
        {
          id: 'f5', type: 'file', name: 'README.md',
          content: '{ Projecto mini-Pascal - LPC 2026 }',
        },
      ],
    },
  ],

  activeId: 'f1',
  _nextId: 100,

  /** Gera um ID único para novos nós */
  genId() {
    return 'f' + (++this._nextId);
  },

  /** Reinicia o projecto com um novo nome */
  newProject(name) {
    this.tree = [
      {
        id: 'root', type: 'folder', name: name.trim() || 'NovoProjecto', open: true,
        children: []
      }
    ];
    this.activeId = 'root';
    return this.tree;
  }
};

export function fsFind(id, nodes = FS.tree) {
  for (const n of nodes) {
    if (n.id === id) return { node: n, parent: null, siblings: nodes };
    if (n.children) {
      const r = _fsFindIn(id, n);
      if (r) return r;
    }
  }
  return null;
}

function _fsFindIn(id, parent) {
  for (const n of parent.children || []) {
    if (n.id === id) return { node: n, parent, siblings: parent.children };
    if (n.children) {
      const r = _fsFindIn(id, n);
      if (r) return r;
    }
  }
  return null;
}

export function fsGetFile(id) {
  const r = fsFind(id);
  return r?.node?.type === 'file' ? r.node : null;
}

/**
 * Devolve todos os ficheiros da árvore em ordem de profundidade.
 */
export function fsAllFiles(nodes = FS.tree) {
  const out = [];
  for (const n of nodes) {
    if (n.type === 'file') out.push(n);
    if (n.children) out.push(...fsAllFiles(n.children));
  }
  return out;
}

export function fsCreateFile(folderId, name) {
  const r = fsFind(folderId);
  if (!r || r.node.type !== 'folder') return null;
  const node = { id: FS.genId(), type: 'file', name: name.trim(), content: '' };
  r.node.children = r.node.children || [];
  r.node.children.push(node);
  r.node.open = true;
  return node;
}

export function fsCreateFolder(folderId, name) {
  const r = fsFind(folderId);
  if (!r || r.node.type !== 'folder') return null;
  const node = { id: FS.genId(), type: 'folder', name: name.trim(), open: false, children: [] };
  r.node.children = r.node.children || [];
  r.node.children.push(node);
  r.node.open = true;
  return node;
}

export function fsRename(id, newName) {
  const r = fsFind(id);
  if (!r || !newName.trim()) return false;
  r.node.name = newName.trim();
  return true;
}

export function fsDelete(id) {
  const r = fsFind(id);
  if (!r) return null;
  const idx = r.siblings.indexOf(r.node);
  if (idx !== -1) r.siblings.splice(idx, 1);
  return r.node;
}