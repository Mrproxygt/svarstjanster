#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXTRA = """
<section class="block wrap enrich">
<h2>Så undviker du vanliga fallgropar</h2>
<p class="p">Köp inte enbart på en snygg demoröst. Be om tre scripts: (1) rutinbokning, (2) ombokning/avvikelse, (3) eskalering till människa. Anteckna om AI:n hittar på policy, priser eller tider ni inte godkänt.</p>
<p class="p">Räkna alltid total månadskostnad vid er volym — abonnemang plus per-samtal plus setup. Jämför med kostnaden för missade leads. Prisintervallen på den här sajten är uppskattningar (augusti 2026), inte offerter.</p>
<p class="p">Kräv EU-lagring, tydliga loggar och att samtal inte används för att träna generella modeller. Skriv eskaleringsregler innan go-live: vilka nyckelord, tider och kundtyper som alltid ska till er personal.</p>
<p class="p">När ni jämför leverantörer: samma scripts, samma volymantaganden, samma krav på kalender och SMS. Dokumentera beslutet så ni kan ompröva efter 30 dagar med riktiga siffror från er egen trafik.</p>
<p class="p">Relaterat material: <a href="/jamfor/">jämförelsematris</a>, <a href="/svarstjanst-pris/">prisguide</a>, <a href="/leverantorer/">leverantörskatalog</a> och er <a href="/branscher/">branschguide</a> om ni har en specifik verksamhet.</p>
</section>
"""

EXTRA2 = """
<section class="block alt enrich2">
<div class="wrap">
<h2>Praktisk checklista innan avtal</h2>
<ul class="checklist">
<li>Tre demoscript godkända internt (rutin, avvikelse, eskalering)</li>
<li>Skriftlig prismodell: setup, månad, överage, SMS, bindningstid</li>
<li>Vidarekoppling utan portering — behåll numret</li>
<li>Kalender + SMS-bekräftelse om bokning är kärnbehov</li>
<li>EU-data, DPA, loggar, retention</li>
<li>Eskaleringslista till namngiven mobil/kö</li>
<li>Uppföljning efter 14 och 30 dagar med antal besvarade/missade</li>
</ul>
<p class="p">Om leverantören inte kan visa hur er bransch-jargong hanteras: pausa. Generisk AI som gissar priser skadar mer än en missad signal.</p>
</div>
</section>
"""


def words(html: str) -> int:
    t = re.sub(r"<script[\s\S]*?</script>", " ", html)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return len([w for w in t.split() if len(w) > 1])


def main():
    n = 0
    for p in ROOT.rglob("index.html"):
        html = p.read_text(encoding="utf-8")
        w = words(html)
        changed = False
        if w < 700 and 'class="block wrap enrich"' not in html and "cta-band" in html:
            html = html.replace(
                '<section class="wrap"><div class="cta-band">',
                EXTRA + '<section class="wrap"><div class="cta-band">',
                1,
            )
            changed = True
        if words(html) < 850 and 'class="block alt enrich2"' not in html and "cta-band" in html:
            html = html.replace(
                '<section class="wrap"><div class="cta-band">',
                EXTRA2 + '<section class="wrap"><div class="cta-band">',
                1,
            )
            changed = True
        if changed:
            p.write_text(html, encoding="utf-8")
            n += 1
    print("enriched_files", n)
    samples = [
        "index.html",
        "jamfor/index.html",
        "ai-receptionist/index.html",
        "branscher/tandlakare/index.html",
        "ai-receptionist/stockholm/index.html",
        "guider/letar-efter-ai-receptionist/index.html",
        "alternativ/wecall/index.html",
        "faq/vad-kostar-ai-receptionist/index.html",
    ]
    for s in samples:
        print(s, words((ROOT / s).read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
