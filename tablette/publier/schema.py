"""Validation du dashboard.json (schéma v1) + garde-fou contre les données sensibles."""
import re
from datetime import datetime

BLOCS = ("priorites", "taches", "mails", "pipeline", "argent")
SOURCES = {"gmail", "notion", "drive", "registre"}
URGENCES = {"haute", "moyenne", "basse"}
ETATS = {"ok", "indisponible"}
_SENSIBLE = [
    ("IBAN", re.compile(r"\bFR\d{2}(?:\s?[0-9A-Z]){10,}", re.I)),
    ("n° de sécurité sociale", re.compile(r"(?<!\d)[12](?:[ .]?\d){12}(?:[ .]?\d{2})?(?!\d)")),
]


def _date_ok(v) -> bool:
    try:
        datetime.fromisoformat(v)
        return True
    except (TypeError, ValueError):
        return False


def _textes(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _textes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _textes(v)


def valider(d: dict) -> list[str]:
    err = []
    if d.get("schema") != 1:
        err.append("schema doit valoir 1")
    for champ in ("genere_le", "prochaine_maj"):
        if not _date_ok(d.get(champ)):
            err.append(f"{champ} : date ISO 8601 attendue")
    blocs = d.get("blocs") or {}
    for nom in BLOCS:
        b = blocs.get(nom)
        if not isinstance(b, dict):
            err.append(f"bloc {nom} manquant")
            continue
        if b.get("etat") not in ETATS:
            err.append(f"{nom}.etat invalide")
        if b.get("depuis") is not None and not _date_ok(b["depuis"]):
            err.append(f"{nom}.depuis invalide")
        for i, x in enumerate(b.get("elements", [])):
            ici = f"{nom}.elements[{i}]"
            if not isinstance(x.get("texte"), str) or not x["texte"].strip():
                err.append(f"{ici}.texte vide")
            if x.get("source") not in SOURCES:
                err.append(f"{ici}.source inconnue : {x.get('source')!r}")
            if x.get("urgence") not in URGENCES:
                err.append(f"{ici}.urgence invalide")
            if x.get("echeance") is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(x["echeance"])):
                err.append(f"{ici}.echeance doit être AAAA-MM-JJ")
    for t in _textes(d):
        for nom, motif in _SENSIBLE:
            if motif.search(t):
                err.append(f"donnée sensible ({nom}) détectée : publication refusée")
    return err
