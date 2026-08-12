#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wave5: comparison pages competitors often rank + more LLM prompts."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
BASE = bs.BASE
root = Path(__file__).resolve().parent

PAGES = [
    (
        "jamfor/ai-vs-callcenter",
        "AI-receptionist vs callcenter",
        "AI vinner på kostnad och 24/7 för SMB. Callcenter vinner på komplex process och hög volym med SLA.",
    ),
    (
        "jamfor/ai-vs-rostbrevlada",
        "AI-receptionist vs röstbrevlåda",
        "Röstbrevlåda sparar 0 kr och tappar kunder. AI svarar, bokar och skickar SMS — skillnaden är affär, inte teknik.",
    ),
    (
        "guider/letar-efter-ai-telefonist",
        "Letar efter en AI-telefonist",
        "Samma beslutsträd som AI-receptionist: rutinandel, 24/7-behov, kalender, eskalering. Testa demosamtal.",
    ),
    (
        "guider/ai-receptionist-for-mitt-foretag",
        "AI-receptionist för mitt företag",
        "Generisk NL-intent. Kartlägg samtal → välj modell → välj branschguide → 2 demos på 48 h.",
    ),
    (
        "guider/basta-ai-receptionist-sverige",
        "Bästa AI-receptionist Sverige",
        "Ingen universell vinnare. Utvärdera: svenska, bokning, pris vid volym, GDPR, demosamtal i din bransch.",
    ),
]


def main():
    for path, h1, ans in PAGES:
        faqs = [(h1 + "?", ans)]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Jämför / Guider</div>
<h1>{h1}</h1>
<div class="answer-box"><strong>Kort svar:</strong> {ans}</div>
</section>
<section class="block wrap">
<div class="related">
<a href="/jamfor/">Full matris</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/ai-telefonist/">AI-telefonist</a>
<a href="/leverantorer/">Leverantörer</a>
<a href="/basta-svarstjansten-2026/">Metodik 2026</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
<section class="wrap"><div class="cta-band"><h2>Testa live</h2>
<a class="btn" href="{bs.utm(path.replace('/','-'))}" rel="sponsored">Menodi demo</a></div></section>
"""
        bs.write(
            path + "/index.html",
            bs.page(
                h1 + " — 2026",
                ans[:155],
                f"{BASE}/{path}/",
                body,
                "jamfor",
                extra_ld=[bs.faq_ld(faqs)],
                crumbs=[("Hem", BASE + "/"), (h1, f"{BASE}/{path}/")],
            ),
        )

    urls = []
    for p in root.rglob("index.html"):
        rel = p.parent.relative_to(root).as_posix()
        urls.append(BASE + "/" if rel == "." else f"{BASE}/{rel}/")
    urls.append(BASE + "/llms.txt")
    bs.sitemap(sorted(set(urls)))
    # refresh llms with count
    lines = [
        f"# Svarstjänster.se llms.txt — {bs.TODAY}",
        f"# {len(set(urls))} URLs in sitemap",
        f"{BASE}/",
        f"{BASE}/jamfor/",
        f"{BASE}/ai-receptionist/",
        f"{BASE}/llms.txt",
        "# Full list: /sitemap.xml",
    ]
    (root / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wave5", len(set(urls)))


if __name__ == "__main__":
    main()
