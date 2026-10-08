"""Claude (Head of Portfolio) reparte el trabajo; Cursor, Grok y Sol lo hacen y le responden.

Lo normal es no usar este archivo directamente: `python hub/server.py` lo arranca solo
y tú hablas con Claude en http://localhost:8765.

python3 hub/orquestador.py --login       # 1ª vez: inicia sesión en Grok y ChatGPT a mano
python3 hub/orquestador.py               # el bucle, sin panel
python3 hub/orquestador.py --una-ronda   # una sola vuelta, para probar

Para pararlo: Ctrl+C, o crea el archivo hub/PARAR.
"""

import json
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

HUB = Path(__file__).resolve().parent
sys.path.insert(0, str(HUB))
import buzon  # noqa: E402

CONFIG = json.loads((HUB / "config.json").read_text(encoding="utf-8"))
PARAR = HUB / "PARAR"
LOG = HUB / "orquestador.log"
TRABAJADORES = ["cursor", "grok", "sol"]

# Lo que el panel enseña: quién está trabajando ahora y las últimas líneas del log.
ESTADO = {"trabajando": None, "ultimas": []}
DESPERTAR = threading.Event()  # el panel lo activa cuando le escribes a Claude


def log(texto: str):
    linea = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {texto}"
    print(linea, flush=True)
    ESTADO["ultimas"] = (ESTADO["ultimas"] + [linea])[-40:]
    with LOG.open("a", encoding="utf-8") as f:
        f.write(linea + "\n")


def automaticos() -> list[str]:
    return [a for a in TRABAJADORES if a not in CONFIG.get("manual", [])]


def correr_cli(agente: str, prompt: str) -> str:
    cmd = list(CONFIG["cli"][agente])
    ruta = shutil.which(cmd[0])  # en Windows encuentra también .cmd / .exe
    if not ruta:
        raise RuntimeError(f"no encuentro '{cmd[0]}' instalado")
    cmd[0] = ruta
    por_stdin = CONFIG.get("entrada", {}).get(agente) == "stdin"
    carpeta = CONFIG.get("carpetas", {}).get(agente) or HUB.parent
    r = subprocess.run(
        cmd if por_stdin else cmd + [prompt],
        input=prompt if por_stdin else None,
        cwd=carpeta, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=CONFIG["timeout_cli_segundos"],
    )
    if r.returncode != 0 and not r.stdout.strip():
        raise RuntimeError(r.stderr.strip()[:500] or f"salió con código {r.returncode}")
    return r.stdout


class Navegadores:
    """Abre el navegador solo la primera vez que hace falta (Grok o ChatGPT)."""

    def __init__(self):
        self._nav = None

    def preguntar(self, agente: str, prompt: str) -> str:
        if self._nav is None:
            from navegador import Navegador
            self._nav = Navegador()
        return self._nav.preguntar(agente, CONFIG["web"][agente], prompt)

    def cerrar(self):
        if self._nav:
            self._nav.cerrar()


def despertar(agente: str, navs: Navegadores) -> bool:
    """Devuelve True si el agente respondió."""
    web = agente in CONFIG["web"]
    prompt, incluidos = buzon.prompt_para(agente, web=web)
    log(f"{agente}: despierta con {len(incluidos)} mensaje(s)")
    ESTADO["trabajando"] = agente
    try:
        salida = navs.preguntar(agente, prompt) if web else correr_cli(agente, prompt)
    except Exception as e:  # un agente caído no detiene a los demás
        log(f"{agente}: ERROR {e}")
        if agente == "claude":
            buzon.escribir("claude", "humano", f"No he podido ejecutarme: {e}")
            for archivo in incluidos:
                buzon.marcar_respondido(archivo)
        return False
    finally:
        ESTADO["trabajando"] = None
    creados = buzon.importar_respuesta(agente, salida, incluidos)
    log(f"{agente}: escribió {', '.join(creados) or 'nada'}")
    return True


def esperando_humano() -> bool:
    return any(m["para"] == "humano" and m["estado"] == "pendiente" for m in buzon.listar())


def ronda(navs: Navegadores) -> bool:
    """Una vuelta. Devuelve True si alguien trabajó."""
    # Si alguien falla (no instalado, sesión caída...) no cuenta como trabajo,
    # así no se reintenta cada 5 s sino en la siguiente vuelta de 5 min.
    hubo = False
    # Claude primero: así lo que le pides llega a los trabajadores en la misma vuelta.
    if buzon.pendientes("claude"):
        hubo |= despertar("claude", navs)
    for agente in automaticos():
        if buzon.pendientes(agente):
            hubo |= despertar(agente, navs)
    if buzon.pendientes("claude"):
        hubo |= despertar("claude", navs)  # resultados recién llegados: Claude te los resume
    elif (not hubo and CONFIG.get("autonomo") and not esperando_humano()
          and not any(buzon.pendientes(a) for a in automaticos())):
        hubo |= despertar("claude", navs)  # modo autónomo: sigue con objetivo.md sin que le escribas
    return hubo


def bucle(una_ronda: bool = False) -> None:
    buzon.MENSAJES.mkdir(exist_ok=True)
    navs = Navegadores()
    n = 0
    try:
        while not PARAR.exists():
            n += 1
            DESPERTAR.clear()
            hubo = ronda(navs)
            if una_ronda or n == CONFIG["max_rondas"]:
                break
            # Si hubo trabajo, se sigue enseguida hasta que nadie tenga nada pendiente.
            # Si no, espera 5 min o hasta que le escribas a Claude en el panel.
            DESPERTAR.wait(5 if hubo else CONFIG["intervalo_segundos"])
        if PARAR.exists():
            log("encontré hub/PARAR: me detengo")
    finally:
        navs.cerrar()


def main():
    if "--login" in sys.argv:
        from navegador import Navegador
        nav = Navegador()
        for agente, url in CONFIG["web"].items():
            nav.abrir(agente, url)
        input("Inicia sesión en cada pestaña y pulsa Enter aquí para guardar... ")
        nav.cerrar()
        return
    try:
        bucle(una_ronda="--una-ronda" in sys.argv)
    except KeyboardInterrupt:
        log("detenido con Ctrl+C")


if __name__ == "__main__":
    main()
