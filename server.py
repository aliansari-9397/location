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
  justify-content: center;
  align-items: center;
  padding: 24px;
  font-family: Arial, sans-serif;
  background:
    radial-gradient(circle at 15% 20%, #dbeafe 0, transparent 35%),
    radial-gradient(circle at 85% 80%, #bfdbfe 0, transparent 38%),
    linear-gradient(135deg, #ffffff, #eff6ff);
  overflow: hidden;
}
.decoration {
  position: fixed;
  border-radius: 50%;
  background: rgba(59,130,246,0.09);
  pointer-events: none;
}
.one { width: 230px; height: 230px; top: -80px; right: -65px; }
.two { width: 180px; height: 180px; bottom: -55px; left: -55px; }
.content {
  width: 100%;
  max-width: 460px;
  padding: 55px 22px;
  text-align: center;
  background: rgba(255,255,255,0.78);
  border: 1px solid rgba(255,255,255,0.95);
  border-radius: 28px;
  box-shadow: 0 18px 55px rgba(30,64,175,0.12);
  position: relative;
}
h1 {
  margin: 0 0 38px;
  font-size: clamp(36px, 9vw, 52px);
  font-weight: 800;
  color: #111827;
  letter-spacing: -1.5px;
}
button {
  width: 100%;
  min-height: 72px;
  border: none;
  border-radius: 17px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  font-size: clamp(19px, 5vw, 24px);
  font-weight: 700;
  box-shadow: 0 10px 24px rgba(37,99,235,0.3);
  cursor: pointer;
}
button:active { transform: scale(0.98); }
#result { color: #111827; font-size: 15px; }
</style>
</head>
<body>
<div class="decoration one"></div>
<div class="decoration two"></div>
<main class="content">
<h1>Phone Update</h1>
<button onclick="share()">Share My Location</button>
<p id="result"></p>
</main>
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
