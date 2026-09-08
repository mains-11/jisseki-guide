#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
実績報告ガイド　静的サイトビルダー
  使い方:  python3 tools/build.py
  出力先:  リポジトリ直下の *.html
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROGRAM = "デジタル化・AI導入補助金"          # 旧：IT導入補助金
SITE_NAME = f"{PROGRAM}｜実績報告ガイド"
SITE_SHORT = "実績報告ガイド"
SITE_SUB = "実績報告のご案内"
COMPANY = "株式会社M'AINS"
CONTACT = "株式会社M'AINSの担当者"   # 問い合わせ先の言い方
PARTNER = "支援事業者"                  # 役割として呼ぶときの言い方

MYPAGE = "https://portal.shinsei.it-shien.smrj.go.jp/"
OFFICIAL = "https://it-shien.smrj.go.jp/"
# サイドバー・フッターから開く公式マニュアル（事務局公開の実績報告マニュアル）
MANUAL = "https://it-shien.smrj.go.jp/pdf/it2026_manual_jisseki.pdf"

# 各ページ本文に置く「公式マニュアルを開く」の個別リンク。
# 指定がないページは MANUAL を使います。
PAGE_MANUAL = {
    "jisseki-seikyusho.html": "https://drive.google.com/file/d/1dQQg_1LinYMtvOC_N2WFwt20AyGrZScu/view?usp=sharing",
    "jisseki-shiharai.html":  "https://drive.google.com/file/d/1MrK8x40OThBEIvcraDZ0a5T_ZTlUONTe/view?usp=sharing",
    "jisseki-software.html":  "https://drive.google.com/file/d/1rIW-8cTN_0BaEpa0abh7A0yorz6khQlx/view?usp=sharing",
    "jisseki-hw-nouhin.html": "https://drive.google.com/file/d/1PRgpTiK5o9b6OTVgl8RYVuZN0DEWc78p/view?usp=sharing",
    "jisseki-hw-shashin.html":"https://drive.google.com/file/d/153jFU6aE-c25ByFyWokID10Yif-P5MWf/view?usp=sharing",
    "jisseki-kouza.html":     "https://drive.google.com/file/d/1ZXgy65cdAF1lCzcJfLVPQsgaLfzdN5FV/view?usp=sharing",
}
KANA_TOOL = "https://tinyurl.com/kouza-kana"

# 添付ファイル名の先頭番号。書類の種類ごとに固定します。
# 目次・書類一覧の表示順にそのまま通し番号を振ります。
# 並び順を変えるときは、ここと NAV の両方を直してください。
FIXED_NO = {"seikyu": "1", "shiharai": "2", "software": "3", "kouza": "4",
            "juugyouin": "5", "nouhin": "6", "shashin": "7"}

# ---------------------------------------------------------------- ナビゲーション
NAV = [
    ("index.html", "はじめに", []),
    ("jisseki.html", "実績報告に必要な書類", [
        # 表示順は「かならず必要な4点 → 小規模事業者のみ → ハードウェアのみ」
        ("jisseki-seikyusho.html", "1 請求書（請求明細書）"),
        ("jisseki-shiharai.html", "2 支払証憑"),
        ("jisseki-software.html", "3 ソフトウェアの利用確認"),
        ("jisseki-kouza.html", "4 補助金の受取口座"),
        ("jisseki-juugyouin.html", "5 従業員一覧"),
        ("jisseki-hw-nouhin.html", "6 ハードウェアの納品書"),
        ("jisseki-hw-shashin.html", "7 ハードウェアの写真"),
    ]),
    ("tejun.html", "申請マイページの入力手順", [
        ("tejun-tsujo.html", "通常枠"),
        ("tejun-inv-chusho-pc1-pos1.html", "中小企業｜PC あり／POS あり"),
        ("tejun-inv-chusho-pc1-pos0.html", "中小企業｜PC あり／POS なし"),
        ("tejun-inv-chusho-pc0-pos1.html", "中小企業｜PC なし／POS あり"),
        ("tejun-inv-chusho-pc0-pos0.html", "中小企業｜PC なし／POS なし"),
        ("tejun-inv-shokibo-pc1-pos1.html", "小規模事業者｜PC あり／POS あり"),
        ("tejun-inv-shokibo-pc1-pos0.html", "小規模事業者｜PC あり／POS なし"),
        ("tejun-inv-shokibo-pc0-pos1.html", "小規模事業者｜PC なし／POS あり"),
        ("tejun-inv-shokibo-pc0-pos0.html", "小規模事業者｜PC なし／POS なし"),
        ("tejun-teishutsu.html", "事務局への提出"),
    ]),
]

ORDER, LABEL, PARENT = [], {}, {}
for href, label, kids in NAV:
    ORDER.append(href); LABEL[href] = label
    for k_href, k_label in kids:
        ORDER.append(k_href); LABEL[k_href] = k_label; PARENT[k_href] = label

# ---------------------------------------------------------------- 部品
def e(t): return html.escape(t, quote=False)

def note(title, body, kind="note"):
    return f'<div class="{kind}"><b>{title}</b>{body}</div>'

def warn(title, body): return note(title, body, "warn")

def summary(text):
    return f'<div class="summary"><b>かんたんに言うと</b><p>{text}</p></div>'

def meta(items):
    return '<p class="meta">' + "".join(f"<span>{i}</span>" for i in items) + "</p>"

def filebox(no, name, where=""):
    w = f'<span class="file__where">{where}</span>' if where else ""
    return (f'<div class="file"><div class="file__no">{no}</div>'
            f'<div class="file__body"><span class="file__name">{name}</span>{w}</div></div>')

def ol(items): return '<ol class="substeps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def ul(items): return '<ul class="ul">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def plainul(items): return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def nextbtn(label="次へ"): return f'<p><span class="uibtn">{label}</span></p>'

def check(items):
    li = "".join(f'<li><label><input type="checkbox"><span>{t}</span></label></li>' for t in items)
    return f'<ul class="check">{li}</ul>'

def okng(ok_items, ng_items):
    return ('<div class="okng">'
            f'<div class="is-ok"><h4>これならOK</h4>{plainul(ok_items)}</div>'
            f'<div class="is-ng"><h4>これはNG</h4>{plainul(ng_items)}</div>'
            "</div>")

def twocol(t1, items1, t2, items2):
    return ('<div class="okng">'
            f'<div class="is-ok"><h4>{t1}</h4>{plainul(items1)}</div>'
            f'<div class="is-ng"><h4>{t2}</h4>{plainul(items2)}</div>'
            "</div>")

