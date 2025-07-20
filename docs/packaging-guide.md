# Vue3项目打包部署完整指南

## 打包方案选择

### 方案对比

| 方案 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| **Electron** | 成熟稳定、跨平台、生态完善 | 包体积较大(100MB+) | 企业级应用、功能复杂 |
| **Tauri** | 体积小(10MB+)、性能高、安全 | 学习成本、生态较小 | 轻量级应用、性能敏感 |
| **PWA** | 无需安装、自动更新、跨平台 | 离线能力有限 | 简单应用、Web优先 |

### 推荐方案：Electron
基于本项目需求，选择Electron方案，理由：
- 成熟的跨平台支持
- 丰富的原生API
- 与现有Python后端集成简单
- 企业级应用稳定性

## Electron打包配置

### 1. 安装Electron依赖

```bash
# 安装Electron核心依赖
npm install -D electron electron-builder

# 安装Electron工具
npm install -D concurrently wait-on

# 安装跨平台工具
npm install -D cross-env
```

### 2. 项目结构调整

```
bridge-vue-frontend/
├── electron/                 # Electron主进程
│   ├── main.js              # 主进程入口
│   ├── preload.js           # 预加载脚本
│   └── menu.js              # 菜单配置
├── src/                     # Vue应用
├── dist/                    # 构建输出
├── build/                   # 构建配置
├── package.json             # 项目配置
└── electron-builder.json    # 打包配置
```

### 3. 主进程配置

**electron/main.js**:
```javascript
const { app, BrowserWindow, Menu, ipcMain, shell } = require('electron')
const path = require('path')
const isDev = process.env.NODE_ENV === 'development'

// 保持窗口对象的全局引用
let mainWindow

// 创建主窗口
function createWindow() {
  // 窗口配置
  const windowOptions = {
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'hiddenInset',
    show: false, // 先不显示，等加载完成后显示
    icon: path.join(__dirname, '../build/icon.png')
  }

  mainWindow = new BrowserWindow(windowOptions)

  // 加载应用
  if (isDev) {
    // 开发环境
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    // 生产环境
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  // 窗口事件
  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
    
    // 启动画面
    if (!isDev) {
      const splash = new BrowserWindow({
        width: 500,
        height: 300,
        frame: false,
        alwaysOnTop: true,
        transparent: true
      })
      
      splash.loadFile(path.join(__dirname, '../build/splash.html'))
      
      setTimeout(() => {
        splash.close()
      }, 2000)
    }
  })

  // 阻止新窗口打开
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })

  // 窗口关闭
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// 应用生命周期
app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// IPC通信
ipcMain.handle('get-app-version', () => {
  return app.getVersion()
})

ipcMain.handle('minimize-window', () => {
  mainWindow?.minimize()
})

ipcMain.handle('maximize-window', () => {
  if (mainWindow?.isMaximized()) {
    mainWindow.unmaximize()
  } else {
    mainWindow?.maximize()
  }
})

ipcMain.handle('close-window', () => {
  mainWindow?.close()
})
```

### 4. 预加载脚本

**electron/preload.js**:
```javascript
const { contextBridge, ipcRenderer } = require('electron')

// 安全的API暴露给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 应用信息
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  
  // 窗口控制
  minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
  maximizeWindow: () => ipcRenderer.invoke('maximize-window'),
  closeWindow: () => ipcRenderer.invoke('close-window'),
  
  // 文件操作
  openExternal: (url) => require('electron').shell.openExternal(url),
  
  // 系统信息
  platform: process.platform,
  
  // 通知
  showNotification: (title, body) => {
    new (require('electron').Notification)({ title, body }).show()
  }
})
```

### 5. 菜单配置

