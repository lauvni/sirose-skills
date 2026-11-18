# Tablette de pilotage Sir'Ose + agent ARGOS — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Une page statique chiffrée, affichée en kiosque sur une Galaxy Tab 3 (Android 4.4 / Chrome 81), alimentée 3×/jour par un agent Claude planifié (ARGOS) qui lit Gmail, Notion et Drive en lecture seule.

**Architecture:** ARGOS (session Claude Code planifiée) écrit un `dashboard.json`. Un script Python le valide, le fusionne avec l'état précédent (blocs indisponibles), calcule le bloc Argent, puis le chiffre (AES-GCM + PBKDF2) dans `dist/data.enc`, à côté d'un `index.html` ES5 fixe. Le tout est déployé sur Netlify. La page déchiffre avec WebCrypto à l'aide d'un PIN mémorisé.

**Tech Stack:** Python 3.13 + `cryptography` + pytest ; HTML/CSS/JS ES5 sans dépendance ; Playwright (Chromium préinstallé) pour les tests navigateur ; `acorn` pour vérifier la syntaxe ES5 ; Netlify (connecteur MCP ou CLI).

**Spec:** `docs/superpowers/specs/2026-11-18-tablette-dashboard-design.md`

## Global Constraints

- Cible : Chrome 81 sur Android 4.4.2. JS strictement **ES5** (vérifié par `npx --yes acorn@8.14.0 --ecma5 --silent <fichier>`). Pas de `fetch` (utiliser XMLHttpRequest), pas de CSS `grid`, pas de dépendance externe ni de CDN.
- Viewport 1280×800 paysage ; texte ≥ 18 px ; thème sombre, fort contraste.
- Chiffrement : AES-GCM 256, clé dérivée par PBKDF2-SHA256, **100 000 itérations**, sel de 16 octets, IV de 12 octets, aléatoires à chaque publication.
- Le PIN n'est **jamais** écrit dans le dépôt ni dans `dist/`. Il est lu depuis la variable d'environnement `SIROSE_DASH_PIN`.
- `dist/` est ignoré par git. `dashboard.json` en clair n'est jamais commité, sauf l'exemple fictif `tablette/exemple/dashboard.json`.
- ARGOS est en **lecture seule** sur Gmail, Notion et Drive. Son seul effet de bord est le déploiement Netlify.
- Ne jamais lire ni afficher : le dossier Drive « Pièces associés », les pièces d'identité, les RIB/IBAN, les CV, les justificatifs personnels, ni les montants ARE/RSA/APL.
- Fuseau horaire : `Indian/Reunion`. Langue de l'interface : français.
- Calendrier BP (doc 02) : M1 = août 2026. Phase 1 = août → nov. 2026, objectifs mensuels 300 / 600 / 1 000 / 1 500 € (total 3 400 €). Phase 2 = déc. 2026 → juil. 2027, objectifs 10 000 / 12 000 / 14 000 / 16 000 / 18 000 / 20 000 / 22 500 / 25 000 € (total 137 500 €). Phase 3 = août 2027 → juil. 2028 : 28 000 / 30 500 / 33 000 / 35 500 / 38 000 / 40 000 puis 41 600 € ×6.
- Commits terminés par les lignes d'attribution de la session. Développement sur `claude/intelligent-curie-cq1hqt`.

## Review Focus

