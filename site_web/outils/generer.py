#!/usr/bin/env python3
"""Génère le site statique Sir'Ose (public/) à partir de modeles/ et config/sirose.json.

Syntaxe des modèles :
  {{ societe.siren }}      -> valeur de la config (chemin pointé)
  {{> pied }}              -> inclusion de modeles/_partiels/pied.html
  {{ produits_html }}      -> cartes produits générées
  {{ si vente_alcool }}...{{ fin }}  -> bloc conditionnel (vente.vente_alcool)

Usage : python3 site_web/outils/generer.py
"""
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MODELES = RACINE / "modeles"
PARTIELS = MODELES / "_partiels"
SORTIE = RACINE / "public"
A_COMPLETER = "A_COMPLETER"

DRAPEAUX = {
    "vente_alcool": lambda c: c["vente"]["vente_alcool"],
    "vente_en_ligne": lambda c: c["vente"]["vente_en_ligne"],
    "financement_ue": lambda c: c["financement_ue"]["actif"],
}


def valeur(config, chemin):
    noeud = config
    for cle in chemin.split("."):
        noeud = noeud[cle]
    if noeud == A_COMPLETER:
        return '<mark class="a-completer">[À COMPLÉTER]</mark>'
    return html.escape(str(noeud))


def cartes_produits(config):
    cartes = []
    for p in config["produits"]:
        def champ(v):
            if v == A_COMPLETER:
                return '<mark class="a-completer">[À COMPLÉTER]</mark>'
            return html.escape(v)

        prix_litre = f'<span class="prix-litre">soit {champ(p["prix_litre"])}</span>' if p["prix_litre"] else ""
        degre = f'<span class="badge">{champ(p["degre"])} vol.</span>' if p["alcool"] else ""
        cartes.append(f"""      <article class="carte-produit">
        <h3>{champ(p["nom"])} {degre}</h3>
        <p class="format">{champ(p["format"])}</p>
        <p>{champ(p["description"])}</p>
        <p class="prix">{champ(p["prix_ttc"])} <small>TTC</small> {prix_litre}</p>
        <details>
          <summary>Ingrédients &amp; allergènes</summary>
          <p><strong>Ingrédients :</strong> {champ(p["ingredients"])}</p>
          <p><strong>Allergènes :</strong> {champ(p["allergenes"])}</p>
        </details>
      </article>""")
    return "\n".join(cartes)


def rendre(texte, config, extras):
    texte = re.sub(r"\{\{>\s*(\w+)\s*\}\}", lambda m: (PARTIELS / f"{m.group(1)}.html").read_text(encoding="utf-8"), texte)

    def conditionnel(m):
        return m.group(2) if DRAPEAUX[m.group(1)](config) else ""

    texte = re.sub(r"\{\{\s*si\s+(\w+)\s*\}\}(.*?)\{\{\s*fin\s*\}\}", conditionnel, texte, flags=re.S)

    def remplacer(m):
        cle = m.group(1)
        return extras[cle] if cle in extras else valeur(config, cle)

    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", remplacer, texte)


def main():
    config = json.loads((RACINE / "config" / "sirose.json").read_text(encoding="utf-8"))
    extras = {
        "produits_html": cartes_produits(config),
        "date_maj": date.today().strftime("%d/%m/%Y"),
        "annee": str(date.today().year),
    }
    if SORTIE.exists():
        shutil.rmtree(SORTIE)
    shutil.copytree(MODELES / "assets", SORTIE / "assets")
    for modele in sorted(MODELES.glob("*.html")):
        # Deux passes : les partiels inclus peuvent eux-mêmes contenir des variables.
        rendu = rendre(rendre(modele.read_text(encoding="utf-8"), config, extras), config, extras)
        (SORTIE / modele.name).write_text(rendu, encoding="utf-8")
        print(f"  ✔ {modele.name}")
    print(f"Site généré dans {SORTIE}")


if __name__ == "__main__":
    main()
