# DESIGN.md — svarstjanster.se

Vinkel: den neutrala jämförelsekatalogen för sökordet "svarstjänst/svarstjänster" —
tre typer (bemannad, callcenter, AI), vilken passar vem. Kvalitetsribba: ska stå
bredvid menodi.se, skaala.ai, telavox.se (sticky header, hero med dubbel-CTA,
80-110px sektionsrytm, feature-grid, numrerade steg, pris-/jämförelsetabell med
highlight, stats-band m. källrad, FAQ-accordion, avslutande CTA-band, kolumn-footer,
scroll-reveal, responsiv 768/480) — se användarens spec för fullständig lista.

## 1. Brand-identitet
**Färgtoken (redan i filen — låsta, mynta inga nya):**
`--bg:#faf6ef --card:#fffdf8 --ink:#1c2536 --ink2:#5a6478 --navy:#1f3a6e
--navy2:#2c4f94 --line:#e6dfd0 --gold:#b98b2e`
Cream-botten, navy för rubriker/CTA-primär, gold som accent (taggar, highlight-rad,
CTA-band-knapp) — aldrig som brödtext.

**Typografi:** humanist system-sans genomgående (`"Segoe UI",system-ui,-apple-system,sans-serif`)
för både rubrik och brödtext — inget Georgia/serif. Rubriker tight letter-spacing
(-.3 till -.5px), h1 `clamp(34px,5vw,56px)`. Detta är en jämförelsesajt, inte en
tidskrift — sans genomgående signalerar produkt/nytta, inte redaktionellt.

**Ton:** saklig, säljande utan utropstecken. Kort stycken (2-3 meningar). Siffror
alltid hedgade med datum ("uppskattning, juli 2026"). "Oberoende jämförelse" i
header-taglinen är ett löfte — inget i copy får motsäga det.

## 2. Sektionsplan (uppifrån-ner)
1. **Sticky halvtransparent header** — logo + ankare (Typer, Jämförelse, FAQ) + CTA-knapp
2. **Hero** — rubrik (problem→lösning), subline, primär-CTA ("Prova gratis") +
   sekundär-CTA ("Se jämförelsen", scrollar till #jamforelse), 2-3 trust-chips
   (t.ex. "Svensk tjänst", "Dygnet runt", "Ingen bindningstid")
3. **Tre typer av svarstjänst** — feature-grid, 3 kort m. inline-SVG-ikon (headset/
   byggnad/robot), redan skrivet innehåll behålls
4. **Så väljer du rätt svarstjänst** — 3 numrerade steg (behåll frågorna)
5. **Jämförelsen i korthet** — pristabell med highlight-rad på AI-svarstjänst-kolumnen
6. **Stats-band** — ENDAST det verifierade talet (se §3), källrad synlig, INGA
   kundcitat/ROI-siffror (de tillhör konkurrenternas produktsidor, inte denna
   neutrala katalog — skulle motsäga "oberoende")
7. **FAQ-accordion** — behåll 4 befintliga Q/A ordagrant
8. **Avslutande CTA-band** — navy bakgrund, upprepar hero-erbjudandet
9. **Flerkolumns-footer** — Kategorier / Om sajten / Menodi / Juridik

## 3. Behålls från nuvarande sida
- Alla 4 FAQ-svar ordagrant (redan hedgade "juli 2026") + FAQPage JSON-LD
- 3-typers-ramverket (bemannad/callcenter/AI) och hela jämförelsetabellen
- UTM-länkmönstret (`utm_source=svarstjanster&utm_medium=satellite&utm_campaign=...`,
  `rel="sponsored"`) på alla Menodi-länkar
- Prisintervallen (1 000-5 000 kr/mån + 15-35 kr/samtal) med disclaimer-raden
- Ingen kalkylator-JS finns på denna sida (den bor på receptionistkostnad.se) —
  bygg ingen ny, länka dit om det behövs
- Enda stat som får visas med siffra: "62% av samtal till småföretag besvaras
  aldrig av en människa" (411 Locals Small Business Phone Study) — källrad
  obligatorisk. Produktfakta får kompletteras utan källa: "Dygnet runt, alla
  dagar", "0 kr startavgift"

## 4. Mockup-bildplan (placeholders)
- Hero, höger om rubrik: skärmdump/illustration av telefonsamtal → bokning i
  kalender (visar "meddelande vs bokning"-skillnaden utan att bygga en till sektion)
- Typ-korten (3 st): liten inline-SVG-ikon per kort, inga foton
- Stats-bandet: ingen bild, bara stor siffra + källrad
- Ingen hero-produktskärmdump av Menodi-appen (sajten är neutral — appvisning hör
  hemma på menodi.se, inte på jämförelsekatalogen)

## 5. Differentiering mot de 10 andra satelliterna
- **aisvarstjanst.se / aitelefonsvarare.se** är AI-first produktsidor; denna sida
  är den enda som seriöst jämför AI MOT bemannad/callcenter — äger bredden av
  sökfrasen, inte AI-nischen
- **telefonpassningpris.se / receptionistkostnad.se** är pris-/kalkylator-vinklade;
  denna sida har bara en jämförelsetabell, ingen interaktiv kalkylator — hänvisar
  dit vid behov
- **telefonvaxelforetag.se / aitelefonvaxel.se / foretagsvaxel.se** handlar om
  växel/infrastruktur; denna sida handlar om svarshantering (personen/AI:n som
  svarar), inte teknisk växellösning — håll ordet "växel" borta ur H1/H2
