from datetime import date

from tablette.publier.argent import bloc_argent, objectif_mois, phase


def test_objectifs():
    assert objectif_mois(date(2026, 11, 30)) == 1500
    assert objectif_mois(date(2026, 12, 1)) == 10000
    assert objectif_mois(date(2026, 8, 1)) == 300
    assert objectif_mois(date(2027, 7, 31)) == 25000
    assert objectif_mois(date(2027, 8, 1)) == 28000
    assert objectif_mois(date(2028, 3, 15)) == 41600


def test_phases():
    assert phase(date(2026, 11, 30)) == ("Phase 1", date(2026, 8, 1), date(2026, 11, 30))
    assert phase(date(2026, 12, 1)) == ("Phase 2", date(2026, 12, 1), date(2027, 7, 31))
    assert phase(date(2027, 8, 1))[0] == "Phase 3"


def test_reversement_payzen_sur_qonto_non_compte():
    """Payzen notifie le paiement client ; Qonto notifie 2 jours plus tard le reversement net (LYRA)."""
    p = [
        {"date": "2026-11-17", "montant": 187.0, "client": "Villa Naya", "origine": "payzen", "ref": "PZ-1"},
        {"date": "2026-11-19", "montant": 185.40, "client": "", "origine": "qonto", "contrepartie": "LYRA NETWORK"},
    ]
    assert bloc_argent([], p, date(2026, 11, 20))["mois"]["encaisse"] == 187.0


def test_virement_client_sur_qonto_compte():
    p = [{"date": "2026-11-10", "montant": 54.0, "client": "Asso", "origine": "qonto", "contrepartie": "ASSO KISANOU"}]
    assert bloc_argent([], p, date(2026, 11, 20))["mois"]["encaisse"] == 54.0


def test_meme_notification_lue_deux_fois_comptee_une_fois():
    n = {"date": "2026-11-17", "montant": 187.0, "client": "Villa Naya", "origine": "payzen", "ref": "PZ-1"}
    assert bloc_argent([], [n, dict(n)], date(2026, 11, 18))["mois"]["encaisse"] == 187.0


def test_deux_vrais_paiements_identiques_comptes():
    p = [
        {"date": "2026-11-17", "montant": 50.0, "client": "A", "origine": "payzen", "ref": "PZ-1"},
        {"date": "2026-11-17", "montant": 50.0, "client": "A", "origine": "payzen", "ref": "PZ-2"},
    ]
    assert bloc_argent([], p, date(2026, 11, 18))["mois"]["encaisse"] == 100.0


def test_cumul_phase_et_mois():
    p = [
        {"date": "2026-09-10", "montant": 88.0, "client": "Asso", "origine": "qonto"},
        {"date": "2026-11-17", "montant": 187.0, "client": "Villa Naya", "origine": "payzen"},
        {"date": "2026-07-01", "montant": 999.0, "client": "Hors phase", "origine": "qonto"},
    ]
    f = [{"date": "2026-11-02", "montant_ht": 450.0, "client": "Villa Naya", "ref": "F-1"}]
    b = bloc_argent(f, p, date(2026, 11, 18))
    assert b["etat"] == "ok"
    assert b["mois"] == {"libelle": "novembre 2026", "facture": 450.0, "encaisse": 187.0, "objectif": 1500}
    assert b["phase"] == {"nom": "Phase 1", "facture": 450.0, "encaisse": 275.0, "objectif": 3400}


def test_premier_jour_de_phase_2():
    p = [{"date": "2026-11-30", "montant": 100.0, "client": "A", "origine": "qonto"}]
    b = bloc_argent([], p, date(2026, 12, 1))
    assert b["mois"]["objectif"] == 10000 and b["mois"]["encaisse"] == 0
    assert b["phase"]["nom"] == "Phase 2" and b["phase"]["objectif"] == 137500 and b["phase"]["encaisse"] == 0
