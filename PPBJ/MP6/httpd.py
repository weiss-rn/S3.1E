import socket
import os
import mimetypes
import urllib.parse
from template import Template

def tcp_server():
	SERVER_HOST = '127.0.0.1'
	SERVER_PORT = 8080
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((SERVER_HOST, SERVER_PORT))
	server_socket.listen()
	print('Listen on http://127.0.0.1:8080')
	while True:
		client_connection, client_address = server_socket.accept()
		request = client_connection.recv(8192).decode(errors="replace")
		print('Request : %s'%(request))
		if(request and request.strip()):
			response = handle_request(request)
			client_connection.sendall(response)
		client_connection.close()
	server_socket.close()

def handle_request(request):
	if "\r\n\r\n" in request:
		head, body = request.split("\r\n\r\n", 1)
	else:
		head, body = request, ""

	request_lines = head.split("\r\n")
	request_line = request_lines[0]
	words = request_line.split()
	if len(words) < 3:
		return response_text("HTTP/1.1", 400, "Bad Request", b"Bad Request")

	method, raw_target, http_version = words[0], words[1], words[2]
	headers = parse_headers(request_lines[1:])
	cookies = parse_cookies(headers.get("cookie", ""))

	parsed = urllib.parse.urlsplit(raw_target)
	path = parsed.path or "/"
	query = urllib.parse.parse_qs(parsed.query)

	if method == "GET":
		return handle_get(path, http_version, query, headers, cookies)
	if method == "POST":
		form = urllib.parse.parse_qs(body)
		return handle_post(path, http_version, form, headers, cookies)

	return response_text(http_version, 405, "Method Not Allowed", b"Method Not Allowed")

def parse_headers(lines):
	headers = {}
	for line in lines:
		if not line or ":" not in line:
			continue
		k, v = line.split(":", 1)
		headers[k.strip().lower()] = v.strip()
	return headers

def parse_cookies(cookie_header):
	cookies = {}
	for part in cookie_header.split(";"):
		part = part.strip()
		if not part or "=" not in part:
			continue
		k, v = part.split("=", 1)
		cookies[k.strip()] = v.strip()
	return cookies

def response_text(http_version, status_code, reason, body, headers=None):
	if headers is None:
		headers = {}
	status_line = f"{http_version} {status_code} {reason}\r\n".encode()
	base_headers = {
		"Content-Type": "text/html; charset=utf-8",
		"Content-Length": str(len(body)),
		"Connection": "close",
	}
	base_headers.update(headers)
	header_bytes = b"".join([f"{k}: {v}\r\n".encode() for k, v in base_headers.items()])
	return b"".join([status_line, header_bytes, b"\r\n", body])

def response_redirect(http_version, location, headers=None):
	if headers is None:
		headers = {}
	headers = {**headers, "Location": location}
	return response_text(http_version, 302, "Found", b"", headers=headers)

def handle_get(path, http_version, query, headers, cookies):
	if path == "/":
		return serve_file("login.html", http_version, cookies=cookies)
	if path == "/home":
		return serve_template("home.html", http_version, cookies=cookies)
	if path == "/admin":
		return serve_template("admin.html", http_version, cookies=cookies, admin_gate=True)
	if path == "/logout":
		return response_redirect(http_version, "/", headers={"Set-Cookie": "username=; Max-Age=0; Path=/"})
	return serve_path(path, http_version, cookies=cookies)

def handle_post(path, http_version, form, headers, cookies):
	if path == "/login":
		username = (form.get("username", [""])[0] or "").strip()
		if not username:
			return response_redirect(http_version, "/")
		username = urllib.parse.quote(username, safe="")
		set_cookie = f"username={username}; Path=/; Max-Age=86400"
		return response_redirect(http_version, "/home", headers={"Set-Cookie": set_cookie})

	return response_text(http_version, 404, "Not Found", b"<h1>404 Not Found</h1>")

def mp6_root():
	return os.path.dirname(os.path.abspath(__file__))

def htdocs_path(filename):
	return os.path.join(mp6_root(), "htdocs", filename)

def safe_join(root, path):
	path = path.lstrip("/").replace("/", os.sep).replace("\\", os.sep)
	full = os.path.abspath(os.path.join(root, path))
	root_abs = os.path.abspath(root)
	if os.path.commonpath([full, root_abs]) != root_abs:
		return None
	return full

def serve_path(path, http_version, cookies=None):
	full = safe_join(os.path.join(mp6_root(), "htdocs"), path)
	if not full or not os.path.exists(full) or os.path.isdir(full):
		return response_text(http_version, 404, "Not Found", b"<h1>404 Not Found</h1>")

	if full.lower().endswith((".html", ".htm")):
		filename = os.path.basename(full)
		if filename in ("home.html", "admin.html"):
			return serve_template(filename, http_version, cookies=cookies, admin_gate=(filename == "admin.html"))

	with open(full, "rb") as f:
		body = f.read()
	content_type = mimetypes.guess_type(full)[0] or "application/octet-stream"
	return response_text(http_version, 200, "OK", body, headers={"Content-Type": content_type})

def serve_file(filename, http_version, cookies=None):
	full = htdocs_path(filename)
	if not os.path.exists(full) or os.path.isdir(full):
		return response_text(http_version, 404, "Not Found", b"<h1>404 Not Found</h1>")
	with open(full, "rb") as f:
		body = f.read()
	content_type = mimetypes.guess_type(full)[0] or "application/octet-stream"
	return response_text(http_version, 200, "OK", body, headers={"Content-Type": content_type})

def serve_template(filename, http_version, cookies=None, admin_gate=False):
	cookies = cookies or {}
	raw_username = cookies.get("username", "")
	user_name = urllib.parse.unquote(raw_username) if raw_username else "Guest"
	is_admin = user_name.lower() == "admin"

	if admin_gate and not is_admin:
		return response_text(http_version, 403, "Forbidden", b"<h1>403 Forbidden</h1><p>Login as <b>admin</b> to access Admin Panel.</p>")

	full = htdocs_path(filename)
	if not os.path.exists(full) or os.path.isdir(full):
		return response_text(http_version, 404, "Not Found", b"<h1>404 Not Found</h1>")
	with open(full, "r", encoding="utf-8") as f:
		html = f.read()

	context = {
		"user_name": user_name,
		"admin_status": "ADMIN" if is_admin else "USER",
	}
	t = Template(html)
	body = t.render(context).encode("utf-8")
	return response_text(http_version, 200, "OK", body, headers={"Content-Type": "text/html; charset=utf-8"})

if __name__ == "__main__":
	tcp_server()
