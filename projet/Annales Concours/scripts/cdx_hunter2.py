import urllib.request, json, ssl, time, os, re

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120'}

def cdx(url_pattern, limit=8000):
    q = ('https://web.archive.org/cdx/search/cdx?url=%s&output=json'
         '&fl=timestamp,original,statuscode,mimetype&limit=%d&collapse=urlkey&filter=statuscode:200' % (url_pattern, limit))
    try:
        data = urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=120, context=CTX).read().decode('utf-8', 'ignore')
        return json.loads(data)
    except Exception as e:
        return [['ERR', str(e)]]

def analyse(site):
    rows = cdx(site + '*')
    if rows and rows[0][0] == 'ERR':
        print(site, 'ERR', rows[0][1], flush=True)
        return
    total = len([r for r in rows if len(r) >= 2 and r[0] != 'ERR'])
    pdfs = [r for r in rows if len(r) >= 3 and r[0] != 'ERR' and r[2].lower().endswith('.pdf')]
    eprev = [r for r in rows if len(r) >= 3 and r[0] != 'ERR' and re.search(r'(epreuve|concours|sujet|telecharg)', r[2], re.I)]
    with open('scripts/cdx_%s_all.tsv' % site.replace('.', '_'), 'w') as f:
        for r in rows:
            if len(r) >= 2 and r[0] != 'ERR':
                f.write('\t'.join(r) + '\n')
    with open('scripts/cdx_%s_pdf.tsv' % site.replace('.', '_'), 'w') as f:
        for r in pdfs:
            f.write('\t'.join(r) + '\n')
    print('%s: total=%d pdf=%d epreuve_pages=%d' % (site, total, len(pdfs), len(eprev)), flush=True)

for s in ['grandprof.net', 'touslesconcours.info', 'orniformation.com', 'ornipreparation.com',
          'kamerpower.com', 'cameroondeskacademy.com', 'promouvoircompetences.com',
          'edukamer.info', 'concourscameroon.com']:
    analyse(s)
    time.sleep(1)
print('DONE', flush=True)