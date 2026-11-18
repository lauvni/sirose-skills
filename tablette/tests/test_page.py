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
