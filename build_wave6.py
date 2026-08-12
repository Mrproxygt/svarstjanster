#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
BASE = bs.BASE
root = Path(__file__).resolve().parent

# more cities for AI receptionist
CITIES = [
    ("umea", "Umeå"),
    ("lulea", "Luleå"),
    ("karlstad", "Karlstad"),
    ("vaxjo", "Växjö"),
    ("sundsvall", "Sundsvall"),
    ("gavle", "Gävle"),
    ("boras", "Borås"),
    ("halmstad", "Halmstad"),
]

# more guider NL
GUIDES = [
    ("guider/ai-reception-for-klinik", "AI-reception för klinik",
     "Klinik (tand, vård, terapi): boka/omboka, akut-policy, SMS, ingen diagnos i telefon."),
    ("guider/svarstjanst-eller-ai", "Svarstjänst eller AI?",
     "Samma behov. Välj AI vid rutin+24/7. Välj bemannad vid komplexa samtal. Hybrid annars."),
    ("guider/hur-valjer-jag-svarstjanst", "Hur väljer jag svarstjänst?",
     "1) Kartlägg intents 2) Pris vid volym 3) Bokning 4) Eskalering 5) Demosamtal ×2."),
]


def main():
    for slug, name in CITIES:
        faqs = [(f"AI-receptionist i {name}?", f"Ja — molnbaserat via vidarekoppling för företag i {name}.")]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/ai-receptionist/">AI-receptionist</a> › {name}</div>
<h1>AI-receptionist i {name}</h1>
<div class="answer-box"><strong>Kort svar:</strong> Fungerar för bolag i {name} utan lokal server. Behåll numret, svara 24/7, boka i kalender.</div>
</section>
<section class="block wrap">
<div class="related">
<a href="/ai-receptionist/">Guide</a>
<a href="/branscher/">Bransch</a>
<a href="/jamfor/">Jämför</a>
<a href="/svarstjanst-pris/">Pris</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
"""
        bs.write(
            f"ai-receptionist/{slug}/index.html",
            bs.page(
                f"AI-receptionist {name}",
                f"AI-receptionist för företag i {name}: 24/7, bokning, vidarekoppling.",
                f"{BASE}/ai-receptionist/{slug}/",
                body,
                "ai-rec",
                extra_ld=[bs.faq_ld(faqs)],
                crumbs=[
                    ("Hem", BASE + "/"),
                    ("AI-receptionist", BASE + "/ai-receptionist/"),
                    (name, f"{BASE}/ai-receptionist/{slug}/"),
                ],
            ),
        )

    for path, h1, ans in GUIDES:
        faqs = [(h1 + "?", ans)]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/guider/">Guider</a></div>
<h1>{h1}</h1>
<div class="answer-box"><strong>Kort svar:</strong> {ans}</div>
</section>
<section class="block wrap">
<div class="related">
<a href="/jamfor/">Jämför</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/branscher/">Branscher</a>
<a href="/faq/">FAQ</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
"""
        bs.write(
            path + "/index.html",
            bs.page(
                h1 + " — guide 2026",
                ans[:155],
                f"{BASE}/{path}/",
                body,
                "guider",
                extra_ld=[bs.faq_ld(faqs)],
                crumbs=[("Hem", BASE + "/"), ("Guider", BASE + "/guider/"), (h1, f"{BASE}/{path}/")],
            ),
        )

    urls = []
    for p in root.rglob("index.html"):
        rel = p.parent.relative_to(root).as_posix()
        urls.append(BASE + "/" if rel == "." else f"{BASE}/{rel}/")
    urls.append(BASE + "/llms.txt")
    bs.sitemap(sorted(set(urls)))
    print("wave6", len(set(urls)))


if __name__ == "__main__":
    main()
