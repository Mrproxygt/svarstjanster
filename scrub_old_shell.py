#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove leftover Menodi satellite funnel from any HTML still on disk."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

# Rebuild the 3 combo pages with independent shell via import
from rebuild_rich_v2 import (
    page, faq_ld, chips, related, cta, faq_html, write, BASE, COMPETITORS
)


def rebuild_combos():
    combos = [
        ("branscher/tandlakare-stockholm", "AI-receptionist tandläkare Stockholm",
         "För kliniker i Stockholm: boka/omboka, efter stängning, SMS mot no-show. Jämför dentala specialister och generella AI-receptionister via leverantörernas egna sajter."),
        ("branscher/frisor-goteborg", "AI-receptionist frisör Göteborg",
         "Salonger i Göteborg: boka medan du klipper, kvällsförfrågningar, ombokning via SMS."),
        ("branscher/maklare-stockholm", "AI-receptionist mäklare Stockholm",
         "Spekulant-samtal kväll/helg i Stockholm — AI kvalificerar och bokar visning."),
    ]
    for path, h1, ans in combos:
        faqs = [(h1 + "?", ans), ("Var hittar jag leverantörer?", "Se /leverantorer/ — länkar går till respektive bolags webbplats.")]
        body = f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/branscher/">Branscher</a></div>
<h1>{h1}</h1>
<div class="answer-box"><span class="lbl">Kort svar</span>{ans}</div>
{chips(["Oberoende", "Svarstjänster AB", "Externa leverantörslänkar"])}
<div class="ctas">
<a class="btn" href="/leverantorer/">Se leverantörer</a>
<a class="btn ghost" href="/jamfor/">Jämför modeller</a>
</div>
</section>
<section class="block wrap">
<p class="p">Svarstjänster.se (Svarstjänster AB) jämför alternativ — vi säljer inte själva tjänsten. När du klickar vidare hamnar du hos leverantörens egen sajt.</p>
{related([("/branscher/","Alla branscher"),("/ai-receptionist/","AI-receptionist"),("/ai-receptionist/stockholm/","Stockholm"),("/ai-receptionist/goteborg/","Göteborg"),("/leverantorer/","Leverantörer")])}
</section>
<section class="block alt" id="faq"><div class="wrap">{faq_html(faqs)}</div></section>
{cta("Gå vidare till en leverantör", "Välj minst två att testa med samma scripts.", path)}
"""
        write(
            path + "/index.html",
            page(
                h1 + " — 2026",
                ans[:155],
                f"{BASE}/{path}/",
                body,
                "bran",
                extra_ld=[faq_ld(faqs)],
                crumbs=[("Hem", BASE + "/"), ("Branscher", BASE + "/branscher/"), (h1, f"{BASE}/{path}/")],
            ),
        )


def scrub_all():
    n = 0
    for p in ROOT.rglob("index.html"):
        html = p.read_text(encoding="utf-8")
        orig = html
        html = re.sub(
            r"https://menodi\.se/\?utm_source=svarstjanster[^\"']*",
            "https://menodi.se/",
            html,
        )
        html = html.replace("en del av Menodi", "Svarstjänster AB")
        html = html.replace('rel="sponsored"', 'rel="noopener noreferrer"')
        html = html.replace(">Prova AI gratis</a>", ">Se leverantörer</a>")
        html = html.replace(">Prova Menodi</a>", ">Se leverantörer</a>")
        # bad nav that still points to menodi utm for CTA
        html = re.sub(
            r'<a class="navcta" href="https://menodi\.se/[^"]*"[^>]*>[^<]*</a>',
            '<a class="navcta" href="/leverantorer/">Se leverantörer</a>',
            html,
        )
        if html != orig:
            p.write_text(html, encoding="utf-8")
            n += 1
    print("scrubbed", n)


if __name__ == "__main__":
    rebuild_combos()
    scrub_all()
    left = 0
    for p in ROOT.rglob("index.html"):
        t = p.read_text(encoding="utf-8")
        if "utm_source=svarstjanster" in t or "en del av Menodi" in t:
            left += 1
            print("STILL", p)
    print("still_bad", left)