def choices(items, pick):
    li = []
    for i, t in enumerate(items):
        if i == pick:
            li.append(f'<li class="pick">{t}<b>これを選ぶ</b></li>')
        else:
            li.append(f"<li>{t}</li>")
    return '<ul class="choices">' + "".join(li) + "</ul>"

def steps(items):
    out = ['<ol class="steps">']
    for title, body in items:
        out.append(f"<li><h3>{title}</h3>{body}</li>")
    out.append("</ol>")
    return "".join(out)

def table(headers, rows):
    h = "".join(f"<th>{c}</th>" for c in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

def terms(pairs):
    return '<dl class="terms">' + "".join(
        f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in pairs) + "</dl>"

def cards(items):
    li = "".join(f'<li><a href="{h}"><strong>{t}</strong><span>{d}</span></a></li>' for h, t, d in items)
    return f'<ul class="cards">{li}</ul>'

def doclist(items):
    """items: (番号, リンク先, タイトル, 説明)"""
    li = "".join(f'<li><a href="{h}"><i>{n}</i><span><strong>{t}</strong>'
                 f'<span>{d}</span></span></a></li>' for n, h, t, d in items)
    return f'<ul class="doclist">{li}</ul>'

def group(title, sub):
    return f'<div class="grouplabel"><h3>{title}</h3><span>{sub}</span></div>'

def phase(current):
    ph = [("①", "書類を添付して送信", "貴社での作業"),
          ("②", "内容の確認", f"{COMPANY}での作業"),
          ("③", "事務局へ提出", "貴社での作業")]
    cells = []
    for i, (n, t, who) in enumerate(ph, 1):
        cls = ' class="is-now"' if i == current else ""
        cells.append(f'<div{cls}><b>{n}</b><strong>{t}</strong><span class="who">{who}</span></div>')
    return '<div class="phase">' + "".join(cells) + "</div>"

def manual_note(slug=None):
    url = PAGE_MANUAL.get(slug, MANUAL)
    return note("公式のマニュアルもあります",
                "<p>画面の細かい表示まで確認したいときはこちらをご覧ください。"
                f'<br><a href="{url}" target="_blank" rel="noopener">公式マニュアルを開く</a></p>')

# ---------------------------------------------------------------- テンプレート
def sidenav(cur):
    out = ['<nav class="sidenav" aria-label="サイト内メニュー"><ul>']
    for href, label, kids in NAV:
        a = ' aria-current="page"' if href == cur else ""
        out.append(f'<li><a href="{href}"{a}>{label}</a>')
        if kids:
            out.append('<ul class="sub">')
            for k_href, k_label in kids:
                ka = ' aria-current="page"' if k_href == cur else ""
                out.append(f'<li><a href="{k_href}"{ka}>{k_label}</a></li>')
            out.append("</ul>")
        out.append("</li>")
    out.append("</ul></nav>")
    return "".join(out)

def pager(cur):
    i = ORDER.index(cur)
    prev_h = ORDER[i - 1] if i > 0 else None
    next_h = ORDER[i + 1] if i < len(ORDER) - 1 else None
    p = (f'<a class="prev" href="{prev_h}"><b>前のページ</b><span>{LABEL[prev_h]}</span></a>'
         if prev_h else '<div class="placeholder"></div>')
    n = (f'<a class="next" href="{next_h}"><b>次のページ</b><span>{LABEL[next_h]}</span></a>'
         if next_h else '<div class="placeholder"></div>')
    return f'<nav class="pager" aria-label="前後のページ">{p}{n}</nav>'

def render(slug, title, desc, body):
    crumb = ['<a href="index.html">ホーム</a>']
    if slug in PARENT:
        crumb.append(f"<span>/</span>{e(PARENT[slug])}")
    if slug != "index.html":
        crumb.append(f"<span>/</span>{e(LABEL[slug])}")
    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}｜{PROGRAM} {SITE_SHORT}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="author" content="{COMPANY}">
<meta property="og:title" content="{e(title)}｜{PROGRAM} {SITE_SHORT}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">本文へ移動</a>

<header class="topbar">
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="sidebar">目次</button>
  <div class="topbar__title"><a href="index.html">{SITE_SHORT}</a></div>
</header>

<button class="scrim" type="button" tabindex="-1" aria-hidden="true"></button>

<aside class="sidebar" id="sidebar">
  <a class="brand" href="index.html">
    <span class="brand__mark">交付決定後</span>
    <span class="brand__prog">{PROGRAM}</span>
    <span class="brand__name">{SITE_SHORT}</span>
    <span class="brand__sub">{SITE_SUB}</span>
  </a>
  {sidenav(slug)}
  <p class="sidelink"><a href="{MANUAL}" target="_blank" rel="noopener">公式マニュアルを開く</a></p>
  <p class="sidefoot">{COMPANY}<br>本サイトの内容の無断転載・複製・再配布を禁じます。</p>
</aside>

<main class="main" id="main">
  <div class="wrap">
    <p class="crumb">{"".join(crumb)}</p>
    {body}
    {pager(slug)}
    <footer class="sitefoot">
      本サイトは、独立行政法人中小企業基盤整備機構および経済産業省が公表する情報をもとに作成しています。
      制度の最新情報・詳細は<a href="{OFFICIAL}" target="_blank" rel="noopener">{PROGRAM}の公式サイト</a>、
      画面の操作は<a href="{MANUAL}" target="_blank" rel="noopener">公式マニュアル</a>をご確認ください。
      <br>{PROGRAM}は、令和7年度補正予算事業からIT導入補助金より名称が変更されています。
      <br>&copy; {COMPANY}
    </footer>
  </div>
</main>

<script src="assets/site.js"></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(doc)
    print("  出力:", slug)

# ================================================================ 各ページ本文
PAGES = {}

