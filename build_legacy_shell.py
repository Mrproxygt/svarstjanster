#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild legacy 5 pages into shared authority shell (keep core facts)."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
BASE = bs.BASE


def pris():
    faqs = [
        ("Vad kostar en svarstjänst?",
         "AI-svarstjänst kan ha fast pris från ca 795 kr/mån. Bemannad svarsservice ofta 1 000–5 000 kr/mån plus ca 15–35 kr/samtal. Anställd receptionist 40 000–50 000 kr/mån i lön-nivå. Uppskattningar, begär offert."),
        ("Vad ingår i ett fast AI-pris?",
         "Hos moderna leverantörer: samtal, röst, ofta kalenderbokning, SMS, transkript. Läs alltid villkor — gränser för minuter kan förekomma."),
        ("Kan jag behålla mitt nummer?",
         "Ja om leverantören använder vidarekoppling istället för portering."),
    ]
    body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Pris</div>
<h1>Svarstjänst pris 2026 — komplett prisguide</h1>
<p class="lede">Jämför kostnad för AI-receptionist, bemannad svarsservice, callcenter och anställd receptionist.</p>
<div class="answer-box"><strong>Kort svar:</strong> Räkna total månadskostnad vid er samtalsvolym. Per-samtal blir dyrt vid 200–400 samtal; fast AI-pris är förutsägbart; anställd är dyrast men mest flexibel på plats.</div>
</section>
<section class="block alt"><div class="wrap">
<h2>Pristabell (marknadsnivåer)</h2>
<div class="tbl"><table>
<thead><tr><th>Typ</th><th>Månad</th><th>Per samtal</th><th>Kommentar</th></tr></thead>
<tbody>
<tr><td class="hl"><strong>AI-svarstjänst (t.ex. Menodi)</strong></td><td class="hl">från ca 795 kr</td><td class="hl">ofta 0 kr</td><td class="hl">24/7, bokning, SMS — kolla gränser</td></tr>
<tr><td>Bemannad svarsservice</td><td>1 000–5 000 kr</td><td>15–35 kr</td><td>Skalar med volym</td></tr>
<tr><td>Callcenter</td><td>5 000–20 000+ kr</td><td>varierar</td><td>Offert, process</td></tr>
<tr><td>Anställd receptionist</td><td>40 000–50 000 kr</td><td>ingår i lön</td><td>+ sociala avgifter</td></tr>
</tbody></table></div>
<p class="note">Uppskattningar {bs.REVIEW}. Inte offerter.</p>
</div></section>
<section class="block wrap">
<h2>Hypotetiskt räkneexempel (300 samtal/mån)</h2>
<ul class="checklist">
<li>Per samtal 25 kr + abonnemang 2 000 kr ≈ 9 500 kr</li>
<li>Fast AI 795 kr ≈ 795 kr</li>
<li>Anställd ≈ 42 000 kr (lön-nivå)</li>
</ul>
<div class="related">
<a href="/jamfor/">Jämför modeller</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/leverantorer/">Leverantörer</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
<section class="wrap"><div class="cta-band"><h2>Testa fast AI-pris</h2>
<a class="btn" href="{bs.utm('pris')}" rel="sponsored">Menodi från 795 kr/mån</a></div></section>
"""
    bs.write("svarstjanst-pris/index.html", bs.page(
        "Svarstjänst pris 2026 — AI vs bemannad vs anställd",
        "Vad kostar en svarstjänst i Sverige? Pristabell för AI-receptionist, bemannad svarsservice, callcenter och receptionist.",
        f"{BASE}/svarstjanst-pris/", body, "pris",
        extra_ld=[bs.faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Pris", f"{BASE}/svarstjanst-pris/")],
    ))


def svarsservice():
    faqs = [
        ("Vad är svarsservice?",
         "Svarsservice innebär att ett externt bolag eller en AI svarar i telefon i ert namn när ni inte kan — tar meddelanden, bokar eller kopplar vidare."),
        ("Svarsservice eller telefonpassning?",
         "Samma behov, olika ord. AI-receptionist är modern variant med bokning och 24/7."),
    ]
    body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Svarsservice</div>
<h1>Svarsservice — definition, pris och AI-alternativ</h1>
<div class="answer-box"><strong>Kort svar:</strong> Svarsservice = någon svarar åt er. Klassiskt bemannat (per samtal) eller AI (ofta fast pris). Välj utifrån samtalskomplexitet och volym.</div>
</section>
<section class="block wrap">
<div class="grid">
<div class="card"><h3>Bemannad</h3><p>Bra för komplexa samtal. Kostnad skalar.</p></div>
<div class="card"><h3>AI-svarsservice</h3><p>Bra för rutin + 24/7. Se <a href="/ai-receptionist/">AI-receptionist</a>.</p></div>
<div class="card"><h3>Hybrid</h3><p>AI först, människa vid eskalering.</p></div>
</div>
<div class="related" style="margin-top:18px">
<a href="/telefonpassning/">Telefonpassning</a>
<a href="/jamfor/">Jämför</a>
<a href="/svarstjanst-pris/">Pris</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
"""
    bs.write("svarsservice/index.html", bs.page(
        "Svarsservice 2026 — definition, pris & AI-alternativ",
        "Vad är svarsservice? Skillnad mot telefonpassning och AI-receptionist, prisriktning och hur du väljer.",
        f"{BASE}/svarsservice/", body, "hem",
        extra_ld=[bs.faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Svarsservice", f"{BASE}/svarsservice/")],
    ))


def callcenter():
    faqs = [
        ("Behöver småföretag callcenter?",
         "Sällan. Callcenter lönar sig vid hög volym och process. Småföretag får oftast bättre ROI av AI-receptionist eller lätt svarsservice."),
    ]
    body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Callcenter</div>
<h1>Callcenter för småföretag — när det lönar sig (och när AI räcker)</h1>
<div class="answer-box"><strong>Kort svar:</strong> Callcenter = skala och process. För de flesta SMB är AI-telefonist + eskalering billigare och snabbare att starta.</div>
</section>
<section class="block wrap">
<ul class="checklist">
<li>Hög volym support</li>
<li>Flera köer och SLA</li>
<li>Utbildade agenter på script</li>
<li>Överväg AI först om volymen är låg–medel</li>
</ul>
<div class="related"><a href="/jamfor/">Jämför</a><a href="/ai-telefonist/">AI-telefonist</a></div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
"""
    bs.write("callcenter/index.html", bs.page(
        "Callcenter för småföretag 2026 — eller räcker AI?",
        "När callcenter lönar sig för SMB, när AI-receptionist räcker, och hur kostnaderna skiljer sig.",
        f"{BASE}/callcenter/", body, "hem",
        extra_ld=[bs.faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Callcenter", f"{BASE}/callcenter/")],
    ))


def personlig():
    faqs = [
        ("Vad betyder personlig svarsservice?",
         "Oftast att samma team/agenter lär sig ert bolag och svarar i er ton — inte anonym kö. AI kan också vara 'personlig' via er brand-röst och regler."),
    ]
    body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Personlig svarsservice</div>
<h1>Personlig svarsservice — vad det faktiskt betyder</h1>
<div class="answer-box"><strong>Kort svar:</strong> “Personlig” ska betyda kontinuitet och bolagskännedom — inte bara ett säljord. Fråga hur agenter tränas, och jämför med AI som konfigureras på er knowledge base.</div>
</section>
<section class="block wrap">
<div class="related">
<a href="/svarsservice/">Svarsservice</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/alternativ/">Alternativ</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
"""
    bs.write("personlig-svarsservice/index.html", bs.page(
        "Personlig svarsservice — betydelse, pris & AI",
        "Vad personlig svarsservice betyder i praktiken, hur det skiljer sig från anonym kö och AI-receptionist.",
        f"{BASE}/personlig-svarsservice/", body, "hem",
        extra_ld=[bs.faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Personlig svarsservice", f"{BASE}/personlig-svarsservice/")],
    ))


def basta():
    faqs = [
        ("Vem är bäst svarstjänst 2026?",
         "Det finns ingen universell vinnare. Bäst beror på volym, bransch och om ni behöver människa eller AI. Använd kriterierna nedan."),
        ("Hur rankar ni?",
         "Vi rankar inte betalt. Vi publicerar metodikkriterier och leverantörskatalog så du kan utvärdera själv."),
    ]
    body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Bästa 2026</div>
<h1>Bästa svarstjänsten 2026 — metodikdriven guide</h1>
<div class="answer-box"><strong>Kort svar:</strong> “Bäst” utan kriterier är reklam. Använd: tillgänglighet, total kostnad vid er volym, bokning, eskalering, data/GDPR, demosamtal i er bransch.</div>
</section>
<section class="block alt"><div class="wrap">
<h2>Utvärderingskriterier</h2>
<ul class="checklist">
<li>Total cost of ownership vid 100 / 300 / 800 samtal</li>
<li>24/7 vs kontorstid</li>
<li>Kalender + SMS</li>
<li>Eskalering med kontext</li>
<li>Svenska språkkvalitet</li>
<li>EU-data, loggar, ingen träningsanvändning</li>
<li>Tid till live</li>
</ul>
</div></section>
<section class="block wrap">
<p>Gå vidare till <a href="/jamfor/">matrisen</a>, <a href="/leverantorer/">leverantörer</a> och din <a href="/branscher/">bransch</a>.</p>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
"""
    bs.write("basta-svarstjansten-2026/index.html", bs.page(
        "Bästa svarstjänsten 2026 — metodik & checklista",
        "Hur du utvärderar bästa svarstjänst 2026 utan köpt ranking: kostnad, 24/7, bokning, GDPR, demosamtal.",
        f"{BASE}/basta-svarstjansten-2026/", body, "jamfor",
        extra_ld=[bs.faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Bästa 2026", f"{BASE}/basta-svarstjansten-2026/")],
    ))


if __name__ == "__main__":
    pris()
    svarsservice()
    callcenter()
    personlig()
    basta()
    print("legacy shell rebuilt")
