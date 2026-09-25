# Sujets des Concours Nationaux du Cameroun (2012 → aujourd'hui)

## Objectif
Collecte, téléchargement et organisation des épreuves/sujets des concours nationaux camerounais
de **2012 à aujourd'hui** via scraping de plateformes éducatives.

## Arborescence
```
sujets_concours/
└── [Nom_du_Concours]/
    └── [Categorie_ou_Filiere]/
        └── Session_[Annee]/
            └── [Epreuve_Annee_NomConcours].pdf
```
Convention de nommage : `[NomDuConcours]_[Filiere]_[NomDeLEpreuve]_[Annee].pdf`

## Concours couverts (42 PDF validés)
| Concours | Épreuves | Sessions |
|---|---|---|
| **ENAM** (14) | Culture Générale, Droit Public, Économie, Statistique, Langue, Organisation Judiciaire | 2012–2015 |
| **ENS Yaoundé** (17) | Maths, Analyse, Physique, Biologie, Histoire, Géo, Philo, Culture G., Maths-Info, 2nd cycle | 2012–2014, 2021 |
| **FASA Dschang** (6) | Maths, Biologie, Chimie-Physique | 2012–2014 |
| **ENIEG** (2) | Culture Générale | 2012–2013 |
| **ENIET** (3) | Maths, Étude de cas, Culture Générale | 2021 |

## Sources ciblées
| Source | Utilisation |
|---|---|
| edukamer.info (Google Drive) | ENS, FASA, ENIEG — liens Drive publics, gratuits |
| concourscameroon.com (Google Drive) | ENAM (filières DARF, Greffe, Contrôleur, etc.) |
| promouvoircompetences.com | ENS 2nd cycle 2021, ENIET 2021 (PDF directs avec Referer) |
| cameroondeskacademy.com | Référence (contenus payants ~400–600 FCFA) |
| kamerpower.com | Référence (contenus via app payante) |
| polytechnique.cm (officiel) | Informations concours, pas de sujets publics |

## Épreuves manquées / non récupérables
- **Polytechnique ENSPY** (2016→2024) : sujets payants (cameroondeskacademy, kamerpower).
- **CUSS / IDE – MINSANTE (infirmiers)** : pas de dépôt public gratuit trouvé.
- **IRIC, Mines Maroua, ENAM ≥ 2016** : pages bloquées (timeouts/406) ou contenus payants.

## Suivi
- `rapport_telechargement.json` : inventaire détaillé (fichiers, tailles, sessions, sources).
- `logs_telechargement.txt` : journal de téléchargement.
- `SYNTHESE_COLLECTE.md` : rapport lisible.