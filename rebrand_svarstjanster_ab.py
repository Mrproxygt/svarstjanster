#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebrand svarstjanster.se as independent Svarstjänster AB comparison site.
- No Menodi parent / satellite funnel
- Outbound CTAs go to real competitor product pages
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "rebuild_rich_v2.py"

# Public competitor destinations (product pages, not our site)
COMPETITORS = {
    "wecall": ("WeCall", "https://wecall.se/svarstjanst/"),
    "answeronline": ("AnswerOnline", "https://answeronline.se/"),
    "responda": ("Responda", "https://respondagroup.se/svarsservice/"),
    "skaala": ("Skaala", "https://www.skaala.ai/sv/"),
    "telink": ("Telink", "https://telink.se/ai-receptionist/"),
    "telavox": ("Telavox", "https://telavox.se/ai-receptionist/"),
    "lynes": ("Lynes", "https://lynes.io/funktioner/ai-telefonist"),
    "ringup": ("Ringup", "https://www.ringup.se/"),
    "itell": ("iTell", "https://www.itell.nu/tjanster/telefonpassning/"),
    "svardirekt": ("SvarDirekt", "https://www.svardirekt.se/"),
    "bigacom": ("Bigacom", "https://bigacom.se/svarstjanst/"),
    "comunit": ("Comunit", "https://comunit.se/tjanster/svarstjanst"),
    "menodi": ("Menodi", "https://menodi.se/"),  # listed as one competitor only
}

# Default CTA rotation targets (AI-ish first for AI CTAs)
CTA_AI = [
    COMPETITORS["skaala"],
    COMPETITORS["telink"],
    COMPETITORS["telavox"],
    COMPETITORS["lynes"],
    COMPETITORS["menodi"],
]
CTA_HUMAN = [
    COMPETITORS["wecall"],
    COMPETITORS["answeronline"],
    COMPETITORS["responda"],
    COMPETITORS["itell"],
    COMPETITORS["svardirekt"],
    COMPETITORS["bigacom"],
    COMPETITORS["ringup"],
]


