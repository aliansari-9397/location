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
  background: linear-gradient(135deg,#fff1f7,#ffffff,#f3e8ff);
  overflow: hidden;
}
.circle {
  position: fixed;
  border-radius: 50%;
  pointer-events: none;
  animation: float 7s ease-in-out infinite alternate;
}
.c1 { width:220px;height:220px;background:#fbcfe8;opacity:.5;top:-70px;right:-60px; }
.c2 { width:180px;height:180px;background:#ddd6fe;opacity:.6;bottom:-50px;left:-50px;animation-delay:2s; }
@keyframes float {
  from { transform: translateY(0); }
  to { transform: translateY(22px); }
}
.card {
  width: 100%;
  max-width: 440px;
  padding: 58px 24px;
  text-align: center;
  background: rgba(255,255,255,.78);
  border: 1px solid white;
  border-radius: 30px;
  box-shadow: 0 20px 60px rgba(150,90,160,.16);
  position: relative;
  backdrop-filter: blur(14px);
}
h1 {
  margin: 0 0 38px;
  color: #211b2d;
  font-family: Georgia, serif;
  font-size: clamp(36px,9vw,50px);
  font-weight: bold;
  letter-spacing: -1px;
}
button {
  width: 100%;
  min-height: 72px;
  border: 0;
  border-radius: 18px;
  background: linear-gradient(110deg,#ec4899,#a855f7);
  color: white;
  font-size: clamp(19px,5vw,23px);
  font-weight: 700;
  box-shadow: 0 10px 25px rgba(192,80,170,.28);
  cursor: pointer;
  transition: transform .2s, box-shadow .2s;
}
button:active {
  transform: scale(.97);
  box-shadow: 0 5px 14px rgba(192,80,170,.25);
}
#result { color:#4b365c; font-size:15px; }
</style>
</head>
<body>
<div class="circle c1"></div>
<div class="circle c2"></div>
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
