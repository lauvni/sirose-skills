import json
import subprocess
import sys

from tablette.publier.crypto import dechiffrer
from tablette.tests.conftest import PIN, RACINE

EXEMPLE = RACINE / "exemple" / "dashboard.json"


def lancer(args, env_pin=PIN, cwd=None):
    import os
    env = dict(os.environ)
    env.pop("SIROSE_DASH_PIN", None)
    if env_pin:
        env["SIROSE_DASH_PIN"] = env_pin
    return subprocess.run([sys.executable, "-m", "tablette.publier.publier", *args],
                          capture_output=True, text=True, env=env, cwd=cwd or RACINE.parent)


def test_cli_produit_dist(tmp_path):
    r = lancer([str(EXEMPLE), "--sortie", str(tmp_path / "dist")])
    assert r.returncode == 0, r.stderr
    dist = tmp_path / "dist"
    assert sorted(p.name for p in dist.iterdir()) == ["app.js", "data.enc", "index.html", "netlify.toml"]
    clair = json.loads(dechiffrer(json.loads((dist / "data.enc").read_text()), PIN))
    assert clair["blocs"]["mails"] == json.loads(EXEMPLE.read_text())["blocs"]["mails"]
    for f in dist.iterdir():
        assert PIN.encode() not in f.read_bytes(), f.name


def test_cli_sans_pin_echoue(tmp_path):
    r = lancer([str(EXEMPLE), "--sortie", str(tmp_path / "dist")], env_pin=None)
    assert r.returncode == 2 and "SIROSE_DASH_PIN" in r.stderr
    assert not (tmp_path / "dist").exists()


def test_cli_schema_invalide_echoue(tmp_path):
    mauvais = tmp_path / "d.json"
    d = json.loads(EXEMPLE.read_text())
    d["blocs"]["mails"]["elements"][0]["texte"] = "IBAN FR7630004000031234567890143"
    mauvais.write_text(json.dumps(d))
    r = lancer([str(mauvais), "--sortie", str(tmp_path / "dist")])
    assert r.returncode == 2 and "donnée sensible" in r.stderr
    assert not (tmp_path / "dist").exists()


def test_cli_precedent_inaccessible_continue(tmp_path):
    r = lancer([str(EXEMPLE), "--sortie", str(tmp_path / "dist"), "--precedent-url", "http://127.0.0.1:9/data.enc"])
    assert r.returncode == 0 and "précédent" in r.stderr


def test_cli_precedent_reutilise(tmp_path, serveur):
    """Un bloc indisponible reprend les données du data.enc déjà en ligne."""
    precedent = json.loads(EXEMPLE.read_text())
    serveur.publier(precedent)
    nouveau = json.loads(EXEMPLE.read_text())
    nouveau["blocs"]["taches"] = {"etat": "indisponible", "depuis": None, "elements": []}
    entree = tmp_path / "n.json"
    entree.write_text(json.dumps(nouveau))
    url = serveur.url.replace("index.html", "data.enc")
    r = lancer([str(entree), "--sortie", str(tmp_path / "dist"), "--precedent-url", url])
    assert r.returncode == 0, r.stderr
    clair = json.loads(dechiffrer(json.loads((tmp_path / "dist" / "data.enc").read_text()), PIN))
    assert clair["blocs"]["taches"]["elements"] == precedent["blocs"]["taches"]["elements"]
    assert clair["blocs"]["taches"]["etat"] == "indisponible"


def test_cli_option_argent_remplit_le_bloc(tmp_path):
    from datetime import datetime, timedelta, timezone
    aujourd_hui = datetime.now(timezone(timedelta(hours=4))).date().isoformat()
    brut = tmp_path / "argent.json"
    brut.write_text(json.dumps({
        "factures": [{"date": aujourd_hui, "montant_ht": 120.0, "client": "X", "ref": "F-9"}],
        "paiements": [
            {"date": aujourd_hui, "montant": 80.0, "client": "X", "origine": "payzen"},
            {"date": aujourd_hui, "montant": 78.9, "client": "", "origine": "qonto", "contrepartie": "LYRA NETWORK"},
        ],
    }))
    r = lancer([str(EXEMPLE), "--sortie", str(tmp_path / "dist"), "--argent", str(brut)])
    assert r.returncode == 0, r.stderr
    clair = json.loads(dechiffrer(json.loads((tmp_path / "dist" / "data.enc").read_text()), PIN))
    assert clair["blocs"]["argent"]["mois"]["facture"] == 120.0
    assert clair["blocs"]["argent"]["mois"]["encaisse"] == 80.0


def test_cli_refuse_pin_faible(tmp_path):
    for faible in ("4821", "123456789012345", "court"):
        r = lancer([str(EXEMPLE), "--sortie", str(tmp_path / "dist")], env_pin=faible)
        assert r.returncode == 2 and "phrase de passe" in r.stderr, faible
    assert not (tmp_path / "dist").exists()
