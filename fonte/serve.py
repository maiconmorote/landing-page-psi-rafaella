"""Servidor local simples para pre-visualizar o site."""
import functools, http.server, os, socketserver
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "publicar")
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8777), handler) as httpd:
    print("servindo", ROOT, "em http://127.0.0.1:8777")
    httpd.serve_forever()
