"""Publie le tableau de bord : valide, fusionne avec l'état en ligne, chiffre, écrit dist/.

Usage : python3 -m tablette.publier.publier ENTREE.json --sortie dist/ [--precedent-url URL] [--argent ARGENT.json]
Le PIN est lu dans la variable d'environnement SIROSE_DASH_PIN.
"""
import argparse
import json
import os
import shutil
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from tablette.publier.crypto import chiffrer, dechiffrer
from tablette.publier.fusion import fusionner
from tablette.publier.schema import valider

REUNION = timezone(timedelta(hours=4))
RACINE = Path(__file__).resolve().parents[1]
FICHIERS_FIXES = ("index.html", "app.js", "netlify.toml")


def _precedent(url: str, pin: str) -> dict | None:
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return json.loads(dechiffrer(json.loads(r.read()), pin))
    except Exception as e:  # noqa: BLE001 — tout échec = pas d'état précédent
        print(f"avertissement : état précédent illisible ({e}) — publication sans reprise", file=sys.stderr)
        return None


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("entree")
    a.add_argument("--sortie", required=True)
    a.add_argument("--precedent-url")
    a.add_argument("--argent", help="JSON {factures, paiements} brut ; remplace blocs.argent")
    args = a.parse_args(argv)

    pin = os.environ.get("SIROSE_DASH_PIN", "")
    if not pin:
        print("erreur : variable SIROSE_DASH_PIN absente", file=sys.stderr)
        return 2

    d = json.loads(Path(args.entree).read_text(encoding="utf-8"))
    maintenant = datetime.now(REUNION)
    if args.argent:
        from tablette.publier.argent import bloc_argent
        brut = json.loads(Path(args.argent).read_text(encoding="utf-8"))
        d.setdefault("blocs", {})["argent"] = bloc_argent(brut["factures"], brut["paiements"], maintenant.date())

    erreurs = valider(d)
    if erreurs:
        print("erreur : dashboard invalide\n- " + "\n- ".join(erreurs), file=sys.stderr)
        return 2

    precedent = _precedent(args.precedent_url, pin) if args.precedent_url else None
    d = fusionner(d, precedent, maintenant)

    sortie = Path(args.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    for f in FICHIERS_FIXES:
        shutil.copy(RACINE / f, sortie / f)
    env = chiffrer(json.dumps(d, ensure_ascii=False).encode("utf-8"), pin)
    (sortie / "data.enc").write_text(json.dumps(env), encoding="utf-8")
    print(f"publié dans {sortie} ({len(d['blocs'])} blocs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
