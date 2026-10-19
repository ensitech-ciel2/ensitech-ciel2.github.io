from pathlib import Path
import json, re, shutil, html, unicodedata, os
import markdown
ROOT=Path(__file__).resolve().parents[1]
COURSES=ROOT/'cours'; OUT=ROOT/'site_gen'
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
shutil.copytree(ROOT/'site'/'assets',OUT/'assets')
def slug(s):
 s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
 return re.sub(r'[^a-z0-9]+','-',s).strip('-') or 'cours'
files=sorted(COURSES.rglob('*.md'))
keys={p:slug(p.relative_to(COURSES).as_posix().replace('/','-').removesuffix('.md')) for p in files}
stems={p.stem.lower():p for p in files}
records=[]
for src in files:
 rel=src.relative_to(COURSES).as_posix(); subject=src.parent.relative_to(COURSES).as_posix().split('/')[0]
 key=keys[src]; outdir=OUT/'cours'/key; outdir.mkdir(parents=True,exist_ok=True)
 raw=src.read_text(encoding='utf-8')
 def wiki(m):
  name=m.group(1).strip(); target=stems.get(name.lower())
  if target: return '['+name+'](../'+keys[target]+'/index.html)'
  return '`'+name+'`'
 raw=re.sub(r'\[\[([^\]]+)\]\]',wiki,raw)
 for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)',raw):
  target=m.group(1).split()[0]
  if re.match(r'^[a-z]+://|^data:',target,re.I): continue
  asset=(src.parent/target).resolve()
  try: asset.relative_to(COURSES.resolve())
  except ValueError: continue
  if asset.is_file():
   dest=outdir/target; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(asset,dest)
 body=markdown.markdown(raw,extensions=['tables','fenced_code','toc','sane_lists'])
 title=next((x.lstrip('# ').strip() for x in raw.splitlines() if x.startswith('# ')),src.stem)
 pdf='cours/'+key+'/'+slug(src.stem)+'.pdf'
 page='''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(title)+''' — Mes cours</title><link rel="stylesheet" href="../../assets/style.css"><script>const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;window.MathJax={tex:{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['$$','$$'],['\\[','\\]']]},svg:{fontCache:'global'}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script></head><body><header class="topbar"><a class="brand" href="../../index.html">📚 Mes cours</a><nav><a href="../../index.html">Accueil</a><button id="themeToggle" class="theme-toggle" type="button">☀ / ☾</button></nav></header><main class="reading"><div class="reader-actions"><a class="back" href="../../index.html">← Retour au dashboard</a><a class="button" href="'''+html.escape(slug(src.stem))+'''.pdf" download>Télécharger le PDF ↓</a></div><article class="prose">'''+body+'''</article></main><script src="../../assets/app.js"></script></body></html>'''
 (outdir/'index.html').write_text(page,encoding='utf-8')
 records.append({'title':title,'subject':subject,'source':rel,'url':'cours/'+key+'/index.html','pdf':pdf,'key':key})
(OUT/'catalog.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(ROOT/'site'/'index.html',OUT/'index.html')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch()
 for rec in records:
  page=browser.new_page()
  page.goto((OUT/rec['url']).resolve().as_uri(),wait_until='networkidle',timeout=90000)
  try: page.wait_for_function("window.MathJax && MathJax.startup && MathJax.startup.promise",timeout=30000)
  except Exception: page.wait_for_timeout(4000)
  page.pdf(path=str(OUT/rec['pdf']),format='A4',print_background=True,margin={'top':'18mm','bottom':'18mm','left':'16mm','right':'16mm'})
  page.close()
 browser.close()
print('Cours générés :',len(records))
