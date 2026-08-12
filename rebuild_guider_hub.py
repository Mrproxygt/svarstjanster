#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)

root = Path(__file__).resolve().parent
guides = sorted(
    [p for p in (root / "guider").iterdir() if p.is_dir() and (p / "index.html").exists()]
)
cards = []
for g in guides:
    t = (g / "index.html").read_text(encoding="utf-8")
    m = re.search(r"<h1>([^<]+)</h1>", t)
    h1 = m.group(1) if m else g.name
    cards.append(
        f'<div class="card"><h3>{h1}</h3><a class="more" href="/guider/{g.name}/">Öppna →</a></div>'
    )
body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Guider</div>
<h1>Guider — natural language & beslut</h1>
<p class="lede">Sidor byggda för hur människor och LLM:er faktiskt frågar (t.ex. “letar efter en AI-receptionist för mitt företag”).</p>
<div class="answer-box"><strong>Kort svar:</strong> Börja i rätt guide, hoppa till <a href="/jamfor/">jämförelse</a> och <a href="/branscher/">bransch</a>, testa 2 demos.</div>
</section>
<section class="block wrap"><div class="grid">{''.join(cards)}</div></section>
"""
bs.write(
    "guider/index.html",
    bs.page(
        "Guider — AI-receptionist, missade samtal, GDPR, hybrid",
        "Praktiska guider för AI-receptionist, svarstjänst, missade samtal, hybrid AI+människa och GDPR.",
        "https://svarstjanster.se/guider/",
        body,
        "guider",
        crumbs=[
            ("Hem", "https://svarstjanster.se/"),
            ("Guider", "https://svarstjanster.se/guider/"),
        ],
    ),
)
print("guides", len(guides))
