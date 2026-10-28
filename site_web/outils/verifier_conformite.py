#!/usr/bin/env python3
"""Vérifie que le site généré (public/) respecte les obligations légales de Sir'Ose.

Contrôles bloquants (✘) : valeurs manquantes, mentions obligatoires absentes,
allégations interdites. Avertissements (!) : points à faire valider.
Code de sortie 1 s'il reste un contrôle bloquant.

Usage : python3 site_web/outils/verifier_conformite.py
"""
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PUBLIC = RACINE / "public"

# Allégations à risque — Règlement (CE) 1924/2006 (santé), Directive (UE) 2024/825
# et loi AGEC art. 13 (environnement), loi 96-603 art. 21 (« artisanal »),
# Règlement (UE) 2018/848 (« bio »).
ALLEGATIONS = {
    r"probioti": "allégation santé non autorisée dans l'UE (« probiotique »)",
    r"bon pour la (sant|digestion)|détox|detox|immunit|guéri|soigne": "allégation santé non autorisée (Règl. 1924/2006)",
    r"éco-?responsable|respectueux de l'environnement|écologique|neutre en carbone|biodégradable": "allégation environnementale générique interdite (Dir. 2024/825, loi AGEC)",
    r"\bbio\b|biologique": "terme « bio » réservé aux produits certifiés (Règl. 2018/848)",
    r"artisan": "« artisan/artisanal » réservé aux entreprises immatriculées comme artisans (loi 96-603 art. 21)",
}
MESSAGE_EVIN = "L'abus d'alcool est dangereux pour la santé, à consommer avec modération."
MENTIONS_LEGALES = ["Raison sociale", "Capital social", "Siège social", "Immatriculation", "TVA intracommunautaire",
                    "Courriel", "Téléphone", "Directeur de la publication", "Hébergeur"]


def main():
    if not PUBLIC.exists():
        sys.exit("Le dossier public/ n'existe pas : lancez d'abord outils/generer.py")
    config = json.loads((RACINE / "config" / "sirose.json").read_text(encoding="utf-8"))
    pages = {p.name: p.read_text(encoding="utf-8") for p in PUBLIC.glob("*.html")}
    erreurs, alertes = [], []

    for nom, contenu in pages.items():
        n = contenu.count("[À COMPLÉTER]")
        if n:
            erreurs.append(f"{nom} : {n} champ(s) [À COMPLÉTER] — remplir config/sirose.json")
        for lien in ("mentions-legales.html", "cgv.html", "confidentialite.html"):
            if lien not in contenu:
                erreurs.append(f"{nom} : lien vers {lien} absent du pied de page")
        if config["vente"]["vente_alcool"]:
            if MESSAGE_EVIN not in contenu:
                erreurs.append(f"{nom} : message sanitaire Loi Évin absent (art. L3323-4 CSP)")
            if 'id="controle-age"' not in contenu:
                erreurs.append(f"{nom} : contrôle d'âge absent (art. L3342-1 CSP)")
        elif re.search(r"\balcool|\brhum|\bliqueur|\bpunch\b|\bcocktail.{0,40}\b(rhum|alcool)", re.sub(r"<[^>]+>", " ", contenu), flags=re.I):
            alertes.append(f"{nom} : mention d'alcool alors que vente_alcool est à false — toute référence à une boisson alcoolisée déclenche la Loi Évin")
        if config["financement_ue"]["actif"] and "Cofinancé par l'Union européenne" not in contenu:
            erreurs.append(f"{nom} : mention FEDER « Cofinancé par l'Union européenne » absente (Règl. 2021/1060 art. 47 et 50)")
        if "<html lang=\"fr\">" not in contenu:
            alertes.append(f"{nom} : attribut lang=\"fr\" manquant (accessibilité)")
        texte = re.sub(r"<[^>]+>", " ", contenu)
        for motif, raison in ALLEGATIONS.items():
            for m in re.finditer(motif, texte, flags=re.I):
                extrait = texte[max(0, m.start() - 30):m.end() + 30].replace("\n", " ").strip()
                alertes.append(f"{nom} : {raison} → « …{extrait}… »")

    mentions = pages.get("mentions-legales.html", "")
    for libelle in MENTIONS_LEGALES:
        if libelle not in mentions:
            erreurs.append(f"mentions-legales.html : « {libelle} » manquant (LCEN art. 1-1)")

    cgv = pages.get("cgv.html", "")
    for attendu, ref in [("Formulaire type de rétractation", "art. L221-5 C. conso"),
                         ("garantie légale de conformité", "art. L217-3 C. conso"),
                         ("médiateur de la consommation", "art. L612-1 C. conso")]:
        if attendu not in cgv:
            erreurs.append(f"cgv.html : « {attendu} » absent ({ref})")

    for p in config["produits"]:
        if p["alcool"] and not p["degre"]:
            erreurs.append(f"Produit « {p['nom']} » : titre alcoométrique manquant")
        if re.search(r"\bcl\b|\bL\b", p["format"]) and not p["prix_litre"]:
            erreurs.append(f"Produit « {p['nom']} » : prix au litre manquant (prix à l'unité de mesure, Directive 98/6/CE)")

    if config["societe"].get("tva_intracom_a_verifier"):
        alertes.append("N° TVA intracommunautaire calculé à partir du SIREN : le confirmer sur le site de l'Union européenne (VIES) puis passer tva_intracom_a_verifier à false")
    if config["vente"]["vente_en_ligne"]:
        alertes.append("Vente en ligne activée : prévoir le bouton « Commande avec obligation de paiement » (art. L221-14 C. conso) et la case d'acceptation des CGV")

    for e in erreurs:
        print(f"  ✘ {e}")
    for a in alertes:
        print(f"  ! {a}")
    print(f"\n{len(erreurs)} point(s) bloquant(s), {len(alertes)} avertissement(s).")
    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()
