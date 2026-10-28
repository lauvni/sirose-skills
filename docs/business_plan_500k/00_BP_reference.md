# 00 — BP de Référence — SAS Sir'Ose (arbitrage Thémis)

*Version de référence du Business Plan v2.0 — établie le 28 octobre 2026. Ce document **prévaut** sur les documents 01 à 05 pour tout chiffre qu'il reprend. Les documents 01 à 05 restent les pièces justificatives (sources, détail machine par machine, stratégie commerciale). Tous les montants ci-dessous sont recalculés par le modèle `modele/bp_reference.py`. Il suffit de relancer `python3 docs/business_plan_500k/modele/bp_reference.py` après toute modification d'hypothèse.*

---

## 0. Règles d'arbitrage

1. **Une seule source par chiffre.** Quand deux documents divergent, le détail chiffré l'emporte sur le forfait, et l'arithmétique l'emporte sur le total affiché.
2. **Statut réel des financements.** Rien n'est « sécurisé » tant qu'il n'est pas signé ou versé. Les statuts sont donc ramenés à leur état documenté (cf. §5).
3. **Aucune ressource comptée deux fois.** L'autofinancement ne finance que des dépenses postérieures à sa génération.
4. **Trajectoire de CA inchangée.** L'objectif de 500 k€ HT reste celui du doc 02. Le présent document en vérifie la cohérence (capacité, trésorerie, financement) et en mesure la sensibilité, sans le réécrire.

---

## 1. Registre des corrections

