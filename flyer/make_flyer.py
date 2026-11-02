"""Flyer (A5 PDF + PNG), invitation email (HTML) and short messages, all pointing to the site.

    python make_flyer.py                                   # the GitHub Pages address
    python make_flyer.py --url https://untoitpourmoi.org/  # once the domain is bought

Writes into flyer/out/. The email's pictures must be online, so it also writes them to docs/flyer/
(hero.jpg, qr.png): they go live with the next push of the site.
Needs: segno, zxing-cpp, Pillow, playwright (uses the installed Edge).
"""
import argparse, html, pathlib
from PIL import Image
import zxingcpp
from playwright.sync_api import sync_playwright
from qr_house import house_qr

HERE = pathlib.Path(__file__).resolve().parent
DOCS = HERE.parent / "docs"
OUT = HERE / "out"
HELLOASSO = "https://www.helloasso.com/associations/un-toit-pour-moi/formulaires/1"
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@1,9..144,500'
         '&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">')

HEADLINE = "Ils ont un toit.<br>Offrons-leur <em>un jardin</em>."
PITCH = ("À la MAS Un Toit pour Moi vivent des jeunes adultes en situation de handicap. "
         "Nous voulons leur offrir un jardin thérapeutique&nbsp;: sentir la lavande, toucher les feuilles, "
         "écouter l'eau, profiter du soleil.")


