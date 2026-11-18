import copy
import json

from tablette.publier.schema import valider
from tablette.tests.conftest import RACINE

EXEMPLE = json.loads((RACINE / "exemple" / "dashboard.json").read_text(encoding="utf-8"))


def test_exemple_valide():
    assert valider(EXEMPLE) == []


def test_source_inconnue_refusee():
    d = copy.deepcopy(EXEMPLE)
    d["blocs"]["mails"]["elements"][0]["source"] = "slack"
    assert len(valider(d)) == 1


def test_bloc_manquant_refuse():
    d = copy.deepcopy(EXEMPLE)
    del d["blocs"]["pipeline"]
    assert any("pipeline" in e for e in valider(d))


def test_date_genere_le_invalide_refusee():
    d = copy.deepcopy(EXEMPLE)
    d["genere_le"] = "hier"
    assert valider(d)


def test_iban_refuse():
    d = copy.deepcopy(EXEMPLE)
    d["blocs"]["mails"]["elements"][1]["texte"] = "Virement depuis FR76 3000 4000 0312 3456 7890 143"
    assert any("donnée sensible" in e for e in valider(d))


def test_iban_colle_refuse():
    d = copy.deepcopy(EXEMPLE)
    d["blocs"]["pipeline"]["elements"][0]["lien_vers"] = "FR7630004000031234567890143"
    assert any("donnée sensible" in e for e in valider(d))


def test_numero_secu_refuse():
    d = copy.deepcopy(EXEMPLE)
    d["blocs"]["priorites"]["elements"][0]["texte"] = "Dossier 1 85 05 78 006 084 36"
    assert any("donnée sensible" in e for e in valider(d))


def test_date_sans_fuseau_refusee():
    d = copy.deepcopy(EXEMPLE)
    d["genere_le"] = "2026-11-18T06:53:00"
    assert any("genere_le" in e for e in valider(d))
