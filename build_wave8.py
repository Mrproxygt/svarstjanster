#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wave8: more FAQ intents that trigger AI Overviews + city × bransch samples."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
BASE = bs.BASE
root = Path(__file__).resolve().parent

FAQS = [
    ("faq/vad-ar-skillnaden-svarsservice-telefonpassning",
     "Vad är skillnaden mellan svarsservice och telefonpassning?",
     "I praktiken samma sak: någon svarar i telefon åt företaget. Orden används omväxlande i Sverige. AI-receptionist är den moderna varianten med bokning och 24/7."),
    ("faq/hur-fungerar-vidarekoppling-ai",
     "Hur fungerar vidarekoppling till AI-receptionist?",
     "Du behåller numret. Samtal som inte besvaras (eller alla samtal) vidarekopplas till AI:n. Ingen portering krävs hos moderna leverantörer."),
    ("faq/ar-ai-receptionist-lagligt",
     "Är AI-receptionist lagligt i Sverige?",
     "Ja. Ni ansvarar för korrekt info, GDPR och hur ni informerar om automatisering i er policy. Kräv EU-data och personuppgiftsbiträdesavtal."),
    ("faq/kan-ai-prata-svenska",
     "Kan AI-receptionist prata svenska?",
     "Ja — det är ett baskrav. Testa demosamtal med dialekt, brus och avbrott innan köp."),
]

COMBOS = [
    ("branscher/tandlakare-stockholm", "AI-receptionist tandläkare Stockholm",
     "För kliniker i Stockholm: boka/omboka, efter stängning, SMS mot no-show. Jämför dentala specialister och generella AI-receptionister."),
    ("branscher/frisor-goteborg", "AI-receptionist frisör Göteborg",
     "Salonger i Göteborg: boka medan du klipper, kvällsförfrågningar, ombokning via SMS."),
    ("branscher/maklare-stockholm", "AI-receptionist mäklare Stockholm",
     "Spekulant-samtal kväll/helg i Stockholm — AI kvalificerar och bokar visning."),
]


def main():
    for path, h1, ans in FAQS:
        faqs = [(h1, ans)]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/faq/">FAQ</a></div>
<h1>{h1}</h1>
<div class="answer-box"><strong>Svar:</strong> {ans}</div>
</section>
<section class="block wrap">
<div class="related">
<a href="/faq/">Alla FAQ</a>
<a href="/jamfor/">Jämför</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/guider/">Guider</a>
</div>
</section>
"""
        bs.write(path + "/index.html", bs.page(
            h1, ans[:155], f"{BASE}/{path}/", body, "hem",
            extra_ld=[bs.faq_ld(faqs)],
            crumbs=[("Hem", BASE+"/"), ("FAQ", BASE+"/faq/"), (h1, f"{BASE}/{path}/")],
        ))

    for path, h1, ans in COMBOS:
        faqs = [(h1 + "?", ans)]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/branscher/">Branscher</a></div>
<h1>{h1}</h1>
<div class="answer-box"><strong>Kort svar:</strong> {ans}</div>
</section>
<section class="block wrap">
<div class="related">
<a href="/branscher/">Alla branscher</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/ai-receptionist/stockholm/">Stockholm</a>
<a href="/ai-receptionist/goteborg/">Göteborg</a>
<a href="/jamfor/">Jämför</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
<section class="wrap"><div class="cta-band"><h2>Demo</h2>
<a class="btn" href="{bs.utm('w8')}" rel="sponsored">Prova Menodi</a></div></section>
"""
        bs.write(path + "/index.html", bs.page(
            h1 + " — 2026", ans[:155], f"{BASE}/{path}/", body, "bran",
            extra_ld=[bs.faq_ld(faqs)],
            crumbs=[("Hem", BASE+"/"), ("Branscher", BASE+"/branscher/"), (h1, f"{BASE}/{path}/")],
        ))

    # refresh faq hub
    all_faq = sorted((root / "faq").glob("*/index.html"))
    cards = []
    import re
    for p in all_faq:
        t = p.read_text(encoding="utf-8")
        m = re.search(r"<h1>([^<]+)</h1>", t)
        h1 = m.group(1) if m else p.parent.name
        cards.append(f'<div class="card"><h3>{h1}</h3><a class="more" href="/faq/{p.parent.name}/">Läs →</a></div>')
    body_h = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › FAQ</div>
<h1>FAQ — korta svar för sök & LLM</h1>
<div class="answer-box"><strong>Syfte:</strong> Citatklara svar på vanliga frågor om AI-receptionist och svarstjänst i Sverige.</div>
</section>
<section class="block wrap"><div class="grid">{''.join(cards)}</div></section>
"""
    bs.write("faq/index.html", bs.page(
        "FAQ — AI-receptionist & svarstjänst",
        "Korta citerbara svar om pris, bokning, nummer, skillnader och laglighet.",
        f"{BASE}/faq/", body_h, "hem",
        crumbs=[("Hem", BASE+"/"), ("FAQ", BASE+"/faq/")],
    ))

    urls = []
    for p in root.rglob("index.html"):
        rel = p.parent.relative_to(root).as_posix()
        urls.append(BASE + "/" if rel == "." else f"{BASE}/{rel}/")
    urls.append(BASE + "/llms.txt")
    bs.sitemap(sorted(set(urls)))
    print("wave8", len(set(urls)))


if __name__ == "__main__":
    main()