| # | Constat | Source | Arbitrage de référence |
|---|---|---|---|
| C1 | Total des charges d'exploitation de l'Année 3 affiché à 175 000 € alors que les lignes détaillées somment à **161 400 €** | doc 02 §4 | La somme des lignes est retenue, et les ajouts C3 sont intégrés → 169 800 € |
| C2 | Amortissements de 3 300 / 13 700 / 16 700 € : ils ne couvrent que le KAP TPE 1 en A1 et ignorent le chiffrage machine par machine | doc 02 §4 vs doc 05 §8 | Plan d'amortissement complet (§4) → **10 508 / 26 883 / 26 883 €** |
| C3 | Postes chiffrés dans le doc 05 mais absents du P&L : ERP HACCP (2 400 €/an) et véhicule n°2 | doc 05 §3.1 | Intégrés dès M13 (ERP 2 400 €/an, véhicule n°2 : hypothèse de 6 000 €/an pour le leasing, le carburant et l'entretien) |
| C4 | Frais d'agence et de notaire du bail (2 000 €) classés en CAPEX | doc 03 §2 | Passés en charge à M5 (non amortissables) |
| C5 | Charges financières de l'A2 (2 045 €) supérieures à celles de l'A1, alors que la seule dette est un prêt amortissable | doc 02 §4 | Recalcul sur le tableau d'amortissement réel (§3) |
| C6 | Autofinancement compté deux fois : 14 500 € (doc 03 §2.1) + 25 500 € (doc 05 §5) = « 39 000 € », alors que le plan du doc 05 couvre déjà les murs | doc 03 §4.1 | Seul le plan consolidé du doc 05 subsiste. Le §2.1 du doc 03 est caduc |
| C7 | L'autofinancement est censé payer des achats faits à M5 (Phase 2) et à M13 (Phase 3) avec un résultat qui n'est généré qu'**après** ces dates | doc 05 §5 et §5.1 | Plan de trésorerie mensuel (§6). Il fait apparaître un **trou de trésorerie** → prêt d'équipement retenu |
| C8 | Prêt bancaire de 50 k€ et prêts d'honneur de 30 k€ marqués « ✔ Sécurisé », alors que le doc 01 les indique « demande en cours » et « en instruction » | doc 03, doc 05 vs doc 01 | Statuts corrigés (§5) |
| C9 | Subvention KAP TPE 1 « obtenue » (doc 05) contre « visée » (doc 01) | doc 05 §1 | Statut « visée — à confirmer par notification Région » |
| C10 | « Marge de 15 000 € sur le prêt » et « 15 000 € de prêts d'honneur » sont tirés de la **même enveloppe** de 88 498 € (plan Juin 2026). Or la ligne « trésorerie de lancement » de ce plan ne fait que 14 607 € | doc 03, doc 05 | Regroupés en une ligne unique « enveloppe non affectée du plan Juin 2026 — 30 000 € », **à rapprocher du BP Juin 2026** (les emplois listés au doc 01 §5.3 ne totalisent que ≈ 49 000 € hors véhicule) |
| C11 | Capacité de production incohérente avec le CA : la Phase 2 exige **590 L/mois dès M5 et 1 470 L/mois à M12**, alors que les docs annoncent 150-300 L/mois (doc 02) ou 300-800 L/mois (doc 05) | doc 02 §1.5, doc 05 §7 | Exigence de capacité fixée (§2.3). Le dimensionnement du matériel Phase 2 est à valider par Lucien |
| C12 | Les subventions KAP TPE 2 et 3 sont versées **sur justificatifs, après l'achat**, et ne sont donc pas disponibles au moment du décaissement | doc 05 §5 | Encaissement modélisé environ 5 mois après l'achat (M10 et M18) |

---

## 2. Hypothèses de référence

### 2.1 Calendrier et périmètre

- M1 = août 2026. A1 = août 2026 à juillet 2027, A2 = août 2027 à juillet 2028, A3 = août 2028 à juillet 2029.
- Ce sont des années de modélisation, pas des exercices comptables. **À caler avec l'expert-comptable** sur la date de clôture réelle de la SAS (immatriculée le 9 octobre 2025).
- Montants HT. La TVA (8,5 % à La Réunion) est neutralisée : on néglige son effet de décalage sur les achats d'équipement.
- Délais de paiement clients : non modélisés. Un délai de 30 jours sur le canal B2B CHR immobiliserait environ 10 k€ à M12 et environ 21 k€ en croisière (cf. risques §8).

### 2.2 Chiffre d'affaires et marge (doc 02, inchangés)

| | A1 | A2 | A3 |
|---|---|---|---|
| CA HT | 140 900 € | 454 600 € | 500 000 € |
| COGS (% CA) | 18 % | 15 % | 14 % |
| Mix B2B CHR / Retail / Événementiel | Transition | → 50/30/20 | 50/30/20 |

Profil mensuel : celui du doc 02 §1 (Phase 1 M1-M4, ouverture du local M5, plateau à 41 600 € de M19 à M24, saisonnalité en A3).

> ⚠️ **Point de contrôle immédiat :** nous sommes à la fin de M3 (octobre 2026, JIE passée). Le réalisé d'août à octobre (cible : 300 + 600 + 1 000 €) doit être reporté dans le modèle avant toute transmission à un financeur.

### 2.3 Exigence de capacité (au prix moyen pondéré de 17 €HT/L)

| Mois | M5 | M8 | M12 | M16 | M19-M24 |
|---|---|---|---|---|---|
| Volume vendu requis | 590 L | 940 L | 1 470 L | 2 090 L | 2 450 L |

**La capacité du matériel Phase 2 (2 cuves de 500 L, 2 cuves de 300 L, 6 bacs de 50 L) doit atteindre environ 1 500 L/mois à M12.** Sinon la trajectoire de la Phase 2 est plafonnée par la production et non par la demande. La Phase 3 (M13) amène la capacité à 2 000-2 500 L/mois, ce qui sature dès M19 et confirme le besoin d'un site plus grand (Maison Sir'Ose) en fin d'A3.

### 2.4 Charges d'exploitation de référence

| Poste | A1 | A2 | A3 |
|---|---|---|---|
| Loyer local Saint-Pierre (1 500 €/mois dès M5) | 12 000 € | 18 000 € | 18 000 € |
| Fluides | 2 400 € | 3 600 € | 3 600 € |
| Assurances | 1 800 € | 2 000 € | 1 800 € |
| Communication / marketing | 12 000 € | 20 000 € | 15 000 € |
| Comptabilité / juridique | 5 000 € | 5 500 € | 6 000 € |
| Véhicule n°1 | 8 400 € | 10 000 € | 9 000 € |
| Véhicule n°2 (dès M13) *(C3)* | — | 6 000 € | 6 000 € |
| ERP traçabilité HACCP (dès M13) *(C3)* | — | 2 400 € | 2 400 € |
| Maintenance / divers | 3 000 € | 6 000 € | 8 000 € |
| Frais d'agence / notaire bail *(C4)* | 2 000 € | — | — |
| Masse salariale chargée | 7 350 € | 61 000 € | 100 000 € |
| **Total** | **53 950 €** | **134 500 €** | **169 800 €** |

