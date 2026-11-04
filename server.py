import os
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<meta name="theme-color" content="#101827">
<title>Shaadi Bazaar India</title>
<style>
* { box-sizing: border-box; }
html, body {
  margin: 0;
  min-height: 100%;
  width: 100%;
  font-family: Arial, sans-serif;
  background: #101827;
  color: white;
}
html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  overscroll-behavior: none;
  touch-action: pan-x pan-y;
}
body {
  min-height: 100vh;
  min-height: 100dvh;
  padding: 0;
}
.container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.container {
  width: 100%;
  max-width: 390px;
  text-align: center;
  padding: 38px 24px;
  background: #1b293c;
  border: 1px solid #34445b;
  border-radius: 20px;
  box-shadow: 0 15px 40px rgba(0,0,0,.25);
}
h1 {
  margin: 0 0 14px;
  font-size: 28px;
  line-height: 1.25;
}
.description {
  color: #c4cfdd;
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 26px;
}
button {
  width: 100%;
  height: 54px;
  border: 0;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  touch-action: manipulation;
}
#start { background: #e7b65c; color: #172033; }
#stop {
  margin-top: 12px;
  background: #34445b;
  color: white;
}
button:disabled { opacity: .55; cursor: not-allowed; }
#status {
  min-height: 42px;
  margin-top: 18px;
  color: #c4cfdd;
  font-size: 13px;
  line-height: 1.5;
  overflow-wrap: anywhere;
}
</style>
</head>
<body>
<main class="container">
  <h1>Shaadi-bazaar-India</h1>
  <button id="start">Start Live Location</button>
</main>

<script>
const startButton = document.getElementById("start");
const statusBox = null;
let watchId = null;
let sending = false;

function stopSharing(message) {
  if (watchId !== null) {
    navigator.geolocation.clearWatch(watchId);
  }
  watchId = null;
  sending = false;
  startButton.disabled = false;
  statusBox.textContent = message || "Location sharing is off.";
}

startButton.addEventListener("click", function () {
  if (!navigator.geolocation) {
    statusBox.textContent = "This browser does not support location access.";
    return;
  }

  if (watchId !== null) return;

  startButton.disabled = true;
  statusBox.textContent = "Waiting for location permission...";

  watchId = navigator.geolocation.watchPosition(
    async function (position) {
      if (sending) return;
      sending = true;

      const locationData = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
        time: new Date().toISOString()
      };

      try {
        const response = await fetch("/location", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(locationData)
        });

        if (!response.ok) throw new Error("Server error");
        startButton.textContent = "Stop Sharing";
      } catch (error) {
        console.error("Connection problem.");
      } finally {
        sending = false;
      }
    },
    function (error) {
      let message = "Unable to get location.";
      if (error.code === 1) message = "Location permission was denied. Allow it in browser settings.";
      if (error.code === 2) message = "Location is unavailable. Check your phone GPS.";
      if (error.code === 3) message = "Location request timed out. Please try again.";
      stopSharing(); 
      alert(message);
    },
    { enableHighAccuracy: true, maximumAge: 0, timeout: 20000 }
  );

  statusBox.textContent = "Please allow location access when your browser asks.";
});

</script>
</body>
</html>
""".encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(PAGE)

    def do_HEAD(self):
        if self.path.split("?")[0] == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE)))
        self.end_headers()

    def do_POST(self):
        if self.path != "/location":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 10000:
                self.send_error(400)
                return
            data = json.loads(self.rfile.read(size))
            lat = float(data["latitude"])
            lon = float(data["longitude"])
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                self.send_error(400)
                return
            print("LIVE LOCATION:", json.dumps(data), flush=True)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception:
            self.send_error(400)

port = int(os.environ.get("PORT", "8000"))
server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
print("Server running on", port, flush=True)
server.serve_forever()
