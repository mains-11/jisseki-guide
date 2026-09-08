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
MERGE_TOOL = "https://www.ilovepdf.com/ja/merge_pdf"   # PDF結合（無料・登録不要）

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

def merge_link(text="複数のPDFを1つにまとめる方法"):
    """まとめ方の解説（必要書類ページ内）へ誘導する短いリンク"""
    return f'<p class="hint"><a href="jisseki.html#merge">{text}</a></p>'

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
 ("確定検査", "<p>提出内容にもとづき、事務局が確認・検査を行います。不備があれば差戻しの連絡が届きますので、指示された期間内にご対応ください。</p>"),
 ("補助金確定内容の承認", "<p>検査が終わると、事務局から承認の依頼が届きます。申請マイページの【確定検査の結果】を開き、補助金の交付予定額と振込先口座を確認して承認します。SMS認証が必要です。</p>"
  + warn("この承認を忘れると補助金は受け取れません", "<p>期日までに承認されなかった場合、<b>交付決定の取消し</b>となります。事務局からの通知メールが届いたら、必ず期日までに手続きしてください。</p>")),
 ("補助金の交付", "<p>承認後に補助金額が確定し、登録した口座に振り込まれます。振込までは確定から<b>約1か月</b>かかります。</p>"),
 ("事業実施効果報告", "<p>補助金の受取後も、決められた期間内にITツールの活用状況を報告する義務があります。時期が来たら別途ご案内します。</p>"),
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
 (FIXED_NO["shashin"], "jisseki-hw-shashin.html", "ハードウェアの写真", "ラベルを貼ってから撮影します。設置状態とラベルの写真が必要です。"),
])}

{note("番号は何ですか", "<p>ファイル名の先頭につける番号です。書類の種類ごとに決まっているので、当てはまらない書類がある方は番号が飛びます。飛んでいても問題ありません。</p>")}

<h2>ファイルの形式</h2>
{warn("形式と容量の決まりがあります", "<p>添付できるのは <b>PDF・JPEG・PNG</b> のいずれかで、<b>1ファイル10MB未満</b>です。<b>Excelファイルは添付できません</b>ので、PDFに変換してください。</p>")}

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
 ("複数枚あるときは1つにまとめる",
  '<p>1つの項目に複数枚ある場合は、必ず1つのPDFにまとめてください。'
  'まとめ方は<a href="#merge">次の項目</a>で説明します。</p>'),
])}

<h2 id="merge">複数のPDFを1つにまとめる</h2>
<p>「1つのPDFにまとめてください」と書かれている箇所は、この方法でまとめられます。無料で、会員登録も要りません。</p>
{steps([
 ("まとめたいPDFを1か所に集める",
  "<p>デスクトップなどに、まとめたいファイルをすべて置いておきます。並べたい順番が決まっている場合は、ファイル名の先頭に 1、2、3 と番号を付けておくと迷いません。</p>"),
 ("PDF結合のページを開く",
  f'<p><a class="btn" href="{MERGE_TOOL}" target="_blank" rel="noopener">iLovePDF（PDF結合）を開く</a></p>'),
 ("ファイルを選ぶ",
  "<p>赤い「PDFファイルを選択」ボタンを押し、まとめたいファイルをすべて選びます。ファイルをまとめて画面にドラッグしても構いません。</p>"),
 ("順番を整える",
  "<p>画面に並んだファイルをドラッグして、提出したい順番に並べ替えます。順番は結果に反映されるので、ここで確認してください。</p>"),
 ("結合してダウンロードする",
  "<p>右下の「PDF結合」ボタンを押すと処理が始まります。終わったら「結合されたPDFのダウンロード」を押して保存し、決められたファイル名に変更してください。</p>"),
])}

{note("外部のサービスです", f"<p>iLovePDFはPDFを扱う無料のウェブサービスで、アップロードしたファイルは一定時間後に自動で削除されます。それでも通帳など大切な書類を外部に送ることに不安がある場合は、下の方法をお使いいただくか、ファイルをそのまま{CONTACT}までお送りください。こちらでまとめます。</p>")}

{note("パソコンだけでまとめる方法（画像の場合）", "<p>写真やスキャン画像であれば、外部サービスを使わずにまとめられます。まとめたい画像をすべて選んで右クリック →「印刷」→ プリンターの一覧から <b>Microsoft Print to PDF</b> を選ぶと、1つのPDFとして保存できます。</p>")}

