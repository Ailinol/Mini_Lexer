const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
    title: "Mini-Pascal Lexer IDE"
  });

  // Aguarda o servidor Python estar pronto e carrega a URL
  mainWindow.loadURL('http://127.0.0.1:8001');

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

function startPythonServer() {
  const isDev = !app.isPackaged;
  let pythonScript;
  let command;
  let args;

  if (isDev) {
    command = 'python';
    pythonScript = path.join(__dirname, 'src', 'server.py');
    args = [pythonScript];
  } else {
    // Em produção, usa o executável dentro da pasta dist ou onde for empacotado
    command = path.join(__dirname, 'dist', 'server.exe');
    args = [];
  }
  
  const env = { ...process.env, ELECTRON_RUNNING: 'true' };

  console.log(`Starting backend: ${command} ${args.join(' ')}`);
  pythonProcess = spawn(command, args, { env });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`);
  });
}

app.on('ready', () => {
  startPythonServer();
  // Dá um tempo para o servidor iniciar antes de abrir a janela
  setTimeout(createWindow, 2000);
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});
