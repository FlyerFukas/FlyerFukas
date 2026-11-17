"""Profil README görsellerini üretir: baslik.svg, dersler-acik.svg, dersler-koyu.svg.

Renkler ve grafikler portföy sitesiyle aynı (Portfoy/app/globals.css, lib/acikKod.ts).
Çalıştırma: py -I assets/uret.py
"""
from pathlib import Path

KLASOR = Path(__file__).parent
YAZI = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"

TEMA = {
    "acik": dict(metin="#0f1b2d", soluk="#475467", vurgu="#12355b", veri="#b7791f", cizgi="#d5dde7", negatif="#475467"),
    "koyu": dict(metin="#e8edf4", soluk="#a7b3c4", vurgu="#8fb8e8", veri="#e0a64a", cizgi="#24324a", negatif="#a7b3c4"),
}

# (başlık, sonuç, grafik türü, veri, etiketler) — rakamlar istatistik-okul-projeleri raporlarından
PROJELER = [
    ("Portfolio optimisation", "Markowitz 0.35%/day vs 0.19% equal weight", "isaretli", [0.352, 0.191, -0.224], ["Markowitz", "Equal", "Min."]),
    ("Game theory as an LP", "Game value 0.513, 4 of 8 strategies used", "olasilik", [0, 0.0698, 0, 0, 0.3923, 0, 0.3062, 0.2317], [str(i) for i in range(1, 9)]),
    ("Dummy variables", "Faculty effect F = 14.41 > 2.98", "nokta", [5.6, 5.57, 3.31, 2.39], ["Sci.", "Eng.", "Lit.", "Econ."]),
    ("Remote work × department", "Effect flips sign by department", "isaretli", [0.25, -0.25, -1, 1], ["HR", "Fin.", "Mkt.", "IT"]),
    ("R programming", "32,735 flights, median 2 min early", "histogram", [1179, 18750, 4528, 2107, 1321, 1311, 828, 1118, 630, 956], []),
    ("Excel dashboard", "7,668 films, comedy leads", "yatay", [2233, 1699, 1483, 545, 440], ["Comedy", "Action", "Drama", "Crime", "Biography"]),
]

# Grafik alanı (hücre içi): genişlik 150, yükseklik 84; sitedeki 168x84 ölçeğinin dar hali.
SOL, SAG, UST, ALT, ETY = 4, 150, 8, 60, 75