<h2>すべての書類に共通する条件</h2>
<p>提出前に、次の5点をご確認ください。チェックを入れながら確認できます。</p>
{check([
 "文字がはっきり読める（ぼやけていない、影で隠れていない）",
 "書類の全体が入っている（端が切れていない）",
 "日付の順番が「契約・発注 → 納品 → 請求 → 支払い」になっている",
 "会社名・屋号が、交付申請の内容と同じ表記になっている",
 "金額が請求書とすべての書類で一致している",
])}

{warn("書類に手を加えないでください", "<p>塗りつぶし・切り取り・文字の書き足しをしたものは受理されません。原本のまま提出してください。ただし、マイナンバーや保険者番号などが写り込んでいる場合は、その部分だけ黒く塗りつぶしてください。</p>")}

<h2>当てはまる方だけ必要な書類</h2>
<p>次の3つは、条件に当てはまる方のみ提出します。心当たりがある場合は{CONTACT}までご相談ください。</p>
{table(["書類", "必要になる方"], [
 ("請求・支払内訳シート", "請求書と支払証憑が<b>どちらも複数枚</b>ある方。申請マイページの【実績報告について】からダウンロードできます。"),
 ("取得財産等管理台帳", "買取で導入したITツールに、<b>単価50万円以上</b>のものがある方。実績報告の提出確認画面からダウンロードし、作成・保管します。"),
 ("インボイス登録通知書", "交付申請のときに<b>インボイス登録で加点を希望した</b>方。適格請求書発行事業者の登録通知書を提出します。"),
])}

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
 ("請求日", "契約・発注の日以降、かつ<b>支払日より前</b>になっているか<br><small>支払ったあとに発行された請求書は認められません。</small>"),
 ("請求元", "支援事業者の名称と完全に一致しているか（法人格を省略していないか）"),
 ("品目", "交付決定を受けた製品・型番が、ITツールごとに分けて記載されているか<br><small>「一式」とまとめた表記は認められません。</small>"),
 ("数量・単価", "実際に導入した数と一致しているか"),
 ("金額", "交付申請時の金額と一致しているか（税抜・税込の表記も確認）"),
 ("値引き", "値引きがある場合、合計からの一括ではなく、製品ごとの単価に反映されているか"),
])}

{note("補助対象外の費用が含まれるとき", "<p>補助対象の費用にマーカーを引くなどして、対象と対象外が見分けられるようにしてください。</p>")}

{warn("金額が違うとき", f"<p>交付決定額と請求額が異なる場合は、そのまま提出せず{CONTACT}までご連絡ください。別の手続きが必要になることがあります。</p>")}

<h2>提出前のチェック</h2>
{merge_link("複数枚あるときのまとめ方はこちら")}
{check([
 f"{PARTNER}から届いた請求書のPDFをパソコンに保存した",
 "複数枚に分かれている場合は、1つのPDFにまとめた",
 "ファイル名を「1_請求明細書_事業者名」にした",
])}

{manual_note("jisseki-seikyusho.html")}
""")

# ---------------------------------------------------------------- 2 支払証憑
PAGES["jisseki-shiharai.html"] = ("2 支払証憑", "支払いが完了したことを示す控えの用意のしかた。", f"""
<h1>支払証憑</h1>
{summary("請求書の金額を「たしかに支払いました」と示す控えです。支払い方法によって、提出するものの組み合わせが変わります。1点だけでは足りない場合があります。")}
{filebox(FIXED_NO["shiharai"], "2_支払証憑_事業者名", "全員が必要です")}

{warn("使える支払い方法は2つだけです", "<p><b>銀行振込</b>、または<b>クレジットカード1回払い</b>のみが対象です。それ以外の方法で支払った場合、補助対象として認められません。</p>")}

<h2>対象にならない支払い方法</h2>
{ul([
 "現金での支払い（引き出した現金を窓口やATMで振り込んだ場合も対象外です）",
 "クレジットカードのリボ払い・分割払い",
 "法人で、代表者など個人名義の口座・カードからの支払い",
 "個人事業主で、家族や親族名義の口座・カードからの支払い",
])}
<p>振込は「事業者の口座」から「支援事業者の口座」へ行ってください。</p>

