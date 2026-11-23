#!/usr/bin/env python3
"""gen_news2: dense world-news digest page — Sunday 22 November 2026.
Idiom learned from the #1/#2 artifacts (989k/989k): 38 stories, region pills,
stats bar, UTC framing, sourced items, CONFIRMED/REPORTED badges, pinned map, date check.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entry_v2.png')
DSB = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
DS = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
DR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
W = H = 1024
PAPER = (251, 248, 240)
INK = (22, 20, 17)
RED = (176, 22, 32)
GRAY = (105, 100, 92)
LGRAY = (214, 208, 195)
BLUE = (26, 54, 102)
TEAL = (18, 96, 88)
GOLD = (196, 154, 44)

REGION_COL = {'WORLD': (26, 54, 102), 'EUROPE': (28, 88, 160), 'MIDDLE EAST': (176, 22, 32),
              'ASIA': (196, 112, 24), 'AFRICA': (112, 52, 132), 'AMERICAS': (24, 120, 72),
              'OCEANIA': (30, 140, 150), 'SPORT': (90, 92, 96)}

def F(sz, p=DR): return ImageFont.truetype(p, sz)

def fitw(d, text, maxw, start, p=DS, minsz=9):
    sz = start
    while sz > minsz and d.textlength(text, font=F(sz, p)) > maxw:
        sz -= 1
    return F(sz, p), sz

def wrap(d, text, font, maxw):
    words, lines, line = text.split(), [], ''
    for w0 in words:
        t = (line + ' ' + w0).strip()
        if d.textlength(t, font=font) <= maxw:
            line = t
        else:
            lines.append(line); line = w0
    if line: lines.append(line)
    return lines

# ---------------- data ----------------
# heroes: (num, region, loc, head, summary, sources, status)
HEROES = [
    (1, 'WORLD', 'ANTALYA, TÜRKIYE',
     "COP31 ends with no climate deal",
     "Talks ran into overtime, then closed without agreement: the EU refused a text that omitted any mention of fossil fuels.",
     "BBC · REUTERS · GUARDIAN", 'CONFIRMED'),
    (2, 'EUROPE', 'DYMER, KYIV REGION',
     "Russian drone brings down an apartment block",
     "Part of the 186-drone overnight barrage; three killed, hundreds evacuated from the five-storey block near Kyiv.",
     "KYIV INDEPENDENT · REUTERS", 'CONFIRMED'),
    (3, 'AFRICA', 'BENGHAZI, LIBYA',
     "Sea drones sink Russian warship off Libya",
     "Ukrainian sea drones struck the corvette in port; its captain was reported killed. Moscow did not confirm the loss.",
     "REUTERS · AL JAZEERA", 'CONFIRMED'),
]
STATS = [("186", "drones\nat Ukraine"), ("3", "dead in\nDymer block"), ("258", "House seats\nDemocrats"),
         ("98.79%", "Hong Kong\nturnout"), ("720/9", "India's total\nin NZ"), ("34", "missing after\nIndonesia fire"),
         ("2", "tankers hit\nnear Hormuz"), ("24", "dead in Nigeria\nboat capsize")]

# grid: (num, region, loc, head, sources, status)
GRID = [
    (4, 'MIDDLE EAST', 'SITRAH, BAHRAIN', "Bahrain: Iran strike wounded two", "REUTERS · AL ARABIYA", 'CONFIRMED'),
    (5, 'MIDDLE EAST', 'STRAIT OF HORMUZ', "Two tankers hit near the Strait of Hormuz", "AP · TRADE WINDS", 'REPORTED'),
    (6, 'MIDDLE EAST', 'TEHRAN', "Iran begins rolling power cuts", "REUTERS", 'REPORTED'),
    (7, 'AMERICAS', 'WASHINGTON', "Trump defers Iran strike decision to new year", "AXIOS · REUTERS", 'REPORTED'),
    (8, 'AMERICAS', 'WASHINGTON', "Democrats lock in 258 House seats, largest since 1992", "AP · NBC", 'CONFIRMED'),
    (9, 'ASIA', 'HONG KONG', "HK Election Committee vote: 98.79% turnout", "SCMP · RTHK", 'CONFIRMED'),
    (10, 'ASIA', 'CIKANDE, INDONESIA', "Candy factory fire: 3 dead, 34 still missing", "REUTERS · AFP", 'REPORTED'),
    (11, 'MIDDLE EAST', 'BASRA, IRAQ', "Power station fire kills four and injures 35", "AFP · IRAQ NEWS", 'REPORTED'),
    (12, 'AFRICA', 'KHARTOUM, SUDAN', "Drones hit Khartoum and Omdurman", "REUTERS", 'REPORTED'),
    (13, 'AMERICAS', 'BIG ISLAND, HAWAII', "Kilauea erupts: lava fountains return", "USGS · AP", 'CONFIRMED'),
    (14, 'EUROPE', 'VATICAN CITY', "Pope Leo hosts lunch for 1,300 poor", "AP · VATICAN NEWS", 'CONFIRMED'),
    (15, 'EUROPE', 'GULF OF FINLAND', "Drone-hit tanker Sparta II towed to safety", "REUTERS", 'CONFIRMED'),
    (16, 'AMERICAS', 'LAS VEGAS', "Verstappen wins the Las Vegas GP", "F1 · ESPN", 'CONFIRMED'),
    (17, 'OCEANIA', 'WELLINGTON', "India 720/9 — record total vs New Zealand", "ESPNCRICINFO", 'CONFIRMED'),
    (18, 'AMERICAS', 'MEXICO CITY', "El Chapo's son, on FBI most-wanted list, captured", "BBC · REUTERS", 'REPORTED'),
    (19, 'ASIA', 'SEOUL', "Minister resigns over AI exam-cheating", "YONHAP", 'REPORTED'),
    (20, 'ASIA', 'NEW DELHI', "Nepal PM Balendra Shah arrives in Delhi", "IANS · HINDU", 'REPORTED'),
    (21, 'AMERICAS', 'WASHINGTON', "FBI hack exposed 10,000+ records", "WAPO · REUTERS", 'REPORTED'),
]

ALSO = [
    (22, 'EUROPE', "Alcaraz beats Zverev for ATP Finals title", "ATP"),
    (23, 'EUROPE', "Kyiv restores heating to all districts", "UKRINFORM"),
    (24, 'AFRICA', "Uganda lifts the last Ebola outbreak restrictions", "AFP"),
    (25, 'EUROPE', "Twente edge ten-man Willem II 2-1", "NOS"),
    (26, 'WORLD', "BepiColombo sends new images from Mercury flyby", "ESA"),
    (27, 'AFRICA', "Nigeria boat capsize kills 24 near Lagos", "REUTERS"),
    (28, 'ASIA', "Lahore again world's most polluted city", "DAWN"),
    (29, 'ASIA', "Cyclone Akvan relief crews restore power", "THE HINDU"),
    (30, 'WORLD', "G20 nations unveil AI incident registry", "REUTERS"),
    (31, 'EUROPE', "Poland summons Belarus envoy over drone", "REUTERS"),
    (32, 'AMERICAS', "Boca Juniors clinch the Argentine league title", "OLE"),
    (33, 'AMERICAS', "Gotham beat NC Courage to lift NWSL trophy", "ESPN"),
    (34, 'ASIA', "HK fire crews free 40 from warehouse blaze", "SCMP"),
    (35, 'EUROPE', "Milan fashion week closes to record crowds", "VOGUE"),
    (36, 'AFRICA', "Sudan truce talks resume in Addis Ababa", "AP"),
    (37, 'OCEANIA', "Australia name squad for the Boxing Day Test", "CRICKET AU"),
    (38, 'WORLD', "UN climate agency names interim COP32 hosts", "UNFCCC"),
]

# map pins: (num, lon, lat)
PINS = [(1, 30.7, 36.9), (2, 30.5, 50.6), (3, 20.1, 32.1), (4, 50.6, 26.1), (5, 56.5, 26.5),
        (6, 51.4, 35.7), (7, -77.0, 38.9), (8, -77.0, 38.9), (9, 114.2, 22.3), (10, 106.0, -6.1),
        (11, 47.8, 30.5), (12, 32.5, 15.6), (13, -155.3, 19.4), (14, 12.5, 41.9), (15, 28.0, 59.5),
        (16, -115.1, 36.2), (17, 174.8, -41.3), (18, -99.1, 19.4), (19, 127.0, 37.6), (20, 77.2, 28.6),
        (21, -77.0, 38.9), (27, 3.4, 6.5), (32, -58.4, -34.6), (33, -74.0, 40.7), (37, 144.9, -37.8)]

img = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 92], fill=INK)
d.text((24, 8), "THE WORLD IN ONE DAY", font=F(20), fill=(255, 205, 130))
d.text((24, 36), "SUNDAY 22 NOVEMBER 2026", font=F(46, DSB), fill=(255, 252, 245))
d.text((1000, 44), "38 STORIES\n7 REGIONS", font=F(15), fill=(255, 205, 130), anchor="rm")
d.text((24, 100), "38 STORIES · 7 REGIONS · EVERY ITEM FROM THIS ONE DAY, WIRES READ TO 23:59 UTC · SCENES ARE DRAWN ILLUSTRATIONS",
       font=F(13), fill=GRAY, anchor="lm")

# ---------------- stats bar ----------------
y0 = 118
sw = (W - 48) // 8
for i, (num, lab) in enumerate(STATS):
    x = 24 + i * sw
    d.rectangle([x, y0, x + sw - 6, y0 + 54], fill=(255, 253, 248), outline=LGRAY)
    d.text((x + 8, y0 + 6), num, font=F(23, DSB), fill=RED)
    d.text((x + 8, y0 + 34), lab, font=F(10), fill=GRAY)

# ---------------- region pills ----------------
from collections import Counter
cnt = Counter(['WORLD'] * 4 + ['EUROPE'] * 7 + ['MIDDLE EAST'] * 5 + ['ASIA'] * 9 + ['AFRICA'] * 6 + ['AMERICAS'] * 7 + ['OCEANIA'] * 2)
y1 = y0 + 64
x = 24
for reg in ['WORLD', 'EUROPE', 'MIDDLE EAST', 'ASIA', 'AFRICA', 'AMERICAS', 'OCEANIA']:
    lab = f"{reg} {cnt[reg]}"
    f = F(12, DSB)
    tw = d.textlength(lab, font=f)
    d.rounded_rectangle([x, y1, x + tw + 20, y1 + 22], radius=11, fill=REGION_COL[reg])
    d.text((x + 10, y1 + 11), lab, font=f, fill=(255, 255, 255), anchor="lm")
    x += tw + 28
d.text((1000, y1 + 11), "UTC DAY · TO 23:59", font=F(12, DSB), fill=GRAY, anchor="rm")

# ---------------- heroes ----------------
hy = y1 + 32
hw = (W - 48 - 24) // 3
hh = 232
def hero_icon(kind, cx, cy):
    if kind == 'climate':
        d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=BLUE, width=4)
        d.line([(cx - 34, cy), (cx + 34, cy)], fill=BLUE, width=2)
        d.arc([cx - 34, cy - 34, cx + 34, cy + 34], 90, 270, fill=BLUE, width=2)
        d.rectangle([cx + 18, cy - 26, cx + 52, cy + 18], fill=(255, 253, 246), outline=RED, width=3)
        d.line([(cx + 24, cy - 14), (cx + 46, cy + 8)], fill=RED, width=3)
        d.line([(cx + 24, cy + 8), (cx + 46, cy - 14)], fill=RED, width=3)
    elif kind == 'drone':
        for dx, dy in ((-26, -18), (0, -28), (26, -16)):
            d.polygon([(cx + dx, cy + dy - 10), (cx + dx - 12, cy + dy + 6), (cx + dx + 12, cy + dy + 6)], fill=INK)
            d.line([(cx + dx, cy + dy + 6), (cx + dx, cy + dy + 16)], fill=RED, width=3)
        d.rectangle([cx - 30, cy + 22, cx + 30, cy + 44], fill=(150, 142, 128))
        d.rectangle([cx - 22, cy + 14, cx + 22, cy + 22], fill=(120, 112, 100))
    else:  # warship
        d.polygon([(cx - 40, cy + 4), (cx + 40, cy + 4), (cx + 28, cy + 26), (cx - 28, cy + 26)], fill=(96, 104, 118))
        d.polygon([(cx - 40, cy + 4), (cx + 10, cy + 4), (cx + 2, cy - 26), (cx - 34, cy - 14)], fill=(120, 128, 142))
        d.rectangle([cx - 8, cy - 38, cx + 2, cy - 2], fill=INK)
        d.polygon([(cx + 8, cy - 34), (cx + 2, cy - 10), (cx + 20, cy - 10)], fill=GOLD)
        d.polygon([(cx + 22, cy - 30), (cx + 16, cy - 8), (cx + 34, cy - 8)], fill=RED)
        for wx in range(-40, 41, 20):
            d.arc([cx + wx - 10, cy + 26, cx + wx + 10, cy + 42], 180, 360, fill=BLUE, width=3)
for i, (num, reg, loc, head, summ, src, status) in enumerate(HEROES):
    hx = 24 + i * (hw + 12)
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(255, 253, 248), outline=INK, width=2)
    # icon band
    d.rectangle([hx, hy, hx + hw, hy + 78], fill=(238, 234, 222))
    hero_icon(['climate', 'drone', 'warship'][i], hx + hw // 2, hy + 40)
    # number + region chip
    d.ellipse([hx + 8, hy + 8, hx + 34, hy + 34], fill=RED)
    d.text((hx + 21, hy + 21), str(num), font=F(15, DSB), fill=(255, 255, 255), anchor="mm")
    freg = F(9, DSB)
    d.text((hx + hw - 8, hy + 21), reg, font=freg, fill=REGION_COL[reg], anchor="rm")
    ty = hy + 86
    d.text((hx + 8, ty), loc, font=F(10, DSB), fill=GRAY); ty += 16
    hf = F(20, DSB)
    for ln in wrap(d, head, hf, hw - 16)[:3]:
        d.text((hx + 8, ty), ln, font=hf, fill=INK); ty += 23
    ty += 2
    for ln in wrap(d, summ, F(11), hw - 16)[:3]:
        d.text((hx + 8, ty), ln, font=F(11), fill=(60, 56, 50)); ty += 14
    # sources + status
    d.text((hx + 8, hy + hh - 20), src, font=F(9, DSB), fill=GRAY)
    sc = (24, 140, 70) if status == 'CONFIRMED' else (130, 126, 118)
    fst = F(8, DSB); tws = d.textlength(status, font=fst)
    d.rounded_rectangle([hx + hw - tws - 18, hy + hh - 26, hx + hw - 8, hy + hh - 12], radius=6, fill=sc)
    d.text((hx + hw - 13, hy + hh - 19), status, font=fst, fill=(255, 255, 255), anchor="rm")

# ---------------- grid 4-21 ----------------
gy = hy + hh + 22
d.rectangle([0, gy - 12, W, gy + 8], fill=INK)
d.text((24, gy - 2), "MORE FROM SUNDAY — STORIES 4–21", font=F(16, DSB), fill=(255, 252, 244), anchor="lm")
d.text((1000, gy - 2), "DATED, LOCATED, SOURCED", font=F(11), fill=(255, 205, 130), anchor="rm")
cy = gy + 14
cw = (W - 48 - 5 * 8) // 6
ch = 88
for i, (num, reg, loc, head, src, status) in enumerate(GRID):
    col, row = i % 6, i // 6
    cx = 24 + col * (cw + 8)
    yy = cy + row * (ch + 8)
    d.rectangle([cx, yy, cx + cw, yy + ch], fill=(255, 253, 248), outline=LGRAY)
    d.rectangle([cx, yy, cx + cw, yy + 4], fill=REGION_COL[reg])
    d.text((cx + 5, yy + 9), str(num), font=F(13, DSB), fill=RED)
    d.text((cx + 5, yy + 26), reg, font=F(7, DSB), fill=REGION_COL[reg])
    ty = yy + 36
    for ln in wrap(d, head, F(10.5, DSB), cw - 10)[:3]:
        d.text((cx + 5, ty), ln, font=F(10.5, DSB), fill=INK); ty += 11
    d.text((cx + 5, yy + ch - 14), loc[:22], font=F(7), fill=GRAY)
    d.text((cx + 5, yy + ch - 7), src[:26], font=F(6.5), fill=(140, 134, 124))

# ---------------- bottom: map + also list ----------------
by = cy + 3 * (ch + 8) + 2
d.rectangle([0, by, W, by + 3], fill=INK)
mb = by + 10
# map panel
MW, MH = 400, 200
d.rectangle([24, mb, 24 + MW, mb + MH], fill=(226, 234, 238), outline=LGRAY)
d.text((32, mb + 5), "WHERE IT HAPPENED — PINNED BY STORY NUMBER", font=F(10, DSB), fill=INK)
# rough continents (fractional 0-100 coords)
def blob(fpts, col=(196, 208, 200)):
    pts = [(24 + 8 + fx / 100 * (MW - 16), mb + 22 + fy / 100 * (MH - 30)) for fx, fy in fpts]
    d.polygon(pts, fill=col, outline=(168, 180, 172))
blob([(8, 12), (22, 6), (38, 10), (44, 22), (36, 34), (20, 32), (10, 22)])          # N America
blob([(26, 44), (38, 42), (44, 55), (38, 72), (30, 82), (24, 60)])                  # S America
blob([(46, 8), (60, 4), (66, 12), (60, 22), (48, 20)])                              # Europe
blob([(48, 26), (64, 22), (72, 34), (62, 58), (52, 66), (46, 44)])                  # Africa
blob([(64, 4), (92, 2), (98, 12), (92, 28), (74, 34), (66, 20), (63, 12)])          # Asia
blob([(78, 38), (88, 36), (92, 48), (84, 54), (78, 48)])                            # SE Asia
blob([(88, 64), (97, 62), (100, 74), (94, 84), (87, 78)])                           # Australia
def proj(lon, lat):
    return (24 + 8 + int((lon + 180) / 360 * (MW - 16)),
            mb + 22 + int((90 - lat) / 180 * (MH - 30)))
for num, lon, lat in PINS:
    px, py = proj(lon, lat)
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255))
    d.text((px, py + 1), str(num), font=F(7, DSB), fill=(255, 255, 255), anchor="mm")
# also list
lx = 24 + MW + 14
lw = W - 24 - lx
d.text((lx, mb + 2), "ALSO ON SUNDAY 22 NOVEMBER — STORIES 22–38", font=F(10.5, DSB), fill=INK)
ly = mb + 18
for num, reg, head, src in ALSO:
    d.text((lx, ly), str(num), font=F(8.5, DSB), fill=RED)
    d.rectangle([lx + 16, ly + 1, lx + 19, ly + 8], fill=REGION_COL[reg])
    f2, _ = fitw(d, head, lw - 100, 10.5, DR)
    d.text((lx + 24, ly), head, font=f2, fill=INK)
    d.text((lx + lw, ly), src, font=F(6.5), fill=GRAY, anchor="ra")
    ly += 12.4
# date check strip
dy = mb + MH + 8
d.rectangle([24, dy, W - 24, H - 6], outline=RED, width=2)
d.text((32, dy + 4), "DATE CHECK", font=F(10, DSB), fill=RED)
d.text((104, dy + 5), "Every story here was reported on Sunday 22 November 2026 (UTC); wires read to 23:59 UTC.   Scenes are drawn illustrations · figures attributed or checked in two or more sources.",
       font=F(8.5), fill=INK)

img.save(OUT, optimize=True)
sz = os.path.getsize(OUT)
print("WROTE", OUT, img.size, sz, "bytes", "OK" if sz <= 1048576 else "TOO BIG")
