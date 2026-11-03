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
  padding: 22px;
  font-family: Arial, sans-serif;
  background:
    radial-gradient(circle at 15% 15%, #ffd6e7 0, transparent 38%),
    radial-gradient(circle at 90% 85%, #ddd6fe 0, transparent 40%),
    linear-gradient(135deg, #fff1f7, #f5f0ff, #eef2ff);
  overflow: hidden;
}
.glow {
  position: fixed;
  border-radius: 50%;
  filter: blur(2px);
  pointer-events: none;
}
.glow1 {
  width: 220px; height: 220px;
  background: #fbcfe8;
  opacity: .45;
  top: -75px; right: -65px;
}
.glow2 {
  width: 190px; height: 190px;
  background: #c4b5fd;
  opacity: .35;
  bottom: -65px; left: -55px;
}
.card {
  width: 100%;
  max-width: 440px;
  padding: 58px 24px;
  text-align: center;
  background: rgba(255,255,255,.78);
  border: 1px solid rgba(255,255,255,.95);
  border-radius: 30px;
  box-shadow: 0 20px 60px rgba(150,90,160,.16);
  position: relative;
  backdrop-filter: blur(12px);
}
h1 {
  margin: 0 0 38px;
  color: #242033;
  font-size: clamp(36px, 9vw, 50px);
  font-weight: 800;
  letter-spacing: -1.5px;
}
button {
  width: 100%;
  min-height: 72px;
  border: 0;
  border-radius: 18px;
  background: linear-gradient(110deg, #ec4899, #a855f7);
  color: white;
  font-size: clamp(19px, 5vw, 23px);
  font-weight: 700;
  box-shadow: 0 10px 25px rgba(192,80,170,.28);
  cursor: pointer;
}
button:active { transform: scale(.98); }
#result { color: #4b365c; font-size: 15px; }
</style>
</head>
<body>
<div class="glow glow1"></div>
<div class="glow glow2"></div>
<main class="card">
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
