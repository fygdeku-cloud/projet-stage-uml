import urllib.request, json, ssl, time, sys, os

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120'}

def cdx(url_pattern, filters=(), limit=1000, collapse='urlkey'):
    params = ['url=%s' % url_pattern, 'output=json', 'fl=timestamp,original,statuscode,mimetype',
              'limit=%d' % limit, 'collapse=%s' % collapse]
    for f in filters:
        params.append('filter=' + f)
    q = 'https://web.archive.org/cdx/search/cdx?' + '&'.join(params)
    try:
        data = urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=90, context=CTX).read().decode('utf-8', 'ignore')
        rows = json.loads(data)
        return rows
    except Exception as e:
        return [['ERR', str(e)]]

def norm(s):
    return s.strip().lower()

def main():
    targets = {
        'grandprof.net': [],
        'touslesconcours.info': [],
        'orniformation.com': [],
        'ornipreparation.com': [],
        'kamerpower.com': ['filter_epreuves'],
        'cameroondeskacademy.com': ['filter_epreuves'],
        'promouvoircompetences.com': ['filter_epreuves'],
        'edukamer.info': ['filter_epreuves'],
    }
    os.makedirs('scripts/', exist_ok=True)
    for site, kinds in targets.items():
        out_pdf = 'scripts/cdx_%s_pdf.tsv' % site.replace('.', '_')
        out_pg = 'scripts/cdx_%s_pages.tsv' % site.replace('.', '_')
        # 1) PDF files archived
        rows = cdx(site + '*', ['mimetype:application/pdf'], limit=2000)
        with open(out_pdf, 'w') as f:
            n = 0
            for r in rows:
                if len(r) >= 4 and r[0] != 'ERR' and norm(r[2]) == '200':
                    f.write('%s\t%s\t%s\n' % (r[0], r[1], r[3]))
                    n += 1
            print(site, 'PDF lignes:', n, flush=True)
        # 2) pages containing 'epreuve' or 'telecharg' or 'concours' in URL
        if kinds:
            rows = cdx(site + '*', ['urlkey:.*(epreuve|telecharg|concours|sujet).*'], limit=3000)
            with open(out_pg, 'w') as f:
                n = 0
                for r in rows:
                    if len(r) >= 4 and r[0] != 'ERR' and norm(r[2]) == '200':
                        f.write('%s\t%s\t%s\n' % (r[0], r[1], r[3]))
                        n += 1
                print(site, 'PAGES epreuve/concours:', n, flush=True)
        time.sleep(2)

main()