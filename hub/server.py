"""Panel local del hub: python3 hub/server.py  ->  http://localhost:8765"""

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import buzon  # noqa: E402

PUERTO = 8765
INDEX = Path(__file__).resolve().parent / "static" / "index.html"


class Panel(BaseHTTPRequestHandler):
    def _json(self, datos, codigo=200):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            cuerpo = INDEX.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)
        elif self.path == "/api/mensajes":
            self._json({"agentes": buzon.AGENTES, "mensajes": buzon.listar()})
        elif self.path.startswith("/api/prompt/"):
            agente = self.path.rsplit("/", 1)[1]
            if agente not in buzon.AGENTES:
                return self._json({"error": "agente desconocido"}, 404)
            self._json({"prompt": buzon.prompt_para(agente)})
        else:
            self._json({"error": "no existe"}, 404)

    def do_POST(self):
        largo = int(self.headers.get("Content-Length", 0))
        datos = json.loads(self.rfile.read(largo) or b"{}")
        try:
            if self.path == "/api/enviar":
                archivo = buzon.escribir(datos["de"], datos["para"], datos["cuerpo"], datos.get("responde_a", ""))
                self._json({"creado": archivo})
            elif self.path == "/api/importar":
                self._json({"creados": buzon.importar_respuesta(datos["agente"], datos["texto"])})
            elif self.path == "/api/respondido":
                buzon.marcar_respondido(datos["archivo"])
                self._json({"ok": True})
            else:
                self._json({"error": "no existe"}, 404)
        except (KeyError, ValueError) as e:
            self._json({"error": str(e)}, 400)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    buzon.MENSAJES.mkdir(exist_ok=True)
    print(f"Hub en http://localhost:{PUERTO}  (Ctrl+C para parar)")
    ThreadingHTTPServer(("127.0.0.1", PUERTO), Panel).serve_forever()