Fondateurs à 0 € en A1 (ARE / RSA-APL), conformément au montage validé. **À vérifier avec l'expert-comptable :** la compatibilité du maintien du RSA du DG avec une société qui dégage environ 40 k€ de résultat dès l'A1, ainsi que la charge de production de la Phase 2 (jusqu'à 1 470 L/mois à M12) portée par deux fondateurs non rémunérés et un alternant.

---

## 3. Compte de résultat de référence

| Poste | **A1** | **A2** | **A3** |
|---|---|---|---|
| **Chiffre d'affaires HT** | **140 900 €** | **454 600 €** | **500 000 €** |
| COGS | 25 362 € | 68 190 € | 70 000 € |
| **Marge brute** | **115 538 € (82,0 %)** | **386 410 € (85,0 %)** | **430 000 € (86,0 %)** |
| Charges d'exploitation | 53 950 € | 134 500 € | 169 800 € |
| **EBE / EBITDA** | **61 588 € (43,7 %)** | **251 910 € (55,4 %)** | **260 200 € (52,0 %)** |
| Amortissements | 10 508 € | 26 883 € | 26 883 € |
| **Résultat d'exploitation** | **51 080 €** | **225 027 €** | **233 317 €** |
| Charges financières (prêt 50 k€ + prêt d'équipement 45 k€) | 2 730 € | 2 909 € | 2 179 € |
| **Résultat avant IS** | **48 351 €** | **222 118 €** | **231 138 €** |
| IS (15 % jusqu'à 42 500 €, puis 25 %) | 7 838 € | 51 279 € | 53 534 € |
| **Résultat net** | **40 513 €** | **170 838 €** | **177 603 €** |

**Écart par rapport au doc 02 :** le résultat net baisse de 7,7 k€ en A1 (48 191 € → 40 513 €), de 16,8 k€ en A2 et de 4,6 k€ en A3. **La cible d'EBITDA de 50-52 % en croisière est confirmée (52,0 %)**, mais pour de bonnes raisons cette fois : les lignes de charges correctement additionnées compensent l'ajout du véhicule n°2 et de l'ERP.

**Prudence :** les quotes-parts de subventions d'investissement virées au résultat (KAP TPE 1, 2 et 3, KAP Numérique) ne sont **pas** comptées en produit. C'est une réserve de prudence d'environ 1,6 k€/an pour le seul KAP TPE 1.

### 3.1 Seuil de rentabilité (A3)

- Charges fixes : 169 800 € de charges d'exploitation + 26 883 € d'amortissements + 2 179 € de charges financières = **198 862 €**
- Taux de marge sur coûts variables : 86 %
- **Seuil : ≈ 231 200 € HT/an, soit ≈ 19 270 €/mois**. Le mois le plus faible de l'A3 (mai, 37 000 €) le couvre 1,9 fois.

### 3.2 Couverture de la dette

| | A1 | A2 | A3 |
|---|---|---|---|
| Annuités (prêt 50 k€ à 909,59 €/mois ; prêt d'équipement à 838,94 €/mois dès M6) | 16 788 € | 20 982 € | 20 982 € |
| EBE / annuités | **3,7×** | **12,0×** | **12,4×** |

---

## 4. Plan d'investissement et d'amortissement de référence

| Immobilisation | Mise en service | Montant HT | Durée | Amort. A1 | A2 | A3 |
|---|---|---|---|---|---|---|
| KAP TPE 1 (lyophilisateur, ultrasonateur, ordinateurs) | M1 | 15 410 € | 5 / 5 / 3 ans | 3 296 € | 3 296 € | 3 296 € |
| Local — travaux HACCP + espace dégustation | M5 | 27 500 € | 10 ans | 1 833 € | 2 750 € | 2 750 € |
| Phase 2, vague 1 (cuves, chambre froide, ligne, pasteurisateur, filtration, CIP, tables, bacs, contrôle qualité) | M5 | 38 100 € | 7 / 5 / 3 ans | 4 589 € | 6 883 € | 6 883 € |
| Phase 2, vague 2 (étiqueteuse, 30 fûts, manutention) | M7 | 7 900 € | 5 ans | 790 € | 1 580 € | 1 580 € |
| Phase 3 (cuves de 1 000 L, froid, ligne, carbonatation, sertisseuse, 2e ultrason, 70 fûts, manutention) | M13 | 67 900 € | 7 / 5 ans | — | 12 374 € | 12 374 € |
| **Total** | | **156 810 €** | | **10 508 €** | **26 883 €** | **26 883 €** |

Non amortissables : dépôt de garantie de 5 000 € (versé à M5) et frais de bail de 2 000 € (en charge). Le séquencement en 2 vagues de la Phase 2 suit la recommandation du doc 05 §5.

---

## 5. Plan de financement consolidé du programme « local + matériel »

*Hors plan de financement initial de Juin 2026 (88 498 €), qui finance ses propres emplois : véhicule, KAP TPE 1, Kaza, stock et trésorerie de lancement.*

### 5.1 Besoins

| Besoin | Date | Montant HT |
|---|---|---|
| Murs (travaux, vitrine, dépôt de garantie, frais de bail) | M5 | 34 500 € |
| Matériel Phase 2 — vague 1 / vague 2 | M5 / M7 | 38 100 € / 7 900 € |
| Matériel Phase 3 | M13 | 67 900 € |
| **Total** | | **148 400 €** |

### 5.2 Ressources (statuts corrigés)

| Ressource | Date d'encaissement | Montant | Statut réel |
|---|---|---|---|
| Apport complémentaire des associés | M4 | 10 000 € | À mobiliser |
| Enveloppe non affectée du plan Juin 2026 (prêts d'honneur + marge sur le prêt de 50 k€) | M5 | 30 000 € | **Conditionnée** à l'octroi du prêt (demande en cours) et des prêts d'honneur (en instruction). Montant à rapprocher du BP Juin 2026 (C10) |
| **Prêt d'équipement Phase 2 (nouveau, cf. §6)** | M5 | **45 000 €** | **À solliciter** : 60 mois, taux hypothèse de 4,5 %. Alternative : crédit-bail sur la ligne de remplissage et la chambre froide |
| Subvention KAP TPE round 2 | M10 (sur justificatifs) | 10 000 € | À déposer **avant** tout achat éligible |
| Subvention KAP TPE round 3 | M18 (sur justificatifs) | 10 000 € | À déposer, éligibilité à reconfirmer |
| Autofinancement (flux d'exploitation nets M1-M13) | Au fil de l'eau | Solde | Généré — couvre la Phase 3 à M13 (cf. §6) |

Le dépôt de garantie de 5 000 € déjà budgété dans le plan Juin 2026 n'est **pas** recompté ici : il est payé par l'enveloppe ci-dessus.

---

## 6. Plan de trésorerie de référence (flux incrémentaux du programme)

*Point de départ fixé à 0 à M1. La trésorerie de lancement du plan Juin 2026 (14 607 €) reste en coussin, en plus. Les flux comprennent l'EBE, le service de la dette, les investissements, les ressources du §5.2 et l'IS (décaissé 4 mois après la clôture : M16, M28).*

| | M3 | M4 | M5 | M7 | M10 | M12 | M13 | M16 | M18 | M24 | M36 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Sans prêt d'équipement** (plan des docs 03/05) | −8,7 k€ | −0,9 k€ | **−40,5 k€** | −39,7 k€ | −4,2 k€ | 22,2 k€ | **−34,0 k€** | 5,6 k€ | 57,7 k€ | 197,1 k€ | 394,7 k€ |
| **Référence (avec prêt d'équipement de 45 k€)** | −8,7 k€ | −0,9 k€ | **+4,5 k€** | +3,6 k€ | +36,6 k€ | 61,3 k€ | **+4,2 k€** | 41,7 k€ | 92,1 k€ | 226,5 k€ | 414,4 k€ |

**Verdict :** le plan de financement des docs 03 et 05 est **équilibré en montant mais pas dans le temps**. Sans ressource nouvelle, il manque environ 40 k€ à l'ouverture du local (M5) et environ 34 k€ à l'achat de la Phase 3 (M13). Le prêt d'équipement de 45 k€ ferme les deux trous : le point bas reste à −8,7 k€ à M3, couvert par la trésorerie de lancement de 14,6 k€. Il ne dégrade le résultat que d'environ 1 k€/an et laisse la couverture de la dette à 3,7× dès l'A1.

Alternatives équivalentes, à arbitrer par les associés : crédit-bail sur environ 25 k€ de matériel combiné à un report de la vague 2, **ou** l'étalement de la Phase 3 en deux tranches (M13 et M19), qui réduit à lui seul le creux de M13 d'environ 30 k€.

---

## 7. Sensibilité (variante de référence)

| CA réalisé vs trajectoire | EBE A1 | Résultat net A1 | EBE A3 (marge) | Trésorerie au plus bas |
|---|---|---|---|---|
| 100 % | 61 588 € | 40 513 € | 260 200 € (52,0 %) | −8,7 k€ (couvert) |
| 80 % | 38 480 € | 21 457 € | 174 200 € (43,5 %) | −23,6 k€ |
| 70 % | 26 927 € | 11 636 € | 131 200 € (37,5 %) | −37,6 k€ |
| 50 % | 3 819 € | −9 418 € | 45 200 € (18,1 %) | −65,4 k€ |

Le modèle tient en rentabilité jusqu'à −30 % de CA, mais **pas en trésorerie** au-delà de −15 % environ, si l'on garde les mêmes dates d'investissement. **Règle de pilotage retenue :** la Phase 3 (M13) n'est engagée que si le CA cumulé de M5 à M12 atteint au moins 80 % de la trajectoire, soit ≥ 110 000 € HT. Sinon elle est reportée ou fractionnée.

---

## 8. Risques et points ouverts

| Risque | Impact | Action |
|---|---|---|
| Saut de CA de M4 (1 500 €) à M5 (10 000 €), soit ×6,7, alors que la traction réelle est de 437,50 € en 7 mois | Trajectoire A1 | Confronter au réalisé d'août à octobre et au pipeline post-JIE. Signer des engagements CHR avant le bail |
| Capacité de la Phase 2 inférieure aux 1 470 L/mois requis à M12 (C11) | Plafonne le CA de la Phase 2 | Lucien valide les cycles de fermentation et la capacité réelle des cuves |
| Délais de paiement B2B (30 jours) | Environ −10 k€ de trésorerie à M12, environ −21 k€ en croisière | Paiement comptant pour le canal événementiel, acomptes sur les premières commandes CHR |
| Prêt de 50 k€ et prêts d'honneur non encore accordés | Tout le plan | Ne pas signer le bail avant l'accord de financement |
| Subventions KAP versées après l'achat | Trésorerie | Préfinancement (prêt d'équipement) déjà intégré |
| Statut social des fondateurs (ARE / RSA) avec une société rentable | Conformité, revenu des fondateurs | Validation par l'expert-comptable |
| Écart d'adresse du siège entre Saint-Denis et Saint-Pierre (doc 01 §1) | Dossiers administratifs | Clarification par l'expert-comptable |

---

## 9. Chiffres de référence (à reprendre à l'identique dans tout dossier)

| Indicateur | Valeur de référence |
|---|---|
| CA HT A1 / A2 / A3 | 140 900 € / 454 600 € / 500 000 € |
| EBITDA A1 / A2 / A3 | 61 588 € (43,7 %) / 251 910 € (55,4 %) / 260 200 € (52,0 %) |
| Résultat net A1 / A2 / A3 | 40 513 € / 170 838 € / 177 603 € |
| Investissement total (KAP TPE 1 + local + Phases 2-3) | 156 810 € HT amortissables + 5 000 € de dépôt de garantie |
| Besoin de financement du programme local + matériel | 148 400 € HT |
| Nouvelle ressource à obtenir | Prêt d'équipement de 45 000 € (ou crédit-bail équivalent) |
| Seuil de rentabilité A3 | ≈ 231 200 € HT/an (≈ 19 270 €/mois) |
| Capacité requise | ≈ 1 500 L/mois à M12, ≈ 2 450 L/mois à M19 |
