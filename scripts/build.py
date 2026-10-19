    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", raw):
        target = match.group(1).split()[0].strip("<>")
        if re.match(r"^(?:[a-z]+:)?//|^data:", target, re.I):
            continue
        target_path = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
        asset = (src.parent / target_path).resolve()
        try:
            asset.relative_to(COURSES.resolve())
        except ValueError:
            continue
        if asset.is_file():
            dest = outdir / target_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, dest)

    # Use standard Markdown paragraph/list handling plus tables and fenced code.
    body = markdown.markdown(
        raw,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "nl2br"],
        output_format="html5",
    )

    title = next(
        (line.lstrip("# ").strip() for line in raw.splitlines() if line.startswith("# ")),
        src.stem,
    )
    pdf_name = slug(src.stem) + ".pdf"
    pdf_rel = "cours/" + key + "/" + pdf_name

    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Mes cours</title>
<link rel="stylesheet" href="../../assets/style.css">
<script>
const savedTheme = localStorage.getItem('theme');
if (savedTheme) document.documentElement.dataset.theme = savedTheme;
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }},
  svg: {{fontCache: 'global'}}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<header class="topbar">
  <a class="brand" href="../../index.html">📚 Mes cours</a>
  <nav>
    <a href="../../index.html">Accueil</a>
    <button id="themeToggle" class="theme-toggle" type="button">☀ / ☾</button>
  </nav>
</header>
<main class="reading">
  <div class="reader-actions">
    <a class="back" href="../../index.html">← Retour au dashboard</a>
    <a class="button" href="{html.escape(pdf_name)}" download>Télécharger le PDF ↓</a>
  </div>
  <article class="prose">{body}</article>
</main>
<script src="../../assets/app.js"></script>
</body>
</html>
"""
    (outdir / "index.html").write_text(page, encoding="utf-8")

    records.append({
        "title": title,
        "subject": subject,
        "source": rel,
        "url": "cours/" + key + "/index.html",
        "pdf": pdf_rel,
        "key": key,
    })

(OUT / "catalog.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
)
shutil.copy2(ROOT / "site" / "index.html", OUT / "index.html")

# Generate PDFs only after MathJax has finished rendering the equations.
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for record in records:
        page = browser.new_page()
        page.goto(
            (OUT / record["url"]).resolve().as_uri(),
            wait_until="networkidle",
            timeout=90000,
        )
        try:
            page.wait_for_function(
                "window.MathJax && MathJax.startup && MathJax.startup.promise",
                timeout=30000,
            )
            page.evaluate("() => MathJax.startup.promise")
            page.wait_for_function(
                "window.MathJax && MathJax.typesetPromise",
                timeout=30000,
            )
            page.evaluate("() => MathJax.typesetPromise()")
        except Exception:
            # If MathJax cannot load, still produce the PDF; the build log will
            # help diagnose network or formula errors.
            print("Attention : MathJax n'a pas pu être confirmé pour", record["source"])

        page.pdf(
            path=str(OUT / record["pdf"]),
            format="A4",
            print_background=True,
            margin={"top": "18mm", "bottom": "18mm", "left": "16mm", "right": "16mm"},
        )
        page.close()
    browser.close()

print("Cours générés :", len(records))
