---
name: sirose-site-web
description: Créer, modifier ou vérifier le site web SIR'OTÉ de la SAS Sir'Ose (site_web/). Utiliser pour toute demande sur le site, ses produits, ses pages légales (mentions légales, CGV, confidentialité), la Loi Évin, les allégations santé/environnement ou la mise en ligne.
---

# Site web SIR'OTÉ

Le site est généré depuis `site_web/config/sirose.json` et `site_web/modeles/` par `site_web/outils/generer.py`. Ne jamais modifier `site_web/public/` à la main : il est écrasé à chaque génération.

## Méthode

1. Lire `site_web/OBLIGATIONS_LEGALES.md` avant toute modification de texte.
2. Données (identité, produits, prix, contacts) → `config/sirose.json`. Mise en page et textes fixes → `modeles/`. Éléments communs → `modeles/_partiels/`.
3. Une nouvelle page = un nouveau fichier `modeles/*.html` qui inclut `{{> tete }}`, `{{> entete }}` et `{{> pied }}` (le pied porte le message Loi Évin, la mention FEDER et les liens légaux) ; ajouter le lien dans le menu de `_partiels/entete.html`.
4. Toujours finir par :
   - `python3 site_web/outils/generer.py`
   - `python3 site_web/outils/verifier_conformite.py`
   et rapporter les points bloquants restants à l'utilisateur.

## Règles de rédaction (non négociables)

- **Ne jamais inventer** une donnée légale (e-mail, téléphone, hébergeur, licence, médiateur, ingrédients, allergènes, degré). Laisser `A_COMPLETER` et le signaler.
- **Aucune référence à l'alcool** : Sir'Ose ne vend pas d'alcool (`vente_alcool: false`) ; ne citer ni rhum, ni cocktail alcoolisé, ni partenaire de boisson alcoolisée, sinon la Loi Évin s'applique. Si l'utilisateur annonce la vente d'un produit alcoolisé, repasser `vente_alcool` à `true` et appliquer la Loi Évin : informations objectives seulement (degré, origine, composition, élaboration, terroir, goût). Pas d'association à la fête, la séduction, le sport, la réussite ; pas de cible jeune.
- **Aucune allégation santé** : pas de « probiotique », « détox », « digestion », « immunité », « bienfaits ».
- **Aucune allégation environnementale générique** (« éco-responsable », « zéro déchet », « 100 % circulaire », « durable ») : décrire des faits précis et prouvables.
- Pas de « bio » ni d'« artisanal » sans justificatif.
- Prix toujours TTC pour les particuliers, avec prix au litre pour les liquides ; les prix HT sont réservés à la section professionnels.
- Langue : français, ton chaleureux et péi, sans jargon technique inutile.

## Contexte entreprise

Données de référence dans `docs/business_plan_500k/01_audit_fichiers.md` (SIREN, adresses, gamme, prix, partenaires). Site financé par KAP Numérique (FEDER 80 %) : la mention « Cofinancé par l'Union européenne » doit rester sur toutes les pages.