1. **Mauvais PIN ou PIN changé** : la page doit afficher « Code incorrect », effacer le PIN mémorisé et redemander, sans boucle ni écran blanc. → test Task 2.
2. **`data.enc` inaccessible** (Wi-Fi coupé, Netlify en panne) : la page garde le dernier affichage et indique « hors ligne depuis HH:MM ». → test Task 4.
3. **Données vieilles de plus de 8 h** (la tâche planifiée n'a pas tourné) : bandeau d'alerte « données du JJ/MM HH:MM ». → test Task 4.
4. **Une source en échec lors d'une exécution** : le bloc reprend les données précédentes, marquées « source indisponible à HH:MM », et ne devient pas vide. → test Task 5.
5. **Paiement notifié deux fois** (Payzen et Qonto, même montant, même jour, même client) : compté une seule fois ; et les mois à cheval sur deux phases (30 nov. → 1er déc.) prennent le bon objectif. → test Task 3.

---

## File Structure

```
tablette/
  index.html              # page fixe : écran PIN + 5 blocs (HTML+CSS inline)
  app.js                  # ES5 : XHR data.enc, déchiffrement WebCrypto, rendu, rafraîchissement
  publier/
    __init__.py
    crypto.py             # chiffrer(json_bytes, pin) -> dict ; dechiffrer(dict, pin) -> bytes
    schema.py             # valider(dashboard: dict) -> list[str] (erreurs)
    argent.py             # objectif_mois(date), phase(date), bloc_argent(factures, paiements, aujourd_hui)
    fusion.py             # fusionner(nouveau, precedent, maintenant) -> dict
    publier.py            # CLI : python -m tablette.publier.publier <dashboard.json> --precedent-url URL --sortie dist/
  tests/
    test_crypto.py  test_schema.py  test_argent.py  test_fusion.py  test_publier.py
    test_page.py          # Playwright : déchiffrement + rendu + cas d'erreur
  exemple/dashboard.json  # données fictives, schéma v1
  netlify.toml            # en-têtes noindex + no-cache sur data.enc
  README.md               # installation tablette pas à pas (FR, non-développeur)
.claude/agents/argos.md   # définition de l'agent
docs/agents/argos/regles.md  # filtrage Gmail, liaison, confidentialité, procédure d'exécution
.gitignore                # + dist/
```

---

### Task 1: Chiffrement Python (`crypto.py`)

**Files:**
- Create: `tablette/publier/__init__.py`, `tablette/publier/crypto.py`, `tablette/__init__.py`
- Test: `tablette/tests/test_crypto.py`

**Interfaces:**
- Produces: `chiffrer(clair: bytes, pin: str, iterations: int = 100_000) -> dict` qui renvoie `{"v": 1, "iter": int, "sel": b64, "iv": b64, "ct": b64}` (base64 standard, `ct` = chiffré + tag GCM concaténés, comme le produit WebCrypto) ; `dechiffrer(enveloppe: dict, pin: str) -> bytes`, qui lève `ValueError("PIN incorrect")` en cas d'échec d'authentification.

- [ ] **Step 1: Write the failing tests**

```python
def test_aller_retour():
    env = chiffrer(b'{"a":1}', "4821")
    assert set(env) == {"v", "iter", "sel", "iv", "ct"} and env["v"] == 1 and env["iter"] == 100_000
    assert dechiffrer(env, "4821") == b'{"a":1}'

def test_sel_et_iv_aleatoires():
    a, b = chiffrer(b"x", "1"), chiffrer(b"x", "1")
    assert a["sel"] != b["sel"] and a["iv"] != b["iv"]

def test_mauvais_pin():
    with pytest.raises(ValueError, match="PIN incorrect"):
        dechiffrer(chiffrer(b"x", "1111"), "2222")
```

- [ ] **Step 2: Run** `python3 -m pytest tablette/tests/test_crypto.py -v`. Expected: FAIL (ImportError).
- [ ] **Step 3: Implement** with `cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC` (SHA256, length 32) and `AESGCM`; `os.urandom` for the salt (16) and the IV (12). Catch `InvalidTag` and raise `ValueError("PIN incorrect")`.
- [ ] **Step 4: Run** the same command. Expected: 3 passed.
- [ ] **Step 5: Commit** `feat(tablette): chiffrement AES-GCM/PBKDF2 du tableau de bord`

### Task 2: Déchiffrement dans la page + écran PIN

**Files:**
- Create: `tablette/index.html`, `tablette/app.js`, `tablette/tests/test_page.py`, `tablette/tests/conftest.py`

**Interfaces:**
- Consumes: enveloppe JSON de Task 1, servie sous le nom `data.enc` dans le même répertoire que `index.html`.
- Produces (globals ES5 in `app.js`): `SIROSE.dechiffrer(enveloppe, pin, ok, ko)` (callbacks, pas de Promise exposée) ; `SIROSE.demarrer()`, appelée au `load`. Clé `localStorage` : `sirose_pin`. Ids DOM : `#ecran-pin`, `#champ-pin`, `#bouton-pin`, `#message-pin`, `#tableau`.

- [ ] **Step 1: Write the failing tests.** `conftest.py` fournit la fixture `serveur(tmp_path)`, qui copie `index.html` et `app.js`, écrit `data.enc = chiffrer(exemple, "4821")` et lance `http.server` sur un port libre. Elle fournit aussi la fixture `page` (Playwright, viewport 1280×800, deviceScaleFactor 1).

```python
def test_pin_correct_affiche_tableau(page, serveur):
    page.goto(serveur.url); page.fill("#champ-pin", "4821"); page.click("#bouton-pin")
    page.wait_for_selector("#tableau:not([hidden])")
    assert page.evaluate("localStorage.getItem('sirose_pin')") == "4821"

def test_pin_memorise_pas_de_saisie(page, serveur):  # rechargement → tableau direct
    ...  # set localStorage then reload; assert #ecran-pin hidden

def test_mauvais_pin(page, serveur):
    page.goto(serveur.url); page.fill("#champ-pin", "0000"); page.click("#bouton-pin")
    assert page.text_content("#message-pin") == "Code incorrect"
    assert page.evaluate("localStorage.getItem('sirose_pin')") is None
```

- [ ] **Step 2: Run** `python3 -m pytest tablette/tests/test_page.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement.** Base64 → `Uint8Array` via `atob` ; `crypto.subtle.importKey("raw", pin UTF-8, "PBKDF2")` → `deriveKey({name:"PBKDF2", hash:"SHA-256", salt, iterations: env.iter}, …, {name:"AES-GCM", length:256})` → `decrypt({name:"AES-GCM", iv})`. Chain with `.then` (Promises natives OK dans Chrome 81, mais pas de syntaxe ES6). Decode UTF-8 with `TextDecoder`. At this stage, `#tableau` displays only `genere_le`.
- [ ] **Step 4: Run** the tests, then `npx --yes acorn@8.14.0 --ecma5 --silent tablette/app.js`. Expected: tests PASS, acorn without error.
- [ ] **Step 5: Commit** `feat(tablette): page ES5 avec écran PIN et déchiffrement WebCrypto`

### Task 3: ✋ Validation sur la tablette réelle (point d'arrêt)

**Files:**
- Create: `tablette/netlify.toml`, `.gitignore` (+ `dist/`)
- Create: `tablette/README.md` (section « 1. Préparer la tablette » only)

`netlify.toml`: `publish = "."`; headers `/*` → `X-Robots-Tag: noindex, nofollow`; `/data.enc` → `Cache-Control: no-cache`.

- [ ] **Step 1:** Build a test `dist/` (index.html, app.js, netlify.toml, `data.enc` chiffré à partir de `exemple/dashboard.json` avec un PIN de test communiqué à Alexandre dans le chat), then deploy it to a **new** Netlify project named `sirose-tablette-<6 caractères aléatoires>`, after Alexandre's explicit go-ahead (`create-new-project`, then `deploy-site`; otherwise Netlify CLI from `dist/`). Note the `siteId` in `docs/agents/argos/regles.md` (created in Task 6, or a temporary note until then).
- [ ] **Step 2:** Write README §1 (FR): install ISRG Root X1 as a user certificate (download `isrgrootx1.der` from letsencrypt.org, Paramètres › Sécurité › Installer depuis la mémoire), update Chrome, keep the screen on when plugged in (Options pour les développeurs › Rester activé), add the page to the home screen. Fallback: Firefox 68.
- [ ] **Step 3: Have Alexandre test it.** Expected result: the URL opens **without a certificate warning**, the PIN unlocks, and the date appears. **If it fails, stop the plan** and go back to the design (option: hosting with a certificate the device trusts).
- [ ] **Step 4:** Measure the unlock time on the tablet. If it is over 5 s, lower `iterations` (minimum 50 000) and record the value in the Global Constraints.
- [ ] **Step 5: Commit** `chore(tablette): config Netlify et guide de préparation de la tablette`

### Task 4: Rendu des 5 blocs + rafraîchissement

**Files:**
- Create: `tablette/exemple/dashboard.json` (fictitious data, all 5 blocks filled in, one item from each source)
- Modify: `tablette/index.html`, `tablette/app.js`, `tablette/tests/test_page.py`

**Interfaces:**
- Consumes: schéma v1 (défini en Task 5 ; l'exemple doit passer `valider`). Racine : `{"schema": 1, "genere_le": ISO8601+04:00, "prochaine_maj": ISO, "blocs": {"priorites", "taches", "mails", "pipeline", "argent"}}`. Chaque bloc : `{"etat": "ok"|"indisponible", "depuis": ISO|null, "elements": [...]}`. Élément générique : `{"texte", "source": "gmail"|"notion"|"drive"|"registre", "lien_vers": str|null, "urgence": "haute"|"moyenne"|"basse", "echeance": "AAAA-MM-JJ"|null}`. `argent.elements` est vide. Bloc argent : `{"etat", "depuis", "mois": {"libelle", "facture", "encaisse", "objectif"}, "phase": {"nom", "facture", "encaisse", "objectif"}}`.
- Produces: `SIROSE.rendre(dashboard)`; ids `#bloc-priorites`, `#bloc-taches`, `#bloc-mails`, `#bloc-pipeline`, `#bloc-argent`, `#bandeau` (alertes), `#horodatage`.

- [ ] **Step 1: Write the failing tests:**
  - `test_cinq_blocs_rendus`: each `#bloc-*` contains the text of its first example item, and `#horodatage` contains "màj" and "prochaine".
  - `test_limites`: at most 3 priorities and at most 8 mails are rendered, even if the JSON contains more.
  - `test_bloc_indisponible`: a block with `etat: "indisponible", depuis: "…T07:30"` shows "source indisponible à 07:30" while keeping its items.
  - `test_donnees_perimees`: `genere_le` more than 8 h old (clock mocked with `page.clock.set_fixed_time`) → `#bandeau` contains "données du".
  - `test_hors_ligne_garde_affichage`: after a successful display, the server returns a 404 on `data.enc`, the refresh is forced (`SIROSE.rafraichir()`), the blocks stay in place, and `#bandeau` contains "hors ligne depuis".
- [ ] **Step 2: Run** the tests. Expected: FAIL.
- [ ] **Step 3: Implement.** 2×2 flexbox layout plus the full-width priorities band, as in spec §5.3. Source icon as a text badge (G / N / D / R). "↔ lien_vers" when not null. Colour by urgency. Argent: horizontal bar showing encaissé/objectif for the month, with the phase total underneath. Refresh every 15 min (`setInterval`, 900 000 ms) through `SIROSE.rafraichir()`. Render with `textContent` only (no `innerHTML` on the data).
- [ ] **Step 4: Run** the tests and acorn ES5. Expected: PASS. Take a 1280×800 screenshot `dist/apercu.png` and look at it to check readability.
- [ ] **Step 5: Commit** `feat(tablette): rendu des cinq blocs, alertes de fraîcheur et hors-ligne`

### Task 5: Pipeline de publication (schéma, argent, fusion, CLI)

**Files:**
- Create: `tablette/publier/schema.py`, `argent.py`, `fusion.py`, `publier.py`
- Test: `tablette/tests/test_schema.py`, `test_argent.py`, `test_fusion.py`, `test_publier.py`

**Interfaces:**
- Consumes: `chiffrer`/`dechiffrer` (Task 1) ; schéma v1 (Task 4 Interfaces).
- Produces:
  - `valider(d: dict) -> list[str]`: empty list if the data is valid.
  - `phase(jour: date) -> tuple[str, date, date]`, for example `("Phase 2", date(2026,12,1), date(2027,7,31))`.
  - `objectif_mois(jour: date) -> int` (euros HT, values from the Global Constraints).
  - `bloc_argent(factures: list[dict], paiements: list[dict], aujourd_hui: date) -> dict`. Inputs: `factures` items look like `{"date","montant_ht","client","ref"}` and `paiements` items look like `{"date","montant","client","origine": "payzen"|"qonto"}`.
  - `fusionner(nouveau: dict, precedent: dict|None, maintenant: datetime) -> dict`.
  - CLI `python3 -m tablette.publier.publier ENTREE.json --sortie dist/ [--precedent-url URL]`, which reads `SIROSE_DASH_PIN` and writes `dist/{index.html, app.js, netlify.toml, data.enc}`. Exit code 2 if the schema is invalid or the PIN is missing.

- [ ] **Step 1: Write the failing tests:**

```python
# test_argent.py
def test_objectifs():
    assert objectif_mois(date(2026,11,30)) == 1500 and objectif_mois(date(2026,12,1)) == 10000
    assert phase(date(2026,11,30))[0] == "Phase 1" and phase(date(2026,12,1))[0] == "Phase 2"
    assert objectif_mois(date(2028,3,15)) == 41600

def test_doublon_payzen_qonto_compte_une_fois():
    p = [{"date":"2026-11-17","montant":187.0,"client":"Villa Naya","origine":"payzen"},
         {"date":"2026-11-17","montant":187.0,"client":"Villa Naya","origine":"qonto"}]
    assert bloc_argent([], p, date(2026,11,18))["mois"]["encaisse"] == 187.0

def test_cumul_phase():  # paiements in Sept and Nov 2026 → phase.encaisse = sum, phase.objectif == 3400
    ...

# test_fusion.py
def test_bloc_indisponible_reprend_precedent():
    # nouveau.taches = {"etat":"indisponible","depuis":None,"elements":[]}; precedent.taches has 2 items
    r = fusionner(nouveau, precedent, datetime(2026,11,18,12,30,tzinfo=REUNION))
    assert r["blocs"]["taches"]["elements"] == precedent["blocs"]["taches"]["elements"]
    assert r["blocs"]["taches"]["etat"] == "indisponible" and r["blocs"]["taches"]["depuis"].startswith("2026-11-18T12:30")

def test_sans_precedent_bloc_vide_reste_indisponible(): ...

# test_schema.py
def test_exemple_valide(): assert valider(json.load(open("tablette/exemple/dashboard.json"))) == []
def test_source_inconnue_refusee(): ...  # "source": "slack" → 1 erreur
def test_donnee_sensible_refusee():  # an IBAN in any text (regex FR\d{2}[ \d]{10,}) → error "donnée sensible"
    ...

# test_publier.py
def test_cli_produit_dist(tmp_path, monkeypatch):  # PIN via env → 4 files, data.enc decryptable, no "4821" in dist/
def test_cli_sans_pin_echoue(): ...  # exit code 2
```

- [ ] **Step 2: Run** `python3 -m pytest tablette/tests -v`. Expected: the new tests FAIL.
- [ ] **Step 3: Implement.** Payment deduplication: same `date`, same `montant` (rounded to the cent) and same `client` (case-insensitive), regardless of `origine`. `fusionner`: for each block with `etat == "indisponible"`, copy the previous `elements` (and `mois`/`phase` for argent) and set `depuis` = `maintenant` if it was `None`. `--precedent-url`: download with `urllib`, then decrypt with the same PIN. Any network or decryption error → `precedent = None`, with a warning on stderr and no crash.
- [ ] **Step 4: Run** `python3 -m pytest tablette/tests -v`. Expected: all tests PASS.
- [ ] **Step 5: Commit** `feat(tablette): validation, calcul argent, fusion et CLI de publication`

### Task 6: Agent ARGOS et ses règles

**Files:**
- Create: `.claude/agents/argos.md`, `docs/agents/argos/regles.md`

**Interfaces:**
- Consumes: the CLI from Task 5, the schema from Task 4, and the `siteId` from Task 3.
- Produces: an agent that can be invoked by name (`argos`), and an execution procedure written in `regles.md` §« Exécution » that the scheduled task will quote.

- [ ] **Step 1: Write `argos.md`** in the format of `hermes.md` (from the `claude/fervent-volta-xpvatp` branch): `name: argos` frontmatter, a `description` in French, the Sir'Ose context, "lecture seule stricte", a pointer to `regles.md`.
- [ ] **Step 2: Write `regles.md`**, with these values set:
  - **Sources Notion**: the "Sir'Ose — Pilotage" page `3faf2bf25d7881088a0eddff4385ec7c`; the Tâches Sir'Ose database `a5544105-9bdc-48d5-b95a-3b32443ff636`; the Clients & prospects database `130678e3-e7c0-49db-b22c-cbb9850a23b3`; the Financeurs database `36b96dd4-86ae-42f5-9819-cb9047924d83`.
  - **Mails** (block ③): Gmail query `in:inbox newer_than:14d -category:promotions -category:social`. Read each thread in full (`get_thread`). Exclude it if its last message comes from `contact.sirose@gmail.com`. Ignore Instagram and Indy/Clementine newsletters. Keep only threads that call for an action or carry money information. 8 maximum, sorted by urgency.
  - **Liaison**: sender's name or domain ↔ title of the Notion Clients / Financeurs page; client name ↔ Drive invoice title (`title contains 'Facture'`).
  - **Argent**: invoices = Drive files whose title contains "Facture"; payments = Payzen (`do_not_reply@payzen.eu`) and Qonto (`hello@qonto.com`) mails, current phase only. Hand these over raw in a sidecar file `argent_entree.json` that the CLI turns into a block through `bloc_argent`. Do **not** compute anything by hand. → Add the `--argent ARGENT.json` option to the CLI, with a test in `test_publier.py` (it fills `blocs.argent`).
  - **Registre THEMIS**: `git show origin/claude/dazzling-planck-ox772a:docs/conformite/registre_obligations.md` (or the file if it has been merged), deadlines ≤ 30 days → block ② with `source: "registre"`.
  - **Exclusions**: the list from the Global Constraints, verbatim.
  - **Exécution**: (1) read the sources; (2) write `/tmp/argos/dashboard.json` and `argent_entree.json`; (3) run `python3 -m tablette.publier.publier … --precedent-url https://<site>.netlify.app/data.enc --sortie dist/`; (4) deploy `dist/` (`deploy-site` siteId); (5) reply with a 3-line summary. A failing source → `etat: "indisponible"`, never invented content.
- [ ] **Step 3: Manual run.** Invoke ARGOS once in this session with `SIROSE_DASH_PIN` set to Alexandre's PIN. Expected: deployment OK, the tablet shows real data, and no excluded data is visible (Alexandre checks).
- [ ] **Step 4: Commit** `feat(argos): agent de synthèse lecture seule pour la tablette`

### Task 7: Planification + guide final

**Files:**
- Modify: `tablette/README.md` (§2 « Utilisation au quotidien », §3 « En cas de problème »)

- [ ] **Step 1: PIN in the environment.** Alexandre adds `SIROSE_DASH_PIN` himself in the cloud environment settings (give him the exact steps after reading `read_documentation` `environment.secrets`). The PIN never goes in the chat or in the task prompt.
- [ ] **Step 2: Create the scheduled task** (`create_trigger`, `create_new_session_on_fire: true`, `connectors: ["Gmail","Notion","Google Drive","Netlify"]`, `cron_expression: "CRON_TZ=Indian/Reunion 53 6,12,18 * * *"` → 6:53, 12:53, 18:53). The prompt is self-contained: "Tu es ARGOS. Suis docs/agents/argos/regles.md §Exécution, branche claude/intelligent-curie-cq1hqt." `source_revision` is that branch.
- [ ] **Step 3: Verify.** Trigger it once with `fire_trigger`, then check: the session finished without error, the timestamp on the tablet has changed, and `prochaine_maj` reads "12:53" or the next slot.
- [ ] **Step 4: README §2–3**: how to read each block; what "source indisponible" and "hors ligne" mean; how to change the PIN (change the variable, then re-enter the PIN on the tablet); what to do if the page shows "données du…" (check the scheduled task).
- [ ] **Step 5: Commit and push** `docs(tablette): guide d'utilisation et planification ARGOS`
