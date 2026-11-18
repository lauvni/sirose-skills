"""Bloc « Argent » : facturé / encaissé vs objectifs du BP v2.0 (doc 02, M1 = août 2026)."""
import re
from datetime import date

MOIS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
           "septembre", "octobre", "novembre", "décembre"]

# Objectifs CA HT mensuels, dans l'ordre à partir d'août 2026 (M1).
_OBJECTIFS = (
    [300, 600, 1000, 1500]                                            # Phase 1 : M1-M4
    + [10000, 12000, 14000, 16000, 18000, 20000, 22500, 25000]       # Phase 2 : M5-M12
    + [28000, 30500, 33000, 35500, 38000, 40000] + [41600] * 6       # Phase 3 : M13-M24
)
PLATEAU = 41600
_PHASES = [("Phase 1", 1, 4), ("Phase 2", 5, 12), ("Phase 3", 13, 24)]


def _rang(jour: date) -> int:
    """Numéro de mois BP : août 2026 = 1."""
    return (jour.year - 2026) * 12 + jour.month - 7


def _debut_mois(rang: int) -> date:
    n = rang + 6  # 0 = janvier 2026
    return date(2026 + n // 12, n % 12 + 1, 1)


def _fin_mois(rang: int) -> date:
    suivant = _debut_mois(rang + 1)
    return date.fromordinal(suivant.toordinal() - 1)


def objectif_mois(jour: date) -> int:
    r = _rang(jour)
    if r < 1:
        return 0
    return _OBJECTIFS[r - 1] if r <= len(_OBJECTIFS) else PLATEAU


def phase(jour: date) -> tuple[str, date, date]:
    r = _rang(jour)
    for nom, debut, fin in _PHASES:
        if debut <= r <= fin:
            return nom, _debut_mois(debut), _fin_mois(fin)
    if r < 1:
        return "Avant lancement", date(2025, 10, 9), _fin_mois(0)
    return "Croisière", _debut_mois(25), date(9999, 12, 31)


def _objectif_periode(debut: date, fin: date) -> int:
    total, r = 0, _rang(debut)
    while _debut_mois(r) <= fin and r <= 240:
        total += objectif_mois(_debut_mois(r))
        r += 1
    return total


# Reversements du prestataire carte (Payzen / Lyra) vers Qonto : déjà comptés via la notification Payzen.
_REVERSEMENT_CARTE = re.compile(r"lyra|payzen", re.I)


def _encaissements(paiements: list[dict]) -> list[dict]:
    """Règle : Payzen = paiements carte (comptés) ; Qonto = crédits hors reversements Payzen/Lyra.
    Une même notification lue deux fois (même origine, même ref) ne compte qu'une fois."""
    vus, out = set(), []
    for p in paiements:
        if p.get("origine") == "qonto" and _REVERSEMENT_CARTE.search(str(p.get("contrepartie", ""))):
            continue
        ref = p.get("ref")
        if ref:
            cle = (p.get("origine"), str(ref))
            if cle in vus:
                continue
            vus.add(cle)
        out.append(p)
    return out


def _somme(lignes, champ, debut: date, fin: date) -> float:
    return round(sum(float(x[champ]) for x in lignes
                     if debut <= date.fromisoformat(x["date"]) <= fin), 2)


def bloc_argent(factures: list[dict], paiements: list[dict], aujourd_hui: date) -> dict:
    paiements = _encaissements(paiements)
    debut_mois = aujourd_hui.replace(day=1)
    nom, debut_phase, fin_phase = phase(aujourd_hui)
    return {
        "etat": "ok",
        "depuis": None,
        "elements": [],
        "mois": {
            "libelle": f"{MOIS_FR[aujourd_hui.month - 1]} {aujourd_hui.year}",
            "facture": _somme(factures, "montant_ht", debut_mois, aujourd_hui),
            "encaisse": _somme(paiements, "montant", debut_mois, aujourd_hui),
            "objectif": objectif_mois(aujourd_hui),
        },
        "phase": {
            "nom": nom,
            "facture": _somme(factures, "montant_ht", debut_phase, aujourd_hui),
            "encaisse": _somme(paiements, "montant", debut_phase, aujourd_hui),
            "objectif": _objectif_periode(debut_phase, fin_phase),
        },
    }
