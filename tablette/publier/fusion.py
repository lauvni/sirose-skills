"""Un bloc indisponible reprend les dernières données connues, marquées avec l'heure de la panne."""
import copy
from datetime import datetime

_CHAMPS_REPRIS = ("elements", "mois", "phase")


def fusionner(nouveau: dict, precedent: dict | None, maintenant: datetime) -> dict:
    out = copy.deepcopy(nouveau)
    anciens = (precedent or {}).get("blocs", {})
    for nom, bloc in out.get("blocs", {}).items():
        if bloc.get("etat") != "indisponible":
            continue
        ancien = anciens.get(nom) or {}
        for champ in _CHAMPS_REPRIS:
            if champ in ancien:
                bloc[champ] = copy.deepcopy(ancien[champ])
        if not bloc.get("depuis"):
            deja = ancien.get("etat") == "indisponible" and ancien.get("depuis")
            bloc["depuis"] = deja or maintenant.isoformat(timespec="seconds")
    return out
