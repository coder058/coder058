"""Maneja Grok y ChatGPT en TU navegador con TU sesión iniciada (sin API).

Usa Playwright con un perfil propio guardado en hub/.perfil-navegador.
La primera vez: python3 hub/orquestador.py --login  (inicias sesión a mano).
"""

import time
from pathlib import Path

import buzon

PERFIL = Path(__file__).resolve().parent / ".perfil-navegador"
CAMPOS = ["#prompt-textarea", "textarea", "div[contenteditable='true']"]


class Navegador:
    def __init__(self):
        from playwright.sync_api import sync_playwright  # pip install playwright

        self._pw = sync_playwright().start()
        opciones = dict(user_data_dir=str(PERFIL), headless=False, viewport=None)
        try:
            self.ctx = self._pw.chromium.launch_persistent_context(channel="chrome", **opciones)
        except Exception:
            self.ctx = self._pw.chromium.launch_persistent_context(**opciones)
        self.paginas = {}

    def pagina(self, agente: str):
        if agente not in self.paginas or self.paginas[agente].is_closed():
            self.paginas[agente] = self.ctx.new_page()
        return self.paginas[agente]

    def abrir(self, agente: str, url: str):
        self.pagina(agente).goto(url)

    def preguntar(self, agente: str, url: str, prompt: str, espera_max: int = 600) -> str:
        """Abre un chat nuevo, envía el prompt y devuelve la respuesta recortada."""
        p = self.pagina(agente)
        p.goto(url)
        p.wait_for_load_state("domcontentloaded")
        campo = None
        for sel in CAMPOS:
            try:
                p.wait_for_selector(sel, state="visible", timeout=15000)
                campo = p.locator(sel).first
                break
            except Exception:
                continue
        if campo is None:
            raise RuntimeError(f"{agente}: no encuentro la caja de texto (¿sesión cerrada? usa --login)")

        antes = p.inner_text("body").count(buzon.FIN)
        campo.click()
        p.keyboard.insert_text(prompt)
        time.sleep(1)
        p.keyboard.press("Enter")

        # La respuesta está lista cuando aparece un @@FIN nuevo (aparte del que trae
        # el propio prompt) y la página deja de cambiar.
        necesario = antes + prompt.count(buzon.FIN) + 1
        ultimo, estable, limite = "", 0, time.time() + espera_max
        while time.time() < limite:
            time.sleep(3)
            texto = p.inner_text("body")
            if texto.count(buzon.FIN) >= necesario:
                estable = estable + 1 if texto == ultimo else 0
                if estable >= 2:
                    return buzon.recortar_web(texto)
            ultimo = texto
        raise TimeoutError(f"{agente}: no terminó de responder en {espera_max}s")

    def cerrar(self):
        self.ctx.close()
        self._pw.stop()
