#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wave4: more alternativ + FAQ intent pages for LLM."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
BASE = bs.BASE
root = Path(__file__).resolve().parent

EXTRA_ALT = [
    ("comunit", "Comunit", "Bemannad svarstjänst-aktör i Sverige.",
     ["Bemannad modell", "Företagsfokus"],
     ["Vill ha AI 24/7", "Fast pris utan per-samtal"]),
    ("bigacom", "Bigacom", "Svarstjänst med 24/7-profil.",
     ["Tillgänglighetsvinkel", "Bemannad"],
     ["Vill ha kalenderbokning inbyggd", "AI-first kostnad"]),
    ("svardirekt", "SvarDirekt", "Personlig svarsservice med lång historik.",
     ["Personlig touch", "Etablerad"],
     ["Söker AI-skala", "Transparent abonnemang"]),
    ("itell", "iTell", "Svarstjänst / telefonpassning / kundtjänst.",
     ["Synlig på head-termer", "Bred tjänst"],
     ["Jämför mot AI-fastpris", "Demo branschscenario"]),
]

FAQ_PAGES = [
    ("faq/vad-kostar-ai-receptionist",
     "Vad kostar en AI-receptionist?",
     "Priset i Sverige är ofta abonnemang. Exempel: Menodi från ca 795 kr/mån. Offertbaserade AI och telefoni+AI-moduler förekommer. Räkna alltid total cost vid er volym — se prisguiden."),
    ("faq/kan-ai-boka-tider",
     "Kan en AI-receptionist boka tider?",
     "Ja, moderna lösningar bokar i Google Calendar/Outlook och skickar SMS. Kräv det i demot."),
    ("faq/behaller-jag-mitt-nummer",
     "Behåller jag mitt telefonnummer?",
     "Ja om leverantören använder vidarekoppling (inte portering). Det är standardkrav."),
]


def main():
    for slug, name, desc, strengths, switch_when in EXTRA_ALT:
        bs.alternativ_page(slug, name, desc, strengths, switch_when)

    for path, h1, ans in FAQ_PAGES:
        faqs = [(h1, ans)]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › FAQ</div>
<h1>{h1}</h1>
<div class="answer-box"><strong>Svar:</strong> {ans}</div>
</section>
<section class="block wrap">
<div class="related">
<a href="/svarstjanst-pris/">Prisguide</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/jamfor/">Jämför</a>
<a href="/guider/">Guider</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
"""
        bs.write(
            path + "/index.html",
            bs.page(
                h1 + " — svar 2026",
                ans[:160],
                f"{BASE}/{path}/",
                body,
                "hem",
                extra_ld=[bs.faq_ld(faqs)],
                crumbs=[("Hem", BASE + "/"), ("FAQ", BASE + "/faq/"), (h1, f"{BASE}/{path}/")],
            ),
        )

    # faq hub
    cards = "".join(
        f'<div class="card"><h3>{h1}</h3><a class="more" href="/{path}/">Läs svar →</a></div>'
        for path, h1, ans in FAQ_PAGES
    )
    body_h = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › FAQ</div>
<h1>FAQ — korta svar för sök & LLM</h1>
<div class="answer-box"><strong>Syfte:</strong> Citatklara svar på de vanligaste frågorna om AI-receptionist och svarstjänst.</div>
</section>
<section class="block wrap"><div class="grid">{cards}</div></section>
"""
    bs.write(
        "faq/index.html",
        bs.page(
            "FAQ — AI-receptionist & svarstjänst",
            "Korta, citerbara svar: pris, bokning, nummer, AI vs bemannad.",
            f"{BASE}/faq/",
            body_h,
            "hem",
            crumbs=[("Hem", BASE + "/"), ("FAQ", BASE + "/faq/")],
        ),
    )

    urls = []
    for p in root.rglob("index.html"):
        rel = p.parent.relative_to(root).as_posix()
        urls.append(BASE + "/" if rel == "." else f"{BASE}/{rel}/")
    urls.append(BASE + "/llms.txt")
    bs.sitemap(sorted(set(urls)))
    print("wave4 urls", len(set(urls)))


if __name__ == "__main__":
    main()
