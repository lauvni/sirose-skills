---
name: sirose-business-plan
description: Création et mise à jour du business plan de référence de Sir'Ose — réconcilier les versions existantes (BP 05/03/2026, BP v2.0 500 k€, BP d'amorçage 100 k€, export Propulse, dossiers KAP), fixer une table unique de données de référence, produire le BP à jour en .docx et contrôler sa cohérence avec chaque dossier de financement. Utiliser dès qu'on parle de « mettre à jour le BP », de prévisionnel, de plan de financement ou de chiffres à présenter à un financeur.
---

# Business plan de référence — Sir'Ose

Objectif : **une seule version du BP qui fait foi**, dont toutes les autres pièces (Propulse, KAP, deck Canva, dossiers France Active et Initiative) reprennent les chiffres à l'identique.

## 1. Versions existantes à réconcilier

| Version | Emplacement | Montant / trajectoire |
|---|---|---|
| BP daté du 05/03/2026 | Drive | CA An 1 : 179 464 € HT |
| Dossiers KAP TPE / Numérique (avril 2026) | Drive | CA An 1 : 191 464 € HT |
| Plan de financement T1 2026 | Drive, Kairos | 73 840 € puis 88 498 € |
| Plan de financement (mémoire Kairos) | Kairos | environ 117 000 € |
| BP d'amorçage 100 k€ (septembre 2026) | Branche `claude/siroise-business-plan-qkz1d6`, `docs/business_plan_100k/` | 100 000 € |
| Export Propulse by CA (11/09/2026) | Drive, et `CORRECTIONS_PROPULSE_ET_PIECES_A_JOINDRE.md` | 92 800 € |
| BP v2.0, trajectoire à 500 k€ HT | `docs/business_plan_500k/` | Horizon 3 ans |

## 2. Procédure

1. **Inventaire :** relire chaque version disponible et noter son hypothèse principale, sa date et sa source.
2. **Table des données de référence :** créer ou mettre à jour `docs/conformite/modeles/bp_donnees_reference.md`, avec une ligne par donnée (capital, siège, CA réalisé, CA An 1/2/3, prix par format, coût de revient, plan de financement par source, investissements, effectifs). Pour chaque donnée : valeur retenue · source · date · valeurs divergentes et leur source · statut (✅ validée / ⏳ à trancher). **Une donnée à trancher l'est par les fondateurs, pas par THÉMIS.**
3. **Prise en compte des faits nouveaux :**
   - **plus de lieu de production** : l'atelier conforme devient la condition de continuité d'activité, et le calendrier de reprise de production conditionne le CA ;
   - **Rhum-Thé 33cl retiré** de la gamme et du chiffrage ;
   - **code APE et taux de TVA** à aligner sur l'activité de sirops ;
   - **seuil de 300 k€ de l'octroi de mer** à intégrer si la trajectoire le dépasse ;
   - **CA réellement facturé** à reprendre des factures du Drive, sans arrondi.
4. **Plan du BP (à valider avant rédaction) :** synthèse · société et équipe · produit et réglementation · marché et concurrence · stratégie commerciale CHR · moyens de production et investissements · prévisionnel sur 3 ans · plan de financement · risques et points de vigilance · annexes (liste des pièces).
5. **Rédaction :** version Markdown dans `docs/business_plan_reference/`, puis .docx avec la bibliothèque Node.js `docx`. Chaque chiffre renvoie à la table de référence.
6. **Contrôle croisé :** vérifier que Propulse, les dossiers KAP, le deck Canva (`DAHM0IaFZAE`) et les dossiers France Active et Initiative reprennent les mêmes chiffres, puis lister les écarts à corriger, pièce par pièce.

## 3. Règles

- Ne jamais présenter une lettre d'intention, un devis non signé ou un financement en instruction comme acquis.
- La trésorerie réelle, même faible, s'assume et s'explique : c'est l'argument de l'urgence du financement.
- Les phases à long terme (Maison Sir'Ose, Éco-Maritime) restent hors du plan de financement tant qu'elles ne sont ni chiffrées ni datées.
- Les chiffres du prévisionnel portent la mention « à valider par Exco » tant que l'expert-comptable ne les a pas revus.
