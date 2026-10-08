"""Loop sin parar: Claude da órdenes, Cursor/Grok/Sol las cumplen y le devuelven resultados.

python3 hub/orquestador.py --login       # 1ª vez: inicia sesión en Grok y ChatGPT a mano
python3 hub/orquestador.py               # loop cada 5 min (config.json)
python3 hub/orquestador.py --una-ronda   # una sola vuelta, para probar

Para pararlo: Ctrl+C, o crea el archivo hub/PARAR.
"""

import json
import shutil
import subprocess
import sys
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


def log(texto: str):
    linea = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {texto}"
    print(linea, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(linea + "\n")


def correr_cli(agente: str, prompt: str) -> str:
    cmd = CONFIG["cli"][agente]
    if not shutil.which(cmd[0]):
        raise RuntimeError(f"no encuentro '{cmd[0]}' instalado")
    r = subprocess.run(cmd + [prompt], cwd=HUB.parent, capture_output=True, text=True,
                       timeout=CONFIG["timeout_cli_segundos"])
    if r.returncode != 0 and not r.stdout.strip():
        raise RuntimeError(r.stderr.strip()[:500] or f"salió con código {r.returncode}")
    return r.stdout


def despertar(agente: str, nav) -> None:
    web = agente in CONFIG["web"]
    prompt, incluidos = buzon.prompt_para(agente, web=web)
    log(f"{agente}: despierta con {len(incluidos)} mensaje(s)")
    try:
        if web:
            salida = nav.preguntar(agente, CONFIG["web"][agente], prompt)
        else:
            salida = correr_cli(agente, prompt)
    except Exception as e:  # un agente caído no detiene a los demás
        log(f"{agente}: ERROR {e}")
        return
    creados = buzon.importar_respuesta(agente, salida, incluidos)
    log(f"{agente}: escribió {', '.join(creados) or 'nada'}")


def esperando_humano() -> bool:
    return any(m["para"] == "humano" and m["estado"] == "pendiente" for m in buzon.listar())


def ronda(nav) -> None:
    for agente in TRABAJADORES:
        if buzon.pendientes(agente):
            despertar(agente, nav)
    # Claude revisa resultados; si nadie tiene nada, da nuevas órdenes para no parar,
    # salvo que esté esperando una decisión tuya.
    nadie_ocupado = not any(buzon.pendientes(a) for a in TRABAJADORES)
    if buzon.pendientes("claude") or (nadie_ocupado and not esperando_humano()):
        despertar("claude", nav)
    elif esperando_humano():
        log("claude espera tu respuesta (mensaje para 'humano' en el panel)")


def main():
    buzon.MENSAJES.mkdir(exist_ok=True)
    nav = None
    if "--login" in sys.argv or CONFIG["web"]:
        from navegador import Navegador
        nav = Navegador()
    if "--login" in sys.argv:
        for agente, url in CONFIG["web"].items():
            nav.abrir(agente, url)
        input("Inicia sesión en cada pestaña y pulsa Enter aquí para guardar... ")
        nav.cerrar()
        return

    n = 0
    try:
        while not PARAR.exists():
            n += 1
            log(f"--- ronda {n} ---")
            ronda(nav)
            if "--una-ronda" in sys.argv or n == CONFIG["max_rondas"]:
                break
            time.sleep(CONFIG["intervalo_segundos"])
        if PARAR.exists():
            log("encontré hub/PARAR: me detengo")
    except KeyboardInterrupt:
        log("detenido con Ctrl+C")
    finally:
        if nav:
            nav.cerrar()


if __name__ == "__main__":
    main()
