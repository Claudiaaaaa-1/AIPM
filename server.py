#!/usr/bin/env python3
"""
AI 学习内化系统 - 轻量本地后端
职责：静态资源服务 + 课程数据读写（内容修正用，无需模型 API）
未来二期在 此文件 基础上增加 /api/generate 接口即可接入模型（Kimi / 司内混元）。

启动：python3 server.py  （默认 127.0.0.1:8777）
"""
import json
import os
import re
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
COURSES = os.path.join(CONTENT, "courses")
PORT = int(os.environ.get("PORT", "8777"))

# 仅允许写这些白名单文件，避免路径穿越
WRITABLE = {
    "index": os.path.join(CONTENT, "index.json"),
    "topics": os.path.join(CONTENT, "topics.json"),
    "user-takes": os.path.join(CONTENT, "user-takes.json"),
}


def safe_course_path(cid: str) -> str | None:
    """校验课程 ID，防止路径穿越。只允许字母数字中文连字符下划线。"""
    if not cid or not re.fullmatch(r"[\w\u4e00-\u9fff\-]+", cid):
        return None
    return os.path.join(COURSES, cid + ".json")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    # ---- helpers ----
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n) if n else b""
        return json.loads(raw.decode("utf-8")) if raw else {}

    def _path_id(self):
        # /api/course/<id>  （URL 解码中文 ID）
        m = re.fullmatch(r"/api/course/([^/]+)", self.path)
        return urllib.parse.unquote(m.group(1)) if m else None

    # ---- GET: 供前端确认后端在线 ----
    def do_GET(self):
        if self.path == "/api/health":
            return self._json(200, {"ok": True, "mode": "local-backend"})
        return super().do_GET()

    # ---- POST: 写课程 / 索引 / 主题 ----
    def do_POST(self):
        try:
            data = self._read_body()
        except Exception as e:
            return self._json(400, {"ok": False, "error": f"invalid json: {e}"})

        if self.path.startswith("/api/course/"):
            cid = self._path_id()
            p = safe_course_path(cid) if cid else None
            if not p:
                return self._json(400, {"ok": False, "error": "invalid course id"})
            try:
                tmp = p + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                os.replace(tmp, p)  # 原子写，避免写一半损坏
                return self._json(200, {"ok": True, "saved": cid})
            except Exception as e:
                return self._json(500, {"ok": False, "error": str(e)})

        if self.path in ("/api/index", "/api/topics", "/api/user-takes"):
            p = WRITABLE[self.path.split("/")[-1]]
            try:
                tmp = p + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                os.replace(tmp, p)
                return self._json(200, {"ok": True, "saved": self.path})
            except Exception as e:
                return self._json(500, {"ok": False, "error": str(e)})

        return self._json(404, {"ok": False, "error": "unknown endpoint"})

    def log_message(self, fmt, *args):
        # 精简日志
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    os.makedirs(COURSES, exist_ok=True)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"AI 学习内化系统后端运行中： http://127.0.0.1:{PORT}")
    print(f"数据目录：{CONTENT}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
