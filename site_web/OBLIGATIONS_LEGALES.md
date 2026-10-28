# Obligations légales du site web — SAS Sir'Ose (SIR'OTÉ)

*Checklist personnalisée pour une SAS réunionnaise qui fabrique et vend des koso, sirops et (bientôt) boissons alcoolisées (APE 1101Z), avec un site vitrine financé par KAP Numérique (FEDER). Ce document est un outil de travail, pas une consultation juridique : faites valider les points marqués ⚠️ par l'expert-comptable ou un juriste avant la mise en ligne.*

Légende : ✅ déjà intégré au site · 🟡 à compléter dans `config/sirose.json` · ⚠️ démarche ou validation à faire hors site

---

## 1. Mentions légales — LCEN, article 1-1 (ex-article 6-III)

Sanction si absentes : jusqu'à 1 an d'emprisonnement et 75 000 € d'amende (375 000 € pour une personne morale).

| Obligation | Statut |
|---|---|
| Raison sociale, forme, capital, siège, RCS, SIREN | ✅ SAS SIR'OSE, capital variable 1 000 €, RCS Saint-Denis 991 091 166 |
| N° TVA intracommunautaire | ✅ FR22 991 091 166 — ⚠️ calculé depuis le SIREN : vérifier sur VIES (ec.europa.eu/taxation_customs/vies) |
| Courriel et téléphone de contact | 🟡 `societe.email`, `societe.telephone` |
| Directeur de la publication | ✅ Lucien MOREAU, Président |
| Hébergeur : nom, adresse, téléphone | 🟡 `hebergeur.*` |
| Adresse du siège | ⚠️ Le siège légal est à Saint-Denis (89 bis Chemin des Fougères) mais les dossiers KAP indiquent Saint-Pierre. Le site affiche le siège Kbis + l'atelier Saint-Pierre. Si le siège a été transféré, mettre à jour le Kbis **et** `societe.siege`. |

## 2. Alcool — Code de la santé publique (Loi Évin)

Activé par `vente.vente_alcool: true` (APE 1101Z + Rhum Koso ~5 % en développement). Si vous ne vendez **aucune** boisson alcoolisée pour l'instant, passez-le à `false` : le contrôle d'âge et le bandeau sanitaire disparaissent.

| Obligation | Référence | Statut |
|---|---|---|
| Message sanitaire « L'abus d'alcool est dangereux pour la santé, à consommer avec modération. » sur toute publicité pour l'alcool | Art. L3323-4 CSP | ✅ pied de chaque page |
| Interdiction de vente aux mineurs, possibilité d'exiger une pièce d'identité | Art. L3342-1 CSP | ✅ contrôle d'âge + CGV §3 |
| Contenu publicitaire limité aux informations objectives : degré, origine, composition, mode d'élaboration, terroir, qualités gustatives. Pas d'association à la fête, au sport, à la réussite sociale ou sexuelle | Art. L3323-4 CSP | ✅ textes actuels conformes — ⚠️ à respecter pour toute photo ou texte ajouté (pas de photos de soirée avec des bouteilles d'alcool, pas de verre à la main d'une personne jeune) |
| Pas de publicité alcool sur un site destiné à la jeunesse ou au sport ; pas de pop-up intrusive | Art. L3323-2 9° CSP | ✅ |
| Licence de vente à emporter (la vente à distance est une vente à emporter) + permis de vente à emporter / formation | Art. L3331-4 CSP | ⚠️ démarche en mairie de Saint-Pierre, puis renseigner `vente.licence_alcool` |
| Statut fiscal de production d'alcool (entrepositaire agréé, déclaration en douane) | Code des impositions sur les biens et services | ⚠️ à voir avec la Direction régionale des douanes de La Réunion avant de produire le Rhum Koso |
| Interdiction d'offrir de l'alcool gratuitement à des fins commerciales (sauf dégustation en vue de la vente) | Art. L3322-9 CSP | ⚠️ attention aux jeux-concours sur les réseaux sociaux |

## 3. Information sur les produits alimentaires

| Obligation | Référence | Statut |
|---|---|---|
| Avant tout achat à distance : dénomination, ingrédients, **allergènes**, quantité, conditions de conservation, nom/adresse de l'exploitant, titre alcoométrique (si > 1,2 % vol.) | Règl. (UE) 1169/2011 art. 9 et 14 | ✅ structure prête — 🟡 `produits[].ingredients`, `produits[].allergenes` |
| Prix TTC + **prix au litre** pour les liquides | Code conso L112-1, Dir. 98/6/CE | ✅ |
| TVA à La Réunion : 2,1 % (sirops et boissons sans alcool), 8,5 % (boissons alcoolisées) | CGI art. 296 | ⚠️ confirmer les taux avec l'expert-comptable |
| **Allégations de santé** : interdiction de « probiotique », « détox », « bon pour la digestion », « renforce l'immunité »… sauf allégation autorisée par l'UE | Règl. (CE) 1924/2006 | ✅ aucune sur le site — ⚠️ point de vigilance majeur pour le koso, souvent vendu avec ce vocabulaire |
| Toute allégation de santé est **interdite** sur une boisson de plus de 1,2 % vol. | Règl. 1924/2006 art. 4.3 | ⚠️ Rhum Koso |
| Mention « bio » réservée aux produits certifiés | Règl. (UE) 2018/848 | ⚠️ le terme « bio-fermentation » du business plan est à éviter sur le site |
| « Artisan / artisanal / fait maison » réservé aux entreprises inscrites au registre des artisans | Loi 96-603 art. 21 | ⚠️ vérifier votre immatriculation avant d'utiliser ce mot |
| Pictogramme femme enceinte sur les étiquettes des boissons alcoolisées | Art. L3322-2 CSP | ⚠️ étiquetage (hors site) |

