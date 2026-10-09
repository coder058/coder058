"""Panel local: hablas con Claude y él reparte el trabajo.

python3 hub/server.py                  ->  http://localhost:8765 (panel + orquestador)
python3 hub/server.py --sin-orquestador  solo el panel, sin despertar a nadie
"""

import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import buzon  # noqa: E402
import orquestador  # noqa: E402

PUERTO = 8765
INDEX = Path(__file__).resolve().parent / "static" / "index.html"
CON_ORQUESTADOR = "--sin-orquestador" not in sys.argv


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
            self._json({
                "agentes": buzon.AGENTES,
                "mensajes": buzon.listar(),
                "orquestador": CON_ORQUESTADOR,
                "trabajando": orquestador.ESTADO["trabajando"],
                "log": orquestador.ESTADO["ultimas"][-15:],
                "web": list(orquestador.CONFIG["web"]),
                "errores": orquestador.ESTADO["errores"],
                "version": (Path(__file__).resolve().parent / "VERSION").read_text(encoding="utf-8").strip(),
            })
        elif self.path.startswith("/api/prompt/"):
            agente = self.path.rsplit("/", 1)[1]
            if agente not in buzon.AGENTES:
                return self._json({"error": "agente desconocido"}, 404)
            self._json({"prompt": buzon.prompt_para(agente)[0]})
        else:
            self._json({"error": "no existe"}, 404)

    def do_POST(self):
        largo = int(self.headers.get("Content-Length", 0))
        datos = json.loads(self.rfile.read(largo) or b"{}")
        try:
            if self.path == "/api/chat":
                texto = datos["texto"].strip()
                if not texto:
                    raise ValueError("mensaje vacío")
                # Lo que Claude te dijo ya lo has visto en el chat.
                for m in buzon.listar():
                    if m["para"] == "humano" and m["estado"] == "pendiente":
                        buzon.marcar_respondido(m["archivo"])
                archivo = buzon.escribir("humano", "claude", texto)
                orquestador.DESPERTAR.set()
                self._json({"creado": archivo})
            elif self.path == "/api/importar":
                creados = buzon.importar_respuesta(datos["agente"], buzon.recortar_web(datos["texto"]))
                orquestador.DESPERTAR.set()
                self._json({"creados": creados})
            else:
                self._json({"error": "no existe"}, 404)
        except (KeyError, ValueError) as e:
            self._json({"error": str(e)}, 400)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    buzon.MENSAJES.mkdir(exist_ok=True)
    try:
        servidor = ThreadingHTTPServer(("127.0.0.1", PUERTO), Panel)
    except OSError:
        print(f"El puerto {PUERTO} ya está en uso: seguramente el panel ya está abierto.")
        webbrowser.open(f"http://127.0.0.1:{PUERTO}")
        sys.exit(1)
    if CON_ORQUESTADOR:
        threading.Thread(target=orquestador.bucle, daemon=True).start()
    url = f"http://127.0.0.1:{PUERTO}"
    print(f"Panel abierto en {url}  (no cierres esta ventana; Ctrl+C para parar)")
    webbrowser.open(url)
    servidor.serve_forever()
