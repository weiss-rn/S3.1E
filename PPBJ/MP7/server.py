import os
import mimetypes
import secrets
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
PORT = 8081
ROOT = os.path.dirname(os.path.abspath(__file__))

DEMO_USER = "admin"
DEMO_PASS = "upscale123"
SESSIONS = {}


def parse_cookies(cookie_header):
    cookies = {}
    for part in cookie_header.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, value = part.split("=", 1)
        cookies[key.strip()] = value.strip()
    return cookies


def safe_join(root, path):
    path = path.lstrip("/").replace("/", os.sep).replace("\\", os.sep)
    full = os.path.abspath(os.path.join(root, path))
    root_abs = os.path.abspath(root)
    if os.path.commonpath([full, root_abs]) != root_abs:
        return None
    return full


class UpscaleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlsplit(self.path)
        path = parsed.path or "/"

        if path in ("/logout", "/logout/"):
            return self.handle_logout()
        if path in ("/login", "/login.html"):
            return self.serve_file("login.html")
        if path in ("/dashboard", "/dashboard.html", "/admin", "/admin.html"):
            if not self.is_authenticated():
                return self.redirect("/login")

        if path in ("/", ""):
            return self.serve_file("index.html")
        if path in ("/upscale", "/upscale/"):
            return self.serve_file("upscale.html")
        if path in ("/dashboard", "/dashboard.html"):
            return self.serve_file("dashboard.html")
        if path in ("/admin", "/admin.html"):
            return self.serve_file("admin.html")

        return self.serve_static(path)

    def do_POST(self):
        parsed = urllib.parse.urlsplit(self.path)
        if parsed.path not in ("/login", "/login.html"):
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        form = urllib.parse.parse_qs(body)
        username = (form.get("username", [""])[0] or "").strip()
        password = (form.get("password", [""])[0] or "").strip()

        if username == DEMO_USER and password == DEMO_PASS:
            token = secrets.token_urlsafe(16)
            SESSIONS[token] = username
            self.send_response(302)
            self.send_header("Location", "/dashboard")
            self.send_header("Set-Cookie", f"session={token}; Path=/; Max-Age=86400")
            self.end_headers()
            return

        self.redirect("/login?error=1")

    def handle_logout(self):
        cookies = parse_cookies(self.headers.get("Cookie", ""))
        token = cookies.get("session")
        if token and token in SESSIONS:
            del SESSIONS[token]

        self.send_response(302)
        self.send_header("Location", "/login")
        self.send_header("Set-Cookie", "session=; Path=/; Max-Age=0")
        self.end_headers()

    def is_authenticated(self):
        cookies = parse_cookies(self.headers.get("Cookie", ""))
        token = cookies.get("session", "")
        return token in SESSIONS

    def redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def serve_file(self, filename):
        full = safe_join(ROOT, filename)
        if not full or not os.path.exists(full) or os.path.isdir(full):
            self.send_error(404)
            return
        self.serve_full_path(full)

    def serve_static(self, path):
        full = safe_join(ROOT, path)
        if not full or not os.path.exists(full) or os.path.isdir(full):
            self.send_error(404)
            return
        self.serve_full_path(full)

    def serve_full_path(self, full):
        with open(full, "rb") as f:
            body = f.read()
        content_type = mimetypes.guess_type(full)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server():
    server = HTTPServer((HOST, PORT), UpscaleHandler)
    print(f"Upscale Lab server running at http://{HOST}:{PORT}")
    print("Open your LAN IP on the same port to access from other devices.")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
