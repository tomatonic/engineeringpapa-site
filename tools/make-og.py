"""紹介ページ用の OG 画像（1200×630）を作る。

既存の og-examdashboard.png と同じ構図に揃える:
  左にアプリアイコン / 右に アプリ名（明朝）→ 金の罫 → キャッチ（角ゴ）→ Engineering Papa
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = "#F3EEE3"           # サイト共通の地色（og-examdashboard.png から抽出）
INK = "#2C2117"          # 見出し（Theme.onStageInk）
RULE = "#B8975E"         # 金の罫（Theme.accent）
LEAD = "#4A3D2C"         # キャッチ
FOOT = "#9C9384"         # 署名

MINCHO_W6 = ("/System/Library/Fonts/ヒラギノ明朝 ProN.ttc", 2)
GOTHIC_W3 = ("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 0)

def font(spec, size):
    path, idx = spec
    return ImageFont.truetype(path, size, index=idx)

def rounded_icon(path, size, radius_ratio=0.225):
    """iOS のアイコンは角丸で表示されるので、元の正方形を角丸に抜く。"""
    icon = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size - 1, size - 1), radius=int(size * radius_ratio), fill=255)
    icon.putalpha(mask)
    return icon

def tracked(draw, xy, text, fnt, fill, tracking=0):
    """字間を空けて描く（PIL に字間指定が無いので1文字ずつ進める）。"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking

def build(icon_path, title, lead, out):
    im = Image.new("RGB", (W, H), BG)

    # --- 左: アイコン（落ち影つき） ---
    S, IX, IY = 330, 120, 150
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (IX + 6, IY + 14, IX + S + 6, IY + S + 14), radius=int(S * 0.225),
        fill=(44, 33, 23, 46))
    from PIL import ImageFilter
    im.paste(Image.alpha_composite(im.convert("RGBA"), shadow.filter(
        ImageFilter.GaussianBlur(18))).convert("RGB"), (0, 0))
    im.paste(rounded_icon(icon_path, S), (IX, IY), rounded_icon(icon_path, S))

    d = ImageDraw.Draw(im)
    X = 520

    # --- 右: アプリ名 → 罫 → キャッチ → 署名 ---
    f_title = font(MINCHO_W6, 96)
    d.text((X, 168), title, font=f_title, fill=INK)

    d.rectangle((X, 316, X + 96, 319), fill=RULE)

    d.text((X, 356), lead, font=font(GOTHIC_W3, 34), fill=LEAD)
    tracked(d, (X, 446), "Engineering Papa", font(GOTHIC_W3, 26), FOOT, tracking=3)

    im.save(out, "PNG", optimize=True)
    print(f"✓ {out}")

build("/Users/kaz/projects/engineering/apps/otokemono-app/Otokemono/Resources/"
      "Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png",
      "オトマモノ", "曲から、モンスターが生まれる。",
      "/Users/kaz/projects/engineeringpapa-site/assets/og-otomamono.png")
