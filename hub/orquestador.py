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
ESTADO = {"trabajando": [], "ultimas": []}
DESPERTAR = threading.Event()  # despierta a Claude: le escribes tú o responde un trabajador
DESPERTAR_TRABAJO = threading.Event()  # despierta a los trabajadores: Claude dio órdenes


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
            try:
                from navegador import Navegador
            except ImportError:
                raise RuntimeError("falta instalar Playwright: pip install playwright") from None
            self._nav = Navegador()
        return self._nav.preguntar(agente, CONFIG["web"][agente], prompt)

    def cerrar(self):
        if self._nav:
            self._nav.cerrar()


def despertar(agente: str, navs: Navegadores | None) -> bool:
    """Devuelve True si el agente respondió."""
    web = agente in CONFIG["web"]
    prompt, incluidos = buzon.prompt_para(agente, web=web)
    log(f"{agente}: despierta con {len(incluidos)} mensaje(s)")
    ESTADO["trabajando"].append(agente)
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
        ESTADO["trabajando"].remove(agente)
    creados = buzon.importar_respuesta(agente, salida, incluidos)
    log(f"{agente}: escribió {', '.join(creados) or 'nada'}")
    return True


def esperando_humano() -> bool:
    return any(m["para"] == "humano" and m["estado"] == "pendiente" for m in buzon.listar())


def turno_claude() -> bool:
    if buzon.pendientes("claude"):
        return despertar("claude", None)
    if (CONFIG.get("autonomo") and not esperando_humano()
            and not any(buzon.pendientes(a) for a in automaticos())):
        return despertar("claude", None)  # modo autónomo: sigue con objetivo.md sin que le escribas
    return False


def turno_trabajadores(navs: Navegadores) -> bool:
    # Si alguien falla (no instalado, sesión caída...) no cuenta como trabajo,
    # así no se reintenta cada 5 s sino en la siguiente vuelta de 5 min.
    hubo = False
    for agente in automaticos():
        if buzon.pendientes(agente) and despertar(agente, navs):
            hubo = True
            DESPERTAR.set()  # Claude revisa el resultado sin esperar a los demás
    return hubo


def carril_claude() -> None:
    """Tú y Claude: nunca espera a que un trabajador termine."""
    while not PARAR.exists():
        DESPERTAR.clear()
        if turno_claude():
            DESPERTAR_TRABAJO.set()  # puede haber órdenes nuevas
        DESPERTAR.wait(CONFIG["intervalo_segundos"])


def carril_trabajadores() -> None:
    """Cursor, Grok y Sol, de uno en uno (el navegador solo se usa desde este hilo)."""
    navs = Navegadores()
    try:
        while not PARAR.exists():
            DESPERTAR_TRABAJO.clear()
            hubo = turno_trabajadores(navs)
            DESPERTAR_TRABAJO.wait(5 if hubo else CONFIG["intervalo_segundos"])
    finally:
        navs.cerrar()


def bucle(una_ronda: bool = False) -> None:
    buzon.MENSAJES.mkdir(exist_ok=True)
    if una_ronda:
        navs = Navegadores()
        try:
            turno_claude()
            turno_trabajadores(navs)
            turno_claude()
        finally:
            navs.cerrar()
        return
    hilos = [threading.Thread(target=carril_claude, daemon=True),
             threading.Thread(target=carril_trabajadores, daemon=True)]
    for h in hilos:
        h.start()
    while any(h.is_alive() for h in hilos):
        time.sleep(1)
    log("encontré hub/PARAR: me detengo")


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
