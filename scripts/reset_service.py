#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP 服务：为导航页提供 ipynb 重置 API"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

class ResetHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/reset':
            self.send_error(404)
            return
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        unit = body.get('unit', '')
        if not unit:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': '缺少 unit 参数'}, ensure_ascii=False).encode())
            return
        path = f"人工智能训练师三级上网素材/{unit}/{unit}.ipynb"
        if not os.path.exists(path):
            self.send_response(404)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': f'{unit} 文件不存在'}, ensure_ascii=False).encode())
            return
        try:
            # 恢复到 enriched 但未填空的版本（第二个 commit，带任务要求但未做题）
            result = subprocess.run(
                ['git', 'log', '--reverse', '--format=%H', '--follow', '--', path],
                check=True, capture_output=True, text=True
            )
            commits = result.stdout.strip().split('\n')
            # 如果有多个 commit，用第二个（enriched 版本）；否则用第一个
            target_commit = commits[1] if len(commits) > 1 else commits[0]
            subprocess.run(['git', 'restore', '--source', target_commit, path], check=True, capture_output=True, text=True)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': f'{unit} 已重置为原始填空状态'}, ensure_ascii=False).encode())
        except subprocess.CalledProcessError as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': e.stderr.strip()}, ensure_ascii=False).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")

if __name__ == '__main__':
    PORT = 8765
    server = HTTPServer(('localhost', PORT), ResetHandler)
    print(f"✅ 重置服务已启动: http://localhost:{PORT}")
    print(f"   工作目录: {ROOT}")
    print("   按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
