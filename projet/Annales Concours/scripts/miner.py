import urllib.request, re, html, ssl, time, sys, traceback

UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120'}
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def get(u, tries=2, timeout=40):
    for i in range(tries):
        try:
            req = urllib.request.Request(u, headers=UA)
            r = urllib.request.urlopen(req, timeout=timeout, context=CTX)
            return r.read().decode('utf-8', 'ignore')
        except Exception as e:
            if i == tries-1:
                return 'ERROR:'+str(e)
            time.sleep(2)

def main():
    kind = sys.argv[1]
    url = sys.argv[2]
    out = sys.argv[3]
    debug = '/home/fygdev/Bureau/Annales Concours/scripts/miner_debug.txt'
    with open(debug, 'w') as d:
        d.write('fetch %s\n' % url)
        data = get(url)
        d.write('data len %s\n' % (len(data) if data else 0))
        results = []
        if data and not data.startswith('ERROR:'):
            for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', data, re.S):
                href = html.unescape(m.group(1)).strip()
                txt = re.sub('<[^>]+>', '', m.group(2)).strip()
                low = href.lower()
                if kind == 'drive' and ('drive.google' in low or 'drive.usercontent' in low):
                    fm = re.search(r'/file/d/([^/]+)/', href)
                    if fm:
                        href = 'https://drive.google.com/uc?export=download&id=' + fm.group(1)
                    if 'uc?export' in href:
                        results.append((txt, href))
                if kind == 'pdf' and (low.endswith('.pdf') or 'images/epreuves' in low):
                    results.append((txt, href))
                if kind == 'link' and 'epreuve' in low:
                    results.append((txt, href))
        with open(out, 'w', encoding='utf-8') as f:
            for txt, href in results:
                f.write('%s\t%s\n' % (txt, href))
        d.write('found %d\n' % len(results))

try:
    main()
except Exception:
    with open('/home/fygdev/Bureau/Annales Concours/scripts/miner_debug.txt', 'a') as d:
        d.write(traceback.format_exc())