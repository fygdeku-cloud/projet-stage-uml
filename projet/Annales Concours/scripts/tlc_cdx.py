import urllib.request, json, ssl, time, os, re

CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120'}

def cdx(path_pattern, limit=15000):
    q = ('https://web.archive.org/cdx/search/cdx?url=touslesconcours.info%s'
         '&output=json&fl=timestamp,original,statuscode,mimetype&limit=%d&filter=statuscode:200' % (path_pattern, limit))
    try:
        data = urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=150, context=CTX).read().decode('utf-8','ignore')
        return json.loads(data)
    except Exception as e:
        return [['ERR', str(e)]]

def grep_word(rows, word):
    hits=[]
    for r in rows:
        if len(r)>=3 and re.search(word, r[1], re.I):
            hits.append(r)
    return hits

out = open('scripts/tlc_epreuves_full.tsv','w')
for conc in ['IRIC','ENAM','ENSP','POLYTECHNIQUE','CUSS','IDE','ISSEA','IFORD','ENS','ENSET','FASA','MINES','ENSEPT','EPF']:
    rows = cdx('/epreuves/'+conc+'*')
    if rows and rows[0][0]=='ERR':
        print(conc, 'ERR', rows[0][1], flush=True); continue
    # keep pdf + pages
    kept=[]
    for r in rows:
        m=r[3].lower() if len(r)>3 else ''
        if m=='application/pdf' or m=='text/html':
            kept.append(r)
    for r in kept:
        out.write('\t'.join(r)+'\n')
    print(conc, 'total', len(rows), 'kept', len(kept), flush=True)
    time.sleep(1)
# Fallback: tout /epreuves/
rows = cdx('/epreuves/*')
for r in rows:
    if r[0]!='ERR' and (len(r)>3 and r[3].lower() in ('application/pdf','text/html')):
        out.write('\t'.join(r)+'\n')
print('fallback /epreuves/* total', len(rows), flush=True)
out.close()
print('DONE', flush=True)