<h2>支払い方法ごとに提出するもの</h2>
{table(["支払い方法", "提出するもの"], [
 ("ATMで振込した", "ATMの利用明細　＋　通帳の表紙　＋　通帳の取引ページ　<b>（3点）</b>"),
 ("金融機関の窓口で振込した", "振込依頼書　＋　通帳の表紙　＋　通帳の取引ページ　<b>（3点）</b>"),
 ("ネットバンキングで振込した", "振込完了が分かる画面　＋　通帳の表紙　<b>（2点）</b><br><small>画面に口座名義人や口座情報が出ていない場合は、それが分かるページも添付します。</small>"),
 ("クレジットカードで支払った", "クレジットカードの利用明細　<b>（1点）</b>"),
])}
<p>複数ある場合は、順番を整えて1つのPDFにまとめてください。</p>
{merge_link()}

{note("通帳の表紙が必要な理由", "<p>誰の口座から支払ったかを確認するためです。利用明細の「依頼人名」や「振込依頼人」だけでは口座名義人と判断されず、不備になります。当座預金をお使いの場合は、通帳の代わりに当座勘定照合表や入金帳を提出してください。</p>")}

<h2>銀行振込のときに写っていなければならない情報</h2>
{check([
 "金融機関名",
 "振込日（請求書の請求日以降であること）",
 "振込元の口座情報（金融機関名・支店名・口座種別・口座番号・口座名義人）",
 "振込先が支援事業者であること",
 "振込金額（請求金額以上であること）",
 "振込が完了していること（「承認待ち」「未完了」「作成中」は不可）",
])}

{warn("振込予約をした場合", "<p>振込指定日を過ぎてから実績報告を行ってください。指定日を迎えていないと支払い完了とみなされません。画面の出力も、指定日を過ぎてから行ってください。</p>")}

<h2>クレジットカードのときに写っていなければならない情報</h2>
{check([
 "カードの名義人（法人は法人名義、個人事業主は代表者名義）",
 "利用日（請求書の請求日以降であること）",
 "利用金額・請求金額（請求金額以上であること）",
 "引き落とし口座（法人は法人名義、個人事業主は事業主名義）",
 "利用内容（導入したITツールと支援事業者名が分かること）",
 "1回払いであること",
])}
{note("カード番号は隠してください", "<p>明細にクレジットカード番号が記載されている場合は、黒く塗りつぶすなどして読み取れないようにしてください。</p>")}

<h2>複数回に分けて支払った場合</h2>
<p>支払日の古い順に番号を付け、1つのPDFにまとめてください。口座が複数あるときは、口座ごとに「支払いの控え → 通帳の表紙 → 通帳の取引ページ」の順に並べます。</p>
{merge_link()}
{note("請求書も支払証憑も複数枚ある場合", f"<p>「請求・支払内訳シート」の提出が必要です。申請マイページの【実績報告について】からダウンロードできます。作成にお困りの場合は{CONTACT}までご連絡ください。</p>")}

<h2>よくある差戻しの例</h2>
{okng(
 ["振込完了画面と通帳の表紙をそろえて1つのPDFにしたもの",
  "通帳の該当ページを、項目名まで含めて撮影したもの",
  "複数回に分けた場合、すべての控えを古い順にまとめたもの"],
 ["振込完了画面だけを提出したもの（口座名義人が確認できない）",
  "金額の部分だけを切り取ったもの、残高を黒く塗りつぶしたもの",
  "「振込予約を受け付けました」の画面（実行前のため不可）",
  "振込精査表"])}

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

{warn("導入したソフトの数だけ必要です", "<p>補助対象のソフトウェアが複数ある場合は、<b>すべてのソフトウェア</b>の画面が必要です。1つ分だけでは不足になります。ただし、同じソフトウェアを複数導入している場合は、1つ分の画面で差し支えありません。</p>")}

<h2>用意するもの</h2>
{check([
 "ログイン後の管理画面など、ソフトウェア名と事業者名が表示されている画面",
 "画面に事業者名が表示されないソフトの場合は、契約書や発注書など契約時の書類",
 "パッケージソフトの場合は、ライセンス証書やライセンスキーがわかる書類",
])}
{note("事業者名が画面に出ないとき", "<p>そのソフトの画面と一緒に、契約時の書類（契約書・発注書など）を提出してください。書類には「事業者と支援事業者の間の契約であること」「導入したソフトについての契約であること」が分かる必要があります。2つを1つのPDFにまとめて添付します。</p>")}

