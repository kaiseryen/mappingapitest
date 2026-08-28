import http.server
import socketserver
import webbrowser

def openmap():
    PORT = 8000

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as server:
        url = f"http://localhost:{PORT}"

        print(f"Map running at {url}")
        webbrowser.open(url)

        server.serve_forever()