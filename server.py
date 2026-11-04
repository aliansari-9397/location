import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Live Location Sharing</title>
<style>
body {
  margin:0; min-height:100vh; display:grid; place-items:center;
  font-family:Arial; background:linear-gradient(135deg,#fce4ec,#e8eaf6);
}
.card {
  background:white; padding:30px; border-radius:22px;
  width:85%; max-width:380px; text-align:center;
  box-shadow:0 8px 30px #0002;
}
h2 {color:#ad4775}
button {
  padding:14px; width:100%; border:0; border-radius:12px;
  background:#bd5790; color:white; font-size:16px; margin-top:12px;
}
#stop {background:#555}
#status {margin-top:18px;color:#444}
</style>
</head>
<body>



</div>
<script>
let watchId = null;

function start() {
  if (!navigator.geolocation) {
    status.textContent = "Location is not supported.";
    return;
  }
  if (watchId !== null) return;

  status.textContent = "Requesting location permission...";
  watchId = navigator.geolocation.watchPosition(async p => {
    const data = {
      latitude: p.coords.latitude,
      longitude: p.coords.longitude,
      accuracy: p.coords.accuracy,
      time: new Date().toISOString()
    };
    try {
      const r = await fetch('/location', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(data)
      });
      status.textContent = r.ok
        ? "Live location sharing is ON 🌸"
        : "Could not send location.";
    } catch(e) {
      status.textContent = "Connection error.";
    }
  }, e => {
    status.textContent = "Location unavailable: " + e.message;
    stop();
  }, {enableHighAccuracy:true, maximumAge:0});

  document.querySelector("button").disabled = true;
  document.getElementById("stop").disabled = false;
}

function stop() {
  if (watchId !== null) navigator.geolocation.clearWatch(watchId);
  watchId = null;
  document.querySelector("button").disabled = false;
  document.getElementById("stop").disabled = true;
  status.textContent = "Location sharing stopped.";
}
</script>
</body>
</html>
""".encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/":
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PAGE)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/location":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(size))
            print("LIVE LOCATION:", json.dumps(data), flush=True)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception:
            self.send_error(400)

port = int(os.environ.get("PORT", 8000))
server = HTTPServer(("0.0.0.0", port), Handler)
print("Server running on", port, flush=True)
server.serve_forever()
