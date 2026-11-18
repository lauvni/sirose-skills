from tablette.tests.conftest import PIN


def deverrouiller(page, url, pin=PIN):
    page.goto(url)
    page.fill("#champ-pin", pin)
    page.click("#bouton-pin")


def test_pin_correct_affiche_tableau(page, serveur):
    deverrouiller(page, serveur.url)
    page.wait_for_selector("#tableau:not([hidden])")
    assert page.evaluate("localStorage.getItem('sirose_pin')") == PIN
    assert page.is_hidden("#ecran-pin")


def test_pin_memorise_pas_de_saisie(page, serveur):
    page.goto(serveur.url)
    page.evaluate(f"localStorage.setItem('sirose_pin', '{PIN}')")
    page.reload()
    page.wait_for_selector("#tableau:not([hidden])")
    assert page.is_hidden("#ecran-pin")


def test_mauvais_pin(page, serveur):
    deverrouiller(page, serveur.url, "0000")
    page.wait_for_function("document.getElementById('message-pin').textContent === 'Code incorrect'", timeout=10000)
    assert page.text_content("#message-pin") == "Code incorrect"
    assert page.evaluate("localStorage.getItem('sirose_pin')") is None
    assert page.is_visible("#ecran-pin")


def test_pin_memorise_devenu_faux_redemande(page, serveur):
    page.goto(serveur.url)
    page.evaluate("localStorage.setItem('sirose_pin', '9999')")
    page.reload()
    page.wait_for_function("document.getElementById('message-pin').textContent === 'Code incorrect'", timeout=10000)
    assert page.text_content("#message-pin") == "Code incorrect"
    assert page.evaluate("localStorage.getItem('sirose_pin')") is None


# ---- Rendu des cinq blocs (Task 4) -------------------------------------

import json

import pytest

from tablette.tests.conftest import RACINE

EXEMPLE = json.loads((RACINE / "exemple" / "dashboard.json").read_text(encoding="utf-8"))
MATIN = "2026-11-18T07:10:00+04:00"


def ouvrir_exemple(page, serveur, heure=MATIN):
    page.clock.set_fixed_time(heure)
    deverrouiller(page, serveur.url)
    page.wait_for_selector("#tableau:not([hidden])")


@pytest.mark.parametrize("donnees", [EXEMPLE])
def test_cinq_blocs_rendus(page, serveur):
    ouvrir_exemple(page, serveur)
    for bloc in ("priorites", "taches", "mails", "pipeline"):
        premier = EXEMPLE["blocs"][bloc]["elements"][0]["texte"]
        assert premier in page.text_content(f"#bloc-{bloc}")
    argent = page.text_content("#bloc-argent")
    assert "187" in argent and "1 500" in argent and "3 400" in argent
    h = page.text_content("#horodatage")
    assert "màj" in h and "prochaine" in h and "06:53" in h and "12:53" in h
    assert "↔ Client Exemple A (client)" in page.text_content("#bloc-mails")


@pytest.mark.parametrize("donnees", [EXEMPLE])
def test_limites(page, serveur):
    ouvrir_exemple(page, serveur)
    assert page.locator("#bloc-priorites li").count() == 3
    assert page.locator("#bloc-mails li").count() == 8
    assert "de trop" not in page.text_content("#tableau")


INDISPO = json.loads(json.dumps(EXEMPLE))
INDISPO["blocs"]["taches"]["etat"] = "indisponible"
INDISPO["blocs"]["taches"]["depuis"] = "2026-11-18T07:30:00+04:00"


@pytest.mark.parametrize("donnees", [INDISPO])
def test_bloc_indisponible(page, serveur):
    ouvrir_exemple(page, serveur)
    t = page.text_content("#bloc-taches")
    assert "source indisponible à 07:30" in t
    assert INDISPO["blocs"]["taches"]["elements"][0]["texte"] in t


@pytest.mark.parametrize("donnees", [EXEMPLE])
def test_donnees_perimees(page, serveur):
    ouvrir_exemple(page, serveur, heure="2026-11-18T15:30:00+04:00")  # 8 h 37 après genere_le
    assert "données du 18/11 06:53" in page.text_content("#bandeau")


@pytest.mark.parametrize("donnees", [EXEMPLE])
def test_donnees_fraiches_pas_de_bandeau(page, serveur):
    ouvrir_exemple(page, serveur)
    assert page.is_hidden("#bandeau")


@pytest.mark.parametrize("donnees", [EXEMPLE])
def test_hors_ligne_garde_affichage(page, serveur):
    ouvrir_exemple(page, serveur)
    serveur.retirer()
    page.evaluate("SIROSE.rafraichir()")
    page.wait_for_function("document.getElementById('bandeau').textContent.indexOf('hors ligne depuis') >= 0")
    assert EXEMPLE["blocs"]["mails"]["elements"][0]["texte"] in page.text_content("#bloc-mails")
    assert page.is_hidden("#ecran-pin")


@pytest.mark.parametrize("donnees", [EXEMPLE])
def test_rafraichir_met_a_jour(page, serveur):
    ouvrir_exemple(page, serveur)
    nouveau = json.loads(json.dumps(EXEMPLE))
    nouveau["blocs"]["mails"]["elements"][0]["texte"] = "Nouveau mail arrivé"
    serveur.publier(nouveau)
    page.evaluate("SIROSE.rafraichir()")
    page.wait_for_function("document.getElementById('bloc-mails').textContent.indexOf('Nouveau mail arrivé') >= 0")


@pytest.mark.parametrize("donnees", [EXEMPLE])
def test_huit_mails_visibles_en_1280x800(page, serveur):
    ouvrir_exemple(page, serveur)
    for bloc in ("mails", "taches", "pipeline"):
        boite = page.locator(f"#bloc-{bloc}").bounding_box()
        items = page.locator(f"#bloc-{bloc} li")
        dernier = items.nth(items.count() - 1).bounding_box()
        assert dernier["y"] + dernier["height"] <= boite["y"] + boite["height"], bloc
