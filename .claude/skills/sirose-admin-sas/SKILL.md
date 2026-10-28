---
name: sirose-admin-sas
description: Vie juridique, administrative et fiscale de la SAS Sir'Ose — Kbis et transfert de siège, domiciliation, code APE, capital variable, approbation et dépôt des comptes, liasse fiscale 2065/2033 via Indy, attestation de régularité fiscale, compte courant d'associé, TVA CA3. Utiliser pour vérifier ou préparer une formalité, un PV, un courrier à l'INSEE, au SIE ou au greffe.
---

# Administration de la SAS — Sir'Ose

Responsable par défaut : **Lucien** pour le juridique (greffe, INSEE, AG), **Steiner** pour la fiscalité liée au financement (Indy, attestation). Toute conclusion fiscale ou comptable porte la mention « à valider par Exco ».

## 1. Identité : données à contrôler sur chaque document

| Donnée | Pièce qui fait foi | Contrôle |
|---|---|---|
| Raison sociale / nom commercial | Statuts + Kbis | SIR'OSE / SIR'OTÉ. Comparer avec le libellé du compte Qonto (registre R08) |
| SIREN | Kbis | 991 091 166 |
| Siège social | **Kbis à jour** | Doit correspondre au PV de transfert, à la domiciliation, aux factures et à Qonto (R01) |
| Capital | Statuts + dernier PV | Distinguer **capital souscrit** et **plafond du capital variable** (R07) |
| Code APE | Avis de situation INSEE | Doit refléter l'activité réelle : sirops / boissons sans alcool (R04) |
| Dirigeants | Kbis | Président Lucien MOREAU, DG Alexandre STEINER |

## 2. Formalités à suivre

- **Transfert de siège :** la décision (PV) doit être suivie d'une formalité au **guichet unique (INPI)** dans le mois, avec un justificatif de jouissance des locaux. Le Kbis n'est à jour qu'à l'issue de cette formalité.
- **Domiciliation :** l'attestation du propriétaire ou du bailleur doit désigner **la société** (SAS SIR'OSE, SIREN), pas un associé à titre personnel. Sinon, risque de rejet par le greffe.
- **Code APE :** il est attribué par l'INSEE d'après l'activité déclarée. On en demande la modification à l'INSEE en justifiant l'activité réelle, et on informe en parallèle le **SIE** pour sécuriser le taux de TVA.
- **Comptes annuels :** approbation par les associés **dans les 6 mois** suivant la clôture (prorogation possible sur requête au tribunal), puis **dépôt au greffe** dans le mois. Une option de confidentialité existe pour les micro-entreprises.
- **Liasse fiscale IS** (2065 + 2033, régime réel simplifié), télétransmise en EDI-TDFC via **Indy**. Un retard entraîne des pénalités et **bloque l'attestation de régularité fiscale**, donc tous les financements.
- **Dépenses de constitution payées par un associé** (par exemple les frais d'avocat) : elles s'inscrivent en **compte courant d'associé**, pas en charge payée directement par la société.
- **TVA :** déclarations CA3 sur impots.gouv.fr (régime et périodicité à vérifier dans l'espace professionnel). Taux DOM : voir le skill `sirose-reglementation`.
- **Registre des bénéficiaires effectifs :** à mettre à jour en cas de changement de détention.

## 3. Procédure de vérification d'une pièce administrative

1. Identifier la pièce (type, date, signataire, version) et son emplacement dans le Drive.
2. Contrôler les données d'identité du § 1, ligne par ligne.
3. Vérifier la cohérence avec les autres pièces : Kbis ↔ PV ↔ domiciliation ↔ Qonto ↔ factures ↔ dossiers de financement.
4. Vérifier les délais légaux (§ 2) par rapport à la date du jour.
5. Restituer un tableau constat · gravité · action · responsable · échéance, et mettre à jour le registre.

## 4. Production de documents

Modèles à préparer, avec le plan d'abord puis le .docx : demande de modification APE (INSEE), courrier au SIE (taux de TVA, attestation de régularité), attestation de domiciliation au nom de la société, PV de décision du Président, PV d'approbation des comptes, demande de prorogation du délai d'approbation, convention de compte courant d'associé.
