#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 data/projects.yaml 生成 docs/index.html（静态卡片页）。
运行：python3 build_page.py
"""
import html
import json
import os

import yaml

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = "https://github.com/xiaopengs/voice-oss-radar"

CATS = [
    ("asr", "ASR 语音识别", "把声音变成文字。中文场景的分水岭在 FunASR 系与 Whisper 系之间。", "01-asr.md"),
    ("tts", "TTS 语音合成", "文字变声音。2026 年的竞争轴是克隆一致性、可控性与单位成本。", "02-tts.md"),
    ("speech-to-speech", "全双工 / 端到端语音", "语音进、语音出，跳过文本瓶颈，换取低延迟与副语言感知。", "03-speech-to-speech.md"),
    ("voice-agent", "语音 Agent 编排", "不产出能力，产出链路：传输、VAD、打断、工具调用、观测。", "04-voice-agent.md"),
    ("diarization", "说话人分离与声纹", "谁在什么时候说话。会议转写里最伤体验的不是错字，是张冠李戴。", "05-diarization.md"),
    ("on-device", "端侧与推理运行时", "看包体积、内存峰值、首字延迟，而不是榜单。", "06-on-device.md"),
    ("audio-frontend", "音频前端", "VAD、降噪、AEC、音源分离。上游差 3dB，下游全白费。", "07-audio-frontend.md"),
    ("voice-conversion", "变声与语音编辑", "保留内容与韵律，只换音色。比让 TTS 重念一遍自然得多。", "08-voice-conversion.md"),
    ("speech-translation", "语音翻译与同传", "级联、端到端、流式三条路线，延迟与质量成反比。", "09-speech-translation.md"),
    ("meeting-app", "会议转写桌面应用", "音频不出本机、双轨采集、结构化纪要。Tauri/Rust 与 Electron/Qt 两个流派。", "10-meeting-desktop.md"),
    ("voice-studio", "语音创作工作台", "克隆、配音、有声书。常被误当成会议工具。", "10-meeting-desktop.md"),
]

FORM_CN = {
    "model": "模型",
    "toolkit": "工具包",
    "framework": "框架",
    "runtime": "运行时",
    "desktop": "桌面应用",
    "library": "库",
}

COMMERCIAL_OK = ("MIT", "APACHE", "BSD", "MPL", "ISC", "ZLIB")


def lic_class(lic):
    """返回 (css_class, 中文标签)。"""
    if not lic:
        return "unknown", "许可待确认"
    u = lic.upper()
    if "NC" in u or "CPML" in u or "NONCOMMERCIAL" in u:
        return "warn", "禁止商用"
    if "AGPL" in u or "GPL" in u:
        return "caution", "传染性开源"
    if any(k in u for k in COMMERCIAL_OK):
        return "ok", "可商用"
    if "UNKNOWN" in u:
        return "unknown", "许可待确认"
    return "caution", "需逐项确认"


def short_repo(url):
    s = url.replace("https://github.com/", "").replace("http://github.com/", "")
    return s.rstrip("/")


def lang_text(langs):
    if not langs:
        return "未标注"
    ls = [str(x) for x in langs]
    if len(ls) <= 3:
        return " / ".join(ls)
    return " / ".join(ls[:3]) + " +%d" % (len(ls) - 3)


def build():
    with open(os.path.join(BASE, "data", "projects.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    projects = data["projects"]

    # 统计
    buckets = {"ok": [], "caution": [], "warn": [], "unknown": []}
    for p in projects:
        cls, _ = lic_class(p.get("license", ""))
        buckets[cls].append(p)
    total = len(projects)

    # 分类分组
    by_cat = {}
    for p in projects:
        by_cat.setdefault(p["category"], []).append(p)

    cards_by_cat = {}
    for key, _title, _desc, _doc in CATS:
        items = by_cat.get(key, [])
        out = []
        for p in items:
            cls, label = lic_class(p.get("license", ""))
            name = html.escape(p["name"])
            desc = html.escape(p["one_liner"])
            repo = html.escape(p["repo"])
            sr = html.escape(short_repo(p["repo"]))
            form = FORM_CN.get(p.get("form", ""), p.get("form", ""))
            caps = "".join('<li>%s</li>' % html.escape(c) for c in p.get("capabilities", []))
            note = p.get("note", "")
            note_clean = note
            for pre in ("⚠️ ", "⚠️", "⚠ ", "⚠"):
                if note_clean.startswith(pre):
                    note_clean = note_clean[len(pre):].lstrip()
            note_html = (
                '<p class="note"><span aria-hidden="true">⚠</span> %s</p>' % html.escape(note_clean)
                if note_clean
                else ""
            )
            wl = p.get("weights_license", "")
            wl_html = ""
            if wl:
                wcls, wlabel = lic_class(wl)
                if wl.upper() == "UNKNOWN":
                    wl_html = '<span class="badge unknown">权重 待确认</span>'
                else:
                    wl_html = '<span class="badge %s">权重 %s · %s</span>' % (
                        wcls,
                        html.escape(wl),
                        wlabel,
                    )
            search = " ".join(
                [p["name"], p["one_liner"], " ".join(p.get("capabilities", [])), note, p.get("license", ""), " ".join(str(x) for x in p.get("language", []))]
            ).lower()
            out.append(
                """      <article class="card" data-lic="{lic}" data-search="{search}">
        <div class="card-head">
          <h3 class="card-name">{name}</h3>
          <span class="form">{form}</span>
        </div>
        <p class="card-desc">{desc}</p>
        <ul class="caps">{caps}</ul>
        {note}
        <div class="badges">
          <span class="badge {lic}">代码 {licraw} · {liclabel}</span>
          {wl}
        </div>
        <div class="card-foot">
          <a href="{repo}" target="_blank" rel="noopener noreferrer">{sr}</a>
          <span class="date">核实 {ver}</span>
        </div>
      </article>""".format(
                    lic=cls,
                    search=html.escape(search, quote=True),
                    name=name,
                    form=html.escape(form),
                    desc=desc,
                    caps=caps,
                    note=note_html,
                    licraw=html.escape(p.get("license", "unknown")),
                    liclabel=label,
                    wl=wl_html,
                    repo=repo,
                    sr=sr,
                    ver=html.escape(p.get("verified", "")),
                )
            )
        cards_by_cat[key] = "\n".join(out)

    # 分类导航
    nav = []
    for i, (key, title, _d, doc) in enumerate(CATS, 1):
        nav.append(
            '<li><a href="#cat-%s"><span class="nav-idx">%02d</span>%s'
            '<span class="nav-count">%d</span></a></li>'
            % (key, i, html.escape(title), len(by_cat.get(key, [])))
        )
    nav_html = "\n".join(nav)

    # 许可风险条
    seg_order = [
        ("ok", "可商用", "代码许可允许商业使用"),
        ("caution", "需逐项确认", "传染性开源或非标准许可"),
        ("warn", "禁止商用", "权重或代码明确非商用"),
        ("unknown", "待确认", "未查到明确许可"),
    ]
    segs = []
    legend = []
    for cls, label, hint in seg_order:
        n = len(buckets[cls])
        if n == 0:
            continue
        pct = 100.0 * n / total
        segs.append(
            '<span class="seg seg-%s" style="flex:%d 0 0" title="%s：%d 个（%.0f%%）"></span>'
            % (cls, n, label, n, pct)
        )
        legend.append(
            '<li><span class="dot dot-%s"></span><b>%s</b> %d 个<em>%s</em></li>'
            % (cls, label, n, hint)
        )
    seg_html = "".join(segs)
    legend_html = "\n".join(legend)

    # 主体分区
    sections = []
    for i, (key, title, desc, doc) in enumerate(CATS, 1):
        items = by_cat.get(key, [])
        if not items:
            continue
        sections.append(
            """    <section class="cat" id="cat-{key}" data-cat="{key}">
      <header class="cat-head">
        <div class="cat-title">
          <span class="cat-idx">{idx:02d}</span>
          <h2>{title}</h2>
          <span class="cat-num">{n} 个项目</span>
        </div>
        <p class="cat-desc">{desc}</p>
        <a class="cat-doc" href="{repo}/blob/main/docs/{doc}" target="_blank" rel="noopener noreferrer">分类详述 →</a>
      </header>
      <div class="grid">
{cards}
      </div>
    </section>""".format(
                key=key,
                idx=i,
                title=html.escape(title),
                n=len(items),
                desc=html.escape(desc),
                repo=REPO,
                doc=doc,
                cards=cards_by_cat[key],
            )
        )
    sections_html = "\n\n".join(sections)

    # 分类筛选 chip
    cat_chips = ['<button class="chip is-active" type="button" data-cat="all" aria-pressed="true">全部<span>%d</span></button>' % total]
    for key, title, _d, _doc in CATS:
        n = len(by_cat.get(key, []))
        if n == 0:
            continue
        cat_chips.append(
            '<button class="chip" type="button" data-cat="%s" aria-pressed="false">%s<span>%d</span></button>'
            % (key, html.escape(title.split(" ")[0] if " " in title else title), n)
        )
    cat_chips_html = "".join(cat_chips)

    lic_chips = ['<button class="chip" type="button" data-lic="all" aria-pressed="true">全部许可</button>']
    for cls, label, _h in seg_order:
        n = len(buckets[cls])
        if n == 0:
            continue
        lic_chips.append(
            '<button class="chip" type="button" data-lic="%s" aria-pressed="false">%s<span>%d</span></button>'
            % (cls, label, n)
        )
    lic_chips_html = "".join(lic_chips)

    page = TEMPLATE.replace("{{NAV}}", nav_html)
    page = page.replace("{{SEGS}}", seg_html)
    page = page.replace("{{LEGEND}}", legend_html)
    page = page.replace("{{CAT_CHIPS}}", cat_chips_html)
    page = page.replace("{{LIC_CHIPS}}", lic_chips_html)
    page = page.replace("{{SECTIONS}}", sections_html)
    page = page.replace("{{TOTAL}}", str(total))
    page = page.replace("{{CATCOUNT}}", str(len([c for c in CATS if by_cat.get(c[0])])))
    page = page.replace("{{REPO}}", REPO)

    out_path = os.path.join(BASE, "docs", "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print("written:", out_path, len(page), "bytes")
    print("counts:", {k: len(v) for k, v in buckets.items()})


TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>语音开源雷达 · 77 个语音开源项目索引</title>
<meta name="description" content="持续收集与核实的语音方向开源项目索引：ASR、TTS、全双工、语音 Agent、说话人分离、端侧推理、音频前端、变声、语音翻译、会议转写。每条标注代码许可与权重许可。">
<style>
  :root{
    --canvas:#0a0c11;
    --surface:#12151d;
    --surface-2:#171b25;
    --line:#242a38;
    --line-soft:#1b2029;
    --ink:#e9ecf3;
    --ink-2:#a7b0c0;
    --ink-3:#7c8798;
    --accent:#6d8dff;
    --accent-2:#a273ff;
    --ok:#3fbf8f;
    --caution:#e0b354;
    --warn:#ef6b6b;
    --unknown:#7b8698;
    --radius:10px;
    --pad:clamp(16px, 3vw, 40px);
    --mono:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    --sans:system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  *,*::before,*::after{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{
    margin:0;
    background:var(--canvas);
    color:var(--ink);
    font-family:var(--sans);
    font-size:16px;
    line-height:1.65;
    overflow-x:hidden;
  }
  body::before{
    content:"";
    position:fixed;
    inset:0 0 auto 0;
    height:1px;
    background:linear-gradient(90deg, transparent, var(--accent), var(--accent-2), transparent);
    opacity:.55;
    z-index:5;
    pointer-events:none;
  }
  a{color:var(--accent);text-decoration:none;overflow-wrap:anywhere}
  a:hover{color:var(--accent-2);text-decoration:underline}
  :focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
  .wrap{padding-left:var(--pad);padding-right:var(--pad)}

  /* ---------- 顶部 ---------- */
  .top{padding-top:clamp(32px,6vw,64px);padding-bottom:clamp(20px,3vw,28px);border-bottom:1px solid var(--line-soft)}
  .top-inner{max-width:1480px;margin:0 auto}
  .eyebrow{
    display:flex;flex-wrap:wrap;align-items:center;gap:10px;
    font-family:var(--mono);font-size:12px;letter-spacing:.08em;color:var(--ink-3);
    text-transform:uppercase;margin:0 0 14px;
  }
  .eyebrow b{color:var(--ink-2);font-weight:600;letter-spacing:.04em}
  h1{
    margin:0 0 14px;
    font-size:clamp(30px,4.4vw,54px);
    line-height:1.08;
    letter-spacing:-.02em;
    font-weight:700;
  }
  h1 em{
    font-style:normal;
    background:linear-gradient(100deg,var(--accent),var(--accent-2));
    -webkit-background-clip:text;background-clip:text;color:transparent;
  }
  .lede{max-width:62ch;margin:0 0 26px;color:var(--ink-2);font-size:clamp(15px,1.4vw,17px)}

  /* 许可风险条：本页的记忆点 */
  .risk{
    border:1px solid var(--line);
    border-radius:var(--radius);
    background:linear-gradient(180deg, var(--surface-2), var(--surface));
    padding:18px 20px 16px;
    max-width:1480px;
  }
  .risk-head{
    display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;
    gap:8px;margin-bottom:12px;
  }
  .risk-head h2{font-size:14px;margin:0;font-weight:600;letter-spacing:.02em}
  .risk-head p{margin:0;font-size:12.5px;color:var(--ink-3)}
  .bar{display:flex;height:12px;border-radius:6px;overflow:hidden;background:var(--line-soft);gap:2px}
  .seg{display:block;height:100%}
  .seg-ok{background:var(--ok)}
  .seg-caution{background:var(--caution)}
  .seg-warn{background:var(--warn)}
  .seg-unknown{background:var(--unknown)}
  .legend{list-style:none;display:flex;flex-wrap:wrap;gap:6px 22px;margin:14px 0 0;padding:0;font-size:13px}
  .legend li{display:flex;align-items:baseline;gap:7px;color:var(--ink-2)}
  .legend b{color:var(--ink);font-weight:600}
  .legend em{font-style:normal;color:var(--ink-3);font-size:12px}
  .dot{width:9px;height:9px;border-radius:50%;flex:0 0 auto;display:inline-block;transform:translateY(-1px)}
  .dot-ok{background:var(--ok)}.dot-caution{background:var(--caution)}
  .dot-warn{background:var(--warn)}.dot-unknown{background:var(--unknown)}

  /* ---------- 分类导航 ---------- */
  .nav{padding-top:18px;padding-bottom:18px;border-bottom:1px solid var(--line-soft)}
  .nav ul{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;max-width:1480px;margin:0 auto}
  .nav a{
    display:inline-flex;align-items:center;gap:8px;
    border:1px solid var(--line);border-radius:999px;
    padding:6px 12px;font-size:13px;color:var(--ink-2);background:var(--surface);
  }
  .nav a:hover{border-color:var(--accent);color:var(--ink);text-decoration:none}
  .nav-idx{font-family:var(--mono);font-size:11px;color:var(--ink-3)}
  .nav-count{font-family:var(--mono);font-size:11px;color:var(--accent);background:rgba(109,141,255,.12);padding:0 6px;border-radius:999px}

  /* ---------- 工具栏 ---------- */
  .toolbar{
    position:sticky;top:0;z-index:4;
    background:rgba(10,12,17,.94);
    backdrop-filter:blur(10px);
    border-bottom:1px solid var(--line);
    padding-top:12px;padding-bottom:12px;
  }
  .toolbar-inner{max-width:1480px;margin:0 auto;display:flex;flex-direction:column;gap:10px}
  .search-row{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
  .search{
    flex:1 1 260px;min-width:0;position:relative;
  }
  .search input{
    width:100%;padding:9px 12px 9px 34px;
    background:var(--surface);border:1px solid var(--line);border-radius:8px;
    color:var(--ink);font-size:14px;font-family:inherit;
  }
  .search input::placeholder{color:var(--ink-3)}
  .search input:focus{border-color:var(--accent);outline:none;box-shadow:0 0 0 3px rgba(109,141,255,.15)}
  .search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);opacity:.5}
  .count{font-size:13px;color:var(--ink-3);font-family:var(--mono);white-space:nowrap}
  .count b{color:var(--accent);font-weight:600}
  .chips{display:flex;flex-wrap:wrap;gap:6px}
  .chips + .chips{margin-top:2px}
  .chip{
    display:inline-flex;align-items:center;gap:6px;
    padding:5px 11px;border-radius:999px;cursor:pointer;
    background:transparent;border:1px solid var(--line);
    color:var(--ink-2);font-size:12.5px;font-family:inherit;
  }
  .chip:hover{border-color:var(--ink-3);color:var(--ink)}
  .chip span{font-family:var(--mono);font-size:11px;color:var(--ink-3)}
  .chip.is-active{background:rgba(109,141,255,.14);border-color:var(--accent);color:var(--ink)}
  .chip.is-active span{color:var(--accent)}
  .chip[data-lic="ok"].is-active{background:rgba(63,191,143,.14);border-color:var(--ok)}
  .chip[data-lic="caution"].is-active{background:rgba(224,179,84,.14);border-color:var(--caution)}
  .chip[data-lic="warn"].is-active{background:rgba(239,107,107,.14);border-color:var(--warn)}
  .chip[data-lic="unknown"].is-active{background:rgba(123,134,152,.16);border-color:var(--unknown)}

  /* ---------- 主体 ---------- */
  main{padding-bottom:clamp(40px,6vw,80px)}
  .cat{max-width:1480px;margin:0 auto;padding-top:clamp(30px,4vw,48px);scroll-margin-top:110px}
  .cat-head{
    display:grid;grid-template-columns:1fr;gap:6px;
    padding-bottom:14px;margin-bottom:18px;border-bottom:1px solid var(--line-soft);
  }
  .cat-title{display:flex;flex-wrap:wrap;align-items:baseline;gap:12px}
  .cat-idx{font-family:var(--mono);font-size:12px;color:var(--ink-3);letter-spacing:.06em}
  .cat-title h2{font-size:clamp(19px,2.1vw,24px);margin:0;font-weight:650;letter-spacing:-.01em}
  .cat-num{font-family:var(--mono);font-size:11.5px;color:var(--ink-3)}
  .cat-desc{margin:0;color:var(--ink-2);font-size:14px;max-width:76ch}
  .cat-doc{font-size:12.5px;justify-self:start}

  .grid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(min(100%,310px),1fr));
    gap:14px;
  }
  .card{
    min-width:0;
    display:flex;flex-direction:column;gap:10px;
    padding:16px 16px 13px;
    background:var(--surface);
    border:1px solid var(--line-soft);
    border-left:2px solid var(--line);
    border-radius:var(--radius);
    transition:border-color .18s ease, transform .18s ease, background .18s ease;
  }
  .card:hover{border-color:var(--line);border-left-color:var(--accent);background:var(--surface-2);transform:translateY(-2px)}
  .card[data-lic="warn"]{border-left-color:rgba(239,107,107,.6)}
  .card[data-lic="caution"]{border-left-color:rgba(224,179,84,.55)}
  .card[data-lic="ok"]{border-left-color:rgba(63,191,143,.5)}
  .card-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
  .card-name{margin:0;font-size:16px;font-weight:650;letter-spacing:-.01em;overflow-wrap:anywhere}
  .form{
    flex:0 0 auto;font-size:11px;color:var(--ink-3);
    border:1px solid var(--line);border-radius:5px;padding:1px 6px;
    font-family:var(--mono);
  }
  .card-desc{margin:0;font-size:13.5px;color:var(--ink-2);line-height:1.6}
  .caps{list-style:none;display:flex;flex-wrap:wrap;gap:5px;margin:0;padding:0}
  .caps li{
    font-size:11.5px;color:var(--ink-2);
    background:rgba(255,255,255,.035);
    border:1px solid var(--line-soft);
    border-radius:4px;padding:1px 6px;
  }
  .note{
    margin:0;font-size:12px;color:var(--caution);
    line-height:1.55;
    border-left:2px solid rgba(224,179,84,.4);
    padding-left:8px;
  }
  .badges{display:flex;flex-wrap:wrap;gap:5px;margin-top:auto;padding-top:2px}
  .badge{
    font-size:11px;font-family:var(--mono);
    padding:1.5px 7px;border-radius:4px;
    border:1px solid transparent;white-space:nowrap;
  }
  .badge.ok{color:var(--ok);background:rgba(63,191,143,.1);border-color:rgba(63,191,143,.28)}
  .badge.caution{color:var(--caution);background:rgba(224,179,84,.1);border-color:rgba(224,179,84,.28)}
  .badge.warn{color:var(--warn);background:rgba(239,107,107,.1);border-color:rgba(239,107,107,.3)}
  .badge.unknown{color:var(--ink-3);background:rgba(123,134,152,.1);border-color:rgba(123,134,152,.25)}
  .card-foot{
    display:flex;align-items:baseline;justify-content:space-between;gap:10px;
    border-top:1px solid var(--line-soft);padding-top:9px;
    font-size:12px;
  }
  .card-foot a{font-family:var(--mono);font-size:11.5px;overflow-wrap:anywhere}
  .date{font-family:var(--mono);font-size:11px;color:var(--ink-3);white-space:nowrap}

  .empty{
    max-width:1480px;margin:48px auto;padding:40px 24px;text-align:center;
    border:1px dashed var(--line);border-radius:var(--radius);color:var(--ink-2);
  }
  .empty strong{display:block;color:var(--ink);font-size:16px;margin-bottom:6px}
  .empty p{margin:0 0 14px;font-size:13.5px}
  .empty button{
    font-family:inherit;font-size:13px;padding:6px 14px;border-radius:6px;
    background:var(--surface-2);color:var(--ink);border:1px solid var(--line);cursor:pointer;
  }
  .empty button:hover{border-color:var(--accent)}
  [hidden]{display:none !important}

  /* ---------- 页脚 ---------- */
  footer{border-top:1px solid var(--line-soft);padding-top:28px;padding-bottom:56px}
  .foot-inner{max-width:1480px;margin:0 auto;display:grid;gap:22px;grid-template-columns:1fr}
  @media (min-width:900px){.foot-inner{grid-template-columns:1.4fr 1fr 1fr}}
  footer h2{font-size:12px;font-family:var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin:0 0 8px;font-weight:600}
  footer p{margin:0 0 8px;font-size:13px;color:var(--ink-2);max-width:56ch}
  footer ul{list-style:none;margin:0;padding:0;font-size:13px}
  footer li{margin-bottom:5px;color:var(--ink-2)}
  .sig{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);margin-top:10px}

  @media (max-width:640px){
    body{font-size:15px}
    .toolbar{position:static}
    .legend{font-size:12px;gap:4px 14px}
  }
  @media (prefers-reduced-motion:reduce){
    *{transition:none !important;animation:none !important}
    .card:hover{transform:none}
  }
  @media print{
    body{background:#fff;color:#111}
    body::before,.toolbar,.nav,.cat-doc{display:none}
    .top,.cat,footer{border-color:#ccc}
    h1 em{color:#111;-webkit-text-fill-color:#111}
    .risk,.card{background:#fff;border-color:#bbb;break-inside:avoid;box-shadow:none}
    .card-desc,.cat-desc,footer p,footer li{color:#333}
    .badge,.caps li{border-color:#bbb;color:#111;background:#fff}
    .date,.form,.cat-num,.cat-idx,.eyebrow{color:#555}
    a{color:#111;text-decoration:underline}
    a[href^="http"]::after{content:" (" attr(href) ")";font-size:9px;word-break:break-all}
  }
</style>
</head>
<body>

<header class="top wrap">
  <div class="top-inner">
    <p class="eyebrow"><b>Voice OSS Radar</b> · v0.1.0 · 更新于 2026-10-27</p>
    <h1>语音开源雷达<br><em>{{TOTAL}} 个项目，11 个分类，每条都标了许可</em></h1>
    <p class="lede">持续收集与核实的语音方向开源项目索引。不只列仓库地址——每个项目都记清它能干什么、坑在哪、代码许可与<b>权重许可</b>能不能商用、什么时候核实的。</p>

    <div class="risk">
      <div class="risk-head">
        <h2>先看许可风险：{{TOTAL}} 个项目里有相当一部分"看着开源，其实不能商用"</h2>
        <p>代码许可与权重许可分开判定</p>
      </div>
      <div class="bar" role="img" aria-label="项目许可分布：可商用、需逐项确认、禁止商用、待确认四类占比">
        {{SEGS}}
      </div>
      <ul class="legend">
{{LEGEND}}
      </ul>
    </div>
  </div>
</header>

<nav class="nav wrap" aria-label="分类导航">
  <ul>
{{NAV}}
  </ul>
</nav>

<div class="toolbar wrap">
  <div class="toolbar-inner">
    <div class="search-row">
      <div class="search">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4.2-4.2"></path></svg>
        <label for="q" class="visually-hidden" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">搜索项目</label>
        <input id="q" type="search" placeholder="搜索项目名、能力、语言、许可……例如 FunASR / 克隆 / 中文" autocomplete="off">
      </div>
      <p class="count" role="status" aria-live="polite"><b id="shown">{{TOTAL}}</b> / {{TOTAL}} 个项目</p>
    </div>
    <div class="chips" id="cat-chips" role="group" aria-label="按分类筛选">
{{CAT_CHIPS}}
    </div>
    <div class="chips" id="lic-chips" role="group" aria-label="按许可筛选">
{{LIC_CHIPS}}
    </div>
  </div>
</div>

<main class="wrap">
{{SECTIONS}}

  <div class="empty" id="empty" hidden>
    <strong>没有匹配的项目</strong>
    <p>换个关键词，或者把筛选条件放开一点。</p>
    <button type="button" id="reset">重置全部筛选</button>
  </div>
</main>

<footer class="wrap">
  <div class="foot-inner">
    <div>
      <h2>维护规则</h2>
      <p>每周扫一次新项目与重大版本，每月复核全部条目的活跃度与许可变更。所有条目带核实日期，过期即视为待复核。</p>
      <p>收录标准：有公开仓库或权重、能说清解决什么问题、仍在维护、许可明确。纯云端 API 与停更超 18 个月的项目不收。</p>
      <p class="sig">数据源：<a href="{{REPO}}/blob/main/data/projects.yaml" target="_blank" rel="noopener noreferrer">data/projects.yaml</a> · 本页由该文件自动生成</p>
    </div>
    <div>
      <h2>三条贯穿全表的结论</h2>
      <ul>
        <li>中文语音的默认答案在 FunASR 系，不在 Whisper 系</li>
        <li>许可证要看权重，不是看代码</li>
        <li>上游音频（AEC → 降噪 → VAD）决定上限</li>
      </ul>
    </div>
    <div>
      <h2>仓库</h2>
      <ul>
        <li><a href="{{REPO}}" target="_blank" rel="noopener noreferrer">github.com/xiaopengs/voice-oss-radar</a></li>
        <li><a href="{{REPO}}/blob/main/README.md" target="_blank" rel="noopener noreferrer">README 与选型速查</a></li>
        <li><a href="{{REPO}}/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer">贡献指南</a></li>
        <li><a href="{{REPO}}/blob/main/CHANGELOG.md" target="_blank" rel="noopener noreferrer">变更记录</a></li>
      </ul>
    </div>
  </div>
</footer>

<script>
(function () {
  try {
    var q = document.getElementById('q');
    var shown = document.getElementById('shown');
    var empty = document.getElementById('empty');
    var reset = document.getElementById('reset');
    var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
    var sections = Array.prototype.slice.call(document.querySelectorAll('.cat'));
    var catChips = Array.prototype.slice.call(document.querySelectorAll('#cat-chips .chip'));
    var licChips = Array.prototype.slice.call(document.querySelectorAll('#lic-chips .chip'));
    var state = { cat: 'all', lic: 'all', text: '' };

    function apply() {
      var n = 0;
      var perCat = {};
      cards.forEach(function (c) {
        var okCat = state.cat === 'all' || c.closest('.cat').getAttribute('data-cat') === state.cat;
        var okLic = state.lic === 'all' || c.getAttribute('data-lic') === state.lic;
        var okText = !state.text || (c.getAttribute('data-search') || '').indexOf(state.text) !== -1;
        var visible = okCat && okLic && okText;
        c.hidden = !visible;
        if (visible) {
          n++;
          var k = c.closest('.cat').getAttribute('data-cat');
          perCat[k] = (perCat[k] || 0) + 1;
        }
      });
      sections.forEach(function (s) {
        var k = s.getAttribute('data-cat');
        s.hidden = !perCat[k];
      });
      shown.textContent = n;
      empty.hidden = n !== 0;
    }

    q.addEventListener('input', function () {
      state.text = q.value.trim().toLowerCase();
      apply();
    });

    catChips.forEach(function (b) {
      b.addEventListener('click', function () {
        state.cat = b.getAttribute('data-cat');
        catChips.forEach(function (x) {
          var on = x === b;
          x.classList.toggle('is-active', on);
          x.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        apply();
      });
    });

    licChips.forEach(function (b) {
      b.addEventListener('click', function () {
        state.lic = b.getAttribute('data-lic');
        licChips.forEach(function (x) {
          var on = x === b;
          x.classList.toggle('is-active', on);
          x.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        apply();
      });
    });

    reset.addEventListener('click', function () {
      q.value = '';
      state = { cat: 'all', lic: 'all', text: '' };
      catChips.forEach(function (x, i) {
        x.classList.toggle('is-active', i === 0);
        x.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
      });
      licChips.forEach(function (x, i) {
        x.classList.toggle('is-active', i === 0);
        x.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
      });
      apply();
      q.focus();
    });

    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href').slice(1);
        var t = document.getElementById(id);
        if (!t) return;
        e.preventDefault();
        if (t.hidden) {
          q.value = '';
          state = { cat: 'all', lic: 'all', text: '' };
          catChips.forEach(function (x, i) {
            x.classList.toggle('is-active', i === 0);
            x.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
          });
          licChips.forEach(function (x, i) {
            x.classList.toggle('is-active', i === 0);
            x.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
          });
          apply();
        }
        t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  } catch (err) {
    /* 脚本失败时静态卡片仍完整可读 */
  }
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
