import urllib.request, re, html, ssl, time

UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120'}
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def get(u, tries=3, timeout=50):
    for i in range(tries):
        try:
            req = urllib.request.Request(u, headers=UA)
            r = urllib.request.urlopen(req, timeout=timeout, context=CTX)
            return r.read().decode('utf-8', 'ignore')
        except Exception as e:
            if i == tries-1:
                return 'ERR'
            time.sleep(4)

def extract_drives(url):
    data = get(url)
    if data == 'ERR':
        return []
    res = []
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']*drive\.google\.com[^"\']*)["\'][^>]*>(.*?)</a>', data, re.S):
        href = html.unescape(m.group(1)).replace('&amp;', '&')
        txt = re.sub('<[^>]+>', '', m.group(2)).strip()
        fm = re.search(r'/file/d/([^/]+)/', href)
        if fm:
            href = 'https://drive.google.com/uc?export=download&id=' + fm.group(1)
        if 'uc?export' in href and href not in [x[1] for x in res]:
            res.append((txt, href))
    return res

# ENSP / Polytechnique + IDE pages (concourscameroon)
urls = [
    'https://concourscameroon.com/anciennes-epreuves-de-mathematique-du_13.html',
    'https://concourscameroon.com/anciennes-epreuves-de-physique-du-2.html',
    'https://concourscameroon.com/anciennes-epreuves-de-mathematique-du-2.html',
    'https://concourscameroon.com/anciennes-epreuves-de-informatique-du.html',
    'https://concourscameroon.com/anciennes-epreuves-de-physique-du_13.html',
    'https://concourscameroon.com/anciennes-epreuves-mathematique-du_28.html',
    'https://concourscameroon.com/anciennes-epreuves-physique-du-concours-2.html',
    'https://concourscameroon.com/anciennes-epreuves-chimie-du-concours-2.html',
    'https://concourscameroon.com/anciennes-epreuves-culture-generale-du_28.html',
    'https://concourscameroon.com/anciennes-epreuves-langue-du-concours.html',
]
out = '/home/fygdev/Bureau/Annales Concours/scripts/ensp_ide_manifest.tsv'
with open(out, 'w', encoding='utf-8') as f:
    for u in urls:
        for txt, href in extract_drives(u):
            f.write('%s\t%s\t%s\n' % (txt, href, u))
        time.sleep(3)
print('done')