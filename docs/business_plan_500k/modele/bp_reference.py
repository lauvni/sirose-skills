"""Modèle de calcul du BP de référence — SAS Sir'Ose (doc 00).

Toutes les valeurs du document 00_BP_reference.md sont produites par ce script :
    python3 docs/business_plan_500k/modele/bp_reference.py

M1 = août 2026. Années de modélisation : A1 = M1-M12, A2 = M13-M24, A3 = M25-M36.
Montants en euros HT (TVA neutralisée — voir hypothèses du doc 00).
"""

MOIS = 36

# --- Chiffre d'affaires mensuel (trajectoire doc 02, inchangée) -------------
CA = (
    [300, 600, 1_000, 1_500]                                          # Phase 1
    + [10_000, 12_000, 14_000, 16_000, 18_000, 20_000, 22_500, 25_000]  # Phase 2
    + [28_000, 30_500, 33_000, 35_500, 38_000, 40_000] + [41_600] * 6  # Phase 3
    + [46_000, 40_000, 44_000, 42_000, 43_000, 45_000,
       42_000, 40_000, 38_000, 37_000, 38_000, 45_000]                 # Année 3
)
PRIX_MOYEN_L = 17.0                 # €HT/L pondéré (doc 02 §6)

# Plafond de production (L/mois) par mois, None = pas de plafond.
# Scénario « contraint par les devis » (doc 00 §10) : tous les devis d'octobre 2026
# sont dimensionnés pour 400-500 L/mois → plafond 500 L/mois de M5 à M12.
PLAFOND_L = None


def ca_mois(m):
    ca = CA[m - 1]
    if PLAFOND_L is not None and PLAFOND_L.get(m) is not None:
        ca = min(ca, PLAFOND_L[m] * PRIX_MOYEN_L)
    return ca
COGS_TAUX = {1: 0.18, 2: 0.15, 3: 0.14}

# --- Charges d'exploitation mensuelles --------------------------------------
def annee(m):
    return (m - 1) // 12 + 1


def opex_mois(m):
    a = annee(m)
    local_ouvert = m >= 5
    lignes = {
        "Loyer local Saint-Pierre": 1_500 if local_ouvert else 0,
        "Fluides": 300 if local_ouvert else 0,
        "Assurances": {1: 1_800, 2: 2_000, 3: 1_800}[a] / 12,
        "Communication / marketing": {1: 12_000, 2: 20_000, 3: 15_000}[a] / 12,
        "Comptabilité / juridique": {1: 5_000, 2: 5_500, 3: 6_000}[a] / 12,
        "Véhicule n°1 (leasing, carburant, entretien)": {1: 8_400, 2: 10_000, 3: 9_000}[a] / 12,
        # Ajouts Thémis : postes chiffrés dans le doc 05 mais absents du P&L du doc 02
        "Véhicule n°2 (dès M13, hypothèse)": 500 if m >= 13 else 0,
        "Logiciel ERP traçabilité HACCP (dès M13)": 200 if m >= 13 else 0,
        "Maintenance équipements / divers": {1: 3_000, 2: 6_000, 3: 8_000}[a] / 12,
        # Ajout Thémis (mails oct. 2026) : analyses alcool / sucres en laboratoire
        # (Anton Paar n'est pas un labo prestataire) — provision en attente de devis
        "Analyses laboratoire (provision)": {1: 2_000, 2: 1_500, 3: 1_500}[a] / 12,
        "Frais d'agence / notaire bail (charge M5)": 2_000 if m == 5 else 0,
        "Masse salariale chargée": (
            (1_050 if m >= 6 else 0) if a == 1 else {2: 61_000, 3: 100_000}[a] / 12
        ),
    }
    return lignes


# --- Immobilisations (mise en service, montant HT, durée en années) ---------
IMMOS = [
    # KAP TPE round 1 — supposé en service à M1
    ("KAP TPE 1 — lyophilisateur", 1, 7_078.34, 5),
    ("KAP TPE 1 — ultrasonateur UP400St", 1, 6_728.11, 5),
    ("KAP TPE 1 — ordinateurs", 1, 1_603.67, 3),
    # Local — volet murs (dépôt de garantie non amortissable, frais de bail en charge)
    ("Local — travaux HACCP", 5, 17_500, 10),
    ("Local — espace dégustation / vitrine", 5, 10_000, 10),
    # Phase 2 — vague 1 à M5 (postes critiques HACCP)
    ("P2 — cuves 500 L + 300 L, chambre froide", 5, 5_600 + 3_600 + 6_500, 7),
    ("P2 — ligne remplissage, pasteurisateur, filtration, CIP, tables, bacs", 5,
     9_500 + 4_500 + 2_100 + 1_800 + 1_500 + 1_800, 5),
    ("P2 — contrôle qualité", 5, 1_200, 3),
    # Machine sous vide double cloche Befor SVF 2-600 (prix public HT, mail Befor
    # du 28/10/2026, hors transport / octroi de mer, remise distributeur non connue)
    ("P2 — machine sous vide Befor SVF 2-600", 5, 11_326, 5),
    # Phase 2 — vague 2 à M7 (étiqueteuse, fûts, manutention)
    ("P2 — étiqueteuse, 30 fûts, manutention", 7, 2_200 + 4_500 + 1_200, 5),
    # Phase 3 — à M13
    ("P3 — cuves 1 000 L, extension froid, groupe froid", 13, 12_600 + 5_000 + 3_500, 7),
    ("P3 — upgrade ligne, carbonatation, sertisseuse, 2e ultrason, 70 fûts, manutention", 13,
     12_000 + 6_800 + 5_500 + 8_500 + 10_500 + 3_500, 5),
]
DEPOT_GARANTIE = 5_000  # versé à M5, non amortissable


