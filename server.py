from http.server import HTTPServer, BaseHTTPRequestHandler
import json

PAGE = b'''<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 24px;
  font-family: Arial, sans-serif;
  background: #ffffff;
}
h1 {
  font-size: clamp(38px, 10vw, 54px);
  font-weight: 800;
  color: #111111;
  text-align: center;
  letter-spacing: -1.5px;
  margin: 0 0 42px;
}
button {
  width: 88vw;
  max-width: 400px;
  min-height: 76px;
  border: none;
  border-radius: 18px;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: #ffffff;
  font-size: clamp(20px, 5vw, 25px);
  font-weight: 700;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.28);
  cursor: pointer;
}
button:active { transform: scale(0.98); }
#result { color: #111111; font-size: 16px; }
</style>
</head>
<body>
<h1>Phone Update</h1>
<button onclick="share()">Share My Location</button>
<p id="result"></p>
<script>
function share() {
 navigator.geolocation.getCurrentPosition(async p => {
  const data = {
   latitude: p.coords.latitude,
   longitude: p.coords.longitude
  };
  const result = document.getElementById('result');
  try {
   const response = await fetch('/location', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
   });
   if (!response.ok) throw new Error('Server error');
   result.textContent = 'Location sent';
  } catch (e) {
   result.textContent = 'Could not send location';
  }
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

import os
HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8000))), Handler).serve_forever()
