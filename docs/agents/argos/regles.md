# ARGOS — Règles de collecte, de liaison et de publication

*Référence d'exécution de l'agent ARGOS (`.claude/agents/argos.md`). Conception : `docs/superpowers/specs/2026-11-18-tablette-dashboard-design.md`. Format des données : `tablette/exemple/dashboard.json` (schéma v1).*

## 1. Sources

### Notion — page « Sir'Ose — Pilotage » (`3faf2bf25d7881088a0eddff4385ec7c`)
| Base | ID | Usage |
|---|---|---|
| Tâches Sir'Ose | `a5544105-9bdc-48d5-b95a-3b32443ff636` | Bloc ② : tâches non terminées en retard ou à échéance ≤ 7 jours |
| Clients & prospects | `130678e3-e7c0-49db-b22c-cbb9850a23b3` | Bloc ④ (compte par statut, 3 dernières évolutions) + liaisons |
| Financeurs | `36b96dd4-86ae-42f5-9819-cb9047924d83` | Bloc ④ + liaisons |

### Gmail — contact.sirose@gmail.com
- Requête : `in:inbox newer_than:14d -category:promotions -category:social`
- Lire chaque fil **en entier** (`get_thread`) : les aperçus de recherche ne montrent pas les derniers messages.
- **Afficher un fil seulement si** son **dernier message ne vient pas** de `contact.sirose@gmail.com` (règle validée par Alexandre : répondre ou archiver le fait disparaître).
- Ignorer le bruit : notifications Instagram / Facebook, newsletters (Indy, Clementine, promotions bancaires), suggestions.
- Garder ce qui appelle une action ou touche à l'argent : administrations (DGFiP, greffe, INPI, URSSAF, DAAF), banque et paiements (Qonto, Payzen), clients et financeurs connus dans Notion, Lucien MOREAU, comptable.
- Bloc ③ : **8 fils maximum**, triés par urgence puis date. `texte` = « Expéditeur — objet résumé ».

### Google Drive
- Factures : fichiers dont le titre contient « Facture » (hors corbeille).
- **Exclu** : le dossier « Pièces associés » et tout document d'identité, RIB, CV, justificatif personnel.

### Registre de conformité (THEMIS)
- Si `docs/conformite/registre_obligations.md` existe sur la branche courante, le lire ; sinon `git show origin/claude/dazzling-planck-ox772a:docs/conformite/registre_obligations.md` (après `git fetch origin claude/dazzling-planck-ox772a`). Absent → ne rien ajouter, sans échouer.
- Bloc ② (`source: "registre"`) : lignes **non réglées** avec une échéance datée ≤ 30 jours, puis, s'il reste de la place, au plus 3 lignes 🔴 ouvertes sans date (`urgence: "haute"`, `echeance: null`).

## 2. Liaisons (`lien_vers`)
Pour chaque élément, chercher à quoi il se rattache et l'écrire sous la forme `« Nom (client) »`, `« Nom (prospect) »`, `« Nom (financeur) »` ou `« Titre de la tâche (tâche) »` :
1. Expéditeur (nom ou domaine) ↔ titre d'une page Clients & prospects ou Financeurs.
2. Nom du client ↔ facture Drive (`title contains '<client>'` et `title contains 'Facture'`).
3. Mail ↔ tâche Notion portant le même sujet.
Pas de correspondance sûre → `lien_vers: null`. Ne jamais deviner.

## 3. Bloc ① — Priorités du jour
3 lignes maximum, formulées comme une **commande qu'Alexandre peut dicter** dans l'application Claude (« Répondre à … sur … », « Envoyer … à … »). Choisies parmi les éléments ②③④ les plus urgents ; même `source` et `lien_vers` que l'élément d'origine.

## 4. Bloc ⑤ — Argent (validé par Alexandre)
ARGOS **ne calcule rien** : il écrit les données brutes dans `argent_entree.json` et le script fait le calcul (dédoublonnage, mois en cours, cumul de phase, objectifs du BP).
```json
{"factures": [{"date": "AAAA-MM-JJ", "montant_ht": 0.0, "client": "…", "ref": "F-…"}],
 "paiements": [{"date": "AAAA-MM-JJ", "montant": 0.0, "client": "…", "origine": "payzen|qonto",
                "ref": "n° de transaction ou null", "contrepartie": "émetteur du virement (Qonto) ou null"}]}
```
- Factures : factures Drive de la phase en cours (date et montant HT lus dans le document).
- Paiements : mails de `do_not_reply@payzen.eu` et `hello@qonto.com` (paiements **reçus** uniquement) depuis le début de la phase en cours.
  - **Payzen** = paiements carte des clients : `ref` = numéro de transaction Payzen.
  - **Qonto** = crédits sur le compte : `contrepartie` = émetteur du virement **tel qu'écrit dans le mail** (ex. « LYRA NETWORK »). Le script **ignore** les reversements Payzen/Lyra (déjà comptés côté Payzen) ; ne les filtre pas toi-même, recopie fidèlement.
  - Une même notification relue deux fois porte la même `ref` : le script ne la compte qu'une fois. Sans référence lisible, `ref: null`.
- Une source illisible → `"argent": {"etat": "indisponible", "depuis": null, "elements": []}` dans `dashboard.json` et **ne pas** passer `--argent`.

## 5. Exclusions (rappel, sans exception)
Dossier Drive « Pièces associés » · pièces d'identité · RIB / IBAN · CV · justificatifs personnels (EDF, Pôle emploi / France Travail…) · montants ARE, RSA, APL des fondateurs.

## 6. Exécution (procédure de la tâche planifiée)
Netlify : projet `sirose-tablette-k7q4zm`, siteId `1c93f9b6-5033-488b-a19a-aa3e4157cfcc`, URL `https://sirose-tablette-k7q4zm.netlify.app`. L'environnement cloud « sirose-skills » autorise `api.netlify.com`, `netlify-mcp.netlify.app` et cette URL.
1. Lire les sources (§1) ; en cas d'échec d'une source, marquer le bloc concerné `indisponible`.
2. Écrire `/tmp/argos/dashboard.json` (schéma v1, `genere_le` = maintenant, `prochaine_maj` = prochain créneau 06:53 / 12:53 / 18:53 ; **toujours avec le fuseau `+04:00`**, sinon la publication est refusée) et `/tmp/argos/argent_entree.json`.
3. Depuis la racine du dépôt :
   ```bash
   python3 -m tablette.publier.publier /tmp/argos/dashboard.json --argent /tmp/argos/argent_entree.json --precedent-url https://sirose-tablette-k7q4zm.netlify.app/data.enc --sortie dist/
   ```
   Code de sortie 2 → lire l'erreur, corriger `dashboard.json` (jamais en supprimant le garde-fou) et relancer.
4. Déployer `dist/` : appeler le connecteur Netlify `deploy-site` avec le siteId ci-dessus ; il renvoie une commande `npx -y @netlify/mcp@latest --site-id … --proxy-path …`. L'exécuter **depuis le dossier `dist/`** en la préfixant de `NODE_USE_ENV_PROXY=1` (sinon Node ne passe pas par le proxy réseau). Attendre « Deploy is ready ».
5. Supprimer `/tmp/argos/` (aucune copie en clair ne doit rester).
6. Répondre par le résumé de 3 lignes. Ne rien commiter.
