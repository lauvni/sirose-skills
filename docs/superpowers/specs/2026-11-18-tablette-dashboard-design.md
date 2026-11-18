# Tablette de pilotage Sir'Ose + agent ARGOS — Document de conception

*18 novembre 2026 — Alexandre STEINER (DG) — statut : à valider*

## 1. Intention

Alexandre veut **suivre rapidement l'activité de Sir'Ose depuis chez lui**, d'un coup d'œil, sans ouvrir l'ordinateur ni trier sa boîte mail. Une vieille tablette Samsung Galaxy Tab 3 10.1 (GT-P5210, Android 4.4.2, build KOT49H.P5210XXUBNK2) devient un écran fixe qui affiche une synthèse à jour.

Un **agent dédié** va chercher les informations dans **Gmail, Notion et Google Drive**, **les relie entre elles** (un mail ↔ le client ou le financeur Notion ↔ la facture Drive) et produit la synthèse.

La tablette sert **uniquement à lire**. Alexandre agit ensuite depuis l'**application Claude sur son téléphone** (« relance Villa Naya », « crée la tâche pour le greffe »…).

## 2. Objectifs, non-objectifs, anti-objectifs

**Objectifs**
- Un écran unique, lisible à 1-2 m, compréhensible en moins de 30 secondes.
- Mise à jour automatique plusieurs fois par jour, sans aucune action d'Alexandre.
- Des liens explicites entre les sources : chaque élément affiché indique d'où il vient (Gmail, Notion ou Drive) et à quoi il se rattache.

**Non-objectifs**
- Aucune interaction sur la tablette : pas de saisie, pas de chat, pas de boutons d'action.
- L'agent n'écrit **nulle part** : ni dans Notion, ni dans Gmail, ni dans Drive. Il est en lecture seule.
- Pas de remplacement de Notion : le pilotage détaillé reste dans « Sir'Ose — Pilotage ».

**Anti-objectifs** (échec même si « ça marche »)
- Des données sensibles lisibles par quelqu'un qui obtient l'adresse de la page.
- L'affichage de pièces d'identité, de RIB/IBAN, de CV, de justificatifs personnels (EDF, Pôle emploi) ou de montants d'aides sociales (ARE, RSA).
- Un écran saturé de bruit : notifications Instagram, newsletters Indy ou Clementine, promotions.
- Des chiffres inventés. Si une source est inaccessible, l'écran le signale au lieu de remplir le vide.

## 3. Contraintes

### 3.1 La tablette
- Android 4.4.2. Le dernier Chrome installable est **Chrome 81**. Le navigateur d'origine est trop ancien pour être utilisé. Les applications Claude, Notion et Google Docs ne fonctionnent pas sur cette version.
- La page doit être **légère, sans framework**, en **ES5** (pas de modules ES, pas de syntaxe récente sans transpilation). Le CSS doit rester simple (flexbox autorisé, `grid` à éviter).
- **Certificats HTTPS (risque n°1)** : Netlify utilise des certificats Let's Encrypt (racine ISRG Root X1), qu'Android 4.4 ne reconnaît pas nativement. Chrome sous Android utilise le magasin de certificats du système. Deux parades sont à valider sur l'appareil réel **avant tout autre développement** :
  1. installer le certificat racine ISRG Root X1 comme certificat utilisateur (Paramètres › Sécurité › Installer depuis la mémoire) ;
  2. à défaut, utiliser Firefox 68 (dernier Firefox compatible avec Android 4.4, qui embarque son propre magasin de certificats).
- **Mode kiosque** : écran toujours allumé (option développeur « Rester activé » sur secteur), page en plein écran, rechargement automatique. L'application kiosque exacte (Fully Kiosk ancienne version, raccourci plein écran Chrome…) est laissée au choix du constructeur, selon ce qui fonctionne sous 4.4.

### 3.2 Les sources (repérage du 18/11/2026)
- **Notion** : page « Sir'Ose — Pilotage », avec trois bases : **Tâches Sir'Ose**, **Clients & prospects** (Villa Naya, Palm Hotel, Mercure Creolia, Cassonade Café, Les Vendanges, Blue Margouillat…) et **Financeurs** (BPI France Réunion, CEPAC, BFCOI…).
- **Gmail** : boîte contact.sirose@gmail.com, environ 480 non lus, dont beaucoup de bruit. Expéditeurs à signal fort : DGFiP, greffe du TMC de Saint-Pierre, INPI / guichet entreprises, Qonto, Payzen (paiements), Lucien MOREAU, clients et financeurs présents dans Notion.
- **Drive** : factures (ex. « Facture F-2026-001 — Villa Naya »), dossiers de financement, mais aussi un dossier « Pièces associés » contenant des pièces d'identité, des RIB et des CV. Ce dossier est **exclu**.
- **Dépôt** : `docs/business_plan_500k/` (trajectoire et objectifs par phase) et le registre de conformité de THEMIS (`docs/conformite/registre_obligations.md`, sur la branche `claude/dazzling-planck-ox772a`, pas encore fusionnée) pour les échéances légales. *Choix de Claude :* tant que la branche n'est pas fusionnée, ARGOS lit le registre directement sur cette branche (`git show`). S'il est absent, le bloc ② l'indique sans échouer.
- **Compte Google** : les connecteurs Gmail et Drive sont déjà connectés à **contact.sirose@gmail.com**, le compte qui contient la boîte pro et les factures (vérifié le 18/11).

