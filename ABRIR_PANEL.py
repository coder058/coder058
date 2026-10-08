"""Doble clic aquí para abrir el panel de Claude en el navegador.

Si no se abre con doble clic: abre esta carpeta, escribe cmd en la barra de
direcciones del Explorador, pulsa Enter y escribe:  python ABRIR_PANEL.py
"""

import runpy
import sys
import traceback
from pathlib import Path

carpeta = Path(__file__).resolve().parent
sys.argv = [str(carpeta / "hub" / "server.py")]
if not Path(sys.argv[0]).exists():
    print("Falta la carpeta 'hub' al lado de este archivo.")
    print("Seguramente lo abriste desde dentro del ZIP. Haz esto:")
    print("  1. Cierra esta ventana.")
    print("  2. Clic derecho en el ZIP -> 'Extraer todo...' -> Extraer.")
    print("  3. En la carpeta nueva que se abre, doble clic en ABRIR_PANEL.py")
    input("\nPulsa Enter para cerrar...")
    sys.exit(1)
try:
    runpy.run_path(sys.argv[0], run_name="__main__")
except KeyboardInterrupt:
    pass
except BaseException:
    traceback.print_exc()
    print("\nAlgo falló. Copia el texto de arriba y pégaselo a Claude.")
    input("Pulsa Enter para cerrar...")