# ---------------------------------------------------------------- はじめに
PAGES["index.html"] = ("はじめに", "交付決定から補助金が振り込まれるまでの流れと、実績報告の進め方をご案内します。", f"""
<h1>交付決定、おめでとうございます</h1>
<p class="lead">補助金を受け取るには、このあと「実績報告」という手続きが必要です。はじめての方でも順番どおりに進められるよう、書類のそろえ方から入力画面の操作まで、ひとつずつご案内します。</p>

{summary("補助金は、交付決定だけでは振り込まれません。「書類をそろえる」「画面に入力して送信する」「事務局へ提出する」――この3つを終えて、はじめて振込に進みます。")}

<h2>やることは3つだけです</h2>
<ul class="entry">
  <li><a href="jisseki.html"><i>1</i><span><strong>書類をそろえる</strong>
    <span>請求書や支払いの控えなど、必要なものを集めてPDFにします。ここが一番時間のかかるところです。</span>
    <em>目安：数日〜1週間</em></span></a></li>
  <li><a href="tejun.html"><i>2</i><span><strong>申請マイページに入力して送信する</strong>
    <span>集めた書類を画面に添付し、口座情報を入力します。送信すると{PARTNER}に引き継がれます。</span>
    <em>目安：20〜30分</em></span></a></li>
  <li><a href="tejun-teishutsu.html"><i>3</i><span><strong>事務局へ提出する</strong>
    <span>{PARTNER}の確認が終わったあと、もう一度ログインして提出ボタンを押します。この操作で完了です。</span>
    <em>目安：5分</em></span></a></li>
</ul>

{warn("よくある取り違え", f"<p>2番の「送信」で終わったと思ってしまう方が多くいらっしゃいます。2番の時点では{PARTNER}に届いただけで、事務局には届いていません。必ず3番まで行ってください。3番のご案内は{COMPANY}からお送りします。</p>")}

<h2>補助金が振り込まれるまでの流れ</h2>
{steps([
 ("交付決定", "<p>申請が採択され、交付決定通知が届きます。通知書は申請マイページからダウンロードできます。</p>"
  + ol([f'<a href="{MYPAGE}" target="_blank" rel="noopener">申請マイページ</a>にログインする',
        "「申請者メニュー」を開く",
        "「交付申請情報詳細」を開く",
        "「交付決定通知書」をクリックしてダウンロードする"])),
 ("契約・発注", "<p>交付決定の日以降に、ソフトウェア・ハードウェアの契約と発注を行います。</p>"),
 ("請求・支払い・納品", "<p>契約・発注のあとに請求書が発行され、支払いと納品を行います。</p>"
  + warn("順番を必ず守ってください", "<p>「契約・発注」より前に「納品」や「請求・支払い」を行うと、補助金を受け取れなくなる場合があります。支払日は請求書の発行日以降にしてください。</p>")),
 ("実績報告", '<p>必要書類をそろえ、申請マイページから報告します。<b>ここからが、このサイトでご案内する作業です。</b></p>'
  + '<p><a class="btn" href="jisseki.html">必要な書類を見る</a></p>'),
 ("確定検査", "<p>提出内容にもとづき、事務局が確認・検査を行います。不備があれば差戻しの連絡が届きます。</p>"),
 ("補助金の交付", "<p>確定後、登録した口座に補助金が振り込まれます。</p>"),
])}

<h2>知っておくと読みやすくなる言葉</h2>
<p>案内のなかで出てくる言葉です。分からなくなったら、このページに戻って確認してください。</p>
{terms([
 ("実績報告", "「補助金を使ってこういう買い物をし、こう支払いました」と報告する手続きのことです。"),
 ("証憑（しょうひょう）", "証拠になる書類のことです。「支払証憑」なら、支払ったことがわかる控えを指します。"),
 ("申請マイページ", "補助金の手続きを行う専用サイトです。GビズIDでログインします。"),
 ("GビズID", "国の行政サービスで共通して使えるIDです。交付申請のときに作ったものをそのまま使います。"),
 ("事務局", "補助金を運営している窓口です。提出した書類はここで審査されます。"),
 ("IT導入支援事業者", f"申請をお手伝いするパートナー事業者のことで、本件では{COMPANY}を指します。"),
])}

{manual_note()}

{note("ご利用にあたって", "<p>申請マイページはパソコンでの操作を前提としています。Windows の Microsoft Edge または Google Chrome の最新版をご利用ください。スマートフォンだけでは入力できない画面があります。</p>")}
""")

# ---------------------------------------------------------------- 必要書類（一覧）
PAGES["jisseki.html"] = ("実績報告に必要な書類", "実績報告で提出する書類の一覧と、ファイルの作り方。", f"""
<h1>実績報告に必要な書類</h1>
<p class="lead">まず、ここに挙げた書類をすべてPDFにしてパソコンに保存してください。先に全部そろえておけば、入力画面ではファイルを選ぶだけになり、一度で終わります。</p>

{summary("書類は全部で7種類ありますが、全員が7つ必要なわけではありません。下の3つのグループを見て、自分に当てはまるものだけを用意してください。")}

{phase(1)}

<h2>書類の一覧</h2>

{group("かならず必要", "全員が対象です・4点")}
{doclist([
 (FIXED_NO["seikyu"], "jisseki-seikyusho.html", "請求書（請求明細書）", f"{COMPANY}が発行してお送りします。金額と宛名をご確認ください。"),
 (FIXED_NO["shiharai"], "jisseki-shiharai.html", "支払証憑", "銀行振込が完了したことがわかる控えです。"),
 (FIXED_NO["software"], "jisseki-software.html", "ソフトウェアの利用確認", "導入したソフトが使える状態になっていることを示す画面の記録です。"),
 (FIXED_NO["kouza"], "jisseki-kouza.html", "補助金の受取口座", "補助金の振込先となる口座の、通帳またはネットバンキング画面です。"),
])}

{group("小規模事業者として申請した方だけ", "中小企業として申請した方は不要です・1点")}
{doclist([
 (FIXED_NO["juugyouin"], "jisseki-juugyouin.html", "従業員一覧", "従業員数の要件を満たしていることを示す一覧です。"),
])}

{group("パソコン・タブレット・POSレジ等を導入した方だけ", "ソフトウェアのみの方は不要です・2点")}
{doclist([
 (FIXED_NO["nouhin"], "jisseki-hw-nouhin.html", "ハードウェアの納品書", "型番と数量がわかる納品書です。"),
 (FIXED_NO["shashin"], "jisseki-hw-shashin.html", "ハードウェアの写真", "現物と設置状況がわかる写真です。"),
])}

{note("番号は何ですか", "<p>ファイル名の先頭につける番号です。書類の種類ごとに決まっているので、当てはまらない書類がある方は番号が飛びます。飛んでいても問題ありません。</p>")}

<h2>ファイル名のつけ方</h2>
<p>ファイル名は「番号＿書類名＿事業者名」の形にしてください。事業者名は交付申請に使った名称です。</p>
{table(["書類", "ファイル名の例"], [
 ("請求書", "1_請求明細書_株式会社サンプル.pdf"),
 ("支払証憑", "2_支払証憑_株式会社サンプル.pdf"),
 ("ソフトウェア証憑", "3_ソフトウェア証憑_株式会社サンプル.pdf"),
 ("口座情報", "4_口座情報_株式会社サンプル.pdf"),
 ("従業員一覧", "5_従業員一覧_株式会社サンプル.pdf"),
 ("ハードウェア納品書", "6_ハードウェア導入情報（納品書）_株式会社サンプル.pdf"),
 ("ハードウェア写真", "7_ハードウェア導入情報（現物写真）_株式会社サンプル.pdf"),
])}

<h2>写真や紙の書類をPDFにする方法</h2>
<p>「PDFにしてください」と言われても分からない場合は、次のどちらかで作れます。</p>
{steps([
 ("スマートフォンで撮る場合",
  "<p>カメラで撮影したあと、写真アプリの「共有」または「印刷」からPDFとして保存できます。</p>"
  + ul(["iPhone：写真を開く →「共有」→「プリント」→ 指で画面を広げる →「共有」→「ファイルに保存」",
        "Android：写真を開く →「印刷」→ 保存先を「PDF形式で保存」に変更 → 保存"])
  + "<p>作ったPDFは、メールで自分宛に送るなどしてパソコンに移してください。</p>"),
 ("パソコンで作る場合",
  "<p>画像やWord・Excelのファイルを開き、「印刷」を選びます。プリンターの一覧から <b>Microsoft Print to PDF</b> を選んで印刷すると、PDFとして保存されます。</p>"),
 ("複数枚を1つにまとめる",
  "<p>1つの項目に複数枚ある場合は、必ず1つのPDFにまとめてください。"
  f"まとめ方が分からない場合は、撮影したファイルをそのまま{CONTACT}までお送りいただければ、こちらでまとめます。</p>"),
])}

<h2>すべての書類に共通する条件</h2>
<p>提出前に、次の5点をご確認ください。チェックを入れながら確認できます。</p>
{check([
 "文字がはっきり読める（ぼやけていない、影で隠れていない）",
 "書類の全体が入っている（端が切れていない）",
 "日付の順番が「契約・発注 → 納品 → 請求 → 支払い」になっている",
 "会社名・屋号が、交付申請の内容と同じ表記になっている",
 "金額が請求書とすべての書類で一致している",
])}

{warn("書類に手を加えないでください", "<p>塗りつぶし・切り取り・文字の書き足しをしたものは受理されません。原本のまま提出してください。</p>")}

{manual_note()}

<p><a class="btn" href="tejun.html">書類がそろったら、入力手順へ進む</a></p>
""")