### 3.3 L'exécution
- L'agent tourne comme une **tâche planifiée Claude Code dans le cloud** (une nouvelle session à chaque déclenchement), avec les connecteurs Gmail, Notion, Google Drive et Netlify.
- Fuseau horaire : Indian/Reunion.

## 4. Approches envisagées

| | Approche | Avantages | Inconvénients |
|---|---|---|---|
| **A** ✅ | Tâche Claude planifiée dans le cloud qui publie une page statique sur Netlify, affichée par la tablette en kiosque | Aucun matériel, pas de clé API, rien à maintenir, connecteurs déjà branchés | Lecture seule, page hébergée sur Internet (d'où le chiffrement) |
| B | Serveur maison (Raspberry Pi) + API Claude + API Google et Notion, page servie en Wi-Fi local | Données qui restent chez soi, interactivité possible | Matériel (~80 €), coût API, clés OAuth à créer, maintenance |
| C | Synthèse écrite dans un Google Doc ou une page Notion | Très simple | Notion et Docs inutilisables sous Android 4.4 |

**Choix d'Alexandre : A.** B reste une évolution possible si l'interactivité sur la tablette devient utile.

## 5. Conception retenue

### 5.1 Vue d'ensemble

```
 [Tâche planifiée 3×/jour]
        │  session Claude Code cloud, agent ARGOS
        ├─ lit Notion (Tâches, Clients & prospects, Financeurs)
        ├─ lit Gmail (14 derniers jours, filtré)
        ├─ lit Drive (factures, dossiers de financement — hors « Pièces associés »)
        ├─ relie les éléments → dashboard.json
        ├─ chiffre dashboard.json avec le code PIN → data.enc
        └─ déploie site statique (index.html fixe + data.enc) sur Netlify
                                   │
 [Tablette GT-P5210, Chrome 81, kiosque]
        └─ ouvre l'URL secrète, PIN mémorisé localement,
           déchiffre et affiche, recharge data.enc toutes les 15 min
```

### 5.2 L'agent ARGOS
- Nom proposé : **ARGOS**, le gardien aux cent yeux. Il s'inscrit dans le panthéon existant (ZEUS, HERMES, THEMIS). *Choix de Claude, modifiable.*
- Défini dans `.claude/agents/argos.md`, au même format que `hermes.md` : frontmatter `name` / `description`, contexte à charger, missions, règles.
- **Lecture seule stricte.** Il n'utilise aucun outil d'écriture Gmail, Notion ou Drive. Son seul effet de bord est la publication du site.
- **Règles de filtrage Gmail** : exclure les catégories promotions et réseaux sociaux, ainsi que les expéditeurs de bruit identifiés (notifications Instagram, newsletters). Ne garder que les mails qui appellent une action ou portent une information d'argent (paiement reçu, facture, relance, échéance administrative).
- **Liaison** : pour chaque mail retenu, chercher le client, le financeur ou la tâche Notion correspondant (par nom ou domaine d'expéditeur), puis la facture ou le document Drive associé. Chaque élément affiché porte sa source et son rattachement.
- **Confidentialité** : ne jamais lire ni citer le dossier Drive « Pièces associés », les pièces d'identité, les RIB/IBAN, les CV, les justificatifs personnels, ni les montants d'aides sociales des fondateurs.
- **Honnêteté** : si une source échoue (connecteur indisponible, quota atteint), le bloc concerné affiche « source indisponible à HH:MM » et l'agent conserve les dernières données valides, avec leur horodatage. *Choix de Claude :* chaque session repartant de zéro, l'agent retélécharge le `data.enc` en ligne et le déchiffre pour retrouver l'état précédent. Rien n'est stocké en clair ailleurs.

### 5.3 Contenu de l'écran (paysage 1280×800)

```
┌──────────────────────────────────────────────────────────────┐
│ SIR'OSE · mercredi 18 novembre        màj 07:30 · prochaine 13:00 │
├──────────────────────────────────────────────────────────────┤
│ ① PRIORITÉS DU JOUR (3 lignes rédigées par ARGOS)            │
├──────────────────────────────┬───────────────────────────────┤
│ ② TÂCHES — en retard / ≤ 7 j │ ③ MAILS À TRAITER             │
│  (Notion)                    │  expéditeur · objet · ↔ lien   │
├──────────────────────────────┼───────────────────────────────┤
│ ④ PIPELINE                   │ ⑤ ARGENT                      │
│  clients & financeurs par    │  factures émises / paiements   │
│  statut (Notion)             │  reçus vs objectif de la phase │
└──────────────────────────────┴───────────────────────────────┘
```

- ① 3 priorités maximum, chacune formulée comme une commande à dicter ensuite dans l'app Claude.
- ② Tâches de la base Notion **Tâches Sir'Ose**, non terminées, en retard ou à échéance dans les 7 jours, **et** échéances légales du registre THEMIS à 30 jours maximum (source `registre`). *Choix de Claude.*
- ③ 8 mails maximum, triés par urgence, chacun avec son rattachement (« ↔ Villa Naya (client) », « ↔ BPI (financeur) »).
- ④ Nombre de clients et financeurs par statut, et les 3 dernières évolutions.
- ⑤ CA facturé et encaissé sur la période, comparé à l'objectif de la phase du BP v2.0 (doc 02).
- Lisibilité : texte d'au moins 18 px, fort contraste, thème sombre (écran allumé en permanence, chez soi).

### 5.4 Format des données
- L'agent produit un `dashboard.json` avec une **version de schéma**, `genere_le` (ISO 8601), et un objet par bloc (①–⑤). Chaque élément contient `texte`, `source` (gmail | notion | drive | registre), `lien_vers` (libellé de l'élément rattaché) et `urgence` (haute | moyenne | basse).
- La page `index.html` est fixe et versionnée dans le dépôt. Seul `data.enc` change à chaque exécution.

### 5.5 Confidentialité de la page
- `dashboard.json` est chiffré en **AES-GCM**, avec une clé dérivée d'un **code PIN / phrase de passe** par **PBKDF2-SHA256** (sel aléatoire, nombre d'itérations réglé pour rester rapide sur la tablette). La page déchiffre avec WebCrypto (disponible dans Chrome 81, en HTTPS).
- Le PIN est saisi une fois sur la tablette et mémorisé dans `localStorage`. Quiconque obtient l'URL ne voit qu'un champ PIN.
- L'URL Netlify est non devinable et non indexée (`noindex`, pas de lien public).
- Le PIN n'est **jamais** écrit dans le dépôt. Alexandre le fournit à l'environnement d'exécution de la tâche planifiée : le constructeur choisit le mécanisme le plus sûr disponible et l'explique à Alexandre.

