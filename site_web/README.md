# Site web SIR'OTÉ — SAS Sir'Ose

Générateur de site vitrine personnalisé pour Sir'Ose, avec les pages légales et un vérificateur de conformité.

## Ce qu'il contient

```
site_web/
├── config/sirose.json        ← LE fichier à modifier : identité, produits, prix, hébergeur…
├── modeles/                  ← pages HTML (accueil, mentions légales, CGV, confidentialité)
│   ├── _partiels/            ← en-tête, pied de page, contrôle d'âge
│   └── assets/               ← style.css, app.js, emblème UE, favicon
├── outils/
│   ├── generer.py            ← fabrique le site dans public/
│   └── verifier_conformite.py← liste ce qui manque avant la mise en ligne
├── OBLIGATIONS_LEGALES.md    ← la checklist de toutes les obligations, avec les références
└── public/                   ← le site prêt à mettre en ligne (généré, non versionné)
```

## Utilisation

1. Remplir les champs `A_COMPLETER` de `config/sirose.json` (e-mail, téléphone, hébergeur, médiateur, licence, ingrédients et allergènes de chaque produit).
2. Générer le site :

```bash
python3 site_web/outils/generer.py
```

3. Vérifier la conformité. Tant qu'un point est bloquant (✘), ne pas mettre en ligne :

```bash
python3 site_web/outils/verifier_conformite.py
```

4. Ouvrir `site_web/public/index.html` dans un navigateur pour relire, puis envoyer le contenu de `public/` chez l'hébergeur (voir le choix de l'hébergeur et du nom de domaine dans `OBLIGATIONS_LEGALES.md` §10).

Python 3 suffit, sans aucune installation.

## Personnaliser

- **Ajouter un produit** : copier un bloc dans `produits` de `config/sirose.json`. Pour une boisson alcoolisée, mettre `"alcool": true` et `"degre": "5 %"`.
- **Alcool** : `"vente_alcool"` est à `false` (aucune boisson alcoolisée vendue). Le passer à `true` le jour où un produit alcoolisé est vendu : le contrôle d'âge et le message Loi Évin s'ajoutent automatiquement.
- **Couleurs et polices** : variables en haut de `modeles/assets/style.css`.
- **Textes de l'accueil** : `modeles/index.html`.

Les champs non remplis s'affichent en **jaune [À COMPLÉTER]** sur le site pour être repérés au premier coup d'œil.

## Avec Claude

Le skill `.claude/skills/sirose-site-web` permet de demander à Claude, par exemple : « ajoute un nouveau koso 33 cl à 4,50 € », « crée une page Ateliers », « vérifie que mon texte respecte la loi Évin ». Il connaît les règles du fichier `OBLIGATIONS_LEGALES.md`.
