#!/usr/bin/env python3
"""RSSから未作成のエピソードページを作る（標準ライブラリのみ・秘密情報なし）。

- 既存の episodes/ep-NN.html は上書きしない（何度実行しても同じ結果）
- 追加するもの: episodes/ep-NN.html / index.html の一覧と話数 / sitemap.xml / 前話ページの「次へ」リンク
- Spotifyの個別URLはRSSに無いため、scripts/spotify_ids.json（{"30": "エピソードID"}）に書いた話だけ埋め込みを付ける
"""
import html, json, re, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED = "https://feed.omoshuwa-podcast.com/feed.xml"
SITE = "https://omoshuwa-podcast.com"
ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
JST = timezone(timedelta(hours=9))
SHOW = "オーモシロ・シュワルツェネッガー"


def fetch(src):
    if src.startswith("http"):
        req = urllib.request.Request(src, headers={"User-Agent": "omoshu-web-episode-gen"})
        return urllib.request.urlopen(req, timeout=30).read()
    return Path(src).read_bytes()


def plain(s):
    s = re.sub(r"</p>\s*<p>", "\n", s or "")
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).replace("​", "").strip()


def safe(s):  # JSON-LD内でも属性内でも壊れない最小限の置換
    return html.escape(s.replace('"', "”"), quote=False)


def summary(desc_html):
    lines = [l.strip() for l in plain(desc_html).split("\n") if l.strip()]
    out = []
    for l in lines:
        if l.startswith(("▼", "＼", "*", "＊", "【番組概要】", "#", "http")):
            break
        out.append(l)
    return out[:6]


def parse(feed_bytes):
    items = []
    for it in ET.fromstring(feed_bytes).findall(".//item"):
        title = (it.findtext("title") or "").strip()
        m = re.match(r"ep\.?\s*(\d+)", title, re.I)
        if not m:
            continue
        n = int(m.group(1))
        clean = re.sub(r"^ep\.?\s*\d+[_\s]*", "", title, flags=re.I)
        clean = re.sub(re.escape(SHOW) + r"\s*$", "", clean).strip()
        dt = parsedate_to_datetime(it.findtext("pubDate")).astimezone(JST)
        dur = (it.findtext(ITUNES + "duration") or "").strip()
        if dur.isdigit():
            s = int(dur); dur = f"{s//3600:02d}:{s%3600//60:02d}:{s%60:02d}"
        parts = [int(x) for x in dur.split(":")] if re.fullmatch(r"\d+(:\d+){1,2}", dur) else []
        while len(parts) < 3 and parts:
            parts.insert(0, 0)
        h, mi, sec = parts or (0, 0, 0)
        items.append(dict(num=n, title=clean, date=dt.strftime("%Y-%m-%d"),
                          dur=f"{h:02d}:{mi:02d}:{sec:02d}", iso=f"PT{h}H{mi}M{sec}S",
                          link=(it.findtext("link") or "").strip(),
                          lines=summary(it.findtext("description"))))
    return items


def render(tpl, e, spotify_id, prev_exists, today):
    nn = f"{e['num']:02d}"
    t = safe(e["title"])
    full = f"{t}｜ep.{e['num']} | {SHOW}"
    body_lines = e["lines"] or [f"{SHOW}第{e['num']}話。"]
    body = "\n    ".join(f"<p>{safe(l)}</p>" for l in body_lines) + "\n    <p>ぜひSpotify、Apple Podcasts、LISTENでお聴きください！</p>"
    desc = safe(" ".join(body_lines))[:140] + f"（再生時間: {e['dur']}）"
    if spotify_id:
        url = f"https://open.spotify.com/episode/{spotify_id}"
        player = ('<!-- Spotify Player -->\n<div style="margin:32px 0;border-radius:12px;overflow:hidden;">\n'
                  f'  <iframe style="border-radius:12px" src="https://open.spotify.com/embed/episode/{spotify_id}?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>\n</div>\n')
    else:
        url, player = "https://open.spotify.com/show/56OB1eYPQ9UdhKkNwn091a", ""
    prev = (f'<a href="ep-{e["num"]-1:02d}.html" class="nav-link prev-link">前のエピソード</a>'
            if prev_exists else "<div></div>")
    m = dict(TITLE_FULL=full, TITLE_H1=f"{t}｜ep.{e['num']} {SHOW}", TITLE_CRUMB=f"{t}｜ep.{e['num']}",
             DESC=desc, DATE=e["date"], ISO_DUR=e["iso"], DUR=e["dur"], NUM=str(e["num"]), NN=nn,
             TODAY=today, SPOTIFY_URL=url, SPOTIFY_PLAYER=player, BODY=body, PREV=prev)
    return re.sub(r"\{\{(\w+)\}\}", lambda x: m[x.group(1)], tpl)