def flyer_html(url, shown, qr_svg):
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">{FONTS}<style>
@page {{ size: 148mm 210mm; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; }}
body {{ width: 148mm; height: 210mm; overflow: hidden; font-family: Manrope, sans-serif; color: #1d231e; background: #f3f0e6;
        display: flex; flex-direction: column; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
em {{ font-family: Fraunces, Georgia, serif; font-style: italic; font-weight: 500; }}
.top {{ position: relative; height: 102mm; color: #fff; padding: 9mm 10mm 8mm; display: flex; flex-direction: column; justify-content: space-between;
        background: linear-gradient(180deg, rgba(12,28,19,.35) 0%, rgba(12,28,19,0) 28%, rgba(12,28,19,.15) 50%, rgba(12,28,19,.88) 100%),
                    url("../../docs/images/hero.webp") 50% 62% / cover; }}
.brand {{ display: flex; align-items: center; justify-content: space-between; }}
.logo {{ width: 21mm; height: 21mm; border-radius: 5mm; background: #fff url("../../docs/images/logo.webp") center / 92% no-repeat;
         box-shadow: 0 2mm 6mm rgba(0,0,0,.25); }}
.pill {{ font-size: 7.4pt; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; padding: 1.6mm 3.6mm; border-radius: 99px;
         background: rgba(12,28,19,.55); border: .3mm solid rgba(255,255,255,.35); }}
h1 {{ margin: 0; font-size: 27pt; line-height: 1.04; letter-spacing: -.02em; font-weight: 800; text-shadow: 0 1mm 4mm rgba(0,0,0,.35); }}
h1 em {{ color: #f4b223; font-size: 1.08em; }}
.mid {{ padding: 6.5mm 10mm 0; }}
.mid p {{ margin: 0; font-size: 10.4pt; line-height: 1.5; }}
.mid strong {{ color: #1f3a2a; }}
.chips {{ display: flex; gap: 2mm; margin-top: 4mm; flex-wrap: wrap; }}
.chips span {{ font-size: 7.6pt; font-weight: 700; color: #1f3a2a; background: #fbf9f3; border: .3mm solid #dfdacb; border-radius: 99px;
               padding: 1.3mm 3.2mm; display: inline-flex; align-items: center; gap: 1.4mm; }}
.chips i {{ width: 2mm; height: 2mm; border-radius: 50%; display: inline-block; }}
.scan {{ flex: 1; display: flex; align-items: center; gap: 6mm; padding: 2mm 10mm 3mm; }}
.scan svg {{ width: 50mm; flex: none; }}
.scan h2 {{ margin: 0 0 2mm; font-size: 15pt; line-height: 1.12; color: #1f3a2a; letter-spacing: -.01em; }}
.scan h2 em {{ color: #5b4a91; }}
.scan p {{ margin: 0 0 3mm; font-size: 8.6pt; line-height: 1.45; color: #5b6259; }}
.url {{ display: inline-block; font-weight: 800; font-size: 8.6pt; color: #2f6b43; border-bottom: .5mm solid #f4b223; padding-bottom: .4mm; }}
.goal {{ margin-top: 3.5mm; display: flex; align-items: center; gap: 2mm; font-size: 8pt; font-weight: 700; color: #1f3a2a; }}
.goal b {{ background: #f4b223; color: #13281c; border-radius: 99px; padding: 1mm 3mm; font-size: 8.4pt; }}
.foot {{ background: #13281c; color: #c9ddb8; font-size: 7.6pt; padding: 3.6mm 10mm; display: flex; justify-content: space-between; align-items: center; }}
.foot strong {{ color: #fff; }}
</style></head><body>
<div class="top">
  <div class="brand"><div class="logo"></div><div class="pill">Projet de jardin thérapeutique</div></div>
  <h1>{HEADLINE}</h1>
</div>
<div class="mid">
  <p>{PITCH.replace("MAS Un Toit pour Moi", "<strong>MAS Un Toit pour Moi</strong>")}</p>
  <div class="chips">
    <span><i style="background:#2f6b43"></i>Allées accessibles</span>
    <span><i style="background:#5b4a91"></i>Plantes à sentir et toucher</span>
    <span><i style="background:#4a8fb5"></i>Eau et ombre</span>
  </div>
</div>
<div class="scan">
  {qr_svg}
  <div>
    <h2>Scannez, découvrez,<br><em>faites-le pousser</em></h2>
    <p>Le jardin en images, notre histoire depuis la première pierre, et le don en ligne en deux minutes.</p>
    <a class="url" href="{html.escape(url)}">{html.escape(shown)}</a>
    <div class="goal"><b>Objectif 50&nbsp;000&nbsp;€</b> chaque don compte</div>
  </div>
</div>
<div class="foot"><span><strong>Association Un Toit pour Moi</strong></span><span>Dons sécurisés via HelloAsso · 100&nbsp;% reversés à l'association</span></div>
</body></html>"""


def email_html(url, shown):
    img = url.rstrip("/") + "/flyer/"
    btn = ("display:inline-block;font-family:Manrope,Arial,sans-serif;font-weight:800;font-size:16px;text-decoration:none;"
           "border-radius:999px;padding:14px 28px;")
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Ils ont un toit. Offrons-leur un jardin.</title>{FONTS}</head>
<body style="margin:0;padding:0;background:#f3f0e6;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f3f0e6;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#fbf9f3;border-radius:18px;overflow:hidden;font-family:Manrope,Arial,sans-serif;color:#1d231e;">
  <tr><td><a href="{url}"><img src="{img}hero.jpg" width="600" alt="Le futur jardin de la MAS Un Toit pour Moi" style="display:block;width:100%;height:auto;border:0;"></a></td></tr>
  <tr><td style="padding:30px 36px 6px;">
    <div style="font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#2f6b43;">Projet de jardin thérapeutique</div>
    <h1 style="margin:10px 0 0;font-size:32px;line-height:1.1;font-weight:800;color:#1f3a2a;letter-spacing:-.02em;">
      Ils ont un toit.<br>Offrons-leur <span style="font-family:Fraunces,Georgia,serif;font-style:italic;font-weight:500;color:#5b4a91;">un jardin</span>.</h1>
  </td></tr>
  <tr><td style="padding:14px 36px 0;font-size:16px;line-height:1.6;">
    <p style="margin:0 0 12px;">Bonjour,</p>
    <p style="margin:0 0 12px;">À la <strong>MAS Un Toit pour Moi</strong> vivent des jeunes adultes en situation de handicap. Ce lieu, nous l'avons construit
      pour eux, pierre après pierre&nbsp;: c'est aujourd'hui leur chez-eux.</p>
    <p style="margin:0 0 12px;">Il leur manque un jardin. Un vrai, pensé pour eux&nbsp;: des allées où l'on circule en fauteuil, des plantes à sentir
      et à toucher, le bruit de l'eau, de l'ombre l'été et du soleil l'hiver.</p>
    <p style="margin:0;">Découvrez le projet en images et notre histoire depuis la première pierre&nbsp;:</p>
  </td></tr>
  <tr><td align="center" style="padding:24px 36px 8px;">
    <a href="{url}" style="{btn}background:#f4b223;color:#13281c;">Découvrir le projet</a>
  </td></tr>
  <tr><td align="center" style="padding:0 36px 6px;font-size:13px;color:#5b6259;">ou directement&nbsp;: <a href="{HELLOASSO}" style="color:#2f6b43;font-weight:700;">faire un don sur HelloAsso</a></td></tr>
  <tr><td style="padding:22px 36px 0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef3e6;border-radius:14px;"><tr>
      <td width="120" style="padding:14px 6px 14px 16px;"><img src="{img}qr.png" width="104" alt="QR code vers le site" style="display:block;border:0;"></td>
      <td style="padding:14px 18px 14px 8px;font-size:14px;line-height:1.5;color:#1f3a2a;">
        <strong>Sur votre téléphone&nbsp;?</strong> Scannez la petite maison.<br>
        <a href="{url}" style="color:#2f6b43;font-weight:700;">{html.escape(shown)}</a></td>
    </tr></table>
  </td></tr>
  <tr><td style="padding:22px 36px 30px;font-size:16px;line-height:1.6;">
    <p style="margin:0 0 12px;">Chaque don, même petit, fait pousser une plante, une allée, <strong>un sourire</strong>. Et transférer ce message à vos proches
      nous aide tout autant.</p>
    <p style="margin:0;">Merci du fond du cœur,<br><strong style="color:#1f3a2a;">L'association Un Toit pour Moi</strong></p>
  </td></tr>
  <tr><td style="background:#13281c;color:#c9ddb8;font-size:12px;padding:14px 36px;">Objectif&nbsp;: 50&nbsp;000&nbsp;€ · Dons sécurisés via HelloAsso, 100&nbsp;% reversés à l'association</td></tr>
</table></td></tr></table></body></html>"""


def messages(url):
    return f"""OBJET DU MAIL
Ils ont un toit. Offrons-leur un jardin 🌿

TEXTE DU MAIL (version texte simple)
Bonjour,

À la MAS Un Toit pour Moi vivent des jeunes adultes en situation de handicap. Ce lieu, nous l'avons construit pour eux, pierre après pierre : c'est aujourd'hui leur chez-eux.

Il leur manque un jardin. Un vrai, pensé pour eux : des allées où l'on circule en fauteuil, des plantes à sentir et à toucher, le bruit de l'eau, de l'ombre l'été et du soleil l'hiver.

Découvrez le projet en images et notre histoire depuis la première pierre :
{url}

Chaque don, même petit, fait pousser une plante, une allée, un sourire. Et transférer ce message à vos proches nous aide tout autant.

Merci du fond du cœur,
L'association Un Toit pour Moi

MESSAGE COURT (WhatsApp, SMS, réseaux sociaux)
🏡 Ils ont un toit. Offrons-leur un jardin 🌿
Les jeunes adultes de la MAS Un Toit pour Moi rêvent d'un jardin à sentir, toucher, écouter. Découvrez le projet et aidez-nous à le faire pousser : {url}

ENCORE PLUS COURT
Ils ont un toit, offrons-leur un jardin 🌿 {url}
"""


def check(png, url):
    got = [r.text for r in zxingcpp.read_barcodes(Image.open(png).convert("RGB"))]
    assert url in got, f"{png.name}: QR does not scan ({got})"
    print(f"  {png.name}: scans OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="https://untoitpourmoi.org/")
    url = ap.parse_args().url
    shown = url.split("://", 1)[-1].rstrip("/")
    OUT.mkdir(exist_ok=True)
    (DOCS / "flyer").mkdir(exist_ok=True)

    qr = house_qr(url)
    (OUT / "qr_maison.svg").write_text(qr, encoding="utf-8")
    (OUT / "flyer.html").write_text(flyer_html(url, shown, qr), encoding="utf-8")
    (OUT / "email.html").write_text(email_html(url, shown), encoding="utf-8")
    (OUT / "messages.txt").write_text(messages(url), encoding="utf-8")
    Image.open(DOCS / "images" / "hero.webp").convert("RGB").resize((1200, 626), Image.LANCZOS) \
        .save(DOCS / "flyer" / "hero.jpg", quality=84, optimize=True, progressive=True)

    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge")
        pg = b.new_page(viewport={"width": 1200, "height": 1600})
        pg.set_content(f'<body style="margin:0;background:transparent">{qr.replace("<svg ", "<svg width=1200 ", 1)}</body>')
        pg.locator("svg").screenshot(path=OUT / "qr_maison.png", omit_background=True)
        pg = b.new_page(viewport={"width": 560, "height": 794}, device_scale_factor=3)   # A5 at ~290 dpi
        pg.goto((OUT / "flyer.html").as_uri(), wait_until="networkidle")
        pg.pdf(path=OUT / "flyer.pdf", width="148mm", height="210mm", print_background=True)
        pg.screenshot(path=OUT / "flyer.png", full_page=False)
        b.close()
    q = Image.open(OUT / "qr_maison.png")
    q.resize((312, round(312 * q.height / q.width)), Image.LANCZOS).save(DOCS / "flyer" / "qr.png", optimize=True)   # 104 px wide in the mail, 3x

    for f in (OUT / "qr_maison.png", OUT / "flyer.png", DOCS / "flyer" / "qr.png"):
        check(f, url)
    print("written to", OUT)


main()
