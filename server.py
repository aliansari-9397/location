import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shaadi-bazaar-India</title>
<style>
body {
  font-family: Arial, sans-serif;
  text-align: center;
  padding: 50px 20px;
  background: #fff;
}
h1 { color: #222; }
p { color: #555; }
button {
  padding: 15px 25px;
  background: #1769aa;
  color: white;
  border: 0;
  border-radius: 8px;
  font-size: 18px;
}
button:disabled { opacity: .6; }
</style>
</head>
<body>
<h1>Shaadi-bazaar-India</h1>
<p>This page shares your live location only after you tap the button and allow location access.</p>
<button id="start">Start Live Location</button>

<script>
let watchId = null;
const button = document.getElementById("start");

button.addEventListener("click", function () {
  if (!navigator.geolocation) {
    alert("Location is not supported by this browser.");
    return;
  }

  button.disabled = true;

  watchId = navigator.geolocation.watchPosition(
    function (position) {
      const data = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
        time: new Date().toISOString()
      };

      fetch("/location", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
      }).catch(function (error) {
        console.error("Location update failed:", error);
      });
    },
    function (error) {
      alert("Location permission/error: " + error.message);
      button.disabled = false;
    },
    { enableHighAccuracy: true, maximumAge: 0 }
  );
});
</script>
</body>
</html>
""".encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(PAGE)))
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

    def do_HEAD(self):
        if self.path.split("?")[0] == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(PAGE)))
            self.end_headers()
        else:
            self.send_error(404)

port = int(os.environ.get("PORT", 8000))
server = HTTPServer(("0.0.0.0", port), Handler)
print("Server running on", port, flush=True)
server.serve_forever()
