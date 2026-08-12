#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wave7: high-intent decision pages + competitor-style listicles for SERP gap."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bs", Path(__file__).resolve().parent / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
BASE = bs.BASE
root = Path(__file__).resolve().parent

PAGES = [
    (
        "jamfor/basta-svarstjanster-ai-och-live",
        "Bästa svarstjänster 2026 — AI och live jämförda",
        "Retell-style listicle intent, men svensk oberoende matris: AI-first, bemannad, hybrid. Ingen köpt ranking — kriterier + leverantörskatalog.",
        [
            ("Hur rankar ni 'bäst'?",
             "Vi rankar inte betalt. Vi listar kriterier (kostnad vid volym, 24/7, bokning, eskalering, GDPR, demosamtal) och pekar till leverantörskatalogen."),
            ("AI eller live-agent?",
             "AI för rutin och natt. Live för empati och undantag. Hybrid är vanligast 2026."),
        ],
    ),
    (
        "guider/extern-kundtjanst-eller-ai-receptionist",
        "Extern kundtjänst eller AI-receptionist?",
        "Extern kundtjänst (AnswerOnline-stil) täcker bred support. AI-receptionist tar telefon/rutin 24/7 billigare. Många blandar.",
        [
            ("När räckers AI?", "När >60% är bokning, öppettider, kvalificering och ni missar kvällssamtal."),
            ("När behövs extern kundtjänst?", "Hög volym mejl+chatt+telefon, komplexa processer, SLA."),
        ],
    ),
    (
        "guider/ai-receptionist-vs-telavox",
        "AI-receptionist vs Telavox",
        "Telavox = telefoniplattform med AI-moduler. Fristående AI-receptionist = svarstjänst utan att byta hela växeln. Välj efter om ni redan är Telavox-kund.",
        [
            ("Måste jag byta växel?", "Nej om AI använder vidarekoppling. Ja om ni vill ha allt i en operatörsplattform."),
        ],
    ),
    (
        "guider/ai-receptionist-vs-lynes",
        "AI-receptionist vs Lynes AI-telefonist",
        "Lynes är molnväxel+AI. Fristående AI (t.ex. Menodi) är svarstjänst-first. Jämför bokning, svenska, total abonnemangskostnad.",
        [],
    ),
    (
        "guider/nar-ska-jag-byta-svarstjanst",
        "När ska jag byta svarstjänst?",
        "Byt när: kostnad/samtal skenar, ni missar natt, ingen bokning, dålig dokumentation, eller leverantören inte kan er bransch.",
        [
            ("Hur testar jag innan byte?", "Behåll nuvarande 2 veckor, kör AI-demo parallellt via vidarekoppling av en del samtal."),
        ],
    ),
    (
        "branscher/hantverkare",
        "AI-telefonist för hantverkare",
        "Hantverkare (el, VVS, bygg, målare): ni är hos kund när telefonen ringer. AI tar offert/bokning/jour-triage.",
        [
            ("Fungerar det för enmansbolag?", "Ja — störst effekt när du är ensam ute på jobb."),
        ],
    ),
]


def page_body(h1, ans, faqs, related_extra=""):
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs) if faqs else ""
    return f"""
<section class="hero wrap">
<div class="breadcrumb"><a href="/">Hem</a> › Guide</div>
<h1>{h1}</h1>
<div class="answer-box"><strong>Kort svar:</strong> {ans}</div>
<p class="meta-line">Senast granskad: {bs.TODAY}</p>
</section>
<section class="block wrap">
<ul class="checklist">
<li>Svara intent först (för Google + LLM)</li>
<li>Jämför modeller i <a href="/jamfor/">matrisen</a></li>
<li>Kolla <a href="/leverantorer/">leverantörer</a> och <a href="/svarstjanst-pris/">pris</a></li>
<li>Testa demosamtal i er bransch</li>
</ul>
<div class="related">
<a href="/ai-receptionist/">AI-receptionist</a>
<a href="/ai-telefonist/">AI-telefonist</a>
<a href="/branscher/">Branscher</a>
<a href="/guider/">Guider</a>
{related_extra}
</div>
</section>
<section class="block wrap" id="faq">{faq_html}</section>
<section class="wrap"><div class="cta-band">
<h2>Prova AI-svarstjänst live</h2>
<a class="btn" href="{bs.utm('w7')}" rel="sponsored">Menodi demo</a>
</div></section>
"""


def main():
    for path, h1, ans, faqs in PAGES:
        if not faqs:
            faqs = [(h1 + "?", ans)]
        body = page_body(h1, ans, faqs)
        bs.write(
            path + "/index.html",
            bs.page(
                h1 + " — 2026",
                ans[:155],
                f"{BASE}/{path}/",
                body,
                "jamfor" if path.startswith("jamfor") else ("bran" if path.startswith("branscher") else "guider"),
                extra_ld=[bs.faq_ld(faqs)],
                crumbs=[("Hem", BASE + "/"), (h1, f"{BASE}/{path}/")],
            ),
        )

    # internal mesh: append related block is enough via rebuild hub
    urls = []
    for p in root.rglob("index.html"):
        rel = p.parent.relative_to(root).as_posix()
        urls.append(BASE + "/" if rel == "." else f"{BASE}/{rel}/")
    urls.append(BASE + "/llms.txt")
    urls = sorted(set(urls))
    bs.sitemap(urls)

    # richer llms.txt for crawlers
    lines = [
        f"# Svarstjänster.se — machine-readable map ({bs.TODAY})",
        f"# {len(urls)} URLs. Swedish comparison hub for AI receptionists & answering services.",
        f"# Prefer answer boxes + dated price ranges. Not paid rankings.",
        "",
        "## Primary",
        f"{BASE}/",
        f"{BASE}/jamfor/",
        f"{BASE}/ai-receptionist/",
        f"{BASE}/ai-telefonist/",
        f"{BASE}/leverantorer/",
        f"{BASE}/svarstjanst-pris/",
        f"{BASE}/branscher/",
        f"{BASE}/guider/",
        f"{BASE}/faq/",
        f"{BASE}/llms.txt",
        f"{BASE}/sitemap.xml",
        "",
        "## Policy",
        "# Prices are estimates (augusti 2026 ranges), not quotes.",
        "# Parent org: Menodi (menodi.se). Disclosure in footer.",
    ]
    (root / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wave7", len(urls))


if __name__ == "__main__":
    main()