# ---------------------------------------------------------------- 1 請求書
PAGES["jisseki-seikyusho.html"] = ("1 請求書（請求明細書）", "請求書（請求明細書）の確認ポイント。", f"""
<h1>請求書（請求明細書）</h1>
{summary(f"{PARTNER}から届いた請求書を、そのままPDFで添付します。ご自身で作成する必要はありません。届いたら金額と宛名をご確認ください。")}
{filebox(FIXED_NO["seikyu"], "1_請求明細書_事業者名", "全員が必要です")}

<h2>届いたら確認していただく点</h2>
{table(["項目", "確認すること"], [
 ("宛名", "交付申請に使った事業者名と同じ表記になっているか"),
 ("発行日", "契約・発注の日以降になっているか"),
 ("品目", "交付決定を受けた製品・型番がもれなく記載されているか"),
 ("数量・単価", "実際に導入した数と一致しているか"),
 ("金額", "交付申請時の金額と一致しているか（税抜・税込の表記も確認）"),
])}

{warn("金額が違うとき", f"<p>交付決定額と請求額が異なる場合は、そのまま提出せず{CONTACT}までご連絡ください。別の手続きが必要になることがあります。</p>")}

<h2>提出前のチェック</h2>
{check([
 f"{PARTNER}から届いた請求書のPDFをパソコンに保存した",
 "複数枚に分かれている場合は、1つのPDFにまとめた",
 "ファイル名を「1_請求明細書_事業者名」にした",
])}

{manual_note("jisseki-seikyusho.html")}
""")

# ---------------------------------------------------------------- 2 支払証憑
PAGES["jisseki-shiharai.html"] = ("2 支払証憑", "振込が完了したことを示す控えの用意のしかた。", f"""
<h1>支払証憑</h1>
{summary("請求書の金額を「たしかに振り込みました」と示す控えです。支払いは銀行振込で行い、その記録を提出します。")}
{filebox(FIXED_NO["shiharai"], "2_支払証憑_事業者名", "全員が必要です")}

{warn("現金払い・手形は使えません", "<p>支払いの事実を確認できないため、対象外です。かならず事業用の口座からの振込にしてください。</p>")}

<h2>支払い方法ごとの用意のしかた</h2>
{table(["支払い方法", "提出するもの"], [
 ("窓口・ATMで振込した", "振込明細票（利用控え）をスキャン、または撮影したもの"),
 ("ネットバンキングで振込した", "振込完了画面、または取引明細の画面をPDFで保存したもの"),
 ("通帳に記帳した", "通帳の表紙と、口座番号が見える見開きページ、および振込が記帳されたページ"),
])}

<h2>写っていなければならない情報</h2>
{check([
 "振込日（請求書の発行日以降になっていること）",
 "振込金額（請求書の金額と同じであること）",
 "振込元の口座名義（申請した事業者のもの）",
 f"振込先の口座名義（{PARTNER}）",
])}

<h2>よくある差戻しの例</h2>
{okng(
 ["振込完了画面をそのままPDFにしたもの",
  "通帳の該当ページを、余白まで含めて撮影したもの",
  "複数回に分けた場合、すべての控えを1つのPDFにまとめたもの"],
 ["金額の部分だけを切り取ったもの",
  "残高を黒く塗りつぶしたもの",
  "「振込予約を受け付けました」の画面（実行前のため不可）"])}

{manual_note("jisseki-shiharai.html")}
""")

