from http.server import HTTPServer, BaseHTTPRequestHandler
import json

PAGE = b'''<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; min-height:100vh; box-sizing:border-box; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:24px; font-family:Arial,sans-serif; background:linear-gradient(135deg,#dbeafe,#eff6ff);">
<h1 style="font-size:clamp(36px,10vw,52px); font-weight:800; color:#172554; text-align:center; margin:0 0 38px;">Phone Update</h1>
<button onclick="share()" style="width:85vw; max-width:400px; min-height:72px; font-size:clamp(20px,5vw,25px); border:0; border-radius:16px; background:#2563eb; color:white; font-weight:bold; box-shadow:0 8px 20px #2563eb44;">Share My Location</button>
<p id="result" style="font-size:16px;color:#172554;"></p>
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
