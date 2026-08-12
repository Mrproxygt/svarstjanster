#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""More longtail pages for LLM natural-language queries."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
BASE = bs.BASE

QUERIES = [
    ("letar-efter-ai-receptionist",
     "Letar efter en AI-receptionist för mitt företag",
     "Letar efter en AI-receptionist för mitt företag? Startguide",
     "Du har redan formulerat behovet. Här är beslutsträdet: rutin vs komplext, pris, och hur du testar leverantörer på 48 timmar."),
    ("ai-receptionist-smaforetag",
     "AI-receptionist för småföretag",
     "AI-receptionist för småföretag — lönsamhet & setup",
     "För enmansbolag och små team är missade samtal dyrare än abonnemanget. Fokus: vidarekoppling, bokning, kvällstäckning."),
    ("ai-svarstjanst",
     "AI-svarstjänst",
     "AI-svarstjänst i Sverige 2026 — guide",
     "AI-svarstjänst = AI som tar inkommande samtal. Synonymt med AI-receptionist/AI-telefonist i många sökningar."),
    ("missade-samtal-foretag",
     "Missade samtal företag",
     "Missade samtal i företaget — kostnad & lösning",
     "62 % av samtal till småföretag besvaras aldrig av en människa (411 Locals). AI-telefonist är den billigaste 24/7-motåtgärden."),
    ("boka-tid-via-telefon-ai",
     "Boka tid via telefon med AI",
     "Boka tid via telefon med AI — så funkar det",
     "AI tar samtalet, kollar kalender, bokar slot, skickar SMS. Kräv integration med Google/Outlook."),
]


def main():
    for slug, intent, title, lede in QUERIES:
        faqs = [
            (f"Vad ska jag göra om jag {intent.lower()}?",
             "Kartlägg topp-5 samtalstyper, välj AI vs bemannad via matrisen, boka 2 demos, ring in samma scenario till båda."),
            ("Hur snabbt kan jag vara live?",
             "Med vidarekoppling ofta samma dag. Full branschanpassning tar längre."),
        ]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Guider</div>
<h1>{title}</h1>
<p class="lede">Intent: “{intent}”.</p>
<div class="answer-box"><strong>Kort svar:</strong> {lede}</div>
</section>
<section class="block wrap">
<div class="steps">
<div class="step"><h3>Räkna missade samtal</h3><p>Hur många/vecka? × snittvärde per lead.</p></div>
<div class="step"><h3>Välj modell</h3><p><a href="/jamfor/">Jämför AI vs bemannad vs callcenter</a>.</p></div>
<div class="step"><h3>Testa 2 leverantörer</h3><p>Samma tre samtalsscript. Se <a href="/leverantorer/">katalogen</a>.</p></div>
</div>
<div class="related">
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/branscher/">Bransch</a>
<a href="/svarstjanst-pris/">Pris</a>
<a href="/vad-ar-ai-receptionist/">Definition</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
<section class="wrap"><div class="cta-band"><h2>Testa live</h2>
<a class="btn" href="{bs.utm('lt-'+slug)}" rel="sponsored">Menodi demo</a></div></section>
"""
        bs.write(f"guider/{slug}/index.html", bs.page(
            f"{title}",
            f"{lede} Jämförelse, pris och nästa steg för svenska företag.",
            f"{BASE}/guider/{slug}/", body, "hem",
            extra_ld=[bs.faq_ld(faqs)],
            crumbs=[("Hem", f"{BASE}/"), ("Guider", f"{BASE}/guider/"), (intent, f"{BASE}/guider/{slug}/")],
        ))

    # guider hub
    cards = "".join(
        f'<div class="card"><h3>{intent}</h3><a class="more" href="/guider/{slug}/">Öppna guide →</a></div>'
        for slug, intent, title, lede in QUERIES
    )
    body_h = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Guider</div>
<h1>Guider — natural language & beslut</h1>
<p class="lede">Sidor byggda för hur människor och LLM:er faktiskt frågar.</p>
</section>
<section class="block wrap"><div class="grid">{cards}</div></section>
"""
    bs.write("guider/index.html", bs.page(
        "Guider — AI-receptionist, missade samtal, beslut",
        "Praktiska guider: letar efter AI-receptionist, småföretag, AI-svarstjänst, missade samtal, boka tid via telefon.",
        f"{BASE}/guider/", body_h, "hem",
        crumbs=[("Hem", f"{BASE}/"), ("Guider", f"{BASE}/guider/")],
    ))

    # more cities
    for slug, name in [("orebro", "Örebro"), ("vasteras", "Västerås"), ("helsingborg", "Helsingborg"), ("jonkoping", "Jönköping"), ("norrkoping", "Norrköping")]:
        faqs = [(f"AI-receptionist i {name}?", f"Ja — molnbaserat via vidarekoppling för bolag i {name}.")]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/ai-receptionist/">AI-receptionist</a> › {name}</div>
<h1>AI-receptionist i {name}</h1>
<div class="answer-box"><strong>Kort svar:</strong> Fungerar för företag i {name} utan lokal server. Behåll numret, svara 24/7, boka i kalender.</div>
</section>
<section class="block wrap">
<div class="related">
<a href="/ai-receptionist/">Guide</a>
<a href="/branscher/">Bransch</a>
<a href="/jamfor/">Jämför</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
"""
        bs.write(f"ai-receptionist/{slug}/index.html", bs.page(
            f"AI-receptionist {name}",
            f"AI-receptionist för företag i {name}: 24/7, bokning, vidarekoppling.",
            f"{BASE}/ai-receptionist/{slug}/", body, "ai-rec",
            extra_ld=[bs.faq_ld(faqs)],
            crumbs=[("Hem", f"{BASE}/"), ("AI-receptionist", f"{BASE}/ai-receptionist/"), (name, f"{BASE}/ai-receptionist/{slug}/")],
        ))

    # update sitemap by re-reading known set + new
    urls = []
    root = Path(__file__).resolve().parent
    for p in root.rglob("index.html"):
        rel = p.parent.relative_to(root).as_posix()
        if rel == ".":
            urls.append(f"{BASE}/")
        else:
            urls.append(f"{BASE}/{rel}/")
    urls.append(f"{BASE}/llms.txt")
    urls = sorted(set(urls))
    bs.sitemap(urls)
    # extend llms
    extra = "\n".join(f"{BASE}/guider/{s}/" for s, *_ in QUERIES)
    llms = (root / "llms.txt").read_text(encoding="utf-8")
    if "guider/" not in llms:
        (root / "llms.txt").write_text(llms.rstrip() + "\n\n# Guider\n" + extra + "\n", encoding="utf-8")
    print("longtail done", len(urls))


if __name__ == "__main__":
    main()