# ---------------------------------------------------------------- 3 従業員一覧
PAGES["jisseki-juugyouin.html"] = ("5 従業員一覧", "小規模事業者として申請した場合に必要な従業員一覧。", f"""
<h1>従業員一覧</h1>
{summary("小規模事業者として申請した方だけが必要です。申請マイページからフォーマットをダウンロードし、従業員の人数を記入して提出します。")}
{filebox(FIXED_NO["juugyouin"], "5_従業員一覧_事業者名", "小規模事業者として申請した方のみ")}

{note("この書類が必要なのは、小規模事業者として申請した方だけです", "<p>中小企業として申請した方は、この書類は不要です。次のページへお進みください。判断がつかない場合は、下の手順でご自身で確認できます。</p>")}

<h2>自分が小規模事業者かどうかを確かめる</h2>
{steps([
 ("申請したときの区分を確認する（もっとも確実です）",
  "<p>小規模事業者かどうかは、交付申請のときにすでに申告しています。まずは申請内容をご確認ください。</p>"
  + ol([f'<a href="{MYPAGE}" target="_blank" rel="noopener">申請マイページ</a>にログインする',
        "「申請者メニュー」をクリックする",
        "「交付申請情報詳細」をクリックする",
        "事業者情報の欄で、事業者区分の記載を確認する"])
  + "<p>「小規模事業者」となっていれば、この書類が必要です。「中小企業」であれば不要です。</p>"),
 ("従業員の人数で判定する",
  "<p>申請内容が確認できない場合は、業種と従業員数で判定できます。"
  "業種によって人数の基準が違うため、必ずご自身の業種の行をご覧ください。</p>"
  + table(["業種", "小規模事業者となる人数"], [
      ("商業・サービス業（宿泊業・娯楽業を除く）", "常時使用する従業員 <b>5人以下</b>"),
      ("サービス業のうち宿泊業・娯楽業", "常時使用する従業員 <b>20人以下</b>"),
      ("製造業・建設業・運輸業 その他", "常時使用する従業員 <b>20人以下</b>"),
  ])
  + "<p>商業とは、卸売業・小売業を指します。飲食店、理美容、士業、医療・介護などはサービス業にあたります。"
  "この人数を超える場合は中小企業となり、この書類は不要です。</p>"),
 ("それでも判断がつかないとき",
  f'<p>事務局が用意している判定ツールで確認できます。組織形態と業種を選ぶだけです。</p>'
  f'<p><a class="btn btn--ghost" href="{OFFICIAL}applicant/subsidy/" target="_blank" rel="noopener">申請対象者チェッカーを開く</a></p>'
  f"<p>それでも分からない場合は、{CONTACT}までお問い合わせください。</p>"),
])}

<h2>従業員の数え方</h2>
<p>ここでいう従業員は「常時使用する従業員」です。働いている方全員を数えるわけではありません。</p>
{twocol("人数に含める", [
  "正社員",
  "契約社員（期間の定めなく雇用している方）",
  "パート・アルバイトのうち、2か月を超えて引き続き雇用している方",
], "人数に含めない", [
  "会社の役員（取締役・監査役など）",
  "個人事業主ご本人",
  "事業主と同居している親族（専従者）",
  "日々雇い入れている方",
  "2か月以内の期間を決めて雇用している方",
  "季節的な仕事で4か月以内の期間を決めて雇用している方",
  "試用期間中で、雇い入れから14日以内の方",
])}
<p>数えた結果、対象となる従業員がいない場合は「0名」となります。その場合も、0名と記載した一覧を提出してください。</p>

{note("医療法人・社会福祉法人・学校法人・商工会などの場合", "<p>これらの組織形態は、従業員数にかかわらず小規模事業者には該当しません。中小企業としての申請となるため、この書類は不要です。</p>")}

<h2>書類の作り方</h2>

<h3>1. フォーマットをダウンロードする</h3>
<p>様式は申請マイページから入手できます。まずファイルを手元に用意してください。</p>
{steps([
 ("申請マイページにログインする",
  f'<p><a class="btn" href="{MYPAGE}" target="_blank" rel="noopener">申請マイページを開く</a></p>'),
 ("「申請者メニュー」をクリックする", "<p>ログイン後の最初の画面にあります。</p>"),
 ("「実績報告について」をクリックする", "<p>実績報告に関する案内と様式がまとまっている画面です。</p>"),
 ("「従業員一覧」をクリックしてダウンロードする",
  "<p>ダウンロードしたファイルは、パソコンの分かりやすい場所（デスクトップなど）に保存してください。</p>"),
])}

<h3>2. 記入する</h3>
<p>ダウンロードしたフォーマットに、次の内容を記入します。</p>
{table(["項目", "記載する内容"], [
 ("氏名", "常時使用する従業員の氏名（番号などでの管理でも可）"),
 ("雇用形態", "正社員・パート・アルバイトなど"),
 ("合計人数", "一覧の最後に合計を記載"),
])}

<h3>3. PDFにして保存する</h3>
<p>記入し終えたExcelファイルを開き、「印刷」を選び、プリンターの一覧から <b>Microsoft Print to PDF</b> を選んで印刷するとPDFになります。ファイル名は「5_従業員一覧_事業者名」にしてください。</p>
<p>賃金台帳や労働者名簿の写しでも差し支えありません。</p>

<h2>提出前のチェック</h2>
{check([
 "小規模事業者として申請していることを確認した",
 "申請マイページからフォーマットをダウンロードした",
 "氏名・雇用形態・合計人数を記入した",
 "PDFにして、ファイル名を「5_従業員一覧_事業者名」にした",
])}
""")

# ---------------------------------------------------------------- 4 ソフトウェア
PAGES["jisseki-software.html"] = ("3 ソフトウェアの利用確認", "導入したソフトウェアが使える状態であることを示す資料。", f"""
<h1>ソフトウェアの利用確認</h1>
{summary("導入したソフトが「たしかに納品され、使える状態になっている」ことを示す画面の記録です。管理画面などを撮影してPDFにします。")}
{filebox(FIXED_NO["software"], "3_ソフトウェア証憑_事業者名", "全員が必要です")}

<h2>用意するもの</h2>
{check([
 "ログイン後の管理画面など、事業者名またはアカウント名が表示されている画面",
 "契約内容がわかる画面（プラン名・契約期間・アカウント数など）",
 "パッケージソフトの場合は、ライセンス証書やライセンスキーがわかる書類",
])}

<h2>画面の撮り方</h2>
{steps([
 ("画面全体を写す", "<p>Windowsなら、キーボードの <b>Windowsキー ＋ Shift ＋ S</b> を同時に押すと、画面を切り取って保存できます。"
  "一部だけでなく、ブラウザの画面全体が入るように撮ってください。</p>"),
 ("必要な情報が写っているか確かめる", "<p>事業者名・アカウント名・日付が読み取れるか確認します。文字が小さくて読めない場合は、画面を拡大してから撮り直してください。</p>"),
 ("1つのPDFにまとめる", "<p>複数の画面が必要な場合は、順番を整えて1つのPDFにします。</p>"),
])}

{manual_note("jisseki-software.html")}
""")

