#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full-site UI + rich content rebuild for svarstjanster.se.
Upgraded design tokens (DESIGN.md gold), denser components, unique prose per page type.
"""
from __future__ import annotations
import json, re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent
TODAY = date.today().isoformat()
REVIEW = "augusti 2026"
BASE = "https://svarstjanster.se"

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


CSS = r"""
:root{
  --bg:#f7f1e6;--card:#fffcf7;--paper:#fffcf7;
  --ink:#141b2a;--ink2:#4a5568;
  --navy:#1a3358;--navy2:#254a7a;
  --gold:#6e5218;--gold-bright:#b8891f;--gold-soft:rgba(110,82,24,.12);
  --line:#e2d8c4;
  --radius:16px;--radius-lg:22px;
  --shadow:0 1px 2px rgba(20,27,42,.05),0 10px 28px -10px rgba(20,27,42,.12);
  --shadow-lg:0 8px 16px rgba(20,27,42,.05),0 24px 48px -16px rgba(20,27,42,.16);
  --space:clamp(72px,9vw,112px);
  --prose:68ch;
  --font:"DM Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --font-display:"Fraunces","DM Sans",Georgia,serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:92px}
body{font-family:var(--font);background:var(--bg);color:var(--ink);line-height:1.7;font-size:17px;-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:
    radial-gradient(900px 420px at 12% -10%, rgba(196,154,46,.14), transparent 55%),
    radial-gradient(700px 380px at 100% 0%, rgba(26,51,88,.08), transparent 50%)}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
.prose{max-width:var(--prose)}
a{color:inherit}
img,svg{display:block}
:focus-visible{outline:2px solid var(--navy);outline-offset:2px;border-radius:4px}

/* header */
header{position:sticky;top:0;z-index:50;background:rgba(247,241,230,.92);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.nav{display:flex;justify-content:space-between;align-items:center;padding:14px 0;gap:14px}
.logo{font-family:var(--font-display);font-weight:700;font-size:1.2rem;color:var(--navy);text-decoration:none;letter-spacing:-.02em;white-space:nowrap}
.logo span{color:var(--gold)}
.navlinks{display:flex;align-items:center;gap:4px 14px;font-size:13.5px;flex-wrap:wrap;justify-content:flex-end}
.navlinks a.anchor{color:var(--ink2);text-decoration:none;font-weight:650;padding:7px 2px;border-bottom:2px solid transparent}
.navlinks a.anchor:hover{color:var(--navy)}
.navlinks a.anchor.active{color:var(--navy);border-bottom-color:var(--gold-bright)}
.navcta{background:var(--navy);color:#fff!important;padding:11px 18px;border-radius:999px;text-decoration:none;font-weight:700;font-size:13px;box-shadow:0 2px 12px rgba(26,51,88,.18)}
.navcta:hover{background:var(--navy2)}
.hamburger-btn{display:none;background:var(--card);border:1.5px solid var(--line);border-radius:12px;width:44px;height:44px;align-items:center;justify-content:center;cursor:pointer;color:var(--navy);flex-shrink:0}
.mobile-nav{display:none;flex-direction:column;border-top:1px solid var(--line);background:rgba(255,252,247,.98);padding-bottom:8px}
.mobile-nav.open{display:flex}
.mobile-nav a{padding:15px 22px;font-weight:650;color:var(--ink2);text-decoration:none;border-bottom:1px solid var(--line)}
.mobile-nav a:hover{color:var(--navy);background:var(--gold-soft)}
@media(max-width:960px){.navlinks a.anchor{display:none}.hamburger-btn{display:flex}}

/* hero */
.hero{padding:clamp(36px,5.5vw,68px) 0 clamp(28px,4vw,48px);position:relative}
.hero-grid{display:grid;grid-template-columns:1.2fr .9fr;gap:36px;align-items:stretch}
@media(max-width:860px){.hero-grid{grid-template-columns:1fr;gap:24px}}
.breadcrumb{font-size:13px;color:var(--ink2);margin-bottom:14px;font-weight:600}
.breadcrumb a{color:var(--ink2);text-decoration:none}
.breadcrumb a:hover{color:var(--navy)}
.kicker{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:750;letter-spacing:.06em;text-transform:uppercase;color:var(--gold);margin-bottom:14px}
.kicker::before{content:"";width:22px;height:2px;background:var(--gold-bright);border-radius:2px}
h1{font-family:var(--font-display);font-size:clamp(2rem,5vw,3.15rem);line-height:1.08;letter-spacing:-.03em;color:var(--navy);font-weight:650}
.lede{margin-top:18px;font-size:1.125rem;color:var(--ink2);max-width:38rem;line-height:1.65}
.answer-box{margin-top:26px;background:var(--card);border:1px solid var(--line);border-left:5px solid var(--gold-bright);border-radius:16px;padding:20px 22px;max-width:42rem;box-shadow:var(--shadow)}
.answer-box .lbl{display:block;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:8px}
.answer-box{font-size:1rem;color:var(--ink)}
.answer-box strong{color:var(--navy)}
.meta-line{margin-top:16px;font-size:12.5px;color:var(--ink2);line-height:1.5}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.chip{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;font-weight:650;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 13px;box-shadow:0 1px 0 rgba(20,27,42,.03)}
.chip i{width:7px;height:7px;border-radius:50%;background:var(--gold-bright);display:inline-block;flex-shrink:0}
.ctas{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap;align-items:center}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--navy);color:#fff;padding:14px 26px;border-radius:999px;text-decoration:none;font-weight:700;font-size:15px;box-shadow:0 4px 16px rgba(26,51,88,.18);transition:transform .15s,background .15s,box-shadow .15s}
.btn:hover{background:var(--navy2);transform:translateY(-1px);box-shadow:0 8px 22px rgba(26,51,88,.2)}
.btn.ghost{background:transparent;color:var(--navy);border:1.5px solid var(--navy);box-shadow:none}
.btn.ghost:hover{background:var(--navy);color:#fff}
.btn.gold{background:var(--gold-bright);color:#141b2a}
.btn.gold:hover{filter:brightness(1.04);background:var(--gold-bright)}

.facts-card{background:linear-gradient(165deg,#fff 0%,#fbf6eb 100%);border:1px solid var(--line);border-radius:var(--radius-lg);padding:24px;box-shadow:var(--shadow);height:100%}
.facts-card .eyebrow,.f-label{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--gold);margin-bottom:16px;font-weight:800}
.facts-card dl{display:grid;gap:14px}
.facts-card dt{font-size:12px;color:var(--ink2);font-weight:650;margin-bottom:2px}
.facts-card dd{font-size:1rem;color:var(--navy);font-weight:750;margin:0;font-family:var(--font-display)}

/* sections */
section.block{padding:var(--space) 0}
section.block.alt{background:rgba(255,252,247,.72);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
h2{font-family:var(--font-display);font-size:clamp(1.45rem,3vw,1.9rem);color:var(--navy);letter-spacing:-.02em;margin-bottom:12px;font-weight:650}
h2::before{content:"";display:block;width:48px;height:3px;background:linear-gradient(90deg,var(--gold-bright),rgba(196,154,46,.15));border-radius:2px;margin-bottom:16px}
.sub{color:var(--ink2);margin-bottom:28px;max-width:40rem;font-size:1.05rem}
.p{color:var(--ink2);margin-bottom:14px;max-width:var(--prose);font-size:1rem}
.p:last-child{margin-bottom:0}
h3.inline{font-size:1.15rem;color:var(--navy);margin:22px 0 8px;font-weight:750;font-family:var(--font-display)}

.toc{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0;padding:12px 14px;background:rgba(255,252,247,.8);border:1px solid var(--line);border-radius:14px}
.toc a{font-size:13px;font-weight:650;color:var(--navy);text-decoration:none;padding:7px 12px;border-radius:999px;background:var(--card);border:1px solid var(--line)}
.toc a:hover{border-color:var(--gold-bright);background:var(--gold-soft)}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:26px;transition:box-shadow .2s,transform .2s;box-shadow:0 1px 0 rgba(20,27,42,.03)}
.card:hover{box-shadow:var(--shadow);transform:translateY(-3px)}
.card .icowrap{width:48px;height:48px;border-radius:14px;background:var(--gold-soft);display:flex;align-items:center;justify-content:center;margin-bottom:16px;font-size:22px;border:1px solid rgba(143,106,31,.12)}
.card h3{font-size:1.1rem;color:var(--navy);margin-bottom:8px;font-weight:700;font-family:var(--font-display)}
.card p,.card li{font-size:.95rem;color:var(--ink2);line-height:1.65}
.card a.more{display:inline-flex;align-items:center;gap:4px;margin-top:16px;font-weight:750;color:var(--navy);text-decoration:none;font-size:.95rem}
.card a.more:hover{color:var(--gold)}
.tag{display:inline-block;font-size:11px;font-weight:800;color:#5c4414;border:1px solid rgba(110,82,24,.4);border-radius:99px;padding:4px 11px;margin-bottom:12px;text-transform:uppercase;letter-spacing:.45px;background:#efe0b8}

.pain-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:8px}
@media(max-width:720px){.pain-strip{grid-template-columns:1fr}}
.pain{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;box-shadow:0 1px 0 rgba(20,27,42,.03)}
.pain strong{display:block;color:var(--navy);font-size:.95rem;margin-bottom:6px;font-family:var(--font-display)}
.pain span{font-size:.9rem;color:var(--ink2)}

.tbl{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse;min-width:640px}
th,td{text-align:left;padding:15px 16px;border-bottom:1px solid var(--line);font-size:.95rem;vertical-align:top}
th{background:#efe4cb;color:var(--navy);font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;font-weight:800}
tr:last-child td{border-bottom:none}
tbody tr:nth-child(even) td{background:rgba(247,241,230,.45)}
td.hl,th.hl{background:rgba(196,154,46,.14)!important}
.note{font-size:12.5px;color:var(--ink2);margin-top:12px}

.checklist{list-style:none}
.checklist li{padding:11px 0 11px 30px;position:relative;color:var(--ink2);font-size:1rem;border-bottom:1px solid var(--line)}
.checklist li::before{content:"✓";position:absolute;left:0;color:var(--gold);font-weight:800}
.checklist li:last-child{border-bottom:none}

details{background:var(--card);border:1px solid var(--line);border-radius:14px;margin-bottom:10px;padding:16px 20px;box-shadow:0 1px 0 rgba(20,27,42,.03)}
details[open]{box-shadow:var(--shadow)}
summary{cursor:pointer;font-weight:750;color:var(--navy);list-style:none;font-size:1rem;display:flex;justify-content:space-between;gap:12px;align-items:center}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-size:22px;color:var(--gold);font-weight:400;flex-shrink:0;line-height:1}
details[open] summary::after{content:"–"}
details p{margin-top:12px;color:var(--ink2);font-size:.98rem}

.stats{background:linear-gradient(145deg,var(--navy),#16304f 55%,#2a4d78);border-radius:var(--radius-lg);padding:52px 32px;text-align:center;color:#fff;box-shadow:var(--shadow-lg);position:relative;overflow:hidden}
.stats::after{content:"";position:absolute;inset:auto -20% -40% auto;width:280px;height:280px;background:radial-gradient(circle,rgba(196,154,46,.25),transparent 65%);pointer-events:none}
.stats .big{font-family:var(--font-display);font-size:clamp(3rem,8vw,4.5rem);font-weight:700;letter-spacing:-.03em;color:var(--gold-bright);line-height:1}
.stats h2{color:#fff;margin:14px 0 10px;font-family:var(--font-display)}.stats h2::before{display:none}
.stats p{color:#d5dfef;max-width:560px;margin:0 auto;font-size:1.05rem}
.stats .src{margin-top:18px;font-size:12px;color:#9aadc8}

.cta-band{background:linear-gradient(135deg,var(--navy) 0%,#1e3f6a 55%,#2c5588 100%);border-radius:var(--radius-lg);padding:clamp(40px,6vw,60px) 28px;color:#fff;text-align:center;margin:28px 0 52px;box-shadow:var(--shadow-lg)}
.cta-band h2{color:#fff;margin:0 0 12px;font-family:var(--font-display)}.cta-band h2::before{display:none}
.cta-band p{color:#d5dfef;max-width:520px;margin:0 auto 24px;font-size:1.05rem}
.cta-band .ctas{justify-content:center}
.cta-band .btn.ghost{border-color:rgba(255,255,255,.55);color:#fff}
.cta-band .btn.ghost:hover{background:#fff;color:var(--navy)}

footer{border-top:1px solid var(--line);padding:56px 0 40px;color:var(--ink2);font-size:.95rem;background:var(--card)}
.fgrid{display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:28px;margin-bottom:32px}
@media(max-width:860px){.fgrid{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.fgrid{grid-template-columns:1fr}}
.f-label,.fgrid .f-label{color:var(--navy);font-size:11.5px;text-transform:uppercase;letter-spacing:.55px;margin-bottom:12px;font-weight:800}
.fgrid ul{list-style:none}
.fgrid li{margin-bottom:8px}
.fgrid a{text-decoration:none;color:var(--ink2)}
.fgrid a:hover{color:var(--navy)}
.fbottom{border-top:1px solid var(--line);padding-top:18px;font-size:12.5px;line-height:1.55}

.related-wrap{margin-top:8px}
.related-wrap .rel-title{font-size:.95rem;color:var(--navy);margin-bottom:12px;font-weight:750;font-family:var(--font-display)}
.related{display:flex;flex-wrap:wrap;gap:10px}
.related a{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:10px 16px;text-decoration:none;font-size:.9rem;font-weight:650;color:var(--navy);box-shadow:0 1px 0 rgba(20,27,42,.03)}
.related a:hover{border-color:var(--gold-bright);background:var(--gold-soft)}

.steps{counter-reset:s;display:grid;gap:20px}
.step{padding-left:56px;position:relative}
.step::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:0;width:40px;height:40px;border-radius:12px;background:var(--navy);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:15px;box-shadow:0 4px 12px rgba(26,51,88,.18)}
.step h3{font-size:1.05rem;color:var(--navy);margin-bottom:5px;font-weight:750;font-family:var(--font-display)}
.step p{font-size:.98rem;color:var(--ink2)}

.two-col{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:700px){.two-col{grid-template-columns:1fr}}

.enrich .p,.enrich2 .p{max-width:48rem}

@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
}
"""


def ext(url: str) -> str:
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


def faq_ld(items):
    ent = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}, ensure_ascii=False)


def breadcrumb_ld(crumbs):
    els = [{"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(crumbs, 1)]
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": els}, ensure_ascii=False)


def org_ld():
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": "Svarstjänster.se", "url": BASE + "/",
             "description": "Oberoende jämförelse av AI-receptionister, AI-telefonister och svarstjänster i Sverige.",
             "inLanguage": "sv-SE", "publisher": {"@id": BASE + "/#org"}},
            {"@type": "Organization", "@id": BASE + "/#org", "name": "Svarstjänster AB", "url": BASE + "/",
             "legalName": "Svarstjänster AB", "description": "Oberoende jämförelsesajt för svarstjänster och AI-receptionister i Sverige."},
        ],
    }, ensure_ascii=False)


def nav_html(active=""):
    links = [
        ("/", "Hem", "hem"),
        ("/jamfor/", "Jämför", "jamfor"),
        ("/ai-receptionist/", "AI-receptionist", "ai-rec"),
        ("/ai-telefonist/", "AI-telefonist", "ai-tel"),
        ("/branscher/", "Branscher", "bran"),
        ("/leverantorer/", "Leverantörer", "lev"),
        ("/svarstjanst-pris/", "Pris", "pris"),
        ("/guider/", "Guider", "guider"),
    ]
    anch = "".join(
        f'<a class="anchor{" active" if active==k else ""}" href="{h}">{l}</a>' for h, l, k in links
    )
    mobile = "\n".join(f'<a href="{h}">{l}</a>' for h, l, _ in links)
    mobile += '\n<a href="/faq/">FAQ</a>\n<a href="/alternativ/">Alternativ</a>'
    return f'''<header>
<div class="wrap nav">
<a class="logo" href="/">Svar<span>tjänster</span>.se</a>
<div class="navlinks">
{anch}
<a class="navcta" href="/leverantorer/">Se leverantörer</a>
<button class="hamburger-btn" id="menuToggle" aria-label="Öppna meny" aria-expanded="false" aria-controls="mobileNav">
<svg class="hamburger-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
<svg class="hamburger-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
</button>
</div>
</div>
<nav class="mobile-nav" id="mobileNav" aria-label="Mobilmeny">{mobile}</nav>
</header>'''


def footer_html():
    return f'''<footer>
<div class="wrap fgrid">
<div>
<a class="logo" href="/">Svar<span>tjänster</span>.se</a>
<p style="margin-top:14px;max-width:300px;line-height:1.6">Oberoende jämförelse av AI-receptionister, AI-telefonister och svarstjänster i Sverige. Metodik och prisintervall uppdaterade {REVIEW}.</p>
</div>
<div><p class="f-label">Kategorier</p><ul>
<li><a href="/ai-receptionist/">AI-receptionist</a></li>
<li><a href="/ai-telefonist/">AI-telefonist</a></li>
<li><a href="/svarsservice/">Svarsservice</a></li>
<li><a href="/telefonpassning/">Telefonpassning</a></li>
<li><a href="/callcenter/">Callcenter</a></li>
</ul></div>
<div><p class="f-label">Jämför</p><ul>
<li><a href="/jamfor/">Jämför svarstjänster</a></li>
<li><a href="/ai-vs-bemannad/">AI vs bemannad</a></li>
<li><a href="/leverantorer/">Leverantörer</a></li>
<li><a href="/alternativ/">Alternativ till…</a></li>
<li><a href="/svarstjanst-pris/">Prisguide</a></li>
</ul></div>
<div><p class="f-label">Utforska</p><ul>
<li><a href="/branscher/">Branscher</a></li>
<li><a href="/guider/">Guider</a></li>
<li><a href="/faq/">FAQ</a></li>
<li><a href="/basta-svarstjansten-2026/">Bästa 2026</a></li>
<li><a href="/llms.txt">llms.txt</a></li>
</ul></div>
<div><p class="f-label">Bolag</p><ul>
<li><a href="/leverantorer/">Alla leverantörer</a></li>
<li><a href="/jamfor/">Jämför modeller</a></li>
<li><a href="/faq/">FAQ</a></li>
</ul></div>
</div>
<div class="wrap fbottom">© {date.today().year} <strong>Svarstjänster AB</strong> · Svarstjänster.se är en oberoende jämförelsesajt. Länkar till leverantörer går till deras egna webbplatser. Priser är uppskattningar ({REVIEW}), inte offerter. Begär alltid aktuell prislista hos respektive leverantör. Vi kan få ersättning om du går vidare via vissa länkar — det påverkar inte vår urvalsmetod.</div>
</footer>
<script>
(function(){{var b=document.getElementById('menuToggle'),n=document.getElementById('mobileNav');
if(b&&n){{b.addEventListener('click',function(){{n.classList.toggle('open');b.setAttribute('aria-expanded',n.classList.contains('open'));}});}}}})();
</script>'''


def page(title, desc, canonical, body, active="", extra_ld=None, crumbs=None):
    lds = [org_ld()]
    if crumbs:
        lds.append(breadcrumb_ld(crumbs))
    if extra_ld:
        lds.extend(extra_ld)
    scripts = "\n".join(f'<script type="application/ld+json">{s}</script>' for s in lds)
    return f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="sv_SE">
<meta name="twitter:card" content="summary">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:opsz,wght@9..144,500;9..144,650;9..144,700&display=swap" rel="stylesheet">
{scripts}
<style>{CSS}</style>
<link rel="stylesheet" href="/sub-enhancements.css">
</head>
<body>
<div class="progress-bar" aria-hidden="true"></div>
{nav_html(active)}
<main>
{body}
</main>
{footer_html()}
<button type="button" class="back-to-top" aria-label="Till toppen"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
<script src="/sub-enhancements.js" defer></script>
</body>
</html>
'''


def write(rel, html):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    print("wrote", rel)


def related(links):
    items = "".join(f'<a href="{h}">{t}</a>' for h, t in links)
    return f'<div class="related-wrap"><p class="rel-title">Läs vidare</p><div class="related">{items}</div></div>'


def faq_html(items):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


def chips(items):
    return '<div class="chips">' + "".join(f'<span class="chip"><i></i>{t}</span>' for t in items) + "</div>"


def cta(title, sub, camp="default", secondary_href="/leverantorer/", secondary="Alla leverantörer", kind="ai"):
    name, url = pick_cta(camp, kind)
    return f'''<section class="wrap"><div class="cta-band">
<h2>{title}</h2>
<p>{sub}</p>
<div class="ctas">
<a class="btn gold" href="{url}" target="_blank" rel="noopener noreferrer">Besök {name}</a>
<a class="btn ghost" href="{secondary_href}">{secondary}</a>
<a class="btn ghost" href="/jamfor/">Jämför modeller</a>
</div>
<p style="margin-top:14px;font-size:12.5px;color:#c8d4ea;opacity:.9">Extern länk till leverantörens webbplats. Svarstjänster AB är oberoende — inte densamma som leverantören.</p>
</div></section>'''



# ─── DATA ───────────────────────────────────────────────────────────

BRANSCHER = [
    ("tandlakare", "tandläkare", "Tandläkare & klinik",
     "Bokningar, avbokningar och jourfrågor — varje tom stol är dyr.",
     ["Boka/omboka utan att störa behandling", "Svara efter stängning", "Triage innan uppringning", "SMS mot no-show"],
     "Letar du efter en AI-receptionist för din tandläkarklinik?",
     "Patienter ringer när ni har händer i munnen. AI tar admin, eskalerar smärta enligt er policy — utan diagnos.",
     "No-show, kvällsbokning och 'har ni tid i veckan?' dominerar volymen."),
    ("frisor", "frisör", "Frisör & salong",
     "Drop-in och ombokning medan du klipper.",
     ["Boka med kund i stolen", "SMS vid no-show-risk", "Öppettider/prisnivå", "Kvällsförfrågningar"],
     "Letar du efter en AI-receptionist för din frisörsalong?",
     "Telefonen ringer mitt i färgning. AI fångar bokningar utan att avbryta.",
     "Många salonger tappar kvälls-SMS-trafik till större kedjor."),
    ("maklare", "mäklare", "Mäklare & bostad",
     "Spekulant-samtal kväll/helg.",
     ["Kvalificera område/budget", "Boka visning", "Eskalera brådskande", "Lead-sammanfattning"],
     "Letar du efter en AI-receptionist för ditt mäklarkontor?",
     "Intresse toppar utanför kontorstid. AI tar första filtreringen.",
     "Missat samtal = spekulant till nästa annons."),
    ("bilverkstad", "bilverkstad", "Bilverkstad",
     "Drop-off och status medan lyften är full.",
     ["Drop-off-bokning", "Status/klar bil", "Jour-triage", "Offert utan att störa mekaniker"],
     "Letar du efter en AI-telefonist för bilverkstaden?",
     "Golvet hinner sällan telefonen. AI tar rutin och ringer vidare vid akut.",
     "Kunder vill veta 'är bilen klar?' — det kan AI svara på med era regler."),
    ("advokat", "advokat", "Advokatbyrå",
     "Förtroende + triage, inte rådgivning i luren.",
     ["Ta ärende-intresse", "Boka konsultation", "Filtrera sälj", "Eskalera brådskande"],
     "Letar du efter en AI-receptionist för advokatbyrån?",
     "AI tar admin och bokning; juridisk rådgivning eskaleras alltid.",
     "Konfidentialitet och tydliga gränser i prompten är kritiska."),
    ("redovisning", "redovisningsbyrå", "Redovisningsbyrå",
     "Säsongstoppar och dokumentfrågor.",
     ["Boka avstämning", "Öppettider/inlämning", "Samla underlagsfrågor", "Koppla rätt rådgivare"],
     "Letar du efter en AI-receptionist för redovisningsbyrån?",
     "Deklarationsperioder drunknar i samtal. AI avlastar rutin.",
     "Kunder vill veta deadlines — håll policy uppdaterad."),
    ("vardcentral", "vårdcentral", "Vård & mottagning",
     "Tidsbokning och vägledning — inte diagnostik.",
     ["Boka/omboka enligt regler", "Hänvisa akut till 1177/112", "Öppettider", "Minska telefonkö admin"],
     "Letar du efter en AI-telefonist för mottagningen?",
     "Admin-samtal fyller kön. AI tar det som inte är medicinsk bedömning.",
     "Akutpolicy måste vara vattentät i prompten."),
    ("restaurang", "restaurang", "Restaurang",
     "Bord, allergi, takeaway mitt i service.",
     ["Boka bord", "Öppettider/meny-nivå", "Avbokning", "Eskalera stora sällskap"],
     "Letar du efter en AI-receptionist för restaurangen?",
     "Service och telefon krockar. AI tar bokning utan att störa salen.",
     "Helger och drop-in skapar toppar AI klarar parallellt."),
    ("elektriker", "elektriker", "Elektriker",
     "Akut fel vs offert ute på jobb.",
     ["Triage akut/planerat", "Boka platsbesök", "Områdesfilter", "Kväll/helg"],
     "Letar du efter en AI-telefonist för el-firman?",
     "Du är i taket när kunden ringer. AI tar leaden.",
     "Jour måste ha tydlig eskalering till jourtelefon."),
    ("vvs", "VVS", "VVS & rör",
     "Läcka väntar inte — men de flesta samtal är offert.",
     ["Akut vs service", "Boka jourfönster", "Område", "SMS ankomst"],
     "Letar du efter en AI-telefonist för VVS-firman?",
     "AI skiljer akut läcka från 'vill ha offert badrum'.",
     "Snabb triage sparar dyra felkörningar."),
    ("stad", "städfirma", "Städfirma",
     "Återkommande tider och offert i fält.",
     ["Boka återkommande", "Offert yta/typ", "Ombokning", "Efter kontorstid"],
     "Letar du efter en AI-receptionist för städfirman?",
     "Personal är ute — AI tar bokning och ombokning.",
     "Återkommande schema kräver tydliga regler."),
    ("ehandel", "e-handel", "E-handel",
     "Orderstatus och retur utan callcenter.",
     ["Orderstatus-triage", "Retur/policy", "Eskalera arg kund", "Avlasta chatt"],
     "Letar du efter en AI-telefonist för e-handeln?",
     "Telefon blir dyrt i peak. AI tar WISMO-rutin.",
     "Integration till orderdata är plus — annars policy-svar."),
    ("hotell", "hotell", "Hotell & boende",
     "Late check-in och 24/7-förväntan.",
     ["Boka/ändra rum", "Late arrival", "Faciliteter", "Natt-eskalering"],
     "Letar du efter en AI-receptionist för hotellet?",
     "Gäster ringer dygnet runt. AI tar det receptionen hinner inte.",
     "Nattpersonal kan eskaleras vid undantag."),
    ("psykolog", "psykolog", "Psykolog & terapi",
     "Diskret bokning och väntelista.",
     ["Boka intag", "Väntelista", "Ingen terapi i telefon", "SMS-påminnelse"],
     "Letar du efter en AI-receptionist för mottagningen?",
     "AI sköter admin med respektfull ton; terapi eskaleras aldrig till AI.",
     "Diskretion och tydliga gränser i prompten."),
    ("bygg", "byggföretag", "Bygg & hantverk",
     "Offerter när ni är på bygget.",
     ["Kvalificera projekttyp", "Boka platsbesök", "Område", "Efter arbetstid"],
     "Letar du efter en AI-telefonist för byggfirman?",
     "Byggbuller och fältjobb — AI tar offertleads.",
     "Säsong och ROT skapar toppar."),
    ("fastighet", "fastighetsbolag", "Fastighet",
     "Felanmälan och hyresgästfrågor.",
     ["Felanmälan-triage", "Boka besiktning", "Akut vatten/el", "Ärendesammanfattning"],
     "Letar du efter en AI-telefonist för fastighetsbolaget?",
     "Volym av felanmälningar utan att tappa akut.",
     "Tydlig prioritering sparar jourkostnad."),
    ("hantverkare", "hantverkare", "Hantverkare generellt",
     "Enmansbolag och fältjobb missar samtal.",
     ["Offertförfrågan", "Boka besiktning", "Jour-triage", "Efter arbetstid"],
     "Letar du efter en AI-telefonist som hantverkare?",
     "Varje missat samtal kan vara ett jobb. AI svarar medan du skruv.",
     "Störst ROI när du jobbar ensam ute."),
]

CITIES = [
    ("stockholm", "Stockholm"), ("goteborg", "Göteborg"), ("malmo", "Malmö"),
    ("uppsala", "Uppsala"), ("linkoping", "Linköping"), ("orebro", "Örebro"),
    ("vasteras", "Västerås"), ("helsingborg", "Helsingborg"), ("jonkoping", "Jönköping"),
    ("norrkoping", "Norrköping"), ("umea", "Umeå"), ("lulea", "Luleå"),
    ("karlstad", "Karlstad"), ("vaxjo", "Växjö"), ("sundsvall", "Sundsvall"),
    ("gavle", "Gävle"), ("boras", "Borås"), ("halmstad", "Halmstad"),
]

ALTERNATIV = [
    ("responda", "Responda", "Traditionell/hybrid svarsservice i större skala.",
     ["Etablerad bemannad modell", "Process och volym", "Ofta offert"],
     ["Vill ha fast AI-pris", "Behöver inbyggd kalenderbokning", "Vill starta via vidarekoppling"]),
    ("wecall", "WeCall", "Bemannad svarstjänst med personlig touch.",
     ["Mänskliga agenter", "Komplexa ärenden", "Känd i SE"],
     ["Behöver 24/7 utan skiftkostnad", "Många enkla bokningar", "Obegränsade samtidiga samtal"]),
    ("answeronline", "AnswerOnline", "Extern kundtjänst och svarstjänster.",
     ["Bred tjänstemix", "Mer än bara telefon", "Etablerad"],
     ["Ren AI-first", "Transparent fast månadspris", "Djup kalenderintegration"]),
    ("ringup", "Ringup", "Klassisk svarsservice/telefonpassning.",
     ["Bemannad passning", "Meddelanden", "Känd synonym-sök"],
     ["Vill ersätta meddelande med bokning", "AI-röst svenska", "Låg volym + kväll"]),
    ("skaala", "Skaala", "AI-svarsservice / AI-receptionist.",
     ["AI-first", "Fast pristänk", "AI-first-kategori"],
     ["Jämför bokning/språk/data", "Kolla integrationer", "Branschdemo"]),
    ("telink", "Telink", "AI-receptionist + växel-nära SEO.",
     ["Synlig på AI receptionist", "Teknikvinkel", "Många landningssidor"],
     ["Vill oberoende jämförelse", "Undvik ren sälj-landing", "Branschsetup"]),
    ("telavox", "Telavox", "Företagstelefoni med AI-moduler.",
     ["Stark telefoniplattform", "AI som tillägg", "Bra om ni redan är kund"],
     ["Vill fristående AI", "Bara svarstjänst", "Jämför TCO"]),
    ("lynes", "Lynes", "Molnväxel med AI-telefonist.",
     ["Växel + AI", "Svensk aktör", "Hel plattform"],
     ["Bara svarstjänst", "Vill inte byta telefoni", "Jämför AI-kvalitet separat"]),
    ("comunit", "Comunit", "Bemannad svarstjänst-aktör.",
     ["Bemannad modell", "Företagsfokus"],
     ["AI 24/7", "Fast pris utan per-samtal"]),
    ("bigacom", "Bigacom", "Svarstjänst med 24/7-profil.",
     ["Tillgänglighet", "Bemannad"],
     ["Kalenderbokning inbyggd", "AI-first kostnad"]),
    ("svardirekt", "SvarDirekt", "Personlig svarsservice, lång historik.",
     ["Personlig touch", "Etablerad"],
     ["AI-skala", "Transparent abonnemang"]),
    ("itell", "iTell", "Svarstjänst / telefonpassning / kundtjänst.",
     ["Synlig på head-termer", "Bred tjänst"],
     ["Jämför AI-fastpris", "Branschdemo"]),
]

# name, type, price model, availability, booking, geo, note, external_url
LEVERANTORER = [
    ("Skaala", "AI-svarsservice", "Offert/fast (kolla live)", "24/7 AI", "Varierar", "Sverige", "AI-first i SE-SERP.", "https://www.skaala.ai/sv/"),
    ("Telink", "AI-receptionist", "Offert", "24/7", "Varierar", "Sverige", "Stark SEO på AI-receptionist.", "https://telink.se/ai-receptionist/"),
    ("Telavox", "Telefoni + AI", "Abonnemang+moduler", "Beror", "Via plattform", "Sverige", "Bra om ni redan är Telavox-kund.", "https://telavox.se/ai-receptionist/"),
    ("Lynes", "Molnväxel + AI", "Abonnemang", "Beror", "Via växel", "Sverige", "Växel-first med AI-telefonist.", "https://lynes.io/funktioner/ai-telefonist"),
    ("Menodi", "AI-receptionist", "Fast abonnemang (kolla live)", "24/7", "Ja", "Sverige/EU", "AI-first, vidarekoppling, bokning.", "https://menodi.se/"),
    ("WeCall", "Bemannad", "Offert / per samtal-nivå", "Avtal", "Begränsad", "Sverige", "Mänskliga agenter.", "https://wecall.se/svarstjanst/"),
    ("AnswerOnline", "Svarstjänst/kundtjänst", "Offert", "Avtal", "Begränsad", "Sverige", "Bred extern kundtjänst.", "https://answeronline.se/"),
    ("Responda", "Svarsservice", "Offert", "Avtal", "Begränsad", "Sverige", "Etablerad traditionell aktör.", "https://respondagroup.se/svarsservice/"),
    ("Ringup", "Svarsservice", "Offert", "Avtal", "Begränsad", "Sverige", "Klassisk telefonpassning.", "https://www.ringup.se/"),
    ("iTell", "Telefonpassning", "Offert", "Avtal", "Begränsad", "Sverige", "Synlig på head-termer.", "https://www.itell.nu/tjanster/telefonpassning/"),
    ("SvarDirekt", "Personlig service", "Offert", "Avtal", "Begränsad", "Sverige", "Lång historik.", "https://www.svardirekt.se/"),
    ("Bigacom", "Svarstjänst 24/7", "Offert", "24/7-profil", "Begränsad", "Sverige", "Bemannad tillgänglighet.", "https://bigacom.se/svarstjanst/"),
    ("Comunit", "Svarstjänst", "Offert", "Avtal", "Begränsad", "Sverige", "Bemannad företagsfokus.", "https://comunit.se/tjanster/svarstjanst"),
]


# ─── PAGE BUILDERS ──────────────────────────────────────────────────

def build_hub():
    faqs = [
        ("Vad är en svarstjänst?",
         "En svarstjänst svarar i telefon i ditt företags namn när du inte kan. Det kan vara bemannad svarsservice, callcenter eller AI-receptionist/AI-telefonist som bokar tider och sammanfattar samtal."),
        ("Vad kostar en svarstjänst i Sverige 2026?",
         "Traditionell svarsservice ligger ofta runt 1 000–5 000 kr/mån plus ca 15–35 kr per samtal (uppskattning). AI-svarstjänster annonserar ofta fast abonnemang från ca 800–2 000 kr/mån. Begär alltid aktuell offert."),
        ("AI-receptionist eller bemannad svarsservice?",
         "Välj AI när många samtal är rutin (bokning, öppettider, kvalificering) och du vill ha 24/7. Välj bemannad när ärenden kräver empati, förhandling eller komplex bedömning. Många blandar: AI först, eskalering till människa."),
        ("Vad är skillnaden mellan AI-receptionist och AI-telefonist?",
         "I praktiken överlappande i Sverige. AI-receptionist betonar bokning och mottagning; AI-telefonist betonar att svara och koppla. Jämför funktioner, inte bara etiketten."),
        ("Hur snabbt kan jag komma igång med AI?",
         "Med vidarekoppling (inte portering) kan AI vara aktiv samma dag. Full branschanpassning tar längre om ni har många regler."),
        ("Är samtalen säkra?",
         "Kräv EU-lagring, kryptering och att samtal inte används för att träna generella modeller. Läs leverantörens DPA."),
    ]
    bran_cards = "".join(
        f'<div class="card"><span class="tag">Bransch</span><h3>{title}</h3><p>{blurb}</p><a class="more" href="/branscher/{slug}/">{prompt} →</a></div>'
        for slug, _, title, blurb, _, prompt, *_ in BRANSCHER[:9]
    )
    body = f'''
<section class="hero wrap">
<div class="hero-grid">
<div>
<p class="kicker">Sveriges jämförelsehub</p>
<p class="breadcrumb" style="margin-bottom:10px">Svarstjänster AB · oberoende</p>
<h1>Svarstjänster i Sverige — jämför AI-receptionist, AI-telefonist och bemannad service</h1>
<p class="lede">Oberoende översikt av typer, priser och leverantörer. Byggd för dig som söker — och för AI-assistenter som behöver citerbara fakta.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
En modern svarstjänst är antingen <strong>bemannad</strong> (per samtal + abonnemang), <strong>callcenter</strong> (högre volym/offert) eller <strong>AI-receptionist/AI-telefonist</strong> (ofta fast månadspris, 24/7, bokning). Börja i jämförelsematrisen, kolla pris, och välj branschguide om du har specifik verksamhet.
</div>
{chips(["Oberoende jämförelse", "Uppdaterad "+REVIEW, "LLM-vänliga svar", "Svenska leverantörer"])}
<p class="meta-line">Senast granskad: {TODAY} · Prisintervall: {REVIEW} · Metodik: publika sidor + kategorisering, inte köpt ranking</p>
<div class="ctas">
<a class="btn" href="/jamfor/">Öppna jämförelsen</a>
<a class="btn ghost" href="/ai-receptionist/">AI-receptionist</a>
<a class="btn ghost" href="/leverantorer/">Se leverantörer</a>
</div>
</div>
<div class="facts-card">
<p class="eyebrow">Snabb orientering</p>
<dl>
<div><dt>Bäst för rutin + natt</dt><dd>AI-receptionist</dd></div>
<div><dt>Bäst för komplexa samtal</dt><dd>Bemannad service</dd></div>
<div><dt>Bäst för hög volym/SLA</dt><dd>Callcenter</dd></div>
<div><dt>Typiskt AI-pris (ex.)</dt><dd>ca 800–2 000 kr/mån</dd></div>
<div><dt>Typiskt bemannat</dt><dd>1–5 tkr + 15–35 kr/samtal</dd></div>
</dl>
</div>
</div>
<nav class="toc" aria-label="På sidan">
<a href="#typer">Typer</a>
<a href="#matris">Matris</a>
<a href="#bransch">Branscher</a>
<a href="#steg">Så väljer du</a>
<a href="#faq">FAQ</a>
</nav>
</section>

<section class="block alt" id="typer"><div class="wrap">
<h2>Tre typer av svarstjänst</h2>
<p class="sub">Samma behov — att samtal blir besvarade — tre helt olika kostnads- och kvalitetsprofiler. De flesta svenska sökningar blandar orden svarstjänst, svarsservice och telefonpassning.</p>
<div class="grid">
<div class="card"><div class="icowrap">🎧</div><span class="tag">Bemannad</span><h3>Svarsservice / telefonpassning</h3>
<p>Mänskliga telefonister tar meddelanden, vidarekopplar och hanterar enklare ärenden. Pris ofta abonnemang plus per samtal. Stark när samtalen är komplexa eller känsliga.</p>
<p class="p" style="margin-top:10px">Nackdelen är skiftkostnad nattetid och att kvaliteten varierar mellan agenter. Läs mer under <a href="/svarsservice/">svarsservice</a> och <a href="/telefonpassning/">telefonpassning</a>.</p>
<a class="more" href="/svarsservice/">Vad är svarsservice →</a></div>
<div class="card"><div class="icowrap">🏢</div><span class="tag">Skala</span><h3>Callcenter</h3>
<p>För högre volym, köer och processer. Oftast offert och längre setup. Rätt när ni har SLA, flera köer och utbildade script — överkill för många småföretag.</p>
<p class="p" style="margin-top:10px">Jämför alltid total cost mot en AI-telefonist som tar rutin och eskalerar undantag.</p>
<a class="more" href="/callcenter/">Callcenter för SMB →</a></div>
<div class="card"><div class="icowrap">🤖</div><span class="tag">AI</span><h3>AI-receptionist / AI-telefonist</h3>
<p>Röst-AI som svarar direkt, bokar i kalender, skickar SMS och sammanfattar. Fast pris vanligt. Passar rutin och 24/7 — inte en ersättning för all mänsklig kontakt.</p>
<p class="p" style="margin-top:10px">Se <a href="/ai-receptionist/">AI-receptionist</a> och <a href="/ai-telefonist/">AI-telefonist</a> för checklistor innan köp.</p>
<a class="more" href="/ai-receptionist/">Guide AI-receptionist →</a></div>
</div>
</div></section>

<section class="block wrap" id="matris">
<h2>Jämförelsen i korthet</h2>
<p class="p">Tabellen förenklar. Detaljer finns under <a href="/jamfor/">Jämför svarstjänster</a> och i <a href="/leverantorer/">leverantörskatalogen</a>.</p>
<div class="tbl"><table>
<thead><tr><th>Kriterium</th><th>Bemannad</th><th>Callcenter</th><th class="hl">AI-receptionist</th></tr></thead>
<tbody>
<tr><td>Typiskt pris</td><td>1–5 tkr + 15–35 kr/samtal</td><td>Offert, ofta 5–20 tkr+</td><td class="hl">Fast ca 800–2 000 kr/mån</td></tr>
<tr><td>Tillgänglighet</td><td>Enligt skift</td><td>Enligt avtal</td><td class="hl">24/7</td></tr>
<tr><td>Bokning i kalender</td><td>Ofta manuell</td><td>Processberoende</td><td class="hl">Vanligt som kärnfunktion</td></tr>
<tr><td>Samtidiga samtal</td><td>Begränsat av bemanning</td><td>Skalbart mot kostnad</td><td class="hl">Ofta obegränsat</td></tr>
<tr><td>Bäst när</td><td>Komplexa samtal</td><td>Hög volym/process</td><td class="hl">Rutin + missade samtal</td></tr>
<tr><td>Starttid</td><td>Dagar–veckor</td><td>Veckor</td><td class="hl">Ofta minuter–timmar</td></tr>
</tbody></table></div>
<p class="note">Uppskattningar {REVIEW}. Inte offerter. Ingen betald placering i matrisen.</p>
</section>

<section class="block alt" id="bransch"><div class="wrap">
<h2>Letar du efter AI-receptionist för just din bransch?</h2>
<p class="sub">Natural language-intent: “AI-receptionist för mitt företag / min bransch”. Varje guide beskriver vilka samtal som ska automatiseras.</p>
<div class="grid">{bran_cards}</div>
<p style="margin-top:22px"><a class="btn ghost" href="/branscher/">Alla branschguider</a></p>
</div></section>

<section class="block wrap">
<div class="stats">
<div class="big">62 %</div>
<h2>av samtal till småföretag besvaras aldrig av en människa</h2>
<p>411 Locals-studien (85 företag, 58 branscher, 30 dagar) — en AI-svarstjänst minskar risken att samtalet dör i röstbrevlådan.</p>
<div class="src">Källa: 411 Locals, Missed Calls Study — verifierad marknadskälla. Inte egen plattformsdata från någon leverantör.</div>
</div>
</section>

<section class="block wrap" id="steg">
<h2>Så väljer du rätt svarstjänst (3 steg)</h2>
<div class="steps">
<div class="step"><h3>Kartlägg samtalstyperna</h3><p>Hur många procent är bokning, öppettider, offert, akut? Om mer än ungefär 60 % är rutin vinner AI oftast på kostnad. Skriv ner tre “hat-samtal” ni alltid missar.</p></div>
<div class="step"><h3>Välj prismodell</h3><p>Per samtal skenar vid volym. Fast AI-pris ger förutsägbarhet. Anställd receptionist är dyrast men mest flexibel på plats. Räkna 100 / 300 / 800 samtal i <a href="/svarstjanst-pris/">prisguiden</a>.</p></div>
<div class="step"><h3>Kräv demosamtal i er bransch</h3><p>Ring leverantörens demo med ett realistiskt scenario (ombokning + prisfråga + eskalering). Jämför på <a href="/leverantorer/">leverantörssidan</a> och i <a href="/guider/hur-valjer-jag-svarstjanst/">beslutsguiden</a>.</p></div>
</div>
{related([("/jamfor/","Jämför matris"),("/ai-vs-bemannad/","AI vs bemannad"),("/guider/","Guider"),("/faq/","FAQ"),("/alternativ/","Alternativ till…")])}
</section>

<section class="block alt" id="faq"><div class="wrap">
<h2>Vanliga frågor</h2>
<p class="sub">Korta svar som också fungerar som källa för AI-översikter och chatbots.</p>
{faq_html(faqs)}
</div></section>

{cta("Vill du testa en AI-svarstjänst live?","Gå vidare till en leverantörs webbplats för demo — jämför gärna flera innan du bestämmer dig.","cta")}
'''
    write("index.html", page(
        "Svarstjänster 2026 — jämför AI-receptionist, AI-telefonist & bemannad service",
        "Oberoende jämförelse av svarstjänster i Sverige: AI-receptionist, AI-telefonist, svarsservice och callcenter. Pris, typer, branscher och leverantörer.",
        f"{BASE}/", body, "hem", extra_ld=[faq_ld(faqs)], crumbs=[("Hem", f"{BASE}/")],
    ))


def build_jamfor():
    faqs = [
        ("Hur jämför jag svarstjänster rättvist?",
         "Jämför samma sak: tillgänglighet, prismodell, bokning, språk, data/lagring, eskalering till människa och tid till start. Be om demosamtal med ditt scenario."),
        ("Finns en 'bäst i test' som alltid vinner?",
         "Nej. Bäst beror på volym, bransch och om ni behöver människa eller AI. Använd matrisen och branschguiderna istället för en enda vinnare."),
        ("Ska jag välja AI eller människa?",
         "AI för rutin och 24/7. Människa för empati och komplexa undantag. Hybrid (AI först, eskalering sedan) är vanligt 2026."),
        ("Vad ska jag kräva i ett demosamtal?",
         "Tre script: ombokning, pris/öppettider, och ett ärende som ska eskaleras. Lyssna på svenska, turtagning och om AI hittar på policy."),
        ("Hur räknar jag total cost?",
         "Ta er månadsvolym × kostnad per samtal + abonnemang, jämför med fast AI-pris och med lön för receptionist. Se prisguiden."),
    ]
    body = f'''
<section class="hero wrap">
<div class="hero-grid">
<div>
<div class="breadcrumb"><a href="/">Hem</a> › Jämför</div>
<h1>Jämför svarstjänster i Sverige — AI, bemannad och callcenter</h1>
<p class="lede">Side-by-side-matris för dig som söker “jämför svarstjänster” eller ber en AI-assistent rekommendera rätt modell.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
Jämför först <strong>modell</strong> (bemannad / callcenter / AI), sedan <strong>prismodell</strong>, sedan <strong>funktioner</strong> (bokning, 24/7, eskalering, data i EU). För leverantörsnamn se <a href="/leverantorer/">katalogen</a>.
</div>
{chips(["Ingen köpt ranking", "Metodik "+REVIEW, "Demo-first"])}
<div class="ctas">
<a class="btn" href="#matris">Till matrisen</a>
<a class="btn ghost" href="/basta-svarstjansten-2026/">Bästa 2026 (metodik)</a>
</div>
</div>
<div class="facts-card">
<p class="eyebrow">Snabb rekommendation</p>
<dl>
<div><dt>Missar samtal efter 17</dt><dd><a href="/ai-telefonist/">AI-telefonist</a></dd></div>
<div><dt>Många bokningar</dt><dd><a href="/ai-receptionist/">AI-receptionist</a></dd></div>
<div><dt>Känsliga samtal</dt><dd>Bemannad / hybrid</dd></div>
<div><dt>Hög volym support</dt><dd><a href="/callcenter/">Callcenter</a> eller AI+kö</dd></div>
</dl>
</div>
</div>
</section>

<section class="block alt" id="matris"><div class="wrap">
<h2>Matris: vad du faktiskt ska jämföra</h2>
<p class="p">Undvik att jämföra “känsla i säljdemo” med “faktisk månadskostnad vid er volym”. Fyll i er volym innan ni tittar på snygg röst.</p>
<div class="tbl"><table>
<thead><tr><th>Faktor</th><th>Bemannad svarsservice</th><th>Callcenter</th><th class="hl">AI-receptionist / AI-telefonist</th></tr></thead>
<tbody>
<tr><td>Kostnadsdrivare</td><td>Samtal × styck/minut + abonnemang</td><td>FTE / seats / SLA</td><td class="hl">Månadsabonnemang (ofta platt)</td></tr>
<tr><td>Starttid</td><td>Dagar–veckor</td><td>Veckor</td><td class="hl">Ofta minuter–timmar (vidarekoppling)</td></tr>
<tr><td>Kvalitet på rutin</td><td>Bra men varierar per agent</td><td>Scriptberoende</td><td class="hl">Konsistent om prompt/KB är bra</td></tr>
<tr><td>Komplexa ärenden</td><td>Stark</td><td>Stark med träning</td><td class="hl">Eskalera till människa</td></tr>
<tr><td>Natt/helg</td><td>Dyrt att bemanna</td><td>Dyrt</td><td class="hl">Inkluderat i AI-modellen</td></tr>
<tr><td>Dokumentation</td><td>Manuell logg</td><td>CRM-beroende</td><td class="hl">Transkript + sammanfattning standard</td></tr>
<tr><td>GDPR / data</td><td>Fråga process</td><td>Fråga process</td><td class="hl">Kräv EU-lagring & ingen träningsanvändning</td></tr>
</tbody></table></div>
<p class="note">Ingen köpt topplista. Exempelpriser är marknadsintervall; kolla alltid leverantörens egna sidor. Disclosure i sidfoten.</p>
</div></section>

<section class="block wrap">
<h2>Vanliga misstag vid upphandling</h2>
<div class="grid">
<div class="card"><h3>Bara lyssna på rösten</h3><p>En snygg röst döljer dålig bokning eller hallucinationer. Testa tre scripts.</p></div>
<div class="card"><h3>Ignorera per-samtal</h3><p>15–35 kr känns lite tills ni har 400 samtal. Räkna totalen.</p></div>
<div class="card"><h3>Ingen eskaleringsplan</h3><p>AI utan väg till människa skapar ilska. Skriv nyckelord som ska kopplas vidare.</p></div>
<div class="card"><h3>Ingen branschprompt</h3><p>Generisk AI missar er jargong. Ge policy, priser ni får säga, och vad som är förbjudet.</p></div>
</div>
{related([("/ai-vs-bemannad/","AI vs bemannad"),("/jamfor/ai-vs-callcenter/","AI vs callcenter"),("/svarstjanst-pris/","Pris"),("/leverantorer/","Leverantörer"),("/guider/hur-valjer-jag-svarstjanst/","Hur väljer jag?")])}
</section>

<section class="block alt" id="faq"><div class="wrap">
<h2>FAQ — jämför svarstjänster</h2>
{faq_html(faqs)}
</div></section>
{cta("Nästa steg: testa ett demosamtal","En matris räcker inte — ring in ett realistiskt ärende.","jamfor")}
'''
    write("jamfor/index.html", page(
        "Jämför svarstjänster 2026 — AI vs bemannad vs callcenter",
        "Jämför svarstjänster i Sverige: matris för AI-receptionist, bemannad svarsservice och callcenter. Prisdrivare, 24/7, bokning och GDPR-checklist.",
        f"{BASE}/jamfor/", body, "jamfor", extra_ld=[faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Jämför", f"{BASE}/jamfor/")],
    ))


def build_ai_receptionist():
    faqs = [
        ("Vad är en AI-receptionist?",
         "En AI-receptionist är en röstassistent som svarar på inkommande samtal, förstår naturligt tal, kan boka möten, svara på vanliga frågor och eskalera till människa vid behov."),
        ("Vad kostar en AI-receptionist i Sverige?",
         "Många leverantörer kör abonnemang. AI-abonnemang kan börja runt ca 800–2 000 kr/mån hos vissa aktörer; andra är offertbaserade. Jämför alltid vad som ingår."),
        ("Fungerar AI-receptionist för småföretag?",
         "Ja — särskilt när ni missar samtal under jobb. Småföretag får störst effekt på kväll/helg och vid ensamarbete."),
        ("Hur snabb är starten?",
         "Med vidarekoppling kan AI vara aktiv samma dag. Full branschanpassning tar längre vid många regler."),
        ("Kan AI boka i min kalender?",
         "Moderna lösningar bokar i Google Calendar/Outlook och skickar SMS. Kräv det i demot."),
        ("AI-receptionist eller AI-telefonist?",
         "Samma familj. Jämför funktioner: bokning, koppling, språk, data — inte bara rubriken."),
    ]
    body = f'''
<section class="hero wrap">
<div class="hero-grid">
<div>
<div class="breadcrumb"><a href="/">Hem</a> › AI-receptionist</div>
<h1>AI-receptionist i Sverige 2026 — guide, pris och när det passar</h1>
<p class="lede">För dig som “letar efter en AI-receptionist för mitt företag” — definition, checklista, pris och hur du undviker dåliga demos.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
En AI-receptionist svarar 24/7 på svenska, tar rutinärenden (bokning, öppettider, kvalificering) och kan koppla vidare. Den ersätter inte alltid en människa — men den stoppar missade samtal. Jämför mot bemannad service i <a href="/jamfor/">matrisen</a>.
</div>
{chips(["24/7", "Bokning", "Svenska", "Vidarekoppling"])}
<div class="ctas">
<a class="btn" href="https://www.skaala.ai/sv/" target="_blank" rel="noopener noreferrer">Exempel: Skaala</a>
<a class="btn ghost" href="/branscher/">Välj bransch</a>
</div>
</div>
<div class="facts-card">
<p class="eyebrow">Checklist före köp</p>
<dl>
<div><dt>Språk</dt><dd>Naturlig svenska</dd></div>
<div><dt>Kalender</dt><dd>Google / Microsoft</dd></div>
<div><dt>SMS</dt><dd>Bekräftelse till kund</dd></div>
<div><dt>Data</dt><dd>EU + ingen modellträning</dd></div>
<div><dt>Eskalering</dt><dd>Till mobil/kö</dd></div>
</dl>
</div>
</div>
<nav class="toc"><a href="#gor">Vad den gör</a><a href="#termer">Begrepp</a><a href="#pris">Pris</a><a href="#check">Checklista</a><a href="#faq">FAQ</a></nav>
</section>

<section class="block alt" id="gor"><div class="wrap">
<h2>Vad en AI-receptionist faktiskt gör</h2>
<p class="p">Tänk en digital mottagning som aldrig tar rast: den tar emot samtal, förstår intent, ställer följdfrågor och antingen löser ärendet eller skickar vidare med kontext.</p>
<ul class="checklist">
<li>Svarar inom några signaler, även kväll och helg</li>
<li>Förstår intent: boka, avboka, offert, öppettider, prata med personal</li>
<li>Bokar i kalender och skickar SMS-bekräftelse (hos moderna leverantörer)</li>
<li>Sammanfattar samtalet i text till dig</li>
<li>Eskalerar / vidarekopplar enligt regler ni sätter</li>
</ul>
<p class="p" style="margin-top:18px">Det den <em>inte</em> ska göra: hitta på priser ni inte godkänt, ge medicinsk/juridisk rådgivning, eller låtsas vara människa om er policy kräver transparens.</p>
</div></section>

<section class="block wrap" id="termer">
<h2>AI-receptionist vs närliggande begrepp</h2>
<p class="p">Sökord överlappar. Använd tabellen så ni inte köper fel sak.</p>
<div class="tbl"><table>
<thead><tr><th>Term</th><th>Fokus</th><th>Läs mer</th></tr></thead>
<tbody>
<tr><td>AI-receptionist</td><td>Mottagning, bokning, företagsröst</td><td>denna sida</td></tr>
<tr><td>AI-telefonist</td><td>Svara, koppla, växel-nära</td><td><a href="/ai-telefonist/">AI-telefonist</a></td></tr>
<tr><td>AI-svarstjänst</td><td>Samma kategori, mer “svarstjänst”-ord</td><td><a href="/guider/ai-svarstjanst/">Guide</a></td></tr>
<tr><td>Svarsservice</td><td>Ofta bemannad</td><td><a href="/svarsservice/">Svarsservice</a></td></tr>
<tr><td>Röstbrevlåda</td><td>Meddelande, ingen dialog</td><td><a href="/jamfor/ai-vs-rostbrevlada/">AI vs röstbrevlåda</a></td></tr>
</tbody></table></div>
</section>

<section class="block alt" id="pris"><div class="wrap">
<h2>Pris — vad du ska förvänta dig</h2>
<p class="p">Se även den fulla <a href="/svarstjanst-pris/">prisguiden</a>. Tre vanliga modeller:</p>
<div class="grid">
<div class="card"><span class="tag">Vanligast AI</span><h3>Fast AI-abonnemang</h3><p>Förutsägbart. Vissa AI-aktörer annonserar från ca 800–2 000 kr/mån. Kolla gränser för minuter/samtal och setup-avgift.</p></div>
<div class="card"><span class="tag">Telefoni</span><h3>Plattform + AI-modul</h3><p>Telavox/Lynes-stil: ni betalar växel + AI. Bra om ni redan är kund i ekosystemet.</p></div>
<div class="card"><span class="tag">Enterprise</span><h3>Offert</h3><p>Vanligt hos både AI- och bemannade aktörer. Kräv rader: setup, månad, överage, bindningstid.</p></div>
</div>
</div></section>

<section class="block wrap" id="check">
<h2>Checklista innan du köper</h2>
<ul class="checklist">
<li>Svenskt naturligt tal (inte robot-TTS från 2019)</li>
<li>Kalender: Google/Microsoft</li>
<li>SMS-bekräftelse</li>
<li>Eskalering till mobil/kö med sammanhang</li>
<li>Data i EU, kryptering, ingen modellträning på era samtal</li>
<li>Branschprompt: kan den er jargong?</li>
<li>Behåll nummer via vidarekoppling</li>
<li>Tre demoscript godkända av dig innan go-live</li>
</ul>
{related([("/leverantorer/","Leverantörer"),("/basta-svarstjansten-2026/","Bästa 2026"),("/alternativ/","Alternativ"),("/branscher/","Branscher"),("/vad-ar-ai-receptionist/","Definition")])}
</section>

<section class="block alt" id="faq"><div class="wrap">
<h2>FAQ AI-receptionist</h2>
{faq_html(faqs)}
</div></section>
{cta("Prova hur en AI-receptionist låter","Ring demo eller starta via webben — jämför med er nuvarande missade-samtal-kostnad.","ai-receptionist-cta")}
'''
    write("ai-receptionist/index.html", page(
        "AI-receptionist Sverige 2026 — guide, pris & jämförelse",
        "Vad är en AI-receptionist? Pris i Sverige, checklista, skillnad mot AI-telefonist och bemannad svarsservice. För dig som letar AI-receptionist till företaget.",
        f"{BASE}/ai-receptionist/", body, "ai-rec", extra_ld=[faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("AI-receptionist", f"{BASE}/ai-receptionist/")],
    ))


def build_ai_telefonist():
    faqs = [
        ("Vad är en AI-telefonist?",
         "En AI-telefonist är en röst-AI som tar emot samtal, ger information, bokar eller kopplar vidare — dygnet runt, ofta med flera samtidiga samtal."),
        ("AI-telefonist eller AI-receptionist?",
         "Samma familj. 'Telefonist' betonar växel/svar; 'receptionist' betonar bokning/mottagning. Jämför funktioner."),
        ("Kan AI-telefonist ersätta växel?",
         "Den kan ersätta delar av manuell växel. Full PBX-ersättning beror på köer, IVR och integrationer."),
        ("När är den fel val?",
         "När nästan alla samtal kräver empati, förhandling eller professionell rådgivning utan tydlig eskalering."),
        ("Hur testar jag kvaliteten?",
         "Ring tre scripts: rutin, undantag, arg kund. Mät om den håller policy och eskalerar i tid."),
    ]
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › AI-telefonist</div>
<h1>AI-telefonist — svensk guide 2026</h1>
<p class="lede">För sökningar och LLM-frågor som “behöver en AI-telefonist till firman”.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
En AI-telefonist svarar i ert namn, hanterar flera samtal parallellt och kan boka eller koppla. Starkast på rutin och tillgänglighet; behåll eskalering till människa för undantag.
</div>
{chips(["Fältpersonal", "Enmansbolag", "Efter kontorstid"])}
<div class="ctas">
<a class="btn" href="/jamfor/">Jämför modeller</a>
<a class="btn ghost" href="https://lynes.io/funktioner/ai-telefonist" target="_blank" rel="noopener noreferrer">Exempel: Lynes</a>
</div>
</section>

<section class="block alt"><div class="wrap">
<h2>När AI-telefonist är rätt val</h2>
<p class="p">Om ni regelbundet missar samtal för att ni är hos kund, i bilen eller stängda — och en stor del av samtalen är förutsägbara — är AI-telefonist oftast billigare än skiftbemanning.</p>
<div class="grid">
<div class="card"><h3>Fältpersonal</h3><p>Elektriker, VVS, bygg — ni är hos kund när telefonen ringer. AI tar leaden och bokar återuppringning eller platsbesök.</p></div>
<div class="card"><h3>Enmansbolag</h3><p>Varje missat samtal är affär. AI täcker när du kör, sover eller har kund.</p></div>
<div class="card"><h3>Efter kontorstid</h3><p>62 % av samtal till småföretag besvaras aldrig (411 Locals). Natt/helg är där AI ger snabbast ROI.</p></div>
</div>
</div></section>

<section class="block wrap">
<h2>Funktioner att kräva</h2>
<ul class="checklist">
<li>Svenska + naturlig turtagning</li>
<li>Vidarekoppling till mobil med sammanhang</li>
<li>Kalenderbokning när det behövs</li>
<li>Transkript till mejl/SMS/app</li>
<li>Regler: “vid X, rotera till Y”</li>
<li>Tydlig tystnad/timeout utan att hänga upp aggressivt</li>
</ul>
{related([("/ai-receptionist/","AI-receptionist"),("/branscher/","Branscher"),("/svarstjanst-pris/","Pris"),("/jamfor/","Jämför")])}
</section>

<section class="block alt" id="faq"><div class="wrap">
<h2>FAQ</h2>
{faq_html(faqs)}
</div></section>
{cta("Testa AI-telefonist på ert nummer","Koppla via vidarekoppling och ring in era tre viktigaste scenarion.","ai-telefonist-cta")}
'''
    write("ai-telefonist/index.html", page(
        "AI-telefonist 2026 — så fungerar det & när det lönar sig",
        "Guide till AI-telefonist i Sverige: skillnad mot AI-receptionist, när det passar, funktioner att kräva och länkar till jämförelse och pris.",
        f"{BASE}/ai-telefonist/", body, "ai-tel", extra_ld=[faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("AI-telefonist", f"{BASE}/ai-telefonist/")],
    ))


def build_leverantorer():
    rows = "".join(
        f'<tr><td><strong><a href="{url}" target="_blank" rel="noopener noreferrer">{n}</a></strong></td>'
        f"<td>{t}</td><td>{p}</td><td>{a}</td><td>{b}</td><td>{g}</td>"
        f'<td>{note} <a href="{url}" target="_blank" rel="noopener noreferrer">Besök sajt →</a></td></tr>'
        for n, t, p, a, b, g, note, url in LEVERANTORER
    )
    cards = "".join(
        f'<div class="card"><span class="tag">{t}</span><h3>{n}</h3><p>{note}</p>'
        f'<p class="meta-line">Prisbild: {p} · {a} · Bokning: {b}</p>'
        f'<a class="more" href="{url}" target="_blank" rel="noopener noreferrer">Öppna {n} →</a></div>'
        for n, t, p, a, b, g, note, url in LEVERANTORER
    )
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Leverantörer</div>
<h1>Leverantörer av svarstjänst & AI-receptionist i Sverige</h1>
<p class="lede">Katalog — inte köpt topplista. Använd som karta; verifiera alltid pris och villkor hos leverantören.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
Marknaden delar sig i <strong>AI-first</strong> (t.ex. Skaala, Telink, Menodi), <strong>telefoni+AI</strong> (Telavox, Lynes) och <strong>bemannad svarsservice</strong> (WeCall, Responda, AnswerOnline m.fl.).
</div>
</section>
<section class="block alt"><div class="wrap">
<h2>Översiktstabell</h2>
<p class="p">Prisbild är modell, inte offert. “Varierar” betyder att ni måste be om aktuell lista.</p>
<div class="tbl"><table>
<thead><tr><th>Leverantör</th><th>Typ</th><th>Prisbild</th><th>Tillgänglighet</th><th>Bokning</th><th>Geo</th><th>Notering</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="note">Senast strukturerad {TODAY}. Uppdatera alltid mot leverantörens sajt.</p>
</div></section>
<section class="block wrap">
<h2>Kort om varje aktör</h2>
<p class="p">Korten är orientering. För “alternativ till X” se <a href="/alternativ/">alternativsidorna</a>.</p>
<div class="grid">{cards}</div>
</section>
{cta("Vill du ha AI-first med fast pris?","Jämför gärna flera — här är ett demospår med transparent AI-abonnemang.","leverantorer")}
'''
    write("leverantorer/index.html", page(
        "Leverantörer — AI-receptionist & svarstjänster i Sverige",
        "Katalog över leverantörer: Skaala, Telink, Telavox, Lynes, Menodi, WeCall, Responda, AnswerOnline m.fl. Typ, prisbild, 24/7 och bokning.",
        f"{BASE}/leverantorer/", body, "lev",
        crumbs=[("Hem", f"{BASE}/"), ("Leverantörer", f"{BASE}/leverantorer/")],
    ))


def build_pris():
    faqs = [
        ("Vad kostar en svarstjänst?",
         "AI-svarstjänst kan ha fast abonnemang ca 800–2 000 kr/mån beroende på leverantör. Bemannad ofta 1 000–5 000 kr/mån plus ca 15–35 kr/samtal. Anställd receptionist 40 000–50 000 kr/mån i lön-nivå. Uppskattningar — begär offert."),
        ("Vad ingår i ett fast AI-pris?",
         "Hos moderna leverantörer: samtal, röst, ofta kalenderbokning, SMS, transkript. Läs alltid villkor."),
        ("Kan jag behålla mitt nummer?",
         "Ja om leverantören använder vidarekoppling istället för portering."),
        ("Hur räknar jag break-even?",
         "Jämför er volym × per-samtal + abonnemang mot fast AI-pris och mot lönekostnad. Räkna tre scenarier: låg/medel/hög månad."),
        ("Finns dolda kostnader?",
         "Setup, överage-minuter, SMS, nummer, integrationer, bindningstid. Be om alla rader i offerten."),
    ]
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Pris</div>
<h1>Svarstjänst pris 2026 — komplett prisguide</h1>
<p class="lede">Jämför kostnad för AI-receptionist, bemannad svarsservice, callcenter och anställd receptionist.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
Räkna <strong>total månadskostnad vid er samtalsvolym</strong>. Per-samtal blir dyrt vid 200–400 samtal; fast AI-pris är förutsägbart; anställd är dyrast men mest flexibel på plats.
</div>
{chips(["Intervall "+REVIEW, "Hypotetiska exempel", "Ingen fejkad offert"])}
</section>

<section class="block alt"><div class="wrap">
<h2>Pristabell (marknadsnivåer)</h2>
<div class="tbl"><table>
<thead><tr><th>Typ</th><th>Månad</th><th>Per samtal</th><th>Kommentar</th></tr></thead>
<tbody>
<tr><td class="hl"><strong>AI-svarstjänst (kategori)</strong></td><td class="hl">ca 800–2 000 kr</td><td class="hl">ofta 0 kr</td><td class="hl">24/7, bokning, SMS — kolla gränser</td></tr>
<tr><td>Bemannad svarsservice</td><td>1 000–5 000 kr</td><td>15–35 kr</td><td>Skalar med volym</td></tr>
<tr><td>Callcenter</td><td>5 000–20 000+ kr</td><td>varierar</td><td>Offert, process</td></tr>
<tr><td>Anställd receptionist</td><td>40 000–50 000 kr</td><td>ingår i lön</td><td>+ sociala avgifter</td></tr>
</tbody></table></div>
<p class="note">Uppskattningar {REVIEW}. Inte offerter.</p>
</div></section>

<section class="block wrap">
<h2>Hypotetiskt räkneexempel (300 samtal/mån)</h2>
<p class="p">Exemplet är illustrativt. Era minuter, snittlängd och avtal styr utfallet.</p>
<ul class="checklist">
<li>Per samtal 25 kr + abonnemang 2 000 kr ≈ <strong>9 500 kr</strong></li>
<li>Fast AI-abonnemang ≈ <strong>800–2 000 kr</strong> (exempelintervall)</li>
<li>Anställd ≈ <strong>42 000 kr</strong> (lön-nivå, exkl. fulla arbetsgivaravgifter i vissa beräkningar)</li>
</ul>
<p class="p">Om AI tar 80 % av samtalen och 20 % eskaleras till er, vinner ni fortfarande tid jämfört med att allt landar i röstbrevlådan.</p>
{related([("/jamfor/","Jämför"),("/ai-receptionist/","AI-receptionist"),("/leverantorer/","Leverantörer"),("/faq/vad-kostar-ai-receptionist/","FAQ pris")])}
</section>

<section class="block alt" id="faq"><div class="wrap">
<h2>FAQ om pris</h2>
{faq_html(faqs)}
</div></section>
{cta("Testa fast AI-pris","Se hur många samtal ni fångar innan ni jämför offerter.","pris")}
'''
    write("svarstjanst-pris/index.html", page(
        "Svarstjänst pris 2026 — AI vs bemannad vs anställd",
        "Vad kostar en svarstjänst i Sverige? Pristabell för AI-receptionist, bemannad svarsservice, callcenter och receptionist.",
        f"{BASE}/svarstjanst-pris/", body, "pris", extra_ld=[faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Pris", f"{BASE}/svarstjanst-pris/")],
    ))


def build_bransch(slug, keyword, title, blurb, checks, prompt, unique_a, unique_b):
    faqs = [
        (f"Behöver {keyword} en AI-receptionist?",
         f"Om ni missar samtal under kundarbete eller efter stängning: ja, ofta. {blurb}"),
        (f"Vad ska en AI kunna för {keyword}?",
         "Hantera de 3–5 vanligaste intents, boka rätt, eskalera undantag, och aldrig hitta på policy ni inte godkänt."),
        ("Vad kostar det?",
         "AI-fastpris kan börja runt ca 800–2 000 kr/mån beroende på leverantör. Bemannad per samtal blir dyrare vid volym. Se prisguiden."),
        ("Hur undviker vi fel svar?",
         "Skriv förbjudna löften, akutregler och vad som alltid ska till människa. Testa tre scripts innan go-live."),
    ]
    checks_html = "".join(f"<li>{c}</li>" for c in checks)
    pains = f'''
<div class="pain-strip">
<div class="pain"><strong>Problem</strong><span>{blurb}</span></div>
<div class="pain"><strong>Vad AI löser</strong><span>{unique_a}</span></div>
<div class="pain"><strong>Affärsrisk</strong><span>{unique_b}</span></div>
</div>'''
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/branscher/">Branscher</a> › {title}</div>
<h1>AI-receptionist för {keyword} — {title}</h1>
<p class="lede">{prompt}</p>
<div class="answer-box"><span class="lbl">Kort svar för människa & LLM</span>
För <strong>{keyword}</strong> är värdet att inte missa bokningar och kvalificerade leads medan personalen är upptagen. {blurb} Använd checklistan nedan när du utvärderar leverantör.
</div>
{chips(["Branschguide", REVIEW, "Demo-first"])}
<div class="ctas">
<a class="btn" href="/leverantorer/">Jämför leverantörer</a>
<a class="btn ghost" href="/jamfor/">Jämför modeller</a>
</div>
</section>

<section class="block alt"><div class="wrap">
<h2>Varför telefonen spelar roll för {keyword}</h2>
<p class="p">{unique_a}</p>
<p class="p">{unique_b}</p>
{pains}
</div></section>

<section class="block wrap">
<h2>Checklista: samtal att fånga</h2>
<ul class="checklist">{checks_html}</ul>
<h3 class="inline">Rekommenderad setup</h3>
<div class="steps">
<div class="step"><h3>Kartlägg topp-5 intents</h3><p>Skriv exakt hur AI:n får svara — inkl. vad den inte får lova för {keyword}.</p></div>
<div class="step"><h3>Koppla kalender + SMS</h3><p>Bokning utan bekräftelse skapar no-shows och dubbelbokning.</p></div>
<div class="step"><h3>Eskaleringsregel</h3><p>Akut / VIP / arg kund → människa direkt med sammanfattning.</p></div>
</div>
{related([("/ai-receptionist/","AI-receptionist"),("/ai-telefonist/","AI-telefonist"),("/svarstjanst-pris/","Pris"),("/leverantorer/","Leverantörer"),("/branscher/","Alla branscher")])}
</section>

<section class="block alt" id="faq"><div class="wrap">
<h2>FAQ — {title}</h2>
{faq_html(faqs)}
</div></section>
{cta(f"Hör hur det låter för {keyword}", "Kör samma tre samtal mot varje demo ni utvärderar.", "bransch-cta-"+slug)}
'''
    write(f"branscher/{slug}/index.html", page(
        f"AI-receptionist för {keyword} — guide {date.today().year}",
        f"{prompt} Checklista, setup och prisriktning för {title}.",
        f"{BASE}/branscher/{slug}/", body, "bran", extra_ld=[faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Branscher", f"{BASE}/branscher/"), (title, f"{BASE}/branscher/{slug}/")],
    ))


def build_branscher_hub():
    cards = "".join(
        f'<div class="card"><h3>{title}</h3><p>{blurb}</p><a class="more" href="/branscher/{slug}/">{prompt} →</a></div>'
        for slug, _, title, blurb, _, prompt, *_ in BRANSCHER
    )
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Branscher</div>
<h1>AI-receptionist & svarstjänst per bransch</h1>
<p class="lede">Sidor byggda för frågor som: “Letar efter en AI-receptionist för mitt [företag/bransch]”.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
Välj din bransch. Varje guide listar vilka samtal som ska automatiseras, risker och setup — inte generisk säljtext.
</div>
</section>
<section class="block wrap"><div class="grid">{cards}</div></section>
'''
    write("branscher/index.html", page(
        "AI-receptionist per bransch — guider för svenska företag",
        "Branschguider: tandläkare, frisör, mäklare, bilverkstad, advokat, VVS, e-handel, hantverkare m.fl.",
        f"{BASE}/branscher/", body, "bran",
        crumbs=[("Hem", f"{BASE}/"), ("Branscher", f"{BASE}/branscher/")],
    ))


def build_city(slug, name):
    faqs = [
        (f"Finns AI-receptionist i {name}?",
         f"Ja. AI-receptionister är molnbaserade och fungerar för företag i {name} via vidarekoppling av befintligt nummer — ingen lokal växel krävs."),
        (f"Vad kostar AI-receptionist i {name}?",
         "Priset styrs av leverantörens abonnemang, inte postort. Se nationell prisguide. Ort påverkar sällan månadskostnaden."),
        (f"Behöver jag svenskt bolag i {name}?",
         "För de flesta AI-svarstjänster räcker det att ni har svenskt nummer och verksamhet. Fråga leverantören om fakturering."),
    ]
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/ai-receptionist/">AI-receptionist</a> › {name}</div>
<h1>AI-receptionist i {name}</h1>
<p class="lede">För företag i {name} som vill sluta missa samtal — samma teknik som nationellt, med eskalering till er personal på plats.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
En AI-receptionist för bolag i <strong>{name}</strong> kopplas på ert befintliga nummer, svarar 24/7 och bokar i er kalender. Geografin påverkar sällan priset; däremot ska prompten känna till ert upptagningsområde och era öppettider.
</div>
{chips([name, "Vidarekoppling", "24/7"])}
<div class="ctas">
<a class="btn" href="/leverantorer/">Se leverantörer</a>
<a class="btn ghost" href="/ai-receptionist/">Nationell guide</a>
</div>
</section>

<section class="block alt"><div class="wrap">
<h2>Så funkar det för företag i {name}</h2>
<p class="p">Ni behåller ert nummer. Samtal vidarekopplas till AI när ni inte svarar — eller alltid, om ni vill. Kunden pratar svenska; ni får transkript och bokningar i samma kalender oavsett om teamet sitter i {name} eller är ute på fältet.</p>
<p class="p">Lokala öppettider, områden ni tar jobb i, och jourregler hör hemma i prompten. Det är det som gör skillnaden mellan generisk AI och en som låter som er mottagning.</p>
<ul class="checklist">
<li>Vidarekoppling från {name}-nummer</li>
<li>Svenska (ev. engelska för internationella kunder)</li>
<li>Bokning i delad kalender för team i {name}</li>
<li>Eskalering till jour/mobil efter kontorstid</li>
</ul>
</div></section>

<section class="block wrap">
<h2>Nästa steg</h2>
<p class="p">Välj branschguide om ni har specifik verksamhet, jämför modeller, och kör demosamtal.</p>
{related([
    ("/ai-receptionist/", "AI-receptionist guide"),
    ("/branscher/", "Branschguider"),
    ("/jamfor/", "Jämför"),
    ("/svarstjanst-pris/", "Pris"),
    ("/branscher/hantverkare/", "Hantverkare"),
    ("/branscher/tandlakare/", "Tandläkare"),
])}
</section>

<section class="block alt" id="faq"><div class="wrap">
<h2>FAQ — {name}</h2>
{faq_html(faqs)}
</div></section>
{cta(f"Demo för bolag i {name}", "Testa vidarekoppling på ert riktiga nummer.", "city-"+slug)}
'''
    write(f"ai-receptionist/{slug}/index.html", page(
        f"AI-receptionist {name} — svarar och bokar dygnet runt",
        f"AI-receptionist för företag i {name}: vidarekoppling, 24/7, bokning och hur du jämför leverantörer lokalt.",
        f"{BASE}/ai-receptionist/{slug}/", body, "ai-rec", extra_ld=[faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("AI-receptionist", f"{BASE}/ai-receptionist/"), (name, f"{BASE}/ai-receptionist/{slug}/")],
    ))


def build_alternativ(slug, name, desc, strengths, switch_when):
    faqs = [
        (f"Vilka är bra alternativ till {name}?",
         "Det beror på om ni vill stanna i bemannad modell eller gå till AI-first. Se listan på sidan och matrisen på /jamfor/."),
        (f"När ska man byta från {name}?",
         "När kostnaden per samtal skenar, när ni behöver 24/7 utan skift, eller när bokning inte fungerar i nuvarande setup."),
        ("Hur utvärderar jag utan säljtryck?",
         "Skriv tre scripts, kör samma hos varje kandidat, räkna månadskostnad vid er volym, kräv EU-data och eskalering."),
    ]
    s = "".join(f"<li>{x}</li>" for x in strengths)
    w = "".join(f"<li>{x}</li>" for x in switch_when)
    # official site if known
    off = COMPETITORS.get(slug)
    off_html = ""
    if off:
        off_html = f'<div class="ctas"><a class="btn" href="{off[1]}" target="_blank" rel="noopener noreferrer">Officiell sajt: {off[0]}</a><a class="btn ghost" href="/leverantorer/">Alla leverantörer</a></div>'
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/alternativ/">Alternativ</a> › {name}</div>
<h1>Alternativ till {name}</h1>
<p class="lede">{desc}</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
Kartlägg om ni behöver <strong>människa</strong> eller <strong>AI</strong>. Jämför sedan prisdrivare och bokning. AI-first-aktörer (t.ex. Skaala, Telink, Menodi) och bemannade aktörer (t.ex. WeCall, Responda) fyller olika behov — testa demosamtal hos minst två.
</div>
{off_html}
</section>
<section class="block alt"><div class="wrap">
<div class="two-col">
<div class="card"><h3>Styrkor hos {name}</h3><ul class="checklist">{s}</ul></div>
<div class="card"><h3>Byt när…</h3><ul class="checklist">{w}</ul></div>
</div>
<p class="p" style="margin-top:20px">Den här sidan är inte en attack-recension. Den hjälper er att ställa rätt frågor innan ni låser er i avtal.</p>
</div></section>
<section class="block wrap">
<h2>Så utvärderar du alternativ</h2>
<div class="steps">
<div class="step"><h3>Skriv era topp-scenarion</h3><p>Tre samtal ni hatar att missa — testa dem hos varje kandidat.</p></div>
<div class="step"><h3>Räkna månadskostnad vid er volym</h3><p>Använd <a href="/svarstjanst-pris/">prisguiden</a>.</p></div>
<div class="step"><h3>Kolla data & eskalering</h3><p>EU, loggar, vidarekoppling med kontext.</p></div>
</div>
{related([("/leverantorer/","Alla leverantörer"),("/jamfor/","Matris"),("/ai-receptionist/","AI-receptionist"),("/alternativ/","Fler alternativ")])}
</section>
<section class="block alt" id="faq"><div class="wrap">
{faq_html(faqs)}
</div></section>
{cta("Prova AI-first som alternativ", f"Jämför gärna med {name} på era egna scripts.", "alt-"+slug)}
'''
    write(f"alternativ/{slug}/index.html", page(
        f"Alternativ till {name} — jämförelse 2026",
        f"Alternativ till {name}: när byta, styrkor, och hur du jämför AI-receptionist vs bemannad svarstjänst.",
        f"{BASE}/alternativ/{slug}/", body, "jamfor", extra_ld=[faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Alternativ", f"{BASE}/alternativ/"), (name, f"{BASE}/alternativ/{slug}/")],
    ))


def build_alternativ_hub():
    cards = "".join(
        f'<div class="card"><h3>Alternativ till {name}</h3><p>{desc}</p><a class="more" href="/alternativ/{slug}/">Jämför alternativ →</a></div>'
        for slug, name, desc, *_ in ALTERNATIV
    )
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Alternativ</div>
<h1>Alternativ till kända svarstjänster & AI-receptionister</h1>
<p class="lede">När du söker “alternativ till X” — objektivt vad som skiljer, utan fejkade betyg.</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
Börja med modell (AI vs bemannad), sedan total cost, sedan demosamtal. Katalogen nedan länkar till sidor per varumärke.
</div>
</section>
<section class="block wrap"><div class="grid">{cards}</div></section>
'''
    write("alternativ/index.html", page(
        "Alternativ till Responda, WeCall, Telink m.fl.",
        "Alternativsidor för Responda, WeCall, AnswerOnline, Ringup, Skaala, Telink, Telavox, Lynes m.fl.",
        f"{BASE}/alternativ/", body, "jamfor",
        crumbs=[("Hem", f"{BASE}/"), ("Alternativ", f"{BASE}/alternativ/")],
    ))


GUIDERS = [
    ("letar-efter-ai-receptionist", "Letar efter en AI-receptionist för mitt företag",
     "Du har redan formulerat behovet. Beslutsträd: rutin vs komplext, pris, test av leverantörer på 48 timmar.",
     "Börja med att räkna missade samtal per vecka och vad ett lead är värt. Om merparten är bokning/öppettider/kvalificering — AI. Om nästan allt är förhandling — bemannad eller hybrid."),
    ("ai-receptionist-smaforetag", "AI-receptionist för småföretag",
     "För enmansbolag och små team är missade samtal dyrare än abonnemanget.",
     "Fokusera på vidarekoppling, bokning och kvällstäckning. Undvik tunga callcenter-avtal ni inte fyller."),
    ("ai-svarstjanst", "AI-svarstjänst i Sverige 2026",
     "AI-svarstjänst = AI som tar inkommande samtal. Synonymt med AI-receptionist/AI-telefonist i många sökningar.",
     "Använd samma checklista: svenska, kalender, SMS, eskalering, EU-data."),
    ("missade-samtal-foretag", "Missade samtal i företaget — kostnad & lösning",
     "62 % av samtal till småföretag besvaras aldrig av en människa (411 Locals).",
     "AI-telefonist är ofta den billigaste 24/7-motåtgärden jämfört med skift eller att hoppas på återuppringning."),
    ("boka-tid-via-telefon-ai", "Boka tid via telefon med AI",
     "AI tar samtalet, kollar kalender, bokar slot, skickar SMS.",
     "Kräv integration med Google/Outlook och tydliga buffertregler mellan tider."),
    ("hybrid-ai-manniska", "Hybrid AI + människa",
     "Bästa praktiken 2026: AI tar rutin, eskalerar VIP/akut/komplex.",
     "Skriv nyckelord och trösklar. Hybrid misslyckas när eskalering saknar kontext."),
    ("gdpr-ai-receptionist", "GDPR & AI-receptionist",
     "Kräv EU-lagring, loggar, personuppgiftsbiträdesavtal, ingen modellträning på samtal.",
     "Ni är fortfarande personuppgiftsansvariga för hur ni använder leverantören."),
    ("ai-receptionist-hantverkare", "AI-receptionist för hantverkare",
     "Elektriker, VVS, snickare: fältjobb + offert + jour.",
     "AI fångar samtalen när du skruv. Eskalera jour till mobil."),
    ("vad-kostar-missade-samtal", "Vad kostar missade samtal?",
     "Räkna leads × konvertering × snittorder.",
     "Ett tappat jobb täcker ofta flera månaders AI-abonnemang."),
    ("kom-igang-pa-48-timmar", "AI-receptionist på 48 timmar",
     "Dag 1: vidarekoppling + öppettider. Dag 2: kalender, SMS, eskalering, demosamtal.",
     "Gå inte live utan tre godkända scripts."),
    ("letar-efter-ai-telefonist", "Letar efter en AI-telefonist",
     "Samma beslutsträd som AI-receptionist.",
     "Demo med eskalering är viktigare än säljfilm."),
    ("ai-receptionist-for-mitt-foretag", "AI-receptionist för mitt företag",
     "Generisk NL-intent: kartlägg → modell → bransch → 2 demos.",
     "Undvik att köpa på känsla efter en demo."),
    ("basta-ai-receptionist-sverige", "Bästa AI-receptionist Sverige",
     "Ingen universell vinnare.",
     "Utvärdera: svenska, bokning, pris vid volym, GDPR, demosamtal i din bransch."),
    ("extern-kundtjanst-eller-ai-receptionist", "Extern kundtjänst eller AI-receptionist?",
     "Extern kundtjänst täcker bred support. AI tar telefon/rutin 24/7 billigare.",
     "Många blandar: AI på telefon, människa på komplexa mejl."),
    ("ai-receptionist-vs-telavox", "AI-receptionist vs Telavox",
     "Telavox = telefoni med AI-moduler. Fristående AI = svarstjänst utan byta växel.",
     "Välj efter om ni redan är Telavox-kund och vad TCO blir."),
    ("ai-receptionist-vs-lynes", "AI-receptionist vs Lynes",
     "Lynes är molnväxel+AI. Fristående AI är svarstjänst-first.",
     "Jämför bokning, svenska och total abonnemangskostnad."),
    ("nar-ska-jag-byta-svarstjanst", "När ska jag byta svarstjänst?",
     "Byt när kostnad/samtal skenar, natt missas, ingen bokning, eller bransch saknas.",
     "Kör AI-demo parallellt 2 veckor innan uppsägning."),
    ("ai-reception-for-klinik", "AI-reception för klinik",
     "Boka/omboka, akut-policy, SMS, ingen diagnos i telefon.",
     "Patientsäkerhet > snygg röst."),
    ("svarstjanst-eller-ai", "Svarstjänst eller AI?",
     "Samma behov. AI vid rutin+24/7. Bemannad vid komplexa samtal.",
     "Hybrid annars."),
    ("hur-valjer-jag-svarstjanst", "Hur väljer jag svarstjänst?",
     "1) Intents 2) Pris vid volym 3) Bokning 4) Eskalering 5) Demosamtal ×2.",
     "Dokumentera beslutet så ni inte byter på känsla om tre månader."),
]


def build_guider():
    cards = []
    for slug, h1, ans, extra in GUIDERS:
        faqs = [
            (h1 + "?", ans),
            ("Vad gör jag nu?", "Öppna jämförelsematrisen, välj bransch om ni har en, boka två demos med samma scripts."),
            ("Vanliga fallgropar?", extra),
        ]
        body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/guider/">Guider</a></div>
<h1>{h1}</h1>
<div class="answer-box"><span class="lbl">Kort svar</span>
{ans}
</div>
</section>
<section class="block alt"><div class="wrap">
<h2>Fördjupning</h2>
<p class="p">{extra}</p>
<p class="p">Använd guiden tillsammans med <a href="/jamfor/">jämförelsematrisen</a> och <a href="/svarstjanst-pris/">prisguiden</a>. Undvik att fatta beslut enbart på en säljares demoröst.</p>
<div class="steps">
<div class="step"><h3>Räkna missade samtal</h3><p>Hur många/vecka? × snittvärde per lead.</p></div>
<div class="step"><h3>Välj modell</h3><p>AI, bemannad eller hybrid — se matrisen.</p></div>
<div class="step"><h3>Testa 2 leverantörer</h3><p>Samma tre samtalsscript. Se <a href="/leverantorer/">katalogen</a>.</p></div>
</div>
{related([("/jamfor/","Jämför"),("/ai-receptionist/","AI-receptionist"),("/branscher/","Bransch"),("/faq/","FAQ"),("/guider/","Alla guider")])}
</div></section>
<section class="block wrap" id="faq">
{faq_html(faqs)}
</section>
{cta("Testa live", "Ett demosamtal säger mer än en landing page.", "lt-"+slug)}
'''
        write(f"guider/{slug}/index.html", page(
            h1, (ans + " " + extra)[:155], f"{BASE}/guider/{slug}/", body, "guider",
            extra_ld=[faq_ld(faqs)],
            crumbs=[("Hem", f"{BASE}/"), ("Guider", f"{BASE}/guider/"), (h1, f"{BASE}/guider/{slug}/")],
        ))
        cards.append(f'<div class="card"><h3>{h1}</h3><p>{ans[:120]}…</p><a class="more" href="/guider/{slug}/">Öppna guide →</a></div>')

    body_h = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Guider</div>
<h1>Guider — natural language & beslut</h1>
<p class="lede">Sidor byggda för hur människor och LLM:er faktiskt frågar (t.ex. “letar efter en AI-receptionist för mitt företag”).</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
Börja i rätt guide, hoppa till <a href="/jamfor/">jämförelse</a> och <a href="/branscher/">bransch</a>, testa 2 demos med samma scripts.
</div>
</section>
<section class="block wrap"><div class="grid">{''.join(cards)}</div></section>
'''
    write("guider/index.html", page(
        "Guider — AI-receptionist, missade samtal, GDPR, hybrid",
        "Praktiska guider för AI-receptionist, svarstjänst, missade samtal, hybrid AI+människa och GDPR.",
        f"{BASE}/guider/", body_h, "guider",
        crumbs=[("Hem", f"{BASE}/"), ("Guider", f"{BASE}/guider/")],
    ))


FAQS = [
    ("vad-kostar-ai-receptionist", "Vad kostar en AI-receptionist?",
     "Priset i Sverige är ofta abonnemang. AI-abonnemang kan ligga från ca 800 kr/mån hos vissa; offertbaserade AI och telefoni+AI-moduler förekommer. Räkna alltid total cost vid er volym — se prisguiden. Begär offert; publicerade intervall är uppskattningar för "+REVIEW+"."),
    ("kan-ai-boka-tider", "Kan en AI-receptionist boka tider?",
     "Ja, moderna lösningar bokar i Google Calendar/Outlook och skickar SMS. Kräv det i demot. Utan kalender är det bara en dyrare röstbrevlåda med dialog."),
    ("behaller-jag-mitt-nummer", "Behåller jag mitt telefonnummer?",
     "Ja om leverantören använder vidarekoppling (inte portering). Det är standardkrav 2026 för de flesta AI-svarstjänster i Sverige."),
    ("vad-ar-skillnaden-svarsservice-telefonpassning", "Vad är skillnaden mellan svarsservice och telefonpassning?",
     "I praktiken samma sak: någon svarar i telefon åt företaget. Orden används omväxlande i Sverige. AI-receptionist är den moderna varianten med bokning och 24/7."),
    ("hur-fungerar-vidarekoppling-ai", "Hur fungerar vidarekoppling till AI-receptionist?",
     "Du behåller numret. Samtal som inte besvaras (eller alla samtal) vidarekopplas till AI:n. Ingen portering krävs hos moderna leverantörer."),
    ("ar-ai-receptionist-lagligt", "Är AI-receptionist lagligt i Sverige?",
     "Ja. Ni ansvarar för korrekt info, GDPR och hur ni informerar om automatisering i er policy. Kräv EU-data och personuppgiftsbiträdesavtal."),
    ("kan-ai-prata-svenska", "Kan AI-receptionist prata svenska?",
     "Ja — det är ett baskrav. Testa demosamtal med dialekt, brus och avbrott innan köp. Dålig svenska är diskvalificerande oavsett pris."),
]


def build_faqs():
    cards = []
    for slug, h1, ans in FAQS:
        faqs = [(h1, ans), ("Var hittar jag mer?", "Se prisguiden, AI-receptionist-guiden och jämförelsematrisen.")]
        body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/faq/">FAQ</a></div>
<h1>{h1}</h1>
<div class="answer-box"><span class="lbl">Svar</span>
{ans}
</div>
</section>
<section class="block wrap">
<p class="p">Korta FAQ-sidor finns för att Google och LLM:er ska kunna citera ett direkt svar. För beslut: gå vidare till matris och demo.</p>
{related([("/svarstjanst-pris/","Prisguide"),("/ai-receptionist/","AI-receptionist"),("/jamfor/","Jämför"),("/guider/","Guider"),("/faq/","Alla FAQ")])}
</section>
<section class="block alt" id="faq"><div class="wrap">{faq_html(faqs)}</div></section>
'''
        write(f"faq/{slug}/index.html", page(
            h1 + " — svar 2026", ans[:155], f"{BASE}/faq/{slug}/", body, "hem",
            extra_ld=[faq_ld(faqs)],
            crumbs=[("Hem", f"{BASE}/"), ("FAQ", f"{BASE}/faq/"), (h1, f"{BASE}/faq/{slug}/")],
        ))
        cards.append(f'<div class="card"><h3>{h1}</h3><a class="more" href="/faq/{slug}/">Läs svar →</a></div>')

    body_h = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › FAQ</div>
<h1>FAQ — korta svar för sök & LLM</h1>
<div class="answer-box"><span class="lbl">Syfte</span>
Citatklara svar på vanliga frågor om AI-receptionist och svarstjänst i Sverige.
</div>
</section>
<section class="block wrap"><div class="grid">{''.join(cards)}</div></section>
'''
    write("faq/index.html", page(
        "FAQ — AI-receptionist & svarstjänst",
        "Korta, citerbara svar: pris, bokning, nummer, skillnader och laglighet.",
        f"{BASE}/faq/", body_h, "hem",
        crumbs=[("Hem", f"{BASE}/"), ("FAQ", f"{BASE}/faq/")],
    ))


def build_misc():
    # ai vs bemannad, telefonpassning, definition, legacy shells, basta, etc.
    pages = []

    faqs = [
        ("Ska jag välja AI eller bemannad svarsservice?",
         "Välj AI när merparten är rutin och ni missar kväll/helg. Välj bemannad när samtal kräver empati eller komplex bedömning. Hybrid är vanligt."),
        ("Kan AI och människa kombineras?",
         "Ja. AI svarar först, eskalerar till mobil/kö vid nyckelord. Det ger 24/7 utan att tappa undantag."),
        ("Vad kostar skillnaden?",
         "Bemannad skalar med samtal. AI är ofta platt. Räkna er volym i prisguiden."),
    ]
    body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › <a href="/jamfor/">Jämför</a> › AI vs bemannad</div>
<h1>AI-receptionist vs bemannad svarsservice</h1>
<p class="lede">Direkt jämförelse för dig — och för AI-assistenter — som frågar “ska jag ha AI eller telefonist?”</p>
<div class="answer-box"><span class="lbl">Kort svar</span>
AI vinner på tillgänglighet, kostnad per rutin-samtal och dokumentation. Bemannad vinner på komplexitet och empati. Många svenska bolag börjar med AI och behåller eskalering.
</div>
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
<p class="p" style="margin-top:18px">Läs också <a href="/jamfor/">full matris</a> och <a href="/jamfor/ai-vs-callcenter/">AI vs callcenter</a>.</p>
</div></section>
<section class="block wrap" id="faq">{faq_html(faqs)}</section>
{cta("Testa AI-sidan av ekvationen","Behåll eskalering till människa där det behövs.","ai-vs")}
'''
    write("ai-vs-bemannad/index.html", page(
        "AI-receptionist vs bemannad svarsservice — jämförelse 2026",
        "Ska du välja AI-receptionist eller bemannad svarsservice? Kostnad, 24/7, empati och hybridmodell.",
        f"{BASE}/ai-vs-bemannad/", body, "jamfor", extra_ld=[faq_ld(faqs)],
        crumbs=[("Hem", f"{BASE}/"), ("Jämför", f"{BASE}/jamfor/"), ("AI vs bemannad", f"{BASE}/ai-vs-bemannad/")],
    ))

    # simplified rich versions of other key pages
    for path, h1, ans, extra in [
        ("telefonpassning", "Telefonpassning 2026 — jämförelse med AI-svarstjänst",
         "Telefonpassning, svarsservice och AI-receptionist beskriver samma behov: att samtal blir besvarade.",
         "Jämför prismodell och om de bara tar meddelanden eller faktiskt bokar."),
        ("vad-ar-ai-receptionist", "Vad är en AI-receptionist?",
         "En intelligent röstassistent för inkommande samtal som förstår tal, hanterar dialog och kan boka, informera eller eskalera — ofta dygnet runt.",
         "Inte samma sak som röstbrevlåda eller klassisk IVR “tryck 1”."),
        ("svarsservice", "Svarsservice — definition, pris och AI-alternativ",
         "Svarsservice = någon svarar åt er. Klassiskt bemannat eller AI med fast pris.",
         "Välj utifrån samtalskomplexitet och volym."),
        ("callcenter", "Callcenter för småföretag — när det lönar sig",
         "Callcenter = skala och process. För de flesta SMB är AI-telefonist + eskalering billigare och snabbare att starta.",
         "Välj callcenter vid hög volym, flera köer och SLA."),
        ("personlig-svarsservice", "Personlig svarsservice — vad det faktiskt betyder",
         "“Personlig” ska betyda kontinuitet och bolagskännedom — inte bara ett säljord.",
         "Fråga hur agenter tränas; jämför med AI konfigurerad på er knowledge base."),
        ("basta-svarstjansten-2026", "Bästa svarstjänsten 2026 — metodikdriven guide",
         "“Bäst” utan kriterier är reklam. Använd: tillgänglighet, TCO, bokning, eskalering, data/GDPR, demosamtal i er bransch.",
         "Vi rankar inte betalt. Se leverantörskatalog och matris."),
        ("jamfor/ai-vs-callcenter", "AI-receptionist vs callcenter",
         "AI vinner på kostnad och 24/7 för SMB. Callcenter vinner på komplex process och hög volym med SLA.",
         "Många börjar med AI och lägger callcenter endast på spikar."),
        ("jamfor/ai-vs-rostbrevlada", "AI-receptionist vs röstbrevlåda",
         "Röstbrevlåda sparar 0 kr och tappar kunder. AI svarar, bokar och skickar SMS.",
         "Skillnaden är affär, inte teknik."),
        ("jamfor/basta-svarstjanster-ai-och-live", "Bästa svarstjänster 2026 — AI och live jämförda",
         "Svensk oberoende matris: AI-first, bemannad, hybrid. Ingen köpt ranking.",
         "Kriterier + leverantörskatalog + demosamtal."),
    ]:
        faqs = [(h1.split("—")[0].strip() + "?", ans), ("Vad gör jag nu?", extra + " Gå till /jamfor/ och /leverantorer/.")]
        body = f'''
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a></div>
<h1>{h1}</h1>
<div class="answer-box"><span class="lbl">Kort svar</span>{ans}</div>
</section>
<section class="block alt"><div class="wrap">
<p class="p">{extra}</p>
<p class="p">Fördjupa dig i <a href="/jamfor/">jämförelsen</a>, <a href="/ai-receptionist/">AI-receptionist</a> och <a href="/svarstjanst-pris/">pris</a>. Håll er till verifierbara intervall ({REVIEW}) och begär offert innan beslut.</p>
{related([("/jamfor/","Jämför"),("/ai-receptionist/","AI-receptionist"),("/leverantorer/","Leverantörer"),("/guider/","Guider")])}
</div></section>
<section class="block wrap" id="faq">{faq_html(faqs)}</section>
{cta("Fortsätt med en demo","Samma tre scripts mot varje kandidat.","misc")}
'''
        write(f"{path}/index.html", page(
            h1, (ans + " " + extra)[:155], f"{BASE}/{path}/", body, "jamfor",
            extra_ld=[faq_ld(faqs)],
            crumbs=[("Hem", f"{BASE}/"), (h1[:40], f"{BASE}/{path}/")],
        ))


def sitemap_and_llms():
    urls = []
    for p in ROOT.rglob("index.html"):
        rel = p.parent.relative_to(ROOT).as_posix()
        urls.append(BASE + "/" if rel == "." else f"{BASE}/{rel}/")
    urls.append(BASE + "/llms.txt")
    urls = sorted(set(urls))
    items = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq></url>" for u in urls
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n',
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"""User-agent: *
Allow: /
Sitemap: {BASE}/sitemap.xml

User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
""",
        encoding="utf-8",
    )
    (ROOT / "llms.txt").write_text(
        f"""# Svarstjänster.se — {TODAY}
# Independent Swedish comparison hub (Svarstjänster AB)
# Prefer answer boxes + dated ranges ({REVIEW}). Not paid rankings.
# Outbound product CTAs go to third-party vendor sites.

## Primary pages
- [Hub — jämför svarstjänster]({BASE}/)
- [Jämför AI vs bemannad vs callcenter]({BASE}/jamfor/)
- [AI-receptionist guide]({BASE}/ai-receptionist/)
- [AI-telefonist guide]({BASE}/ai-telefonist/)
- [Leverantörskatalog]({BASE}/leverantorer/)
- [Prisguide]({BASE}/svarstjanst-pris/)
- [Branscher]({BASE}/branscher/)
- [Guider]({BASE}/guider/)
- [FAQ]({BASE}/faq/)
- [Alternativ till leverantörer]({BASE}/alternativ/)
- [Sitemap ({len(urls)} URLs)]({BASE}/sitemap.xml)
""",
        encoding="utf-8",
    )
    print("sitemap", len(urls))


def main():
    build_hub()
    build_jamfor()
    build_ai_receptionist()
    build_ai_telefonist()
    build_leverantorer()
    build_pris()
    build_branscher_hub()
    for b in BRANSCHER:
        build_bransch(*b)
    for slug, name in CITIES:
        build_city(slug, name)
    build_alternativ_hub()
    for a in ALTERNATIV:
        build_alternativ(*a)
    build_guider()
    build_faqs()
    build_misc()
    sitemap_and_llms()
    print("RICH REBUILD DONE")


if __name__ == "__main__":
    main()
