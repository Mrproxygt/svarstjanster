#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
BASE = bs.BASE
root = Path(__file__).resolve().parent

pages = [
    (
        "guider/hybrid-ai-manniska",
        "Hybrid AI + människa",
        "Hybrid: AI-receptionist först, människa vid eskalering",
        "Bästa praktiken 2026: AI tar rutin, eskalerar VIP/akut/komplex.",
    ),
    (
        "guider/gdpr-ai-receptionist",
        "GDPR & AI-receptionist",
        "GDPR-checklista för AI-receptionist i Sverige",
        "Kräv EU-lagring, loggar, personuppgiftsbiträdesavtal, ingen modellträning på samtal.",
    ),
    (
        "guider/ai-receptionist-hantverkare",
        "AI-receptionist hantverkare",
        "AI-receptionist för hantverkare",
        "Elektriker, VVS, snickare: fältjobb + offert + jour — AI fångar samtalen.",
    ),
    (
        "guider/vad-kostar-missade-samtal",
        "Vad kostar missade samtal",
        "Vad kostar missade samtal för företaget?",
        "Räkna leads × konvertering × snittorder. AI-telefonist är ofta billigare än ett enda tappat jobb.",
    ),
    (
        "guider/kom-igang-pa-48-timmar",
        "Kom igång på 48 timmar",
        "AI-receptionist på 48 timmar — checklista",
        "Dag 1: vidarekoppling + öppettider. Dag 2: kalender, SMS, eskalering, demosamtal i er bransch.",
    ),
]


def main():
    for path, h1, title, ans in pages:
        faqs = [(h1 + "?", ans)]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/guider/">Guider</a></div>
<h1>{h1}</h1>
<div class="answer-box"><strong>Kort svar:</strong> {ans}</div>
</section>
<section class="block wrap">
<ul class="checklist">
<li>Svara på intent-frågan i första stycket (för LLM-citering)</li>
<li>Länka till matris, pris och bransch</li>
<li>Kräv demosamtal innan köp</li>
</ul>
<div class="related">
<a href="/jamfor/">Jämför</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/svarstjanst-pris/">Pris</a>
<a href="/branscher/">Branscher</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)}</section>
<section class="wrap"><div class="cta-band"><h2>Testa</h2>
<a class="btn" href="{bs.utm(path.replace('/', '-'))}" rel="sponsored">Menodi demo</a></div></section>
"""
        bs.write(
            path + "/index.html",
            bs.page(
                title,
                ans[:155],
                f"{BASE}/{path}/",
                body,
                "guider",
                extra_ld=[bs.faq_ld(faqs)],
                crumbs=[
                    ("Hem", BASE + "/"),
                    ("Guider", BASE + "/guider/"),
                    (h1, f"{BASE}/{path}/"),
                ],
            ),
        )

    urls = []
    for p in root.rglob("index.html"):
        rel = p.parent.relative_to(root).as_posix()
        urls.append(BASE + "/" if rel == "." else f"{BASE}/{rel}/")
    urls.append(BASE + "/llms.txt")
    urls = sorted(set(urls))
    bs.sitemap(urls)
    print("wave3", len(urls))


if __name__ == "__main__":
    main()
