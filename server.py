from http.server import HTTPServer, BaseHTTPRequestHandler
import json

PAGE = '''<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ladies Fashion</title>
<style>
* { box-sizing:border-box; }
body {
 margin:0; min-height:100vh; padding:25px 18px;
 display:flex; align-items:center; justify-content:center;
 font-family:Arial,sans-serif;
 background:linear-gradient(135deg,#ffe4ef,#f5eaff,#fff7fb);
}
.card {
 width:100%; max-width:440px; text-align:center;
 padding:38px 23px; border-radius:30px;
 background:rgba(255,255,255,.88);
 border:1px solid white;
 box-shadow:0 18px 55px rgba(180,80,140,.18);
}
.flowers { font-size:35px; letter-spacing:9px; margin-bottom:18px; }
h1 { color:#9d276b; font-family:Georgia,serif;
 font-size:clamp(38px,10vw,48px); margin:0 0 12px; }
.subtitle { color:#76516e; font-size:17px; margin:0 0 25px; }
.dresses {
 display:flex; justify-content:center; gap:12px;
 margin:20px 0 27px; font-size:42px;
}
.notice { color:#66536b; font-size:14px; line-height:1.5; margin:0 0 18px; }
button {
 width:100%; min-height:65px; border:0; border-radius:17px;
 background:linear-gradient(110deg,#e83e91,#9254db);
 color:white; font-size:19px; font-weight:bold;
 box-shadow:0 9px 22px rgba(190,60,145,.28);
}
#result { color:#783b70; font-size:14px; }
</style>
</head>
<body>
<main class="card">
<div class="flowers">🌸 🌷 🌸</div>
<h1>Ladies Fashion</h1>
<p class="subtitle">Style • Beauty • Elegance</p>
<div class="dresses">👗 👚 👗</div>
<p class="notice">Share your location with this page only if you choose to.</p>
<button onclick="share()">Share My Location</button>
<p id="result"></p>
</main>
<script>
function share() {
 const result = document.getElementById('result');
 result.textContent = 'Please allow location access if you want to share it.';
 navigator.geolocation.getCurrentPosition(async p => {
  const data = {latitude:p.coords.latitude, longitude:p.coords.longitude};
  try {
   const response = await fetch('/location', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(data)
   });
   if (!response.ok) throw new Error('Server error');
   result.textContent = 'Location shared successfully.';
  } catch(e) {
   result.textContent = 'Could not send location. Please try again.';
  }
 }, e => { result.textContent = 'Location was not shared: ' + e.message; });
}
</script>
</body>
</html>'''.encode("utf-8")

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