# ---------------------------------------------------------------- 5 納品書
PAGES["jisseki-hw-nouhin.html"] = ("6 ハードウェアの納品書", "パソコン・POSレジ等を導入した場合の納品書。", f"""
<h1>ハードウェアの納品書</h1>
{summary("パソコン・タブレット・POSレジなどを導入した方だけが必要です。何を何台納品したかがわかる納品書を提出します。")}
{filebox(FIXED_NO["nouhin"], "6_ハードウェア導入情報（納品書）_事業者名", "ハードウェアを導入した方のみ")}

<h2>記載されている必要がある項目</h2>
{check([
 "納品日（契約・発注の日以降になっていること）",
 "納品先の事業者名",
 "製品名・型番",
 "数量",
])}

{note("メーカーの出荷伝票しかない場合", f"<p>型番と数量が確認できれば差し支えありません。判断に迷う場合は{COMPANY}担当へご連絡ください。</p>")}

{warn("入力画面での注意", "<p>パソコン等とPOSレジ等の両方を導入した方は、入力画面に納品書の欄が2か所出てきます。同じPDFを両方の欄に添付してください。</p>")}

{manual_note("jisseki-hw-nouhin.html")}
""")

# ---------------------------------------------------------------- 6 写真
PAGES["jisseki-hw-shashin.html"] = ("7 ハードウェアの写真", "導入した機器の現物写真の撮り方。", f"""
<h1>ハードウェアの写真</h1>
{summary("買った機器が実際に届き、事業所で使える状態になっていることを写真で示します。3種類の写真を撮り、1つのPDFにまとめます。")}
{filebox(FIXED_NO["shashin"], "7_ハードウェア導入情報（現物写真）_事業者名", "ハードウェアを導入した方のみ")}

<h2>撮る写真は3種類です</h2>
{steps([
 ("機器の全体", "<p>正面から、機器の形がはっきりわかるように撮ります。</p>"),
 ("型番・製造番号のラベル", "<p>本体の裏面や側面にあるシールを、文字が読める距離で撮ります。ピントが合っているか必ず確認してください。</p>"),
 ("設置している様子", "<p>事業所の中に置かれ、使える状態になっていることがわかるように撮ります。周りの様子も少し入れてください。</p>"),
])}

<h2>よくある差戻しの例</h2>
{okng(
 ["明るい場所で、ピントの合った写真",
  "台数が複数ある場合は、すべての機器を撮影したもの",
  "型番の文字が読み取れる写真"],
 ["段ボールに入ったままの写真",
  "床に置いたままで、設置が確認できない写真",
  "暗い・ぶれている・型番が読めない写真"])}

<h2>提出のしかた</h2>
<p>撮影した写真は、3種類まとめて1つのPDFにしてください。PDFの作り方は<a href="jisseki.html">必要な書類のページ</a>で説明しています。</p>

{manual_note("jisseki-hw-shashin.html")}
""")

# ---------------------------------------------------------------- 7 口座
PAGES["jisseki-kouza.html"] = ("4 補助金の受取口座", "補助金が振り込まれる口座の資料と、名義の確認方法。", f"""
<h1>補助金の受取口座</h1>
{summary("補助金の振込先になる口座の情報です。この書類を見ながら、入力画面に口座情報を打ち込むことになります。")}
{filebox(FIXED_NO["kouza"], "4_口座情報_事業者名", "全員が必要です")}

{warn("口座名義は、必ず事前に金融機関へ確認してください", "<p>金融機関に登録されている名義と<b>1文字も違わず一致</b>している必要があります。ここが最も差戻しの多いところです。スペースの有無、濁点・半濁点、法人格の略し方にご注意ください。</p>")}

<h2>口座名義（カナ）の書き方</h2>
<p>法人の場合、「株式会社」などは決まった記号に置き換えて登録されています。ご自身の口座がどう登録されているか分からない場合は、通帳やキャッシュカードの表記を確認するか、金融機関へお問い合わせください。</p>
{table(["会社名の形", "カナでの書き方の例"], [
 ("株式会社サンプル（前株）", "カ）サンプル"),
 ("サンプル株式会社（後株）", "サンプル（カ"),
 ("有限会社サンプル", "ユ）サンプル"),
 ("合同会社サンプル", "ド）サンプル"),
 ("個人事業主（屋号あり）", "屋号 ＋ 代表者名、または代表者名のみ（口座の登録どおり）"),
])}
<p><a class="btn btn--ghost" href="{KANA_TOOL}" target="_blank" rel="noopener">口座名義変換ツールを開く</a></p>
{note("ツールの使い方", "<p>会社名を入力すると、カナ表記の候補が表示されます。あくまで確認の補助ですので、最終的には金融機関に登録されている表記が正となります。</p>")}

<h2>提出するもの</h2>
{table(["口座の種類", "提出するもの"], [
 ("通帳がある口座", "通帳の表紙と、見開き1ページ目（金融機関名・支店名・口座番号・名義が見えるページ）"),
 ("ネット銀行など通帳がない口座", "口座情報が表示された画面（金融機関名・支店名・口座番号・名義がわかるもの）"),
])}

<h2>提出前のチェック</h2>
{check([
 "申請した事業者の口座である（代表者個人の口座は原則使えません）",
 "金融機関名・支店名・口座種別・口座番号・名義（カナ）がすべて読み取れる",
 "画面や通帳が途中で切れていない",
 "口座名義の表記を金融機関に確認した",
])}

{manual_note("jisseki-kouza.html")}
""")

