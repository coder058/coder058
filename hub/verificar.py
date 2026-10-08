"""Comprueba la prueba de conexión: ¿cada trabajador leyó su código y respondió?

python3 hub/verificar.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import buzon  # noqa: E402


def main():
    mensajes = buzon.listar()
    pruebas = [m for m in mensajes if m["de"] == "claude" and "PRUEBA DE CONEXIÓN" in m["cuerpo"]]
    if not pruebas:
        print("No hay mensajes de prueba en hub/mensajes/.")
        return
    todo_ok = True
    for prueba in pruebas:
        agente = prueba["para"]
        codigo = re.search(r"Tu código es: (\S+)", prueba["cuerpo"]).group(1)
        respuestas = [m for m in mensajes if m["de"] == agente and m["para"] == "claude"]
        if not respuestas:
            print(f"{agente:7} FALTA    no ha respondido (estado de la prueba: {prueba['estado']})")
            todo_ok = False
            continue
        texto = "\n".join(m["cuerpo"] for m in respuestas)
        if codigo[::-1] in texto:
            print(f"{agente:7} OK       leyó su código y lo devolvió al revés ({codigo[::-1]})")
        elif codigo in texto:
            print(f"{agente:7} A MEDIAS respondió con el código, pero sin darle la vuelta")
            todo_ok = False
        else:
            print(f"{agente:7} MAL      respondió, pero sin su código: no leyó bien la orden")
            todo_ok = False
        if prueba["estado"] != "respondido":
            print(f"{'':7}          (aviso: no marcó la orden como respondida)")
    print("\nTodo funciona." if todo_ok else "\nHay algo que revisar.")


if __name__ == "__main__":
    main()