def amort_mois(m):
    total = 0.0
    for _, debut, montant, duree in IMMOS:
        if debut <= m < debut + duree * 12:
            total += montant / (duree * 12)
    return total


def capex_mois(m):
    return sum(montant for _, debut, montant, _ in IMMOS if debut == m and debut > 1)


# --- Prêt bancaire 50 000 €, 60 mois, 3,5 %, 1re échéance M1 ---------------
PRET, TAUX, DUREE = 50_000, 0.035 / 12, 60
ECHEANCE = PRET * TAUX / (1 - (1 + TAUX) ** -DUREE)

# Variante de référence retenue (doc 00 §6) : prêt d'équipement Phase 2
# 45 000 €, 60 mois, 4,5 % (taux hypothèse), décaissé à M5, 1re échéance M6.
PRET_EQUIP = (45_000, 0.045 / 12, 60, 5)


def tableau_pret(montant, taux, duree, debut=0):
    echeance = montant * taux / (1 - (1 + taux) ** -duree)
    crd, lignes = montant, [(0.0, 0.0)] * debut
    for _ in range(duree):
        interets = crd * taux
        capital = echeance - interets
        crd -= capital
        lignes.append((interets, capital))
    return lignes + [(0.0, 0.0)] * MOIS


PRET_LIGNES = tableau_pret(PRET, TAUX, DUREE)
AVEC_PRET_EQUIP = False


def service_dette(m):
    i, c = PRET_LIGNES[m - 1]
    if AVEC_PRET_EQUIP:
        i2, c2 = tableau_pret(*PRET_EQUIP)[m - 1]
        i, c = i + i2, c + c2
    return i, c


def impot(resultat):
    if resultat <= 0:
        return 0.0
    return min(resultat, 42_500) * 0.15 + max(resultat - 42_500, 0) * 0.25


# --- Financements externes du programme local + matériel --------------------
# (hors plan de financement initial Juin 2026, déjà consommé par ses propres emplois)
FINANCEMENTS = {
    4: ("Apport complémentaire associés", 10_000),
    5: ("Enveloppe non affectée du plan Juin 2026 (prêts d'honneur + marge prêt)", 30_000),
    10: ("KAP TPE round 2 (versée sur justificatifs, ~5 mois après achat)", 10_000),
    18: ("KAP TPE round 3 (versée sur justificatifs)", 10_000),
}


def calcul():
    pl = {a: dict(ca=0, cogs=0, opex=0, amort=0, interets=0) for a in (1, 2, 3)}
    opex_detail = {a: {} for a in (1, 2, 3)}
    mensuel = []
    for m in range(1, MOIS + 1):
        a = annee(m)
        ca = ca_mois(m)
        cogs = ca * COGS_TAUX[a]
        lignes = opex_mois(m)
        opex = sum(lignes.values())
        amort = amort_mois(m)
        interets, capital = service_dette(m)
        p = pl[a]
        p["ca"] += ca
        p["cogs"] += cogs
        p["opex"] += opex
        p["amort"] += amort
        p["interets"] += interets
        for k, v in lignes.items():
            opex_detail[a][k] = opex_detail[a].get(k, 0) + v
        mensuel.append(dict(m=m, ca=ca, ebe=ca - cogs - opex, capital=capital,
                            interets=interets, capex=capex_mois(m)
                            + (DEPOT_GARANTIE if m == 5 else 0)))
    for a, p in pl.items():
        p["mb"] = p["ca"] - p["cogs"]
        p["ebe"] = p["mb"] - p["opex"]
        p["rex"] = p["ebe"] - p["amort"]
        p["rai"] = p["rex"] - p["interets"]
        p["is"] = impot(p["rai"])
        p["rn"] = p["rai"] - p["is"]
    return pl, opex_detail, mensuel


