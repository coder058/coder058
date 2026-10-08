"""Loop de aviso: cada 5 min dice qué agente tiene mensajes pendientes.

python3 hub/vigilar.py            # cada 5 minutos
python3 hub/vigilar.py --una-vez  # revisa una sola vez
"""

import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import buzon  # noqa: E402

INTERVALO = 5 * 60
COMO_DESPERTAR = {
    "claude": "lo hace solo con /loop 5m",
    "cursor": "dile en Cursor: 'procesa tus mensajes pendientes en hub/mensajes/'",
    "grok": "panel localhost:8765 -> Copiar prompt -> grok.com -> Pegar respuesta",
    "sol": "panel localhost:8765 -> Copiar prompt -> Sol -> Pegar respuesta",
}


def revisar():
    hora = datetime.now().strftime("%H:%M")
    hay = False
    for agente in buzon.AGENTES:
        n = len(buzon.pendientes(agente))
        if n:
            hay = True
            print(f"[{hora}] {agente}: {n} pendiente(s) -> {COMO_DESPERTAR[agente]}\a")
    if not hay:
        print(f"[{hora}] nada pendiente")


if __name__ == "__main__":
    revisar()
    while "--una-vez" not in sys.argv:
        time.sleep(INTERVALO)
        revisar()