**electron/menu.js**:
```javascript
const { Menu } = require('electron')

const isMac = process.platform === 'darwin'

const template = [
  ...(isMac ? [{
    label: '桥梁工程评估',
    submenu: [
      { role: 'about' },
      { type: 'separator' },
      { role: 'services' },
      { type: 'separator' },
      { role: 'hide' },
      { role: 'hideothers' },
      { role: 'unhide' },
      { type: 'separator' },
      { role: 'quit' }
    ]
  }] : []),
  {
    label: '文件',
    submenu: [
      {
        label: '新建项目',
        accelerator: 'CmdOrCtrl+N',
        click: () => {
          // 发送事件到渲染进程
          require('./main').mainWindow.webContents.send('menu-new-project')
        }
      },
      {
        label: '打开项目',
        accelerator: 'CmdOrCtrl+O',
        click: () => {
          require('./main').mainWindow.webContents.send('menu-open-project')
        }
      },
      { type: 'separator' },
      {
        label: '导出Excel',
        accelerator: 'CmdOrCtrl+E',
        click: () => {
          require('./main').mainWindow.webContents.send('menu-export-excel')
        }
      },
      {
        label: '导出PDF',
        accelerator: 'CmdOrCtrl+P',
        click: () => {
          require('./main').mainWindow.webContents.send('menu-export-pdf')
        }
      },
      { type: 'separator' },
      isMac ? { role: 'close' } : { role: 'quit' }
    ]
  },
  {
    label: '编辑',
    submenu: [
      { role: 'undo' },
      { role: 'redo' },
      { type: 'separator' },
      { role: 'cut' },
      { role: 'copy' },
      { role: 'paste' },
      { role: 'selectall' }
    ]
  },
  {
    label: '视图',
    submenu: [
      { role: 'reload' },
      { role: 'forceReload' },
      { role: 'toggleDevTools' },
      { type: 'separator' },
      { role: 'resetZoom' },
      { role: 'zoomIn' },
      { role: 'zoomOut' },
      { type: 'separator' },
      { role: 'togglefullscreen' }
    ]
  },
  {
    label: '帮助',
    submenu: [
      {
        label: '用户手册',
        click: () => {
          require('electron').shell.openExternal('https://docs.example.com')
        }
      },
      {
        label: '关于',
        click: () => {
          require('./main').mainWindow.webContents.send('menu-about')
        }
      }
    ]
  }
]

module.exports = Menu.buildFromTemplate(template)
```

### 6. 打包配置文件

**electron-builder.json**:
```json
{
  "productName": "桥梁工程安全评估系统",
  "appId": "com.bridge.safety.assessment",
  "directories": {
    "output": "dist_electron"
  },
  "files": [
    "dist/**/*",
    "electron/**/*",
    "build/**/*",
    "node_modules/**/*",
    "package.json"
  ],
  "extraResources": [
    {
      "from": "build/extra",
      "to": "extra"
    }
  ],
  "win": {
    "icon": "build/icon.ico",
    "target": [
      {
        "target": "nsis",
        "arch": ["x64", "ia32"]
      },
      {
        "target": "portable",
        "arch": ["x64"]
      }
    ],
    "publisherName": "桥梁工程评估系统"
  },
  "mac": {
    "icon": "build/icon.icns",
    "target": [
      {
        "target": "dmg",
        "arch": ["x64", "arm64"]
      }
    ],
    "category": "public.app-category.productivity"
  },
  "linux": {
    "icon": "build/icon.png",
    "target": [
      {
        "target": "AppImage",
        "arch": ["x64"]
      },
      {
        "target": "deb",
        "arch": ["x64"]
      }
    ]
  },
  "nsis": {
    "oneClick": false,
    "allowToChangeInstallationDirectory": true,
    "createDesktopShortcut": true,
    "createStartMenuShortcut": true,
    "shortcutName": "桥梁工程安全评估",
    "include": "build/installer.nsh"
  },
  "dmg": {
    "title": "桥梁工程安全评估系统",
    "iconSize": 100,
    "contents": [
      {
        "x": 410,
        "y": 150,
        "type": "link",
        "path": "/Applications"
      },
      {
        "x": 130,
        "y": 150,
        "type": "file"
      }
    ]
  }
}
```

### 7. 更新package.json

```json
{
  "name": "bridge-safety-assessment",
  "version": "2.0.0",
  "description": "现代化桥梁工程安全评估系统",
  "main": "electron/main.js",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "electron:dev": "concurrently \"npm run dev\" \"wait-on http://localhost:5173 && electron .\"",
    "electron:build": "npm run build && electron-builder",
    "electron:pack": "npm run build && electron-builder --publish=never",
    "electron:pack:win": "npm run build && electron-builder --win",
    "electron:pack:mac": "npm run build && electron-builder --mac",
    "electron:pack:linux": "npm run build && electron-builder --linux"
  },
  "build": {
    "extends": "./electron-builder.json"
  }
}
```

