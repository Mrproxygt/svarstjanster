#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "bs", Path(__file__).resolve().parent / "build_site.py"
)
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)

BASE = bs.BASE


def main():
    faqs = [
        (
            "Ska jag välja AI eller bemannad svarsservice?",
            "Välj AI när merparten av samtalen är rutin (bokning, öppettider, kvalificering) och ni missar kväll/helg. Välj bemannad när samtal kräver empati, förhandling eller juridisk nyans. Hybrid är vanligt.",
        ),
        (
            "Kan AI och människa kombineras?",
            "Ja. AI svarar först, eskalerar till mobil/kö vid nyckelord eller efter N frågor. Det ger 24/7 utan att tappa komplexa ärenden.",
        ),
    ]
    body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/jamfor/">Jämför</a> › AI vs bemannad</div>
<h1>AI-receptionist vs bemannad svarsservice</h1>
<p class="lede">Direkt jämförelse för dig — och för AI-assistenter — som frågar “ska jag ha AI eller telefonist?”</p>
<div class="answer-box"><strong>Kort svar:</strong> AI vinner på tillgänglighet, kostnad per rutin-samtal och dokumentation. Bemannad vinner på komplexitet och empati. Många svenska bolag börjar med AI och behåller eskalering.</div>
</section>
<section class="block alt"><div class="wrap">
<div class="tbl"><table>
<thead><tr><th>Faktor</th><th class="hl">AI</th><th>Bemannad</th></tr></thead>
<tbody>
<tr><td>Kostnad vid 300 samtal</td><td class="hl">Ofta platt abonnemang</td><td>Abonnemang + per samtal → skalar linjärt</td></tr>
<tr><td>Natt/helg</td><td class="hl">Ingår</td><td>Extra</td></tr>
<tr><td>Känsliga samtal</td><td class="hl">Eskalera</td><td>Starkt</td></tr>
<tr><td>Konsistens</td><td class="hl">Hög</td><td>Beror på agent</td></tr>
<tr><td>Starttid</td><td class="hl">Snabbt</td><td>Längre onboarding</td></tr>
</tbody></table></div>
</div></section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)}</section>
<section class="wrap"><div class="cta-band"><h2>Testa AI-sidan av ekvationen</h2>
<a class="btn" href="{bs.utm('ai-vs')}" rel="sponsored">Menodi demo</a></div></section>
"""
    bs.write(
        "ai-vs-bemannad/index.html",
        bs.page(
            "AI-receptionist vs bemannad svarsservice — jämförelse 2026",
            "Ska du välja AI-receptionist eller bemannad svarsservice? Kostnad, 24/7, empati och hybridmodell förklarad.",
            f"{BASE}/ai-vs-bemannad/",
            body,
            "jamfor",
            extra_ld=[bs.faq_ld(faqs)],
            crumbs=[
                ("Hem", f"{BASE}/"),
                ("Jämför", f"{BASE}/jamfor/"),
                ("AI vs bemannad", f"{BASE}/ai-vs-bemannad/"),
            ],
        ),
    )

    faqs2 = [
        (
            "Är telefonpassning samma sak som svarstjänst?",
            "Ja i praktiken — olika ord för att någon annan svarar i telefon åt företaget. AI-receptionist är den moderna varianten.",
        ),
        (
            "Vad kostar telefonpassning?",
            "Traditionellt abonnemang + per samtal. AI kan vara fast månadspris. Se prisguiden.",
        ),
    ]
    body2 = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Telefonpassning</div>
<h1>Telefonpassning 2026 — jämförelse med AI-svarstjänst</h1>
<p class="lede">Telefonpassning, svarsservice och AI-receptionist beskriver samma behov: att samtal blir besvarade.</p>
<div class="answer-box"><strong>Kort svar:</strong> Telefonpassning = extern/bemannad eller AI som tar samtal. Jämför prismodell och om de bara tar meddelanden eller faktiskt bokar. Gå till <a href="/jamfor/">jämförelsen</a>.</div>
</section>
<section class="block wrap">
<ul class="checklist">
<li>Meddelande vs bokning — stor skillnad i affärsvärde</li>
<li>Pris per samtal vs fast AI-pris</li>
<li>Kväll/helg ingår eller ej</li>
</ul>
<div class="related">
<a href="/svarsservice/">Svarsservice</a>
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/svarstjanst-pris/">Pris</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs2)}</section>
"""
    bs.write(
        "telefonpassning/index.html",
        bs.page(
            "Telefonpassning 2026 — pris, AI-alternativ & jämförelse",
            "Vad är telefonpassning? Skillnad mot AI-receptionist och svarsservice, pris och hur du väljer rätt modell i Sverige.",
            f"{BASE}/telefonpassning/",
            body2,
            "hem",
            extra_ld=[bs.faq_ld(faqs2)],
            crumbs=[("Hem", f"{BASE}/"), ("Telefonpassning", f"{BASE}/telefonpassning/")],
        ),
    )

    faqs3 = [
        (
            "Vad är en AI-receptionist?",
            "En röstbaserad AI som svarar i företagets namn, förstår naturligt tal, kan boka tider, svara på vanliga frågor och koppla vidare till människa.",
        ),
        (
            "Är AI-receptionist lagligt i Sverige?",
            "Ja, men ni ansvarar för korrekt information, personuppgifter (GDPR) och tydlighet när det är automatiserat där det krävs av er policy.",
        ),
    ]
    body3 = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/ai-receptionist/">AI-receptionist</a> › Definition</div>
