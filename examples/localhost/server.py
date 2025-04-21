from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

def run_server(port=8000):
    web_dir = os.path.join(os.path.dirname(__file__), "")
    os.chdir(web_dir)

    # HTTP 서버 시작
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print(f"Serving HTTP on port {port}...")
    print(f"Open your browser and go to http://localhost:{port}/")

    httpd.serve_forever()

if __name__ == "__main__":
    run_server()