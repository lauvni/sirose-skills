# HERMES — Catalogue des connecteurs et méthodes de lecture

*Document de travail tenu à jour par HERMES. Chaque connecteur testé change de statut : `à tester` → `installé` → `testé OK` / `abandonné (raison)`.*

> ⚠️ Les noms de paquets et les offres évoluent vite. Avant toute installation, HERMES vérifie l'éditeur, la date de dernière mise à jour et la documentation officielle, puis demande l'accord de l'utilisateur.

---

## 1. Ordre de priorité par source

| Plateforme | 1. Natif / gratuit | 2. Connecteur recommandé | 3. Repli |
|---|---|---|---|
| **Site web / article** | `WebFetch` | Firecrawl MCP (pages JavaScript, sites entiers) | Jina Reader : `https://r.jina.ai/<url>` |
| **YouTube** | `yt-dlp` (sous-titres et métadonnées) | Serveur MCP « YouTube transcript » (à choisir dans le registre MCP) | `youtube-transcript-api` (Python) |
| **Instagram** | — (mur de connexion) | Meta Graph API pour **le compte Sir'Ose** · Apify MCP pour les contenus publics | Navigateur de l'utilisateur (Claude in Chrome) ou capture d'écran / texte collé |
| **Facebook / Meta** | `WebFetch` (pages publiques, résultat partiel) | Meta Graph API pour **la page Sir'Ose** · Apify MCP pour les pages publiques | Navigateur de l'utilisateur ou copie manuelle |
| **LinkedIn** | `WebFetch` (souvent bloqué) | Apify MCP (pages entreprises publiques) | Navigateur de l'utilisateur ou copie manuelle (recommandé pour les posts) |

---

## 2. Fiches connecteurs

### 2.1 `yt-dlp` — YouTube (outil en ligne de commande)
- **Statut :** à tester · **Coût :** gratuit · **Clé :** aucune
- **Installation :** `pip install yt-dlp`
- **Usage (sous-titres sans télécharger la vidéo) :**
  ```bash
  yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "fr.*,en.*" --sub-format vtt -o "%(id)s.%(ext)s" "<URL>"
  ```
  Métadonnées (titre, chaîne, date, description) : `yt-dlp --dump-json --skip-download "<URL>"`
- **Limites :** une vidéo sans sous-titres n'est pas lisible ; il faut alors une transcription audio (Whisper), à proposer à l'utilisateur.

### 2.2 Firecrawl MCP — sites web
- **Statut :** à tester · **Coût :** offre gratuite limitée, puis payante · **Clé :** `FIRECRAWL_API_KEY`
- **Installation :**
  ```bash
  claude mcp add --scope project firecrawl -e FIRECRAWL_API_KEY='${FIRECRAWL_API_KEY}' -- npx -y firecrawl-mcp
  ```
- **Intérêt :** pages rendues en JavaScript, exploration d'un site entier (concurrents, fournisseurs, appels à projets).

### 2.3 Apify MCP — Instagram, Facebook, LinkedIn (contenus publics)
- **Statut :** à tester · **Coût :** crédit gratuit mensuel, puis à l'usage · **Clé :** `APIFY_TOKEN`
- **Installation :**
  ```bash
  claude mcp add --scope project apify -e APIFY_TOKEN='${APIFY_TOKEN}' -- npx -y @apify/actors-mcp-server
  ```
- **Acteurs utiles :** scraper Instagram (posts, reels, hashtags publics), scraper de posts Facebook (pages publiques), scrapers de pages entreprises LinkedIn.
- **Vigilance :** usage ciblé (un lien partagé, un concurrent, un hashtag), jamais d'aspiration massive de profils de particuliers. Vérifier les CGU de chaque plateforme.

### 2.4 Meta Graph API — comptes Instagram / Facebook **de Sir'Ose**
- **Statut :** à tester · **Coût :** gratuit · **Clé :** jeton d'accès Meta (`META_ACCESS_TOKEN`)
- **Prérequis :** compte Instagram professionnel relié à la page Facebook Sir'Ose, application créée sur Meta for Developers.
- **Intérêt :** méthode officielle pour lire les publications, commentaires et statistiques **de nos propres comptes** (retours clients, questions fréquentes, contenus qui fonctionnent). Elle sert aussi à ZEUS pour le pilotage marketing.

### 2.5 Navigateur de l'utilisateur (Claude in Chrome)
- **Statut :** disponible si l'extension est installée · **Coût :** gratuit
- **Intérêt :** lit les contenus derrière connexion (Instagram, LinkedIn, groupes Facebook) **avec la session de l'utilisateur et son accord**, page par page. C'est le meilleur repli pour un post partagé ponctuellement.

### 2.6 Copie manuelle
Toujours valable : l'utilisateur colle le texte, la légende ou une capture d'écran, et HERMES rédige la fiche à partir de ce contenu.

---

## 3. Grille d'évaluation d'un nouveau connecteur

| Critère | Question | Bloquant si… |
|---|---|---|
| Éditeur | Officiel, entreprise reconnue ou projet open source suivi ? | Auteur anonyme, aucun code source |
| Maintenance | Dernière mise à jour < 6 mois ? | Abandonné depuis plus d'un an |
| Permissions | Que peut-il lire ou écrire ? | Demande des droits d'écriture inutiles |
| Secrets | Clé API ? Stockée comment ? | Exige un mot de passe de compte personnel |
| Coût | Gratuit, crédit, abonnement ? | Coût récurrent non validé par les fondateurs |
| CGU | Respecte les conditions de la plateforme ? | Contourne une protection ou un mur de connexion |

---

## 4. Environnement cloud (Claude Code sur le web)

Dans une session cloud, la politique réseau de l'environnement peut bloquer certains domaines (youtube.com, instagram.com, api.apify.com…). Si un appel échoue avec une erreur de proxy ou une 403, HERMES le signale et indique à l'utilisateur d'autoriser le domaine dans les paramètres réseau de l'environnement. Les clés API se déclarent comme variables d'environnement de l'environnement, jamais dans le dépôt.

---

## 5. Journal des installations

| Date | Connecteur | Action | Résultat | Remarque |
|---|---|---|---|---|
| — | — | — | — | Aucun connecteur installé pour l'instant |