## 4. Allégations environnementales

Depuis le **27 septembre 2026**, la directive (UE) 2024/825 « transition verte » interdit les allégations environnementales génériques non prouvées (« éco-responsable », « respectueux de l'environnement », « vert », « durable ») et les allégations de neutralité carbone fondées sur la compensation. La loi AGEC (art. 13) interdit déjà « biodégradable » et « respectueux de l'environnement » sur les produits et emballages.

- ✅ Le site décrit des **faits précis et vérifiables** (« à partir d'agrumes pressés, de cosses de cacao… »).
- ⚠️ Les formules du pitch JIE « Zéro déchet, 100 % circulaire » sont à éviter sur le site et les étiquettes, sauf à pouvoir le prouver (bilan matière). Préférez « nous valorisons X kg de co-produits par mois ».

## 5. Conditions générales de vente (consommateurs)

| Obligation | Référence | Statut |
|---|---|---|
| CGV accessibles avant la commande | Code conso L221-5 | ✅ `cgv.html` |
| Droit de rétractation 14 jours + **formulaire type** + exceptions (denrées périssables, produits descellés) | L221-18, L221-28 | ✅ |
| Encadré « garantie légale de conformité » + vices cachés | L217-3 et s., D211-2 | ✅ |
| Médiateur de la consommation (gratuit pour le client) | L612-1 | 🟡 `vente.mediateur_*` — ⚠️ adhérer à un médiateur agréé (liste sur economie.gouv.fr/mediation-conso) |
| Délai de livraison (à défaut : 30 jours max) | L216-1 | 🟡 `vente.delai_livraison` |
| Si vente en ligne : bouton « Commande avec obligation de paiement » et confirmation sur support durable | L221-14, L221-13 | ⚠️ seulement si `vente.vente_en_ligne` passe à `true` |
| Lien vers la plateforme européenne de règlement en ligne des litiges | — | Plus obligatoire : la plateforme a fermé le 20 juillet 2025 (Règl. (UE) 2024/3228) |

## 6. Données personnelles et cookies — RGPD / CNIL

| Obligation | Statut |
|---|---|
| Politique de confidentialité (responsable, finalités, bases légales, durées, droits, réclamation CNIL) | ✅ `confidentialite.html` |
| Bandeau cookies | ✅ **inutile** : le site n'utilise aucun traceur soumis à consentement. Le contrôle d'âge utilise le stockage de session, sans cookie. |
| Si ajout de Google Analytics, Meta Pixel, YouTube, Google Maps… | ⚠️ il faudra un bandeau conforme CNIL (« Tout refuser » aussi visible que « Tout accepter ») — préférer Matomo configuré en mode exempté |
| Registre des traitements (même pour une TPE) | ⚠️ un tableur simple suffit : clients, prospects CHR, contacts |
| Formulaire de contact : case d'information + lien vers la politique | ⚠️ si un formulaire est ajouté |
| Prospection par e-mail : consentement préalable pour les particuliers ; information + droit d'opposition pour les professionnels | ⚠️ newsletters |

## 7. Financement européen — KAP Numérique (FEDER)

Le site est cofinancé à 80 % par le FEDER : la publicité du financement est une **condition du versement de la subvention** (Règl. (UE) 2021/1060 art. 47 et 50).

- ✅ Emblème de l'UE + mention « Cofinancé par l'Union européenne » + description de l'opération dans le pied de page.
- ⚠️ Vérifier dans la convention KAP Numérique si le logo de la Région Réunion est aussi exigé, et remplacer `assets/embleme-ue.svg` par le fichier officiel (european-union.europa.eu → Emblème de l'UE).
- ⚠️ Garder des captures d'écran datées du site comme preuve pour le dossier de paiement.

## 8. Accessibilité

La directive européenne sur l'accessibilité (en vigueur depuis le 28 juin 2025) exempte les **microentreprises** (moins de 10 salariés et moins de 2 M€ de CA ou de bilan) pour les services. Sir'Ose est exemptée aujourd'hui ; le site respecte déjà les bases (langue déclarée, lien d'évitement, contrastes, navigation au clavier, textes alternatifs). À réexaminer si l'entreprise dépasse ces seuils.

## 9. Propriété intellectuelle

- ⚠️ Déposer la marque **SIR'OTÉ** à l'INPI (classes 32 boissons sans alcool, 33 boissons alcoolisées hors bière, 30 biscuits/infusions) si ce n'est pas fait.
- ⚠️ Récupérer une cession de droits écrite de l'agence Kaza (identité visuelle) et des photographes.
- ⚠️ Mentionner les partenaires (Délices d'Amandine, Calicoco, Rhum au Thé, Villa Delisle) **avec leur accord écrit**, surtout pour leurs logos.