<h2>画面の撮り方</h2>
{steps([
 ("画面全体を写す", "<p>Windowsなら、キーボードの <b>Windowsキー ＋ Shift ＋ S</b> を同時に押すと、画面を切り取って保存できます。"
  "一部だけでなく、ブラウザの画面全体が入るように撮ってください。</p>"),
 ("必要な情報が写っているか確かめる", "<p>事業者名・アカウント名・日付が読み取れるか確認します。文字が小さくて読めない場合は、画面を拡大してから撮り直してください。</p>"),
 ("1つのPDFにまとめる", '<p>複数の画面が必要な場合は、順番を整えて1つのPDFにします。'
  'まとめ方は<a href="jisseki.html#merge">こちら</a>をご覧ください。</p>'),
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
 "納品日（契約日以降になっていること）",
 "納品元の名称（支援事業者名と一致していること）",
 "納品先の事業者名（申請した事業者名と一致していること）",
 "製品名・型番",
 "数量",
])}
<p>付属品も補助対象に含めている場合は、付属品の明細も分かるようにしてください。納品書に金額の記載がある場合は、実績報告の内容と食い違いがないようにしてください。</p>

{note("メーカーの出荷伝票しかない場合", f"<p>型番と数量が確認できれば差し支えありません。判断に迷う場合は{COMPANY}担当へご連絡ください。</p>")}

{note("パソコン等とPOSレジ等の両方を導入した場合", "<p>入力画面は「パソコン・タブレット等」と「POSレジ等」で分かれており、それぞれに納品書の欄があります。それぞれの欄に、該当する機器の納品書を添付してください。1枚の納品書に両方の機器が記載されている場合は、同じファイルを両方の欄に添付します。</p>")}

{manual_note("jisseki-hw-nouhin.html")}
""")

# ---------------------------------------------------------------- 6 写真
PAGES["jisseki-hw-shashin.html"] = ("7 ハードウェアの写真", "導入した機器へのラベル貼付と現物写真の撮り方。", f"""
<h1>ハードウェアの写真</h1>
{summary("導入した機器に「この補助金で買ったもの」と分かるラベルを貼り、その状態を撮影して提出します。撮影の前にラベルを貼る作業が必要です。")}
{filebox(FIXED_NO["shashin"], "7_ハードウェア導入情報（現物写真）_事業者名", "ハードウェアを導入した方のみ")}

{warn("先にラベルを貼ってください", "<p>写真を撮る前に、機器にシールやラベルを貼る必要があります。貼らずに撮影すると、撮り直しになります。</p>")}

<h2>1. ラベルを貼る</h2>
<p>本事業で導入した製品であることを見分けられるように、機器の現物にシールやラベルを貼ります。市販のラベルシールに手書きや印刷で表示すれば差し支えありません。</p>
{table(["項目", "決まり"], [
 ("書く内容", "デジタル化・AI導入補助金2026 と分かる表示"),
 ("大きさ", "設置した状態で文字が読み取れるサイズ"),
 ("貼る場所", "表に貼り、常に見える状態にする（表への貼付が難しい製品は裏面でも可）"),
 ("付属品", "付属品にも貼付する。貼付が難しいものは、対象製品であることを管理簿等で管理する"),
 ("複数台の場合", "「対象製品－1」「対象製品－2」のように番号を付けて管理する"),
])}

<h2>2. 写真を撮る</h2>
<p>機器1台につき、次の2種類を撮影します。</p>
{steps([
 ("設置した状態の写真",
  "<p>事業所に設置され、使える状態になっていることが分かるように撮ります。"
  "<b>ハードウェア1台につき1枚ずつ</b>必要です。導入した全ての機器を撮影してください。</p>"
  + warn("パソコン・タブレット・モバイルPOSレジの場合",
         "<p>補助金で導入した<b>ソフトウェアを立ち上げた状態</b>で撮影してください。電源を切った状態や、別の画面が映った状態では認められません。</p>")),
 ("ラベルの貼付が確認できる写真",
  "<p>貼ったラベルの文字が読み取れる距離で撮ります。ピントが合っているか必ず確認してください。</p>"),
])}
<p>付属品や周辺機器も補助対象に含めている場合は、本体とともに写るように撮影します。1枚に収まらない場合は、別に撮影しても差し支えありません。</p>

