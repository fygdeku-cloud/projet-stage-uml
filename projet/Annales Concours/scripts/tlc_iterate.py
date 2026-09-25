import urllib.request, json, ssl, time, re

CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120'}

def cdx(p, limit=20000):
    q = ('https://web.archive.org/cdx/search/cdx?url=%s&output=json'
         '&fl=timestamp,original,statuscode,mimetype&limit=%d&filter=statuscode:200' % (p, limit))
    try:
        d = urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=180, context=CTX).read().decode('utf-8','ignore')
        return json.loads(d)
    except Exception as e:
        return [['ERR', str(e)]]

def show(rows, label, limit=100):
    print('====', label, '====')
    if rows and rows[0][0]=='ERR':
        print('ERR', rows[0][1]); return
    uniq={}
    for r in rows:
        if len(r)>=3:
            uniq[r[1]]=(r[0], r[3] if len(r)>3 else '')
    print('uniq urls:', len(uniq))
    for u,(t,m) in list(sorted(uniq.items()))[:limit]:
        print('%s | %s | %s' % (t, m, u[:190]))
    return uniq

# Toutes URLs du domaine contenant 'epreuve' OU 'concours' dans le chemin
show(cdx('touslesconcours.info', 50000), 'TOUS touslesconcours (bulk)', 0)

# Récupération via boucle pour un motif élargi : requête CDX par sous-chaîne via l'API (limite pratique)