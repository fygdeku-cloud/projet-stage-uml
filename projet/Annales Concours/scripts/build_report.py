import os, re, json, time

BASE = '/home/fygdev/Bureau/Annales Concours/sujets_concours'
PROJ = '/home/fygdev/Bureau/Annales Concours'

sources = {
    'ENS_Yaounde': 'edukamer.info (Google Drive) + promouvoircompetences.com',
    'ENAM': 'concourscameroon.com (Google Drive)',
    'ENIEG': 'edukamer.info (Google Drive)',
    'ENIET': 'promouvoircompetences.com',
    'FASA_Dschang': 'edukamer.info (Google Drive)',
}

def valid_pdf(path):
    try:
        with open(path, 'rb') as f:
            return f.read(5) == b'%PDF-'
    except Exception:
        return False

def build():
    report = {
        'generated_by': 'agent_automatisation_scraping',
        'date_generation': time.strftime('%Y-%m-%d %H:%M'),
        'plage_temporelle': '2012-present',
        'total_pdfs_valides': 0,
        'conventions_nommage': '[NomConcours]_[Filiere_ou_Categorie]_[NomEpreuve]_[Annee].pdf',
        'sources_utilisees': sources,
        'concours': {},
    }
    logs = []
    n = 0
    invalides = 0
    for root, dirs, files in os.walk(BASE):
        dirs.sort()
        for f in sorted(files):
            if not f.lower().endswith('.pdf'):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, BASE)
            parts = rel.split(os.sep)
            if len(parts) < 3:
                continue
            conc, filiere, session = parts[0], parts[1], parts[2]
            if not valid_pdf(path):
                invalides += 1
                logs.append('INVALIDE %s' % rel)
                continue
            size = os.path.getsize(path)
            node = report['concours'].setdefault(conc, {}).setdefault(filiere, {}).setdefault('sessions', {})
            node.setdefault(session, []).append({'fichier': f, 'taille_octets': size})
            n += 1
            logs.append('OK %s (%d o)' % (rel, size))
    report['total_pdfs_valides'] = n
    report['pdfs_invalides'] = invalides
    with open(os.path.join(PROJ, 'rapport_telechargement.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(os.path.join(PROJ, 'logs_telechargement.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(logs))
    # synthese lisible
    with open(os.path.join(PROJ, 'SYNTHESE_COLLECTE.md'), 'w', encoding='utf-8') as f:
        f.write('# Rapport de collecte — Sujets Concours Cameroun (2012 → aujourd\'hui)\n\n')
        f.write('## Récapitulatif\n\n')
        f.write('- **Total PDF téléchargés et valides :** %d\n' % n)
        f.write('- **PDF invalides :** %d\n' % invalides)
        f.write('- **Plage :** 2012 → %s\n\n' % time.strftime('%Y'))
        f.write('## Concours couverts\n\n')
        for c, fil in report['concours'].items():
            tot = sum(len(v.get('sessions', {}).get(s, [])) for f, v in fil.items() for s in v.get('sessions', {}))
            f.write('### %s — %d PDF\n' % (c, tot))
            for filiere, v in fil.items():
                for sess, items in v.get('sessions', {}).items():
                    for it in items:
                        f.write('- `%s` (session %s, filière %s, %d o)\n' % (it['fichier'], sess, filiere, it['taille_octets']))
            f.write('\n')
        f.write('## Sources exploitées\n\n')
        for k, v in sources.items():
            f.write('- **%s** : %s\n' % (k, v))
        f.write('\n## Épreuves manquées / non récupérables\n\n')
        f.write('- **Polytechnique ENSPY (sujets 2012→présent)** : paywalled (cameroondeskacademy 400–600 FCFA/épreuve, kamerpower via app payante). Liens Drive publics non trouvés pour les sessions récentes.\n')
        f.write('- **CUSS / IDE / MINSANTE (infirmiers)** : pas de dépôt public gratuit trouvé (seulement concourscameroon listant des pages qui n\'ont pas exposé de lien Drive pendant les fenêtres de collecte).\n')
        f.write('- **IRIC, Mines Maroua, ENAM sessions ≥2016** : contenus soit payants, soit pages non joignables (timeouts 000 / 406).\n')
        f.write('\n')
    print('total valide:', n, 'invalides:', invalides)

build()