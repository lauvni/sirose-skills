import copy
import json
from datetime import datetime, timedelta, timezone

from tablette.publier.fusion import fusionner
from tablette.tests.conftest import RACINE

REUNION = timezone(timedelta(hours=4))
EXEMPLE = json.loads((RACINE / "exemple" / "dashboard.json").read_text(encoding="utf-8"))
MIDI = datetime(2026, 11, 18, 12, 30, tzinfo=REUNION)


def indispo(d, bloc):
    d = copy.deepcopy(d)
    d["blocs"][bloc] = {"etat": "indisponible", "depuis": None, "elements": []}
    return d


def test_bloc_indisponible_reprend_precedent():
    r = fusionner(indispo(EXEMPLE, "taches"), EXEMPLE, MIDI)
    t = r["blocs"]["taches"]
    assert t["elements"] == EXEMPLE["blocs"]["taches"]["elements"]
    assert t["etat"] == "indisponible" and t["depuis"].startswith("2026-11-18T12:30")


def test_indisponible_depuis_conserve_la_premiere_panne():
    precedent = copy.deepcopy(EXEMPLE)
    precedent["blocs"]["mails"]["etat"] = "indisponible"
    precedent["blocs"]["mails"]["depuis"] = "2026-11-18T06:53:00+04:00"
    r = fusionner(indispo(EXEMPLE, "mails"), precedent, MIDI)
    assert r["blocs"]["mails"]["depuis"] == "2026-11-18T06:53:00+04:00"
    assert r["blocs"]["mails"]["elements"] == precedent["blocs"]["mails"]["elements"]


def test_argent_indisponible_reprend_mois_et_phase():
    nouveau = indispo(EXEMPLE, "argent")
    r = fusionner(nouveau, EXEMPLE, MIDI)
    assert r["blocs"]["argent"]["mois"] == EXEMPLE["blocs"]["argent"]["mois"]
    assert r["blocs"]["argent"]["phase"] == EXEMPLE["blocs"]["argent"]["phase"]


def test_sans_precedent_bloc_vide_reste_indisponible():
    r = fusionner(indispo(EXEMPLE, "taches"), None, MIDI)
    assert r["blocs"]["taches"]["etat"] == "indisponible"
    assert r["blocs"]["taches"]["elements"] == []
    assert r["blocs"]["taches"]["depuis"].startswith("2026-11-18T12:30")


def test_bloc_ok_inchange():
    r = fusionner(copy.deepcopy(EXEMPLE), None, MIDI)
    assert r["blocs"]["mails"] == EXEMPLE["blocs"]["mails"]
