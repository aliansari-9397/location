from http.server import HTTPServer, BaseHTTPRequestHandler
import json

PAGE = b'''<!DOCTYPE html>
<html>
<body>
<h2>Location Sharing</h2>
<button onclick="share()">Share My Location</button>
<p id="result"></p>
<script>
function share() {
 navigator.geolocation.getCurrentPosition(async p => {
  const data = {
   latitude: p.coords.latitude,
   longitude: p.coords.longitude
  };
  document.getElementById('result').textContent = 'Location sent';
  await fetch('/location', {
   method: 'POST',
   headers: {'Content-Type': 'application/json'},
   body: JSON.stringify(data)
  });
 }, e => alert(e.message));
}
</script>
</body>
</html>'''

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(PAGE)

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))
        print("Latitude:", data["latitude"], flush=True)
        print("Longitude:", data["longitude"], flush=True)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Received")

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