def patch_generator():
    t = SRC.read_text(encoding="utf-8")

    # Constants: drop MENODI funnel helper
    t = t.replace(
        'MENODI = "https://menodi.se/?utm_source=svarstjanster&utm_medium=satellite&utm_campaign={c}"\n',
        "",
    )

    # Insert competitor constants after BASE
    if "COMPETITORS =" not in t:
        insert = '''
# Outbound: real competitor product pages (Svarstjänster AB is independent comparison media)
COMPETITORS = {
    "wecall": ("WeCall", "https://wecall.se/svarstjanst/"),
    "answeronline": ("AnswerOnline", "https://answeronline.se/"),
    "responda": ("Responda", "https://respondagroup.se/svarsservice/"),
    "skaala": ("Skaala", "https://www.skaala.ai/sv/"),
    "telink": ("Telink", "https://telink.se/ai-receptionist/"),
    "telavox": ("Telavox", "https://telavox.se/ai-receptionist/"),
    "lynes": ("Lynes", "https://lynes.io/funktioner/ai-telefonist"),
    "ringup": ("Ringup", "https://www.ringup.se/"),
    "itell": ("iTell", "https://www.itell.nu/tjanster/telefonpassning/"),
    "svardirekt": ("SvarDirekt", "https://www.svardirekt.se/"),
    "bigacom": ("Bigacom", "https://bigacom.se/svarstjanst/"),
    "comunit": ("Comunit", "https://comunit.se/tjanster/svarstjanst"),
    "menodi": ("Menodi", "https://menodi.se/"),
}
CTA_AI = ["skaala", "telink", "telavox", "lynes", "menodi"]
CTA_HUMAN = ["wecall", "answeronline", "responda", "itell", "svardirekt", "bigacom", "ringup"]

'''
        t = t.replace(
            'BASE = "https://svarstjanster.se"\n',
            'BASE = "https://svarstjanster.se"\n' + insert,
        )

    # Replace utm() with competitor_link helpers
    old_utm = '''def utm(c: str) -> str:
    return MENODI.format(c=c)
'''
    new_helpers = '''def ext(url: str) -> str:
    """External competitor link attrs."""
    return f'href="{url}" target="_blank" rel="noopener noreferrer"'


def competitor_href(key: str) -> str:
    return COMPETITORS[key][1]


def competitor_name(key: str) -> str:
    return COMPETITORS[key][0]


def pick_cta(seed: str = "default", kind: str = "ai") -> tuple[str, str]:
    """Deterministic CTA pick from seed so pages stay stable."""
    keys = CTA_AI if kind == "ai" else CTA_HUMAN
    idx = sum(ord(c) for c in seed) % len(keys)
    k = keys[idx]
    return COMPETITORS[k]
'''
    if "def utm(" in t:
        t = t.replace(old_utm, new_helpers)
    elif "def competitor_href" not in t:
        # MENODI already removed; insert helpers before faq_ld
        t = t.replace("def faq_ld(items):", new_helpers + "\ndef faq_ld(items):")

    # Organization JSON-LD: Svarstjänster AB, no Menodi parent
    t = t.replace(
        '''{"@type": "Organization", "@id": BASE + "/#org", "name": "Svarstjänster.se", "url": BASE + "/",
             "parentOrganization": {"@type": "Organization", "name": "Menodi", "url": "https://menodi.se"}},''',
        '''{"@type": "Organization", "@id": BASE + "/#org", "name": "Svarstjänster AB", "url": BASE + "/",
             "legalName": "Svarstjänster AB", "description": "Oberoende jämförelsesajt för svarstjänster och AI-receptionister i Sverige."},''',
    )

    # Nav CTA → leverantörer (internal) + secondary external
    t = t.replace(
        '''<a class="navcta" href="{utm('nav')}" rel="sponsored">Prova AI gratis</a>''',
        '''<a class="navcta" href="/leverantorer/">Se leverantörer</a>''',
    )

    # Footer: remove Menodi column, company disclosure
    old_footer_col = '''<div><h4>Menodi</h4><ul>
<li><a href="{utm('footer')}" rel="sponsored">Prova gratis demo</a></li>
<li><a href="tel:+46844680844">Ring demo 08-446 80 844</a></li>
</ul></div>'''
    new_footer_col = '''<div><h4>Bolag</h4><ul>
<li><a href="/leverantorer/">Alla leverantörer</a></li>
<li><a href="/jamfor/">Jämför modeller</a></li>
<li><a href="/faq/">FAQ</a></li>
</ul></div>'''
    t = t.replace(old_footer_col, new_footer_col)

    t = t.replace(
        '''<div class="wrap fbottom">© {date.today().year} Svarstjänster.se — en del av <a href="{utm('footer')}" rel="sponsored">Menodi</a>. Priser är uppskattningar ({REVIEW}), inte offerter. Begär alltid aktuell prislista hos leverantören.</div>''',
        '''<div class="wrap fbottom">© {date.today().year} <strong>Svarstjänster AB</strong> · Svarstjänster.se är en oberoende jämförelsesajt. Länkar till leverantörer går till deras egna webbplatser. Priser är uppskattningar ({REVIEW}), inte offerter. Begär alltid aktuell prislista hos respektive leverantör. Vi kan få ersättning om du går vidare via vissa länkar — det påverkar inte vår urvalsmetod.</div>''',
    )

    # cta() helper — link to competitor, not Menodi
    old_cta = '''def cta(title, sub, camp, secondary_href="/jamfor/", secondary="Se jämförelsen"):
    return f\'\'\'<section class="wrap"><div class="cta-band">
<h2>{title}</h2>
<p>{sub}</p>
<div class="ctas">
<a class="btn gold" href="{utm(camp)}" rel="sponsored">Prova AI-svarstjänst gratis</a>
<a class="btn ghost" href="{secondary_href}">{secondary}</a>
</div>
</div></section>\'\'\'
'''
    new_cta = '''def cta(title, sub, camp="default", secondary_href="/leverantorer/", secondary="Alla leverantörer", kind="ai"):
    name, url = pick_cta(camp, kind)
    return f\'\'\'<section class="wrap"><div class="cta-band">
<h2>{title}</h2>
<p>{sub}</p>
<div class="ctas">
<a class="btn gold" href="{url}" target="_blank" rel="noopener noreferrer">Besök {name}</a>
<a class="btn ghost" href="{secondary_href}">{secondary}</a>
<a class="btn ghost" href="/jamfor/">Jämför modeller</a>
</div>
<p style="margin-top:14px;font-size:12.5px;color:#c8d4ea;opacity:.9">Extern länk till leverantörens webbplats. Svarstjänster AB är oberoende — inte densamma som leverantören.</p>
</div></section>\'\'\'
'''
    if "def cta(" in t:
        # flexible replace of cta function body
        t = re.sub(
            r"def cta\(title, sub, camp.*?(?=\n\n# ─|\n\nBRANSCHER|\n\ndef )",
            new_cta + "\n",
            t,
            count=1,
            flags=re.S,
        )

    # Text cleanups — independence
    replacements = [
        (
            "Inte Menodi-egendata.",
            "Inte egen plattformsdata från någon leverantör.",
        ),
        (
            "Menodi kopplas via vidarekoppling — behåll numret, prova bokning och svensk röst.",
            "Gå vidare till en leverantörs webbplats för demo — jämför gärna flera innan du bestämmer dig.",
        ),
        (
            '<a class="btn ghost" href="{utm(\'hero\')}" rel="sponsored">Prova Menodi</a>',
            '<a class="btn ghost" href="/leverantorer/">Se leverantörer</a>',
        ),
        (
            "Ingen betald placering. Menodi kan lyftas som exempel på AI-fastpris eftersom sajten är en del av Menodi — se disclosure i sidfoten.",
            "Ingen köpt topplista. Exempelpriser är marknadsintervall; kolla alltid leverantörens egna sidor. Disclosure i sidfoten.",
        ),
        (
            "Exempel: Menodi från ca 795 kr/mån. Andra är offertbaserade.",
            "AI-abonnemang kan börja runt ca 800–2 000 kr/mån hos vissa aktörer; andra är offertbaserade.",
        ),
        (
            "Exempel Menodi från ca 795 kr/mån.",
            "Vissa AI-aktörer annonserar från ca 800–2 000 kr/mån.",
        ),
        (
            '<a class="btn" href="{utm(\'ai-receptionist\')}" rel="sponsored">Testa AI-receptionist</a>',
            f'<a class="btn" href="{COMPETITORS["skaala"][1]}" target="_blank" rel="noopener noreferrer">Exempel: Skaala</a>',
        ),
        (
            "Exempel Menodi från ca 795 kr/mån. Kolla gränser",
            "Vissa AI-abonnemang från ca 800 kr/mån (marknadsnivå). Kolla gränser",
        ),
        (
            '<a class="btn ghost" href="{utm(\'ai-telefonist\')}" rel="sponsored">Lyssna på demo</a>',
            f'<a class="btn ghost" href="{COMPETITORS["lynes"][1]}" target="_blank" rel="noopener noreferrer">Exempel: Lynes</a>',
        ),
        (
            "t.ex. Menodi, Skaala, Telink",
            "t.ex. Skaala, Telink, Menodi",
        ),
        (
            "Katalog över leverantörer: Menodi, Skaala, Telink, Telavox, Lynes, WeCall, Responda, AnswerOnline m.fl.",
            "Katalog över leverantörer: Skaala, Telink, Telavox, Lynes, Menodi, WeCall, Responda, AnswerOnline m.fl.",
        ),
        (
            "<tr><td class=\"hl\"><strong>AI-svarstjänst (t.ex. Menodi)</strong></td>",
            "<tr><td class=\"hl\"><strong>AI-svarstjänst (kategori)</strong></td>",
        ),
        (
            "AI-fastpris kan börja runt 795 kr/mån (exempel Menodi).",
            "AI-fastpris kan börja runt ca 800–2 000 kr/mån beroende på leverantör.",
        ),
        (
            '''<a class="btn" href="{utm('bransch-'+slug)}" rel="sponsored">Testa AI för {keyword}</a>''',
            '''<a class="btn" href="/leverantorer/">Jämför leverantörer</a>''',
        ),
        (
            '''<a class="btn" href="{utm('city-'+slug)}" rel="sponsored">Demo för bolag i {name}</a>''',
            '''<a class="btn" href="/leverantorer/">Se leverantörer</a>''',
        ),
        (
            "Menodi är ett AI-first alternativ med fast prismodell — men bemannade aktörer kan vara rätt vid komplexa samtal.",
            "AI-first-aktörer (t.ex. Skaala, Telink, Menodi) och bemannade aktörer (t.ex. WeCall, Responda) fyller olika behov — testa demosamtal hos minst två.",
        ),
        (
            "Samma kategori som Menodi",
            "AI-first-kategori",
        ),
        (
            "# Parent: Menodi (menodi.se).",
            "# Operated by Svarstjänster AB. Outbound links go to third-party vendor sites.",
        ),
        (
            "Exempel: Menodi från ca 795 kr/mån. Offertbaserade AI",
            "AI-abonnemang kan ligga från ca 800 kr/mån hos vissa; offertbaserade AI",
        ),
    ]
    for a, b in replacements:
        t = t.replace(a, b)

    # LEVERANTORER table: Menodi stays as one row but not special — already fine
    # Fix any remaining utm( or rel="sponsored" menodi
    t = re.sub(r'rel="sponsored"', 'rel="noopener noreferrer"', t)
    # leftover utm( calls → competitor or internal
    t = re.sub(
        r'href="\{utm\([^)]+\)\}"',
        'href="/leverantorer/"',
        t,
    )

    # cta titles that still say Prova Menodi / Menodi demo
    t = t.replace("Prova Menodi", "Se en leverantör")
    t = t.replace("Menodi demo", "Leverantörsdemo")
    t = t.replace("Starta demo", "Jämför leverantörer")
    t = t.replace("Testa Menodi", "Besök leverantör")

    SRC.write_text(t, encoding="utf-8")
    print("patched rebuild_rich_v2.py")
    # leftover checks
    left = []
    for pat in ["utm(", "rel=\"sponsored\"", "en del av", "MENODI =", "Prova Menodi", "parentOrganization"]:
        if pat in t:
            left.append(pat)
    print("leftover_patterns", left)


def scrub_html_files():
    """Post-pass on any HTML not fully regenerated."""
    n = 0
    for p in ROOT.rglob("index.html"):
        html = p.read_text(encoding="utf-8")
        orig = html
        html = html.replace("en del av Menodi", "Svarstjänster AB")
        html = html.replace("en del av <a", "driven av Svarstjänster AB · <a")
        html = re.sub(
            r'https://menodi\.se/\?utm_source=svarstjanster[^"\']*',
            "https://menodi.se/",
            html,
        )
        html = html.replace('rel="sponsored"', 'rel="noopener noreferrer"')
        # nav CTA text
        html = html.replace(">Prova AI gratis</a>", ">Se leverantörer</a>")
        html = html.replace('href="https://menodi.se/" rel="noopener noreferrer">Prova', 'href="/leverantorer/">Se')
        if html != orig:
            p.write_text(html, encoding="utf-8")
            n += 1
    print("scrubbed_html", n)


if __name__ == "__main__":
    patch_generator()
