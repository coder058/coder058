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
            try:
                self.ctx = self._pw.chromium.launch_persistent_context(channel="chrome", **opciones)
            except Exception:
                self.ctx = self._pw.chromium.launch_persistent_context(**opciones)
        except Exception:
            self._pw.stop()  # si no, el siguiente intento falla con otro error
            raise RuntimeError("no puedo abrir el navegador: instala Google Chrome "
                               "o ejecuta  python -m playwright install chromium") from None
        self.paginas = {}

    def pagina(self, agente: str):
        if agente not in self.paginas or self.paginas[agente].is_closed():
            self.paginas[agente] = self.ctx.new_page()
        return self.paginas[agente]

    def abrir(self, agente: str, url: str):
        self.pagina(agente).goto(url)

    def preguntar(self, agente: str, url: str, prompt: str, espera_max: int = 240) -> str:
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
            raise RuntimeError(f"{agente}: no encuentro dónde escribir. Mira su ventana de Chrome e inicia "
                               "sesión ahí (se guarda); se reintenta solo")

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
        raise TimeoutError(f"{agente}: sin respuesta en {espera_max // 60} min. Mira su ventana de Chrome: "
                           "si pide iniciar sesión, inicia sesión ahí (se guarda) y se reintenta solo")

    def cerrar(self):
        self.ctx.close()
        self._pw.stop()
