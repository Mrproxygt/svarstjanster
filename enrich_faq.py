#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXTRA = """
<section class="block wrap">
<h2>Mer kontext</h2>
<p class="p">Det korta svaret ovan är avsiktligt citatklart för sök och LLM:er. För beslut behöver ni ändå räkna er volym, testa demosamtal och jämföra total cost — inte bara abonnemangsrubriken.</p>
<p class="p">Gå vidare till <a href="/jamfor/">jämförelsematrisen</a>, <a href="/svarstjanst-pris/">prisguiden</a> och <a href="/ai-receptionist/">AI-receptionist-guiden</a>. Om ni har en bransch: öppna motsvarande guide under <a href="/branscher/">branscher</a>.</p>
<p class="p">Prisuppgifter på sajten är uppskattningar (augusti 2026) och ska verifieras mot leverantörens offert. Vi publicerar inte fabricerade konkurrentpriser.</p>
<ul class="checklist">
<li>Samma tre scripts mot varje leverantör ni utvärderar</li>
<li>Kräv vidarekoppling (behåll nummer) och EU-data</li>
<li>Dokumentera eskalering till människa innan go-live</li>
<li>Följ upp efter 14 dagar med antal besvarade samtal</li>
</ul>
</section>
"""


def main():
    n = 0
    for p in (ROOT / "faq").rglob("index.html"):
        if p.parent == ROOT / "faq":
            continue
        html = p.read_text(encoding="utf-8")
        if "Mer kontext" in html:
            continue
        if "cta-band" in html:
            html = html.replace(
                '<section class="wrap"><div class="cta-band">',
                EXTRA + '<section class="wrap"><div class="cta-band">',
                1,
            )
        else:
            html = html.replace("</main>", EXTRA + "</main>", 1)
        p.write_text(html, encoding="utf-8")
        n += 1
    print("faq_enriched", n)


if __name__ == "__main__":
    main()