def add_next_links(floor):
    for p in sorted((ROOT / "episodes").glob("ep-*.html")):
        n = int(re.search(r"ep-(\d+)", p.name).group(1))
        if n < floor or not (ROOT / "episodes" / f"ep-{n+1:02d}.html").exists():
            continue
        s = p.read_text(encoding="utf-8")
        if "next-link" in s or "related-nav" not in s:
            continue
        i = s.index("related-nav\">", s.index("<!-- Related Episodes -->"))
        j = s.index("</div>\n</article>", i)
        blk = s[i:j]
        k = blk.rfind("<div></div>")
        if k < 0:
            continue
        link = f'<a href="ep-{n+1:02d}.html" class="nav-link next-link">次のエピソード</a>'
        p.write_text(s[:i] + blk[:k] + link + blk[k + len("<div></div>"):] + s[j:], encoding="utf-8")


def main(src=FEED):
    items = parse(fetch(src))
    ids_f = ROOT / "scripts" / "spotify_ids.json"
    ids = json.loads(ids_f.read_text()) if ids_f.exists() else {}
    tpl = (ROOT / "scripts" / "episode_template.html").read_text(encoding="utf-8")
    today = datetime.now(JST).strftime("%Y-%m-%d")
    created = []
    # 欠番の過去話は作らない: 既存ページの最大番号より新しい話だけ対象
    have = [int(re.search(r"ep-(\d+)", p.name).group(1)) for p in (ROOT / "episodes").glob("ep-*.html")]
    floor = max(have) if have else 0
    for e in sorted(items, key=lambda x: x["num"]):
        if e["num"] <= floor:
            continue
        nn = f"{e['num']:02d}"
        f = ROOT / "episodes" / f"ep-{nn}.html"
        if f.exists():
            continue
        prev_exists = (ROOT / "episodes" / f"ep-{e['num']-1:02d}.html").exists()
        f.write_text(render(tpl, e, ids.get(str(e["num"])), prev_exists, today), encoding="utf-8")
        created.append(e)
        # sitemap
        sm = ROOT / "sitemap.xml"; s = sm.read_text(encoding="utf-8")
        loc = f"{SITE}/episodes/ep-{nn}.html"
        if loc not in s:
            entry = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{e['date']}</lastmod>\n"
                     "    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n")
            first = s.index("<loc>", s.index("<loc>") + 1)
            first = s.rfind("  <url>", 0, first)
            sm.write_text(s[:first] + entry + s[first:], encoding="utf-8")
        # index.html 一覧（新しい順）
        ix = ROOT / "index.html"; s = ix.read_text(encoding="utf-8")
        if f'<span class="episode-num">EP{e["num"]}</span>' not in s:
            sid = ids.get(str(e["num"]))
            attr = f'data-spotify="{sid}"' if sid else f'data-href="episodes/ep-{nn}.html"'
            item = (f'    <div class="episode-item fade-in" {attr} onclick="toggleEpEmbed(this)">\n'
                    f'      <div class="episode-row"><span class="episode-num">EP{e["num"]}</span><div class="episode-info"><div class="episode-title">{safe(e["title"])}</div><div class="episode-meta">{e["date"]} &#183; {e["dur"]}</div></div><span class="episode-play">&#9654;</span></div>\n'
                    '      <div class="episode-embed"></div>\n    </div>\n')
            pos = s.index('<div class="episode-list">') + len('<div class="episode-list">\n')
            # 自分より番号が小さい最初の項目の前に入れる
            for m in re.finditer(r'    <div class="episode-item[^\n]*\n      <div class="episode-row"><span class="episode-num">EP(\d+)</span>', s):
                if int(m.group(1)) < e["num"]:
                    pos = m.start(); break
            ix.write_text(s[:pos] + item + s[pos:], encoding="utf-8")
    if created:
        top = max(int(re.search(r"ep-(\d+)", p.name).group(1)) for p in (ROOT / "episodes").glob("ep-*.html"))
        ix = ROOT / "index.html"; s = ix.read_text(encoding="utf-8")
        s = re.sub(r'"numberOfEpisodes": \d+', f'"numberOfEpisodes": {top}', s)
        s = re.sub(r'(<span class="stat-num">)\d+(</span><span class="stat-label">EPISODES)', rf"\g<1>{top}\2", s)
        ix.write_text(s, encoding="utf-8")
    add_next_links(floor)
    print("created:", [f"ep-{e['num']:02d}" for e in created] or "none")


if __name__ == "__main__":
    main(*sys.argv[1:2])
