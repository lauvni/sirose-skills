---
name: sirose-dossiers-financement
description: Préparation et contrôle des dossiers de financement et de subvention de Sir'Ose — Crédit Agricole (Propulse by CA), Bpifrance Garantie Création, France Active Réunion, Initiative Réunion, KAP TPE et KAP Numérique (Région Réunion), FEDER, ADEME. Utiliser pour dresser la liste des pièces, vérifier un dossier avant dépôt ou répondre à une demande de complément.
---

# Dossiers de financement — Sir'Ose

Responsable : **Steiner**. Les contacts des chargés d'affaires sont dans la mémoire Kairos et le Drive, jamais dans le dépôt.

## 1. Pièces communes (à vérifier pour chaque dossier)

| Pièce | Critère de validité |
|---|---|
| Kbis | Moins de 3 mois, **adresse du siège à jour** (registre R01) |
| Statuts à jour | Signés, cohérents avec le capital déclaré (R07) |
| Pièces d'identité des dirigeants | En cours de validité |
| Attestation de régularité fiscale | Délivrée par le SIE. **Bloquée tant que la liasse 2025 n'est pas déposée** (R03) |
| Attestation de vigilance URSSAF | Si elle est demandée |
| Liasse / comptes 2025 | Déposés et approuvés |
| Business plan + prévisionnel sur 3 ans | **Une seule version de référence** (skill `sirose-business-plan`, R10) |
| Plan de financement | Mêmes montants dans tous les dossiers |
| Devis | Datés de moins de 6 mois, au nom de la SAS |
| RIB professionnel | Libellé identique à la raison sociale (R08) |
| Justificatif du lieu d'activité | Bail ou convention **en cours de validité** (R06) |
| Preuves de traction | Factures, bons de livraison, devis signés. Les lettres d'intention sont présentées comme pipeline, pas comme CA |

## 2. Spécificités par financeur (à confirmer auprès de chaque organisme)

- **Crédit Agricole / Propulse by CA :** le BP saisi dans Propulse doit être **identique** au BP de référence (montant total, CA An 1, ventilation).
- **Bpifrance Garantie Création :** garantie d'une partie du prêt bancaire, demandée par la banque, qui facilite l'accord de crédit.
- **France Active Réunion / Initiative Réunion :** prêts d'honneur aux dirigeants et comité d'engagement. Ils exigent un dossier complet (Kbis à jour, attestation fiscale) et un plan de financement cohérent avec la banque.
- **KAP TPE / KAP Numérique (Région Réunion) :** subventions sur dépenses éligibles (matériel, numérique), avec un calendrier et des justificatifs de dépense. ⚠️ **Sans lieu de production**, l'installation et l'utilisation du matériel subventionné doivent être expliquées (R06).
- **ADEME / FEDER :** valorisation matière et économie circulaire. Ce sont des dossiers longs, à préparer une fois la phase 1 financée.

## 3. Procédure de contrôle avant dépôt

1. Lister les pièces demandées (site, e-mail du financeur dans Gmail) et l'état de chacune : ✅ disponible et valide / ⚠️ à mettre à jour / ❌ manquante.
2. Faire passer chaque pièce au contrôle du skill `sirose-admin-sas`.
3. Vérifier que **montants, dates et adresses sont identiques** dans toutes les pièces du dossier et entre les dossiers déjà déposés ailleurs.
4. Restituer une checklist (pièce · état · action · responsable · échéance) dans `docs/conformite/verifications/`, et inscrire au registre chaque blocage nouveau.
5. Si une pièce manque à cause d'un blocage administratif, nommer **la ligne du registre qui bloque**, pour que ZEUS priorise le déblocage.
