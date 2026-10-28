# Agents Sir'Ose

Les agents sont des sous-agents Claude Code définis dans `.claude/agents/`. Dans Claude Code, on les appelle par leur nom (« demande à hermes de lire ce lien… ») ou Claude les choisit d'après leur description.

| Agent | Rôle | Écrit dans | Lit |
|---|---|---|---|
| **HERMES** (`.claude/agents/hermes.md`) | Messager et veille : lit les partages et discussions (YouTube, Instagram, Facebook/Meta, LinkedIn, web), cherche et installe les connecteurs utiles | `vision/fiches/`, `vision/SYNTHESE.md`, `docs/agents/hermes/connecteurs.md` | `docs/business_plan_500k/` |
| **ZEUS** *(à créer)* | CEO : arbitre, priorise, pilote la trajectoire 500 k€ via ses propres connecteurs | à définir | `vision/SYNTHESE.md` (section « Signaux pour ZEUS »), `docs/business_plan_500k/` |

## Flux

```
partages / discussions ──► HERMES ──► vision/fiches/*.md
                                  └─► vision/SYNTHESE.md ──► « Signaux pour ZEUS » ──► ZEUS ──► décisions
```

## Contrat HERMES → ZEUS

- HERMES **n'efface jamais** une ligne de « Signaux pour ZEUS » ; il ajoute.
- ZEUS traite les signaux, renseigne la colonne « Suite donnée » (décision, tâche, rejet motivé) et peut demander à HERMES d'approfondir une source.
- Les connecteurs installés au niveau projet (`.mcp.json`) sont partagés : ZEUS peut réutiliser ceux d'HERMES (par exemple Meta Graph API pour les statistiques des comptes Sir'Ose).

## Exemples d'usage

- « hermes, lis cette vidéo et dis-moi ce qu'elle apporte à notre koso : https://youtube.com/… »
- « hermes, Lucien a partagé ce post Instagram d'un bar à Saint-Gilles, fais-en une fiche. »
- « hermes, trouve un connecteur pour lire les pages LinkedIn d'entreprises et propose-le-moi. »
