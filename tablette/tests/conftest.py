import functools
import http.server
import json
import os
import shutil
import threading
from pathlib import Path

import pytest

from tablette.publier.crypto import chiffrer

RACINE = Path(__file__).resolve().parents[1]
PIN = "vanille-koso-margouillat-2026"
MINIMAL = {"schema": 1, "genere_le": "2026-11-18T07:30:00+04:00"}


class Serveur:
    def __init__(self, dossier: Path):
        self.dossier = dossier
        handler = functools.partial(_Silencieux, directory=str(dossier))
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}/index.html"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def publier(self, donnees: dict, pin: str = PIN):
        env = chiffrer(json.dumps(donnees, ensure_ascii=False).encode("utf-8"), pin)
        (self.dossier / "data.enc").write_text(json.dumps(env))

    def retirer(self):
        (self.dossier / "data.enc").unlink()


class _Silencieux(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


@pytest.fixture
def donnees():
    """Données servies par défaut ; surchargée dans les tests de rendu."""
    return MINIMAL


@pytest.fixture
def serveur(tmp_path, donnees):
    for f in ("index.html", "app.js"):
        shutil.copy(RACINE / f, tmp_path / f)
    s = Serveur(tmp_path)
    s.publier(donnees)
    yield s
    s.httpd.shutdown()


@pytest.fixture(scope="session")
def navigateur():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium"))
        yield b
        b.close()


@pytest.fixture
def page(navigateur):
    ctx = navigateur.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
    pg = ctx.new_page()
    yield pg
    ctx.close()