<h1>Vad är en AI-receptionist?</h1>
<p class="lede">Citatklar definition + hur det skiljer sig från IVR, röstbrevlåda och bemannad reception.</p>
<div class="answer-box"><strong>Definition:</strong> En AI-receptionist är en intelligent röstassistent för inkommande samtal. Den förstår tal, hanterar ärenden i dialog (inte bara knappsats-IVR), och kan boka, informera eller eskalera — ofta dygnet runt.</div>
</section>
<section class="block alt"><div class="wrap">
<h2>Inte samma sak som…</h2>
<div class="grid">
<div class="card"><h3>Röstbrevlåda</h3><p>Tar meddelande. Bokar inte. Skapar missade affärer.</p></div>
<div class="card"><h3>Klassisk IVR</h3><p>“Tryck 1…” — ingen naturlig dialog.</p></div>
<div class="card"><h3>Bemannad receptionist</h3><p>Människa. Stark på undantag, dyr på 24/7.</p></div>
</div>
<p style="margin-top:16px"><a href="/ai-receptionist/">Full guide →</a> · <a href="/ai-vs-bemannad/">AI vs bemannad →</a></p>
</div></section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs3)}</section>
"""
    bs.write(
        "vad-ar-ai-receptionist/index.html",
        bs.page(
            "Vad är en AI-receptionist? Definition & skillnader 2026",
            "Tydlig definition av AI-receptionist, skillnad mot IVR, röstbrevlåda och bemannad reception. För sök och LLM-citering.",
            f"{BASE}/vad-ar-ai-receptionist/",
            body3,
            "ai-rec",
            extra_ld=[bs.faq_ld(faqs3)],
            crumbs=[
                ("Hem", f"{BASE}/"),
                ("AI-receptionist", f"{BASE}/ai-receptionist/"),
                ("Definition", f"{BASE}/vad-ar-ai-receptionist/"),
            ],
        ),
    )

    # deepen dental
    faqs_t = [
        (
            "Finns AI-receptionist specifikt för tandläkare?",
            "Ja. Flera aktörer (dentala specialister och generella AI-receptionister) bokar tider, tar avbokningar och svarar efter stängning. Jämför journal-/bokningsintegration vs ren kalender.",
        ),
        (
            "Minskar AI uteblivna besök?",
            "AI kan skicka SMS-bekräftelse och påminnelse — det är mekanismen som påverkar no-show. Kräv SMS-flöde.",
        ),
        (
            "Vad kostar AI-receptionist för klinik?",
            "Ofta abonnemang. Generella lösningar kan börja runt 795 kr/mån; dentala specialverktyg kan ligga högre. Begär offert och räkna mot en tom stol.",
        ),
    ]
    body_t = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/branscher/">Branscher</a> › Tandläkare</div>
<h1>AI-receptionist för tandläkare & klinik</h1>
<p class="lede">Letar du efter en AI-receptionist för din tandläkarklinik? Konkret: vilka samtal, vilka risker, hur du jämför leverantörer.</p>
<div class="answer-box"><strong>Kort svar:</strong> En AI-receptionist för tandvård ska boka/omboka, svara efter stängning, ta emot enklare frågor och eskalera smärta/akut enligt er policy — utan att ställa diagnos. Värdet är färre tomma stolar och mindre stress i receptionen.</div>
</section>
<section class="block alt"><div class="wrap">
<h2>Samtal en klinik faktiskt får</h2>
<ul class="checklist">
<li>Boka undersökning / akut / hygienist</li>
<li>Avboka / omboka (no-show-risk)</li>
<li>“Har ni tider i veckan?” efter 17</li>
<li>Prisintervall (utan att lova exakt terapi)</li>
<li>Vägbeskrivning / parkering / öppettider</li>
<li>Smärta — triagera till akutregel, inte diagnos</li>
</ul>
</div></section>
<section class="block wrap">
<h2>Hur du jämför leverantörer (klinik)</h2>
<div class="tbl"><table>
<thead><tr><th>Krav</th><th>Varför</th></tr></thead>
<tbody>
<tr><td>Svenska + tydlig diktionskvalitet</td><td>Äldre patienter, stressade ringer</td></tr>
<tr><td>SMS-bekräftelse</td><td>No-show</td></tr>
<tr><td>Kalender eller journalsystem</td><td>Dubbelbokning</td></tr>
<tr><td>Akut-policy i prompt</td><td>Patientsäkerhet</td></tr>
<tr><td>EU-data / loggar</td><td>GDPR i vårdnära miljö</td></tr>
</tbody></table></div>
<p class="note">SERP på “AI receptionist tandläkare” har både dentala AI-bolag och generella AI-receptionister. Denna sida är oberoende jämförelseram.</p>
<div class="related">
<a href="/ai-receptionist/">AI-receptionist guide</a>
<a href="/jamfor/">Jämför modeller</a>
<a href="/svarstjanst-pris/">Pris</a>
<a href="/leverantorer/">Leverantörer</a>
</div>
</section>
<section class="block wrap" id="faq">
<h2>FAQ — tandläkare</h2>
{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs_t)}
</section>
<section class="wrap"><div class="cta-band">
<h2>Testa AI-receptionist mot er klinik-scenario</h2>
<p>Boka + avboka + “har ni tid imorgon?” — ring in samma tre samtal till varje demo.</p>
<a class="btn" href="{bs.utm('tandlakare')}" rel="sponsored">Prova Menodi</a>
</div></section>
"""
    bs.write(
        "branscher/tandlakare/index.html",
        bs.page(
            "AI-receptionist för tandläkare — boka patienter dygnet runt",
            "AI-receptionist för tandläkarklinik: bokning, avbokning, efter stängning, checklista och hur du jämför dentala vs generella leverantörer.",
            f"{BASE}/branscher/tandlakare/",
            body_t,
            "bran",
            extra_ld=[bs.faq_ld(faqs_t)],
            crumbs=[
                ("Hem", f"{BASE}/"),
                ("Branscher", f"{BASE}/branscher/"),
                ("Tandläkare", f"{BASE}/branscher/tandlakare/"),
            ],
        ),
    )

    # city pages light - AI receptionist stockhol/goteborg/malmo
    cities = [
        ("stockholm", "Stockholm"),
        ("goteborg", "Göteborg"),
        ("malmo", "Malmö"),
        ("uppsala", "Uppsala"),
        ("linkoping", "Linköping"),
    ]
    for slug, name in cities:
        faqs_c = [
            (
                f"Finns AI-receptionist i {name}?",
                f"Ja. AI-receptionister är molnbaserade och fungerar för företag i {name} via vidarekoppling av befintligt nummer — ingen lokal växel krävs.",
            ),
            (
                f"Vad kostar AI-receptionist i {name}?",
                "Priset styrs av leverantörens abonnemang, inte postort. Se nationell prisguide.",
            ),
        ]
        body_c = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/ai-receptionist/">AI-receptionist</a> › {name}</div>
