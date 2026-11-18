# Tablette de pilotage Sir'Ose

Écran fixe à la maison qui affiche, 3 fois par jour, la synthèse préparée par l'agent **ARGOS** à partir de Gmail, Notion et Google Drive.
La tablette ne fait que **lire**. Pour agir (relancer un client, créer une tâche…), utilisez l'application Claude sur votre téléphone.

Tablette : Samsung Galaxy Tab 3 10.1 — GT-P5210 — Android 4.4.2.

---

## 1. Préparer la tablette (une seule fois)

### 1.1 Mettre Chrome à jour
1. Ouvrir **Play Store**, chercher **Chrome**, appuyer sur **Mettre à jour**.
   La dernière version possible sur cette tablette est la 81 : c'est normal.
2. Ne pas utiliser le navigateur « Internet » d'origine Samsung, il est trop ancien.

### 1.2 Installer le certificat de sécurité (indispensable)
La page est hébergée en HTTPS avec un certificat **Let's Encrypt**, qu'Android 4.4 ne connaît pas d'origine. Sans cette étape, Chrome affiche « Votre connexion n'est pas privée ».

1. Sur la tablette, dans Chrome, ouvrir : `http://x1.i.lencr.org/` → un fichier `isrgrootx1.der` (ou `.crt`) est téléchargé.
   *Si la page ne s'ouvre pas, télécharger le fichier « ISRG Root X1 (DER) » depuis letsencrypt.org/certificates sur un ordinateur et le copier dans le dossier `Download` de la tablette par câble USB.*
2. **Paramètres** › **Sécurité** › **Installer depuis la mémoire** (ou « Installer à partir de la carte SD »).
3. Choisir le fichier, lui donner le nom **ISRG Root X1**, usage **VPN et applications**, puis **OK**.
4. Android demande un code de verrouillage d'écran s'il n'y en a pas : en créer un (code PIN de l'écran de la tablette, différent du code du tableau de bord si vous voulez).

**Plan B** si le certificat ne passe toujours pas : installer **Firefox 68** (dernière version compatible Android 4.4, depuis l'APK officiel de Mozilla : archive.mozilla.org › pub › mobile › releases › 68.12.0) — Firefox embarque ses propres certificats.

### 1.3 Garder l'écran allumé
1. **Paramètres** › **À propos de l'appareil** › appuyer **7 fois** sur **Numéro de version** → « Mode développeur activé ».
2. **Paramètres** › **Options de développement** › cocher **Rester activé** (l'écran reste allumé tant que la tablette est branchée).
3. Brancher la tablette sur secteur en permanence.

### 1.4 Ouvrir le tableau de bord
1. Dans Chrome, ouvrir l'adresse secrète fournie (format `https://sirose-tablette-xxxxxx.netlify.app`). **Ne la partagez pas.**
2. Saisir le **code du tableau de bord** → l'écran s'affiche. Le code est mémorisé, plus besoin de le retaper.
3. Menu Chrome **⋮** › **Ajouter à l'écran d'accueil** → l'icône « Sir'Ose » ouvre la page en plein écran.

L'écran se met à jour tout seul toutes les 15 minutes ; les données changent après chaque passage d'ARGOS (vers 7h, 13h et 19h).

---

## 2. Lire l'écran au quotidien

| Zone | Ce qu'elle montre | D'où ça vient |
|---|---|---|
| **Priorités du jour** | 3 choses à faire aujourd'hui, écrites comme une phrase à dicter dans l'app Claude | ARGOS, à partir des autres blocs |
| **Tâches & échéances** | Tâches Notion en retard ou à faire sous 7 jours + obligations légales (registre THEMIS) | Notion, registre |
| **Mails à traiter** | Les mails qui attendent une réponse ou une action (8 max) | Gmail |
| **Pipeline** | Où en sont clients, prospects et financeurs | Notion, Drive |
| **Argent** | Encaissé ce mois-ci et sur la phase, comparé à l'objectif du business plan | Factures Drive, mails Payzen/Qonto |

- Les pastilles **G / N / D / R** indiquent la source : Gmail, Notion, Drive, Registre.
- **↔ Nom** : l'élément auquel ARGOS a relié l'information (un client, un financeur, une tâche).
- **⏰ 21/11** : échéance.
- Le trait de couleur à gauche : **rouge** = urgent, **orange** = à surveiller, **vert** = pour info.
- Un mail disparaît de l'écran à la mise à jour suivante dès que vous y avez **répondu** ou que vous l'avez **archivé**.

Pour agir : ouvrez l'application **Claude** sur votre téléphone et dictez la priorité telle qu'elle est écrite.

## 3. En cas de problème

| Ce que vous voyez | Ce que ça veut dire | Que faire |
|---|---|---|
| **⚠ source indisponible à 12:53** dans un bloc | ARGOS n'a pas pu lire cette source à ce passage ; le bloc montre les dernières données connues | Rien : le passage suivant réessaiera. Si ça dure une journée, vérifier les connecteurs dans claude.ai |
| **⚠ hors ligne depuis 14:10** en haut | La tablette n'arrive plus à joindre Internet | Vérifier le Wi-Fi de la tablette. L'écran garde le dernier affichage |
| **⚠ données du 18/11 06:53 — pas de mise à jour depuis plus de 8 h** | La tâche planifiée ARGOS n'a pas tourné | Dans l'app Claude : demander « vérifie la tâche planifiée ARGOS » |
| **Code incorrect** | Le code a été changé, ou mal saisi | Retaper le nouveau code |
| « Votre connexion n'est pas privée » | Le certificat de l'étape 1.2 n'est pas installé | Refaire l'étape 1.2 (ou plan B Firefox) |

### Changer le code du tableau de bord
1. Dans claude.ai, réglages de l'environnement cloud : modifier la valeur de `SIROSE_DASH_PIN`.
2. Au passage suivant d'ARGOS, la tablette affichera « Code incorrect » : saisir le nouveau code.

---

## Pour les développeurs

- Tests : `pip install playwright cryptography pytest` puis `python3 -m pytest tablette/tests -q` (Chromium attendu dans `/opt/pw-browsers/chromium`, ou variable `CHROMIUM`).
- Vérification ES5 : `npx --yes acorn@8.14.0 --ecma5 --silent tablette/app.js`.
- Publication manuelle : `SIROSE_DASH_PIN=… python3 -m tablette.publier.publier tablette/exemple/dashboard.json --sortie dist/`.
- Règles d'ARGOS : `docs/agents/argos/regles.md`.
