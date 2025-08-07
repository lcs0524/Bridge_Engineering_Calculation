import threading
import time
import socket
from flask import Flask, send_from_directory, jsonify, request
import webview
import os
import sys

# 将打包后的资源路径添加到系统路径中
def resource_path(relative_path):
    """ 获取资源的绝对路径，无论是开发环境还是打包后 """
    try:
        # PyInstaller 创建一个临时文件夹，并把路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Vue应用的静态文件目录
# 在打包后，这个目录是 'bridge-safety-vue/dist'
STATIC_DIR = resource_path('bridge-safety-vue/dist')

# 初始化Flask应用
app = Flask(__name__, static_folder=STATIC_DIR)

# --- API Endpoints ---
# 这里我们会添加所有计算模块的API接口

# 示例：路基顶管计算API
@app.route('/api/calculate/roadbed', methods=['POST'])
def calculate_roadbed():
    data = request.json
    # 在这里调用您的核心计算逻辑
    # from calculation.roadbed_calculator import perform_calculation
    # results = perform_calculation(data)
    # 暂时返回一个模拟结果
    results = {'status': 'success', 'message': '计算完成', 'data': data}
    return jsonify(results)

# 示例：塔基稳定性计算API
@app.route('/api/calculate/tower', methods=['POST'])
def calculate_tower():
    data = request.json
    # 在这里调用您的核心计算逻辑
    # from calculation.tower_calculator import perform_calculation
    # results = perform_calculation(data)
    results = {'status': 'success', 'message': '计算完成', 'data': data}
    return jsonify(results)

# --- Serving Vue App ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# --- Main Application Logic ---
def find_free_port():
    """ 查找一个空闲的端口 """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_flask(port):
    """ 在指定端口运行Flask应用 """
    # 使用 waitress 作为生产环境的 WSGI 服务器
    from waitress import serve
    serve(app, host='127.0.0.1', port=port)

if __name__ == '__main__':
    port = find_free_port()
    
    # 在后台线程中启动Flask服务器
    flask_thread = threading.Thread(target=run_flask, args=(port,), daemon=True)
    flask_thread.start()
    
    time.sleep(1) # 等待服务器启动

    # 创建并启动webview窗口
    webview.create_window(
        '桥梁跨越工程安全性评估软件',
        f'http://127.0.0.1:{port}',
        width=1280,
        height=800,
        resizable=True,
        min_size=(1000, 700)
    )
    webview.start(debug=False)

    sys.exit() 