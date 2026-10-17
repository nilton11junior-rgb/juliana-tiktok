#!/usr/bin/env python3
"""Renderiza os carrosséis do TikTok da Juliana (1080x1920, 9:16).

Uso (na raiz do projeto):
  python3 src/render.py conteudo/calendario/semana-2026-10-12.json
  python3 src/render.py conteudo/calendario/semana-2026-10-12.json --post seg-erros-preco

Cada slide usa uma imagem de fundo de imagens/<id-do-post>/<arquivo> (gerada no ChatGPT).
A arte da oferta (marca/oferta-final.png) entra SEMPRE como último slide, automaticamente.
Saída: criativos/gerados/<semana>/<id>/slide-NN.png e slide-NN.jpg"""
import base64, html, json, re, sys
from pathlib import Path
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
W, H = 1080, 1920
OFERTA = ROOT / "marca" / "oferta-final.png"
FONTES = ROOT / "marca" / "fontes"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


FONT_CSS = "".join(
    f"@font-face{{font-family:'P';src:url({b64(FONTES / f, 'font/ttf')});font-weight:{w}}}"
    for f, w in [("Poppins-Medium.ttf", 500), ("Poppins-Bold.ttf", 700)]
)

CSS = FONT_CSS + """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:'P',sans-serif;color:#1d1412;
 background:linear-gradient(160deg,#f6d9cf,#e9b8a8)}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.shade{position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(rgba(0,0,0,.28),rgba(0,0,0,0))}
.zona{position:absolute;left:90px;right:120px;top:430px;display:flex;flex-direction:column;align-items:center;gap:22px}
.caixa{background:#fff;border-radius:26px;padding:30px 40px;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.18)}
.capa .caixa{font-size:66px;line-height:1.16;font-weight:700}
.rosa{background:#e2336b;color:#fff;font-size:44px;line-height:1.22;font-weight:700;border-radius:22px;padding:20px 34px;text-align:center}
em{font-style:normal;color:#e2336b}
.rosa em{color:#fff;text-decoration:underline}
.item .caixa,.lista .caixa,.prova .caixa{text-align:left;width:100%}
.num{width:96px;height:96px;border-radius:50%;background:#e2336b;color:#fff;font-weight:700;font-size:48px;
 display:flex;align-items:center;justify-content:center;margin-bottom:18px}
h2{font-size:60px;line-height:1.14;font-weight:700}
.texto{font-size:42px;line-height:1.36;font-weight:500;margin-top:18px;color:#3a2b27}
.lista h2{margin-bottom:10px}
.linha{font-size:44px;line-height:1.3;font-weight:500;margin-top:20px;display:flex;gap:18px}
.linha b{font-weight:700;flex:none}
.prova .caixa{text-align:center}
.grande{font-size:84px;line-height:1.08;font-weight:700}
.arraste{position:absolute;left:0;right:0;bottom:420px;text-align:center}
.arraste span{background:rgba(255,255,255,.92);border-radius:40px;padding:14px 34px;font-size:30px;font-weight:700;letter-spacing:.06em}
"""


def fmt(t):
    t = html.escape(t or "").replace("\n", "<br>")
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)


def corpo(s):
    t = s["tipo"]
    if t == "capa":
        out = f'<div class="caixa">{fmt(s["titulo"])}</div>'
        if s.get("destaque"):
            out += f'<div class="rosa">{fmt(s["destaque"])}</div>'
        return "capa", out
    if t == "item":
        return "item", (f'<div class="caixa"><div class="num">{html.escape(s["num"])}</div>'
                        f'<h2>{fmt(s["titulo"])}</h2><div class="texto">{fmt(s["texto"])}</div></div>')
    if t == "lista":
        linhas = "".join(f'<div class="linha"><b>{html.escape(s.get("marca", "✅"))}</b><span>{fmt(l)}</span></div>'
                         for l in s["linhas"])
        return "lista", f'<div class="caixa"><h2>{fmt(s["titulo"])}</h2>{linhas}</div>'
    if t == "prova":
        out = f'<div class="caixa"><div class="grande">{fmt(s["titulo"])}</div>'
        if s.get("texto"):
            out += f'<div class="texto">{fmt(s["texto"])}</div>'
        return "prova", out + "</div>"
    raise ValueError(f"tipo de slide desconhecido: {t}")


def slide_html(s, post_id, primeiro):
    classe, conteudo = corpo(s)
    img = ROOT / "imagens" / post_id / s.get("imagem", "")
    if s.get("imagem") and img.is_file():
        bg = f'<div class="bg" style="background-image:url({b64(img, "image/jpeg" if img.suffix.lower() in (".jpg", ".jpeg") else "image/png")})"></div><div class="shade"></div>'
    else:
        print(f"   AVISO: sem imagem de fundo ({post_id}/{s.get('imagem')}), usando fundo liso")
        bg = ""
    arraste = '<div class="arraste"><span>ARRASTA PRO LADO →</span></div>' if primeiro else ""
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{bg}'
            f'<div class="zona {classe}">{conteudo}</div>{arraste}</body></html>')


def oferta(destino):
    """Arte da oferta em 9:16: imagem inteira no centro, sobre ela mesma desfocada."""
    # a arte inteira fica dentro da faixa central 3:4 (o TikTok corta topo e rodapé de fotos 9:16)
    arte = Image.open(OFERTA).convert("RGB")
    fundo = arte.resize((W, H)).filter(ImageFilter.GaussianBlur(40))
    alt = 1380
    frente = arte.resize((int(arte.width * alt / arte.height), alt), Image.LANCZOS)
    fundo.paste(frente, ((W - frente.width) // 2, (H - alt) // 2))
    fundo.save(destino)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    so = sys.argv[sys.argv.index("--post") + 1] if "--post" in sys.argv else None
    data = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for post in data["posts"]:
            if so and post["id"] != so:
                continue
            d = ROOT / "criativos" / "gerados" / data["semana"] / post["id"]
            d.mkdir(parents=True, exist_ok=True)
            for old in d.glob("slide-*"):
                old.unlink()
            for i, s in enumerate(post["slides"]):
                pg.set_content(slide_html(s, post["id"], i == 0))
                pg.wait_for_timeout(150)
                pg.screenshot(path=str(d / f"slide-{i+1:02d}.png"))
            n = len(post["slides"]) + 1
            oferta(d / f"slide-{n:02d}.png")
            for png in sorted(d.glob("slide-*.png")):
                Image.open(png).convert("RGB").save(png.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
            print(f"ok {post['id']}: {n} slides (último = oferta)")
        b.close()


if __name__ == "__main__":
    main()