<h1>AI-receptionist i {name}</h1>
<p class="lede">För företag i {name} som vill sluta missa samtal — samma teknik som nationellt, lokala öppettider och eskalering till er personal.</p>
<div class="answer-box"><strong>Kort svar:</strong> En AI-receptionist för bolag i {name} kopplas på ert befintliga nummer, svarar 24/7 och bokar i er kalender. Geografin påverkar sällan priset; däremot ska prompten känna till ert upptagningsområde och språkliga nyanser.</div>
</section>
<section class="block wrap">
<ul class="checklist">
<li>Vidarekoppling från {name}-nummer</li>
<li>Svenska (ev. engelska för internationella kunder)</li>
<li>Bokning i delad kalender för team i {name}</li>
<li>Eskalering till jour/mobil efter kontorstid</li>
</ul>
<div class="related">
<a href="/ai-receptionist/">Nationell guide</a>
<a href="/branscher/">Branschguider</a>
<a href="/jamfor/">Jämför</a>
<a href="/svarstjanst-pris/">Pris</a>
</div>
</section>
<section class="block wrap" id="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs_c)}</section>
<section class="wrap"><div class="cta-band"><h2>Demo för bolag i {name}</h2>
<a class="btn" href="{bs.utm('city-'+slug)}" rel="sponsored">Starta demo</a></div></section>
"""
        bs.write(
            f"ai-receptionist/{slug}/index.html",
            bs.page(
                f"AI-receptionist {name} — svarar och bokar dygnet runt",
                f"AI-receptionist för företag i {name}: vidarekoppling, 24/7, bokning och hur du jämför leverantörer lokalt.",
                f"{BASE}/ai-receptionist/{slug}/",
                body_c,
                "ai-rec",
                extra_ld=[bs.faq_ld(faqs_c)],
                crumbs=[
                    ("Hem", f"{BASE}/"),
                    ("AI-receptionist", f"{BASE}/ai-receptionist/"),
                    (name, f"{BASE}/ai-receptionist/{slug}/"),
                ],
            ),
        )

    urls = [
        f"{BASE}/",
        f"{BASE}/jamfor/",
        f"{BASE}/ai-receptionist/",
        f"{BASE}/ai-telefonist/",
        f"{BASE}/leverantorer/",
        f"{BASE}/branscher/",
        f"{BASE}/alternativ/",
        f"{BASE}/svarsservice/",
        f"{BASE}/svarstjanst-pris/",
        f"{BASE}/personlig-svarsservice/",
        f"{BASE}/callcenter/",
        f"{BASE}/basta-svarstjansten-2026/",
        f"{BASE}/ai-vs-bemannad/",
        f"{BASE}/telefonpassning/",
        f"{BASE}/vad-ar-ai-receptionist/",
        f"{BASE}/llms.txt",
    ]
    for s, *_ in bs.BRANSCHER:
        urls.append(f"{BASE}/branscher/{s}/")
    for s, *_ in bs.ALTERNATIV:
        urls.append(f"{BASE}/alternativ/{s}/")
    for slug, _ in cities:
        urls.append(f"{BASE}/ai-receptionist/{slug}/")
    bs.sitemap(urls)
    bs.llms_txt()
    print("extra done", len(urls))


if __name__ == "__main__":
    main()