# ---------------------------------------------------------------- 手順トップ
PAGES["tejun.html"] = ("申請マイページの入力手順", "枠と導入内容にあわせた入力手順の選び方。", f"""
<h1>申請マイページの入力手順</h1>
<p class="lead">入力する画面は、申請した枠と導入した内容によって変わります。下の質問に答えると、あなたに当てはまる手順ページが開きます。</p>

{summary("すべての方に同じ画面が出るわけではありません。まず自分がどのパターンかを選んでから、手順を読み進めてください。")}

{phase(1)}

{warn("先に書類をそろえてください", '<p>入力の途中でファイルが見つからないと、探しているあいだに画面が切れてしまうことがあります。<a href="jisseki.html">必要な書類</a>をすべてPDFにしてから始めてください。</p>')}

<h2>あてはまるものを選んでください</h2>
<form class="chooser" id="chooser">
  <fieldset>
    <legend>1. 申請した枠はどちらですか</legend>
    <div class="opts">
      <label><input type="radio" name="waku" value="inv" checked><span>インボイス枠</span></label>
      <label><input type="radio" name="waku" value="tsujo"><span>通常枠</span></label>
    </div>
  </fieldset>
  <fieldset data-inv>
    <legend>2. 事業者の区分はどちらですか</legend>
    <div class="opts">
      <label><input type="radio" name="kubun" value="chusho"><span>中小企業</span></label>
      <label><input type="radio" name="kubun" value="shokibo"><span>小規模事業者</span></label>
    </div>
  </fieldset>
  <fieldset data-inv>
    <legend>3. パソコン・タブレット等を導入しましたか</legend>
    <div class="opts">
      <label><input type="radio" name="pc" value="1"><span>導入した</span></label>
      <label><input type="radio" name="pc" value="0"><span>導入していない</span></label>
    </div>
  </fieldset>
  <fieldset data-inv>
    <legend>4. POSレジ等を導入しましたか</legend>
    <div class="opts">
      <label><input type="radio" name="pos" value="1"><span>導入した</span></label>
      <label><input type="radio" name="pos" value="0"><span>導入していない</span></label>
    </div>
  </fieldset>
  <p class="chooser__msg" id="chooser-msg" hidden>通常枠は、事業者の区分や導入内容にかかわらず入力手順が同じです。2〜4の質問はありません。</p>
  <div class="chooser__out" id="chooser-result" hidden>
    <p>あてはまる手順が決まりました。</p>
    <a class="btn" id="chooser-link" href="#">手順を開く</a>
  </div>
</form>

{note("区分がわからないとき", f"<p>交付決定通知書に記載された枠と、申請時に選んだ事業者区分をご確認ください。判断がつかない場合は{CONTACT}までお問い合わせください。</p>")}

{manual_note()}

<h2>一覧から選ぶ</h2>
{cards([("tejun-tsujo.html", "通常枠", "ソフトウェアのみを導入した通常枠の方はこちら。")]
       + [(h, t, "この区分の入力手順を開きます。") for h, t in NAV[2][2] if h.startswith("tejun-inv")]
       + [("tejun-teishutsu.html", "事務局への提出", f"{COMPANY}の確認後に行う、最後の操作です。")])}
""")

# ---------------------------------------------------------------- 事務局への提出
PAGES["tejun-teishutsu.html"] = ("事務局への提出", f"{COMPANY}の確認後に行う、最後の提出操作。", f"""
<h1>事務局への提出</h1>
<p class="lead">実績報告の最後の操作です。{COMPANY}からご案内が届いたら、この手順で提出してください。</p>

{summary(f"入力して送信しただけでは、事務局には届いていません。{COMPANY}の確認が終わったあと、貴社でもう一度ログインして提出ボタンを押していただく必要があります。")}

{meta(["所要時間：<b>5分ほど</b>", "使うもの：<b>パソコン・GビズID</b>", "行うのは：<b>貴社</b>"])}

{phase(3)}

{warn("この操作をしないと、実績報告は完了しません", f"<p>①の送信だけでは、書類は事務局に届いていません。{COMPANY}からのご案内が届いてから、この操作を行ってください。</p>")}

<h2>提出の手順</h2>
{steps([
 ("申請マイページにログインする", f'<p><a class="btn" href="{MYPAGE}" target="_blank" rel="noopener">申請マイページを開く</a></p>'
  + note("推奨環境", "<p>Windows の Microsoft Edge または Google Chrome の最新版でご利用ください。</p>")),
 ("実績報告の画面を開く", ol(["「申請者メニュー」をクリックする", "「実績報告情報詳細」をクリックする"])),
 ("内容を確認する", "<p>添付したファイルと入力内容が、画面に正しく表示されているかを上から順に確認します。</p>"
  + check(["添付したファイルが開ける（別のファイルを間違えて添付していない）",
           "口座情報の入力に誤りがない",
           "金額が請求書と一致している"])),
 ("事務局へ提出する", "<p>画面の一番下にあるボタンを押します。</p>" + nextbtn("事務局に提出")
  + warn("押したあとは修正できません", "<p>提出後の内容は変更できません。ボタンを押す前に、もう一度上から見直してください。事務局から差戻しがあった場合は、その指示にしたがって修正し、あらためて提出します。</p>")),
 ("完了を確認する", "<p>画面のステータスが「提出済み」に変われば完了です。あとは事務局の確定検査を待ちます。</p>"
  + note("このあとの流れ", "<p>検査で問題がなければ補助金額が確定し、登録した口座に振り込まれます。不備があった場合は事務局から差戻しの連絡が届きますので、内容を確認のうえご対応ください。</p>")),
])}

{manual_note()}
""")

