#!/usr/bin/env python3
import re, urllib.request, ssl

ctx = ssl.create_default_context()
# corporate TLS intercept may need unverified
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")

home = get("https://svarstjanster.se/")
lev = get("https://svarstjanster.se/leverantorer/")
jam = get("https://svarstjanster.se/jamfor/")

checks = {
    "home_legalName": "legalName" in home,
    "home_no_utm_funnel": "utm_source=svarstjanster" not in home,
    "home_no_en_del_av": "en del av" not in home,
    "home_Se_leverantorer": "Se leverant" in home,
    "home_Svarstjanster_AB": "Svarstjänster AB" in home or "Svarstj" in home and "AB" in home,
    "lev_wecall": "wecall.se" in lev,
    "lev_skaala": "skaala.ai" in lev,
    "lev_noopener": "noopener" in lev,
    "jam_Besok_cta": "Besök" in jam or "Bes" in jam,
    "jam_competitor_host": any(x in jam for x in ("skaala.ai", "telink.se", "wecall.se", "lynes.io", "menodi.se")),
}
for k, v in checks.items():
    print(f"{k}={v}")

golds = re.findall(r'class="btn gold" href="([^"]+)"', home + jam)
print("gold_cta_hrefs", golds[:8])