<h2>3. 1つのファイルにまとめる</h2>
<p>ハードウェアごとに「設置状態」と「起動画面（ラベルが確認できる写真）」の2種類をまとめ、全ての機器分を1つのPDFにして添付します。</p>
{merge_link()}

<h2>よくある差戻しの例</h2>
{okng(
 ["ラベルを貼り、その文字が読み取れる写真",
  "事業所に設置され、ソフトウェアが立ち上がった状態の写真",
  "導入した機器を1台ずつ、もれなく撮影したもの"],
 ["ラベルを貼っていない状態の写真",
  "段ボールに入ったまま、床に置いたままの写真",
  "複数台あるのに1台分しか撮っていないもの",
  "暗い・ぶれている・文字が読めない写真"])}

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
 ("通帳がある口座", '通帳の<b>表紙</b>と<b>表紙の裏面</b>の写しを、1つのファイルにまとめて提出'),
 ("ネット銀行など通帳がない口座", "口座情報が表示されたページ（下の6項目がすべて確認できるもの）"),
 ("当座預金の口座", "当座勘定照合表、残高証明書、当座勘定入金票など"),
])}
{merge_link()}
{warn("キャッシュカードは認められません", "<p>キャッシュカードの写真では受理されません。通帳またはネットバンキングの口座情報ページを提出してください。</p>")}
<p>次の6項目がすべて読み取れる必要があります。</p>
{ul(["金融機関名", "金融機関コード", "支店名", "口座種別", "口座番号", "口座名義人"])}

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
      <label><input type="radio" name="waku" value="inv" checked><span>インボイス枠（インボイス対応類型）</span></label>
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

{warn("インボイス枠には2つの類型があります", f"<p>このページの手順は、<b>インボイス対応類型</b>を申請した方向けです。パソコンやPOSレジが補助対象になるのはこの類型のみです。<b>電子取引類型</b>を申請した方は、取引先アカウント一覧など別の書類が必要になりますので、{CONTACT}までご連絡ください。</p>")}

{note("区分がわからないとき", f"<p>交付決定通知書に記載された枠・類型と、申請時に選んだ事業者区分をご確認ください。判断がつかない場合は{CONTACT}までお問い合わせください。</p>")}

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
 ("実績報告の画面を開く",
  ol(["「申請者メニュー」をクリックする", "「実績報告情報編集」をクリックする"])
  + note("「実績報告情報詳細」ではありません", "<p>提出の操作は<b>実績報告情報編集</b>から行います。「詳細」は内容を見るだけの画面です。</p>")),
 ("内容を確認する", "<p>最終確認画面が開きます。添付したファイルと入力内容が正しく表示されているかを、上から順に確認してください。</p>"
  + check(["添付したファイルが開ける（別のファイルを間違えて添付していない）",
           "口座情報の入力に誤りがない",
           "金額が請求書と一致している"])
  + note("備考欄について", "<p>画面に【備考欄】がありますが、事務局から指示があったときだけ使う欄です。問い合わせや申請情報の変更などを書かないでください。</p>")
  + nextbtn()),
 ("SMS認証を行う", "<p>本人確認のため、携帯電話へのSMS認証があります。</p>"
  + ol(["「認証コード発行」ボタンを押す",
        "登録した携帯電話にSMSで認証コードが届く",
        "届いたコードを画面に入力する"])
  + note("コードが届かないとき", f"<p>登録した携帯電話番号あてに届きます。番号が変わっている場合は提出できませんので、{CONTACT}までご連絡ください。</p>")),
 ("事務局へ提出する", "<p>認証が終わったら、提出ボタンを押します。</p>" + nextbtn("事務局へ提出")
  + warn("押したあとは修正できません", "<p>提出後の内容は変更できません。ボタンを押す前に、もう一度上から見直してください。事務局から差戻しがあった場合は、その指示にしたがって修正し、あらためて提出します。</p>")),
 ("完了を確認する", "<p>ステータスが「実績報告済」に変われば完了です。あとは事務局の確定検査を待ちます。</p>"),
])}