# ---------------------------------------------------------------- 入力手順（枠別）
def build_tejun(kubun, pc, pos):
    """kubun: 'chusho' | 'shokibo' | 'tsujo'"""
    tsujo = (kubun == "tsujo")
    shokibo = (kubun == "shokibo")
    hw = bool(pc or pos) and not tsujo

    g = FIXED_NO
    no_seikyu, no_shiharai = g["seikyu"], g["shiharai"]
    no_software, no_kouza = g["software"], g["kouza"]
    no_juugyouin = g["juugyouin"] if shokibo else None
    no_nouhin = g["nouhin"] if hw else None
    no_shashin = g["shashin"] if hw else None

    if tsujo:
        title = "通常枠"
        tags = ['<span class="tag tag--on">通常枠</span>']
    else:
        kubun_ja = "小規模事業者" if shokibo else "中小企業"
        title = f"インボイス枠｜{kubun_ja}｜PC {'あり' if pc else 'なし'}／POS {'あり' if pos else 'なし'}"
        tags = ['<span class="tag tag--on">インボイス枠</span>',
                f'<span class="tag tag--on">{kubun_ja}</span>',
                f'<span class="tag tag--{"on" if pc else "off"}">パソコン・タブレット等 {"あり" if pc else "なし"}</span>',
                f'<span class="tag tag--{"on" if pos else "off"}">POSレジ等 {"あり" if pos else "なし"}</span>']

    files = [(no_seikyu, "1_請求明細書_事業者名"),
             (no_shiharai, "2_支払証憑_事業者名"),
             (no_software, "3_ソフトウェア証憑_事業者名"),
             (no_kouza, "4_口座情報_事業者名")]
    if shokibo:
        files.append((no_juugyouin, "5_従業員一覧_事業者名"))
    if hw:
        files.append((no_nouhin, "6_ハードウェア導入情報（納品書）_事業者名"))
        files.append((no_shashin, "7_ハードウェア導入情報（現物写真）_事業者名"))
    filelist = "".join(filebox(n, nm) for n, nm in files)

    st = []
    st.append(("申請マイページにログインする",
        f'<p><a class="btn" href="{MYPAGE}" target="_blank" rel="noopener">申請マイページを開く</a></p>'
        + note("推奨環境", "<p>Windows の Microsoft Edge または Google Chrome の最新版でご利用ください。</p>")
        + ol(["ログイン画面で、紫色の「GビズIDでログイン」を押す",
              "GビズIDのアカウントとパスワードを入力する",
              "画面の案内にしたがって二要素認証を行う",
              "ログイン後、「申請者メニュー」→「実績報告情報編集」へ進む"])
        + note("ログインできないとき", "<p>パスワードが分からない場合は、GビズIDのサイトから再設定してください。"
               "スマートフォンを機種変更した場合は、認証アプリの再登録が必要になることがあります。</p>")))

    st.append(("説明画面を確認する",
        "<p>最初に注意事項の説明画面が表示されます。動画を見てチェックを入れないと、次に進めません。</p>"
        + ol(["画面内の研修動画のリンクをクリックする",
              "動画を最後まで視聴したら、ブラウザの「戻る」で説明画面に戻る",
              "「動画を視聴して内容を理解しました」のチェックを入れる"]) + nextbtn()))

    st.append(("請求書を添付する",
        "<p>1番のファイルを選んで添付します。</p>"
        + filebox(no_seikyu, f"{no_seikyu}_請求明細書_事業者名") + nextbtn()))

    st.append(("支払方法を選択する",
        "<p>「銀行振込」を選択してください。</p>"
        + choices(["銀行振込", "クレジットカード払い"], 0) + nextbtn()))

    st.append(("支払証憑を添付する",
        filebox(no_shiharai, f"{no_shiharai}_支払証憑_事業者名") + nextbtn()))

    if shokibo:
        st.append(("その他資料を添付する",
            "<p>小規模事業者として申請しているため、従業員一覧を添付します。</p>"
            + filebox(no_juugyouin, f"{no_juugyouin}_従業員一覧_事業者名") + nextbtn()))
    else:
        st.append(("その他資料を確認する",
            "<p>中小企業として申請しているため、この画面で添付する資料はありません。"
            "画面の内容を確認して、そのまま次へ進みます。</p>" + nextbtn()))

    st.append(("ソフトウェア証憑を添付する",
        filebox(no_software, f"{no_software}_ソフトウェア証憑_事業者名") + nextbtn()))

    if not tsujo:
        for label, flag in (("パソコン・タブレット等", pc), ("POSレジ等", pos)):
            if flag:
                body = (f"<p>{label}を導入しているので「はい」を選び、2つのファイルを添付します。</p>"
                        + choices(["はい", "いいえ"], 0)
                        + filebox(no_nouhin, f"{no_nouhin}_ハードウェア導入情報（納品書）_事業者名", "納品書の欄")
                        + filebox(no_shashin, f"{no_shashin}_ハードウェア導入情報（現物写真）_事業者名", "現物写真の欄")
                        + nextbtn())
            else:
                body = (f"<p>{label}は導入していないので「いいえ」を選びます。ファイルの添付はありません。</p>"
                        + choices(["はい", "いいえ"], 1)
                        + nextbtn())
            st.append((f"ハードウェア導入情報（{label}）", body))

    st.append(("口座情報を添付する",
        filebox(no_kouza, f"{no_kouza}_口座情報_事業者名") + nextbtn()))

    st.append(("口座情報を入力する",
        "<p>いま添付したPDFを開き、そこに書かれている内容を画面の項目へ入力します。</p>"
        + warn("ここが一番間違えやすいところです",
               "<p>口座名義は、金融機関に登録されている表記と<b>1文字も違わず一致</b>している必要があります。"
               "スペース・濁点・半濁点にご注意ください。"
               f'<br><a href="{KANA_TOOL}" target="_blank" rel="noopener">口座名義変換ツールを開く</a>'
               '　<a href="jisseki-kouza.html">カナ表記の書き方を見る</a></p>')
        + table(["項目", "入力のしかた"], [
            ("金融機関名", "画面を下にスクロールし、紫色の「検索」ボタンをクリック → 全角カタカナで入力 → 入力欄の外をクリック →「検索」→ 候補から選択<br><small>文字を入力している間は「検索」ボタンを押せません。一度、入力欄の外をクリックしてください。</small>"),
            ("支店名", "金融機関名と同じ手順で検索して選択します。"),
            ("口座種別・口座番号", "通帳または口座情報の画面のとおりに入力します。"),
            ("口座名義（カナ）", "金融機関の登録どおりに入力します。"),
        ]) + nextbtn()))

    st.append(("実績報告の入力を完了する",
        "<p>入力確認画面で内容を確認し、画面の一番下のボタンを押します。</p>" + nextbtn("実績報告入力完了")
        + note("ここで①は完了です",
               f'<p>入力内容が{COMPANY}に引き継がれます。確認が終わりましたら、'
               f'③「<a href="tejun-teishutsu.html">事務局への提出</a>」の操作をご案内しますので、'
               "その連絡をお待ちください。</p>")))

    body = f"""
<h1>{e(title)}</h1>
<p class="lead">申請マイページでの操作手順です。画面の表示にあわせて、上から順に進めてください。</p>
<div class="tag-row">{"".join(tags)}</div>

{meta([f"ステップ数：<b>{len(st)}</b>", "所要時間：<b>20〜30分ほど</b>", "使うもの：<b>パソコン・GビズID</b>"])}

{phase(1)}

<h2>始める前に用意するファイル</h2>
<p>この区分では、次の{len(files)}つのファイルを使います。すべてPDFにして、すぐ選べる場所に置いてから始めてください。</p>
{filelist}
<p><a class="btn btn--ghost" href="jisseki.html">書類のそろえ方を確認する</a></p>

{manual_note()}

<h2>入力の手順</h2>
{steps(st)}

<h2>入力が終わったら</h2>
<p>ここまでで①は完了です。{COMPANY}が内容を確認し、問題がなければ③のご案内をお送りします。
届きましたら<a href="tejun-teishutsu.html">事務局への提出</a>の操作を行ってください。</p>
{warn("まだ提出は終わっていません", f"<p>「実績報告入力完了」を押した時点では、書類は{COMPANY}に届いただけです。事務局にはまだ届いていません。</p>")}
"""
    return title, f"{title}の申請マイページ入力手順。", body

PAGES["tejun-tsujo.html"] = build_tejun("tsujo", 0, 0)
for kubun in ("chusho", "shokibo"):
    for pc in (1, 0):
        for pos in (1, 0):
            PAGES[f"tejun-inv-{kubun}-pc{pc}-pos{pos}.html"] = build_tejun(kubun, pc, pos)

# ================================================================ 出力
if __name__ == "__main__":
    print("ビルドを開始します…")
    for slug in ORDER:
        title, desc, body = PAGES[slug]
        render(slug, title, desc, body)
    print(f"完了しました（{len(ORDER)}ページ）")