def tresorerie(mensuel, pl, avec_financements=True):
    """Trésorerie incrémentale du programme (point de départ 0 à M1).

    IS de l'année N décaissé 4 mois après sa clôture (M16, M28).
    """
    is_dates = {16: pl[1]["is"], 28: pl[2]["is"]}
    solde, serie = 0.0, []
    for r in mensuel:
        m = r["m"]
        flux = r["ebe"] - r["interets"] - r["capital"] - r["capex"] - is_dates.get(m, 0)
        if avec_financements and m in FINANCEMENTS:
            flux += FINANCEMENTS[m][1]
        if AVEC_PRET_EQUIP and m == PRET_EQUIP[3]:
            flux += PRET_EQUIP[0]
        solde += flux
        serie.append((m, flux, solde))
    return serie


def sensibilite(facteur):
    global CA
    base = CA
    CA = [c * facteur for c in base]
    try:
        pl, _, mensuel = calcul()
        serie = tresorerie(mensuel, pl)
        return pl, min(s for _, _, s in serie)
    finally:
        CA = base


def e(x):
    return f"{x:,.0f} €".replace(",", " ")


if __name__ == "__main__":
    pl, opex_detail, mensuel = calcul()
    print("== P&L ==")
    for k in ("ca", "cogs", "mb", "opex", "ebe", "amort", "rex", "interets", "rai", "is", "rn"):
        print(f"{k:9}", *(e(pl[a][k]).rjust(12) for a in (1, 2, 3)))
    print("marge EBE", *(f"{pl[a]['ebe'] / pl[a]['ca']:.1%}".rjust(12) for a in (1, 2, 3)))
    print("\n== Détail opex ==")
    for k in opex_detail[1]:
        print(f"{k[:60]:60}", *(e(opex_detail[a][k]).rjust(10) for a in (1, 2, 3)))
    print("\n== Amortissements par immo (A1/A2/A3) ==")
    for nom, debut, montant, duree in IMMOS:
        par_an = [sum(montant / (duree * 12) for m in range(12 * (a - 1) + 1, 12 * a + 1)
                      if debut <= m < debut + duree * 12) for a in (1, 2, 3)]
        print(f"{nom[:70]:70} {e(montant):>10}", *(e(x).rjust(9) for x in par_an))
    print(f"\nÉchéance prêt : {ECHEANCE:,.2f} €/mois")
    print("Volumes L/mois requis :", [round(c / PRIX_MOYEN_L) for c in CA[:24]])
    print("Volumes annuels L :", [round(sum(CA[12 * a:12 * a + 12]) / PRIX_MOYEN_L) for a in range(3)])
    print("\n== Trésorerie incrémentale (sans financements externes) ==")
    for m, f, s in tresorerie(mensuel, pl, avec_financements=False):
        print(f"M{m:02d} flux {e(f):>12} cumul {e(s):>12}")
    print("\n== Trésorerie incrémentale (avec financements) ==")
    for m, f, s in tresorerie(mensuel, pl):
        print(f"M{m:02d} flux {e(f):>12} cumul {e(s):>12}")
    a3 = pl[3]
    fixes = a3["opex"] + a3["amort"] + a3["interets"]
    tmcv = a3["mb"] / a3["ca"]
    print(f"\nSeuil A3 : charges fixes {e(fixes)} / {tmcv:.1%} = {e(fixes / tmcv)} ({e(fixes / tmcv / 12)}/mois)")
    AVEC_PRET_EQUIP = True
    pl_v, _, mensuel_v = calcul()
    print("\n== Variante retenue : prêt d'équipement 45 k€ ==")
    print("interets", *(e(pl_v[a]["interets"]) for a in (1, 2, 3)), "RN", *(e(pl_v[a]["rn"]) for a in (1, 2, 3)))
    for m, f, s_ in tresorerie(mensuel_v, pl_v):
        print(f"M{m:02d} flux {e(f):>12} cumul {e(s_):>12}")
    PLAFOND_L = {m: 500 for m in range(5, 13)}
    pl_c, _, mensuel_c = calcul()
    print("\n== Scénario contraint par les devis (500 L/mois M5-M12) ==")
    for k in ("ca", "ebe", "rn"):
        print(k, *(e(pl_c[a][k]) for a in (1, 2, 3)))
    print("marge EBE", *(f"{pl_c[a]['ebe'] / pl_c[a]['ca']:.1%}" for a in (1, 2, 3)))
    serie_c = tresorerie(mensuel_c, pl_c)
    print("tréso", [(m, round(s_ / 1000, 1)) for m, _, s_ in serie_c if m in (3, 4, 5, 7, 10, 12, 13, 16, 18, 24, 36)])
    print("tréso mini", e(min(s_ for _, _, s_ in serie_c)))
    PLAFOND_L = None
    print("\n== Sensibilité CA (variante retenue) ==")
    for f in (1.0, 0.8, 0.7, 0.5):
        p, mini = sensibilite(f)
        print(f"CA x{f}: EBE A1 {e(p[1]['ebe'])} RN A1 {e(p[1]['rn'])} EBE A3 {e(p[3]['ebe'])} "
              f"({p[3]['ebe'] / p[3]['ca']:.1%}) tréso mini {e(mini)}")