### 5.6 Fréquence
- 3 exécutions par jour, heure de La Réunion : **≈ 7h00, 12h30, 18h30** (minutes décalées légèrement, au choix du constructeur).
- La tablette recharge `data.enc` toutes les 15 minutes, ce qui suffit à capter chaque nouvelle publication.

### 5.7 Emplacement dans le dépôt
- Développement sur la branche `claude/intelligent-curie-cq1hqt`. La tâche planifiée pointe sur la branche qui contient `argos.md` et `tablette/`, puis sur la branche par défaut une fois la fusion faite (décision d'Alexandre).
- `.claude/agents/argos.md` : définition de l'agent.
- `tablette/` : `index.html`, script de chiffrement, `README.md` (installation de la tablette pas à pas, en français, pour un non-développeur).
- `docs/agents/argos/` : règles de filtrage et de liaison, détaillées et maintenables.

## 6. Ce qui est laissé au constructeur
- Le choix de l'application kiosque et la procédure exacte de mise en veille ou de réveil de l'écran.
- La méthode de déploiement Netlify depuis une session planifiée (connecteur Netlify ou CLI), à valider de bout en bout.
- Le langage du script de chiffrement (Python recommandé, déjà utilisé dans le dépôt).
- Le détail visuel de la page, dans le respect du § 5.3.
- Les heures exactes et le décalage des minutes des exécutions.

## 7. Ordre de construction conseillé
1. **Test sur l'appareil** : une page « hello » en HTTPS sur Netlify, chiffrée et déchiffrée avec WebCrypto, ouverte dans Chrome 81 sur la GT-P5210. Si le certificat ou WebCrypto échoue, on revoit la conception avant d'aller plus loin.
2. La page `index.html` avec un `dashboard.json` d'exemple.
3. L'agent ARGOS (lecture des sources, liaison, JSON), lancé à la main.
4. Le chiffrement et le déploiement automatisés.
5. La tâche planifiée et le guide d'installation de la tablette.