def yazi(x, y, s, renk, boy: float = 9, anchor="middle", agirlik=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{renk}" font-size="{boy}" font-weight="{agirlik}" text-anchor="{anchor}">{s}</text>'


def cubuk(x, y, w, h, renk, i, kok_y, yatay=False):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{renk}"/>'


def grafik(tur, d, et, r):
    p = []
    if tur == "isaretli":
        ust = max(0, *d)
        olcek = (ALT - UST) / (ust - min(0, *d))
        sifir = UST + ust * olcek
        adim = (SAG - SOL) / len(d)
        for i, v in enumerate(d):
            h = abs(v) * olcek
            x, w = SOL + i * adim + adim * 0.22, adim * 0.56
            renk = r["negatif"] if v < 0 else (r["veri"] if v == ust else r["vurgu"])
            p.append(cubuk(x, sifir - h if v >= 0 else sifir, w, h, renk, i, sifir))
        p.append(f'<line x1="{SOL}" x2="{SAG}" y1="{sifir:.1f}" y2="{sifir:.1f}" stroke="{r["metin"]}" stroke-opacity=".5"/>')
        p += [yazi(SOL + i * adim + adim / 2, ETY, e, r["soluk"]) for i, e in enumerate(et)]
    elif tur == "olasilik":
        adim = (SAG - SOL) / len(d)
        eb = max(d)
        for i, v in enumerate(d):
            x, w = SOL + i * adim + adim * 0.2, adim * 0.6
            if v == 0:
                p.append(f'<circle cx="{x + w / 2:.1f}" cy="{ALT - 1.5}" r="1.5" fill="{r["cizgi"]}"/>')
            else:
                h = v / eb * (ALT - UST)
                p.append(cubuk(x, ALT - h, w, h, r["veri"] if v == eb else r["vurgu"], i, ALT))
        p.append(f'<line x1="{SOL}" x2="{SAG}" y1="{ALT}" y2="{ALT}" stroke="{r["metin"]}" stroke-opacity=".5"/>')
        p += [yazi(SOL + i * adim + adim / 2, ETY, e, r["soluk"]) for i, e in enumerate(et)]
    elif tur == "nokta":
        adim = (SAG - SOL) / len(d)
        eb = -(-max(d) // 1)
        p.append(f'<line x1="{SOL}" x2="{SAG}" y1="{ALT}" y2="{ALT}" stroke="{r["metin"]}" stroke-opacity=".5"/>')
        for i, v in enumerate(d):
            x = SOL + i * adim + adim / 2
            y = ALT - v / eb * (ALT - UST)
            p.append(f'<g><line x1="{x:.1f}" x2="{x:.1f}" y1="{ALT}" y2="{y:.1f}" stroke="{r["cizgi"]}" stroke-width="1.5"/>'
                     f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{r["veri"] if i == 0 else r["vurgu"]}"/></g>')
        p += [yazi(SOL + i * adim + adim / 2, ETY, e, r["soluk"]) for i, e in enumerate(et)]
    elif tur == "histogram":
        adim = (SAG - SOL) / len(d)
        eb = max(d)
        for i, v in enumerate(d):
            h = v / eb * (ALT - UST)
            x = SOL + i * adim + 0.6
            p.append(cubuk(x, ALT - h, adim - 1.2, h, r["veri"] if i < 2 else r["vurgu"], i, ALT))
        sx = SOL + 2 * adim
        p.append(f'<line x1="{SOL}" x2="{SAG}" y1="{ALT}" y2="{ALT}" stroke="{r["metin"]}" stroke-opacity=".5"/>')
        p.append(f'<line x1="{sx:.1f}" x2="{sx:.1f}" y1="{UST - 4}" y2="{ALT}" stroke="{r["soluk"]}" stroke-dasharray="2 2"/>')
        p.append(yazi(sx, ETY, "0 min", r["soluk"]))
        p.append(yazi(SAG, ETY, "delay →", r["soluk"], anchor="end"))
    elif tur == "yatay":
        satir = (ETY - UST + 2) / len(d)
        eb = max(d)
        bas = 54
        for i, v in enumerate(d):
            y = UST - 6 + i * satir
            p.append(yazi(bas - 4, y + satir * 0.62, et[i], r["soluk"], anchor="end"))
            p.append(cubuk(bas, y + satir * 0.18, v / eb * (SAG - bas), satir * 0.6, r["veri"] if i == 0 else r["vurgu"], i, 0, yatay=True))
    return "".join(p)


def dersler(tema):
    r = TEMA[tema]
    hg, hy, sutun = 600, 270, 2  # README ~830 px gösterilir: 2 sütunda yazı ~16 px kalır
    satir = -(-len(PROJELER) // sutun)
    gen, yuk = hg * sutun, hy * satir
    hucreler = []
    for k, (ad, sonuc, tur, d, et) in enumerate(PROJELER):
        ox, oy = (k % sutun) * hg, (k // sutun) * hy
        hucreler.append(
            f'<g transform="translate({ox + 24},{oy + 22})">'
            f'<g transform="translate(0,72) scale(2)">{grafik(tur, d, et, r)}</g>'
            + yazi(0, 22, ad, r["metin"], boy=25, anchor="start", agirlik=600)
            + yazi(0, 52, sonuc, r["soluk"], boy=19, anchor="start")
            + "</g>"
        )
    ayirici = "".join(
        f'<line x1="20" x2="{gen - 20}" y1="{j * hy}" y2="{j * hy}" stroke="{r["cizgi"]}"/>' for j in range(1, satir)
    )
    # Animasyon yok: GitHub mobil ve önizlemeler SVG'yi durağan çizebiliyor, çubuklar boş kalmasın.
    stil = ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {gen} {yuk}" width="{gen}" height="{yuk}" font-family="{YAZI}" role="img">'
        f"<title>Statistics coursework: six projects, each drawn from its own result</title>{stil}{ayirici}{''.join(hucreler)}</svg>"
    )


def baslik():
    gen, yuk = 1200, 250
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {gen} {yuk}" width="{gen}" height="{yuk}" font-family="{YAZI}" role="img">'
        "<title>Furkan Akduman, Applied AI and Automation</title>"
        f'<rect width="{gen}" height="{yuk}" rx="14" fill="#0b2545"/>'
        + yazi(56, 66, "Applied AI &amp; Automation", "#a9c8ec", boy=24, anchor="start", agirlik=600)
        + yazi(53, 128, "Furkan Akduman", "#f5f8fc", boy=60, anchor="start", agirlik=700)
        + yazi(56, 176, "I build AI systems that businesses can trust: agents, automations", "#f5f8fc", boy=24, anchor="start")
        + yazi(56, 210, "and data products with checks, audit trails and cost control built in.", "#f5f8fc", boy=24, anchor="start")
        + "</svg>"
    )


(KLASOR / "baslik.svg").write_text(baslik(), encoding="utf-8")
for t in TEMA:
    (KLASOR / f"dersler-{t}.svg").write_text(dersler(t), encoding="utf-8")
print("üretildi:", [p.name for p in KLASOR.glob("*.svg")])
