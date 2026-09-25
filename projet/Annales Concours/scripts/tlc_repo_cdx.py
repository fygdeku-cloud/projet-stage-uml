import urllib.request, json, ssl, time, re, os

CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120'}

def cdx(p, limit=50000):
    q = ('https://web.archive.org/cdx/search/cdx?url=%s&output=json'
         '&fl=timestamp,original,statuscode,mimetype&limit=%d&filter=statuscode:200&collapse=urlkey' % (p, limit))
    try:
        d = urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=200, context=CTX).read().decode('utf-8','ignore')
        return json.loads(d)
    except Exception as e:
        return [['ERR', str(e)]]

outs = {'repository': open('scripts/tlc_repository.tsv','w'),
        'epreuves': open('scripts/tlc_epreuves_dir.tsv','w')}

# 1) /repository/ -> pages documents (liste)
rows = cdx('touslesconcours.info/repository/*')
n=0
for r in rows:
    if len(r)>=3 and r[0]!='ERR':
        outs['repository'].write('\t'.join(r)+'\n'); n+=1
print('repository rows:', n, flush=True)

# 2) /epreuves/ -> les PDF bruts
rows = cdx('touslesconcours.info/epreuves/*')
n=0
for r in rows:
    if len(r)>=3 and r[0]!='ERR':
        outs['epreuves'].write('\t'.join(r)+'\n'); n+=1
print('epreuves dir rows:', n, flush=True)

# 3) index global du site (pour mapper concours->id) : home + sitemap
for p in ['touslesconcours.info/', 'touslesconcours.info/sitemap.xml']:
    rows = cdx(p, 1000)
    for r in rows:
        if len(r)>=3 and r[0]!='ERR' and 'repository' not in r[1] and 'epreuves' not in r[1]:
            outs['repository'].write('\t'.join(r)+'\n')
    print('home/sitemap', p, 'rows', len(rows), flush=True)

for f in outs.values(): f.close()
print('DONE', flush=True)