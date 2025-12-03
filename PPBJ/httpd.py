import socket
import os
from datetime import datetime
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

def log_request(client_address, request_line, status_code):
    """Log incoming requests with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {client_address[0]}:{client_address[1]} - {request_line.strip()} - Status: {status_code}")

def route_request(request):
    """Route requests to appropriate files"""
    lines = request.split('\r\n')
    request_line = lines[0]
    method, path, protocol = request_line.split()
    
    # Clean path
    if path == '/':
        path = 'index.html'
    else:
        path = path.lstrip('/')
    
    return path

def get_content_type(filename):
    """Determine content type based on file extension"""
    ext = os.path.splitext(filename)[1].lower()
    content_types = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.txt': 'text/plain',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.gif': 'image/gif'
    }
    return content_types.get(ext, 'application/octet-stream')

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)  # ✨ NEW: Queue up to 5 connections
print('🚀 HTTP Server Started')
print(f'📍 Listening on http://{SERVER_HOST}:{SERVER_PORT}')
print('⏹️  Press Ctrl+C to exit\n')

request_count = 0  # ✨ NEW: Track total requests

try:
    while True:	
        try:
            client_connection, client_address = server_socket.accept()
            request_count += 1
            
            # Request handling with error handling
            try:
                request = client_connection.recv(1024).decode()
                
                if request:
                    # ✨ NEW: Route the request
                    filename = route_request(request)
                    
                    # ✨ NEW: Check if file exists
                    if os.path.exists(filename):
                        try:
                            with open(filename, 'rb') as file:
                                body = file.read()
                            
                            response_line = 'HTTP/1.1 200 OK'.encode()
                            content_type = get_content_type(filename)
                            entity_header = f'Content-Type: {content_type}'.encode()
                            enter = '\r\n'.encode()
                            
                            response = b''.join([response_line, enter, entity_header, enter, enter, body])
                            client_connection.send(response)
                            
                            # ✨ NEW: Log successful request
                            log_request(client_address, request.split('\r\n')[0], '200 OK')
                        
                        except Exception as e:
                            # ✨ NEW: Error handling for file read
                            error_response = b'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n<h1>500 - Server Error</h1>'
                            client_connection.send(error_response)
                            log_request(client_address, request.split('\r\n')[0], '500 Error')
                    else:
                        # ✨ NEW: 404 Not Found response
                        not_found_html = b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 - File Not Found</h1><p>The requested file was not found on this server.</p>'
                        client_connection.send(not_found_html)
                        log_request(client_address, request.split('\r\n')[0], '404 Not Found')
            
            except Exception as e:
                print(f"❌ Error processing request: {e}")
            
            finally:
                client_connection.close()
        
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"❌ Connection error: {e}")
            continue

except KeyboardInterrupt:
    print(f"\n\n📊 Server Statistics:")
    print(f"   Total requests handled: {request_count}")
    print(f"⛔ Server shutting down...")
    server_socket.close()
    sys.exit(0)