<h2>このあとの流れ</h2>
{steps([
 ("確定検査", "<p>事務局が内容を検査します。確認事項や不備があった場合は差戻しの連絡が届きますので、<b>指示された期間内に</b>対応してください。期間内に不備が解消しないと、交付決定の取消しとなる場合があります。</p>"),
 ("補助金確定内容の承認", "<p>検査が終わると、事務局から承認の依頼が届きます。申請マイページの【確定検査の結果】を開き、補助金の交付予定額と振込先口座を確認します。相違がなければ宣誓事項にチェックを入れ、「確定検査の結果を承認する」を押し、SMS認証を行ってください。</p>"
  + warn("承認しないと補助金は受け取れません", "<p>期日までに承認されなかった場合、<b>交付決定の取消し</b>となります。通知メールが届いたら必ず期日までに手続きしてください。</p>")),
 ("補助金の交付", "<p>承認後に補助金額が確定し、確定通知書が発行されます。振込までは確定から<b>約1か月</b>かかります。</p>"),
])}

{note("提出後も書類は保管してください", "<p>補助事業が完了した年度の終了後<b>5年間</b>は、交付決定通知書・契約書・注文書・納品書・請求書・振込の控えなど、すべての書類を保管する義務があります。</p>")}

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
        tags = ['<span class="tag tag--on">インボイス枠（インボイス対応類型）</span>',
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
        "<p>最初に実績報告の流れと注意事項の説明画面が表示されます。"
        "「ITツールの解約」に関する説明動画を見てチェックを入れないと、次に進めません。</p>"
        + ol(["画面内の説明動画のリンクをクリックする",
              "動画を最後まで視聴したら、ブラウザの「戻る」で説明画面に戻る",
              "内容を理解できたことを示すチェックを入れる"]) + nextbtn()))

    st.append(("請求書を添付する",
        "<p>1番のファイルを選んで添付します。</p>"
        + filebox(no_seikyu, f"{no_seikyu}_請求明細書_事業者名") + nextbtn()))

    st.append(("支払方法を選択する",
        "<p>実際に支払った方法を選びます。対象になるのはこの2つだけです。"
        "両方の方法で支払った場合は、両方を選べます。</p>"
        + '<ul class="choices"><li>銀行振込</li><li>クレジットカード払い</li></ul>'
        + note("どちらを選ぶか", "<p>事業者の口座から振り込んだ場合は「銀行振込」、カードで支払った場合は「クレジットカード払い」を選びます。"
               "選んだ方法に応じて、次の画面で添付する証憑が変わります。</p>")
        + nextbtn()))

    st.append(("支払証憑を添付する",
        "<p>支払い方法によって必要な点数が変わります。ATM・窓口振込は3点、ネットバンキングは2点を1つのPDFにまとめてください。</p>"
        + filebox(no_shiharai, f"{no_shiharai}_支払証憑_事業者名")
        + note("通帳の表紙を忘れずに", '<p>振込の控えだけでは口座名義人が確認できず、不備になります。'
               '<a href="jisseki-shiharai.html">支払証憑のページ</a>で組み合わせを、'
               '<a href="jisseki.html#merge">こちら</a>でPDFのまとめ方をご確認ください。</p>')
        + nextbtn()))

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
                body = (f"<p>{label}を導入しているので「はい」を選び、2つのファイルを添付します。"
                        f"この画面では<b>{label}の分</b>を添付してください。</p>"
                        + choices(["はい", "いいえ"], 0)
                        + filebox(no_nouhin, f"{no_nouhin}_ハードウェア導入情報（納品書）_事業者名", "納品書の欄")
                        + filebox(no_shashin, f"{no_shashin}_ハードウェア導入情報（現物写真）_事業者名", "現物写真の欄")
                        + warn("写真はラベルを貼ってから撮影します",
                               '<p>「この補助金で導入した」と分かるシール・ラベルを機器に貼り、設置状態と'
                               'ラベルの写真を撮る必要があります。パソコン・タブレット・モバイルPOSレジは'
                               'ソフトウェアを立ち上げた状態で撮影してください。'
                               '<br><a href="jisseki-hw-shashin.html">写真の撮り方を見る</a></p>')
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
{note("ファイルの形式", "<p>添付できるのは PDF・JPEG・PNG のいずれかで、1ファイル10MB未満です。Excelファイルは添付できません。</p>")}
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