## Tauri备选方案

### 1. 安装Tauri

```bash
# 安装Tauri CLI
npm install -D @tauri-apps/cli

# 初始化Tauri
npm run tauri init
```

### 2. Tauri配置

**src-tauri/tauri.conf.json**:
```json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "devPath": "http://localhost:5173",
    "distDir": "../dist"
  },
  "package": {
    "productName": "桥梁工程安全评估系统",
    "version": "2.0.0"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "shell": {
        "all": false,
        "open": true
      },
      "dialog": {
        "all": false,
        "open": true,
        "save": true
      },
      "fs": {
        "all": false,
        "writeFile": true,
        "readFile": true
      }
    },
    "bundle": {
      "active": true,
      "targets": "all",
      "identifier": "com.bridge.safety.assessment",
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ]
    },
    "security": {
      "csp": null
    },
    "windows": [
      {
        "fullscreen": false,
        "resizable": true,
        "title": "桥梁工程安全评估系统",
        "width": 1400,
        "height": 900,
        "minWidth": 1200,
        "minHeight": 700
      }
    ]
  }
}
```

## 构建和发布流程

### 1. 开发环境

```bash
# 启动开发环境
npm run electron:dev
# 或
npm run tauri dev
```

### 2. 生产构建

#### Electron构建
```bash
# 构建所有平台
npm run electron:build

# 仅Windows
npm run electron:pack:win

# 仅macOS
npm run electron:pack:mac

# 仅Linux
npm run electron:pack:linux
```

#### Tauri构建
```bash
# 构建所有平台
npm run tauri build

# 指定平台
npm run tauri build -- --target x86_64-pc-windows-msvc
```

### 3. 发布配置

#### GitHub Actions自动发布

**.github/workflows/release.yml**:
```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ${{ matrix.os }}
    
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build application
        run: npm run build
        
      - name: Build and release (Windows)
        if: matrix.os == 'windows-latest'
        run: npm run electron:pack:win
        
      - name: Build and release (macOS)
        if: matrix.os == 'macos-latest'
        run: npm run electron:pack:mac
        
      - name: Build and release (Linux)
        if: matrix.os == 'ubuntu-latest'
        run: npm run electron:pack:linux
        
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.os }}-build
          path: dist_electron/*
```

## 安装包优化

### 1. 体积优化

```javascript
// webpack.config.js优化
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },
}
```

### 2. 代码压缩

```bash
# 使用压缩工具
npm install -D terser-webpack-plugin
```

### 3. 图片优化

```bash
# 图片压缩
npm install -D imagemin-webpack-plugin
```

## 部署验证

### 1. 安装测试

```bash
# Windows
# 运行安装包并验证安装
# 检查桌面快捷方式
# 验证程序正常启动

# macOS
# 运行.dmg文件
# 拖拽到Applications
# 验证启动

# Linux
# 运行AppImage
# 或安装deb包
```

### 2. 功能测试清单

- [ ] 程序正常启动
- [ ] 窗口大小调整正常
- [ ] 菜单功能正常
- [ ] 计算功能正常
- [ ] 导出功能正常
- [ ] 多窗口支持
- [ ] 系统托盘功能
- [ ] 自动更新检查

### 3. 性能测试

```bash
# 内存使用检查
# CPU占用检查
# 启动时间测试
```

## 常见问题解决

### 1. 打包错误

```bash
# 清理缓存
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# 重新构建
npm run build
npm run electron:build
```

### 2. 图标问题

确保图标文件存在且格式正确：
- Windows: .ico格式，256x256
- macOS: .icns格式，多种尺寸
- Linux: .png格式，128x128

### 3. 权限问题

```bash
# macOS权限
sudo codesign --force --deep --sign - /Applications/桥梁工程安全评估系统.app
```

### 4. 防病毒软件误报

- 使用代码签名证书
- 提交到杀毒软件白名单
- 使用知名证书颁发机构