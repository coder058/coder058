"""Doble clic aquí para abrir el panel de Claude en el navegador.

Al abrirse se actualiza solo desde GitHub: no hace falta volver a bajar el ZIP.
Tus mensajes, objetivo.md y tus ajustes de config.json no se tocan.

Si no se abre con doble clic: abre esta carpeta, escribe cmd en la barra de
direcciones del Explorador, pulsa Enter y escribe:  python ABRIR_PANEL.py
"""

import io
import json
import runpy
import sys
import traceback
import urllib.request
import zipfile
from pathlib import Path

ZIP = "https://github.com/coder058/coder058/archive/refs/heads/claude/optimistic-mayer-nym3mi.zip"
# Lo que es tuyo y nunca se sobrescribe.
TUYO = ("hub/mensajes/", "hub/objetivo.md", "hub/PARAR",
        "hub/.perfil-navegador/", "hub/orquestador.log")
# De config.json solo se conservan tus ajustes; el resto se actualiza.
AJUSTES_TUYOS = ("carpetas", "manual")

carpeta = Path(__file__).resolve().parent


def actualizar() -> None:
    try:
        datos = urllib.request.urlopen(ZIP, timeout=20).read()
    except Exception:
        print("Sin conexión con GitHub: abro la versión que ya tienes.")
        return
    nuevos = 0
    with zipfile.ZipFile(io.BytesIO(datos)) as z:
        for nombre in z.namelist():
            ruta = nombre.split("/", 1)[1] if "/" in nombre else ""
            if nombre.endswith("/") or not (ruta.startswith("hub/") or ruta == "ABRIR_PANEL.py"):
                continue
            destino = carpeta / ruta
            if ruta.startswith(TUYO) and destino.exists():
                continue
            contenido = z.read(nombre)
            if ruta == "hub/config.json" and destino.exists():
                try:
                    viejo = json.loads(destino.read_text(encoding="utf-8"))
                    nuevo = json.loads(contenido)
                    for clave in AJUSTES_TUYOS:
                        if viejo.get(clave):
                            nuevo[clave] = viejo[clave]
                    contenido = (json.dumps(nuevo, indent=2, ensure_ascii=False) + "\n").encode()
                except ValueError:
                    pass
            if not destino.exists() or destino.read_bytes() != contenido:
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_bytes(contenido)
                nuevos += 1
    version = (carpeta / "hub" / "VERSION").read_text(encoding="utf-8").strip() \
        if (carpeta / "hub" / "VERSION").exists() else "?"
    print(f"Panel actualizado ({nuevos} archivo(s) nuevos). Versión: {version}")


def main() -> None:
    if not (carpeta / "hub" / "server.py").exists():
        print("Falta la carpeta 'hub' al lado de este archivo.")
        print("Seguramente lo abriste desde dentro del ZIP. Haz esto:")
        print("  1. Cierra esta ventana.")
        print("  2. Clic derecho en el ZIP -> 'Extraer todo...' -> Extraer.")
        print("  3. En la carpeta nueva que se abre, doble clic en ABRIR_PANEL.py")
        input("\nPulsa Enter para cerrar...")
        sys.exit(1)
    try:
        actualizar()
        sys.argv = [str(carpeta / "hub" / "server.py")]
        runpy.run_path(sys.argv[0], run_name="__main__")
    except KeyboardInterrupt:
        pass
    except BaseException:
        traceback.print_exc()
        print("\nAlgo falló. Copia el texto de arriba y pégaselo a Claude.")
        input("Pulsa Enter para cerrar...")


if __name__ == "__main__":
    main()
