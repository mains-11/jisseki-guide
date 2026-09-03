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
SITE_NAME = f"{PROGRAM}｜実績報告ガイド"       # サイト正式名称
SITE_SHORT = "実績報告ガイド"                  # スマホのヘッダーなど狭い場所用
SITE_SUB = "実績報告のご案内"                  # サブタイトル
COMPANY = "株式会社M'AINS"                     # 運営会社
MYPAGE = "https://portal.shinsei.it-shien.smrj.go.jp/"
OFFICIAL = "https://it-shien.smrj.go.jp/"

# ---------------------------------------------------------------- ナビゲーション
NAV = [
    ("index.html", "はじめに", []),
    ("jisseki.html", "実績報告に必要な書類", [
        ("jisseki-seikyusho.html", "請求書（請求明細書）"),
        ("jisseki-software.html", "ソフトウェアの利用確認"),
        ("jisseki-shiharai.html", "支払証憑"),
        ("jisseki-kouza.html", "補助金の受取口座"),
        ("jisseki-hw-nouhin.html", "ハードウェアの納品書"),
        ("jisseki-hw-shashin.html", "ハードウェアの写真"),
        ("jisseki-juugyouin.html", "従業員一覧"),
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

def filebox(no, name, where=""):
    w = f'<span class="file__where">{where}</span>' if where else ""
    return (f'<div class="file"><div class="file__no">{no}</div>'
            f'<div class="file__body"><span class="file__name">{name}</span>{w}</div></div>')

def ol(items): return "<ol class=\"substeps\">" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def ul(items): return "<ul class=\"ul\">" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def nextbtn(label="次へ"): return f'<p><span class="uibtn">{label}</span></p>'

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

def cards(items):
    li = "".join(f'<li><a href="{h}"><strong>{t}</strong><span>{d}</span></a></li>' for h, t, d in items)
    return f'<ul class="cards">{li}</ul>'

def phase(current):
    ph = [("①", "書類を添付して送信", "貴社での作業"),
          ("②", "内容の確認", "弊社での作業"),
          ("③", "事務局へ提出", "貴社での作業")]
    cells = []
    for i, (n, t, who) in enumerate(ph, 1):
        cls = ' class="is-now"' if i == current else ""
        cells.append(f'<div{cls}><b>{n}</b><strong>{t}</strong><span class="who">{who}</span></div>')
    return '<div class="phase">' + "".join(cells) + "</div>"

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
<meta property="og:title" content="{e(title)}｜{PROGRAM} {SITE_SHORT}">
<meta name="author" content="{COMPANY}">
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
  <p class="sidefoot">{COMPANY}<br>本サイトの内容の無断転載・複製・再配布を禁じます。</p>
</aside>

<main class="main" id="main">
  <div class="wrap">
    <p class="crumb">{"".join(crumb)}</p>
    {body}
    {pager(slug)}
    <footer class="sitefoot">
      本サイトは、独立行政法人中小企業基盤整備機構および経済産業省が公表する情報をもとに作成しています。
      制度の最新情報・詳細は必ず<a href="{OFFICIAL}" target="_blank" rel="noopener">{PROGRAM}の公式サイト</a>をご確認ください。
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
<p class="lead">ここから補助金の受取までに必要な手続きが「実績報告」です。このサイトでは、そろえる書類と申請マイページの入力手順を、画面の順番どおりにご案内します。</p>

{note("はじめにお読みください", "<p>実績報告は、①貴社での添付・送信　②弊社での確認　③貴社から事務局へ提出　の3段階で進みます。①が終わっただけでは提出は完了しません。</p>")}

<h2>補助金が振り込まれるまでの流れ</h2>
{steps([
 ("交付決定", "<p>申請が採択され、交付決定通知が届きます。通知書は申請マイページからダウンロードできます。</p>"
  + ol(["<a href=\"" + MYPAGE + "\" target=\"_blank\" rel=\"noopener\">申請マイページ</a>にログインする",
        "「申請者メニュー」を開く",
        "「交付申請情報詳細」を開く",
        "「交付決定通知書」をクリックしてダウンロードする"])),
 ("契約・発注", "<p>交付決定の日以降に、ソフトウェア・ハードウェアの契約と発注を行います。</p>"),
 ("請求・支払い・納品", "<p>契約・発注のあとに請求書が発行され、支払いと納品を行います。</p>"
  + warn("順番を必ず守ってください", "<p>「契約・発注」より前に「納品」や「請求・支払い」を行うと、補助金を受け取れなくなる場合があります。支払日は請求書の発行日以降にしてください。</p>")),
 ("実績報告", "<p>必要書類をそろえ、申請マイページから報告します。</p><p><a class=\"btn\" href=\"jisseki.html\">必要な書類を見る</a></p>"),
 ("確定検査", "<p>提出内容にもとづき、事務局が確認・検査を行います。不備があれば差戻しの連絡が届きます。</p>"),
 ("補助金の交付", "<p>確定後、登録した口座に補助金が振り込まれます。</p>"),
])}

<h2>このサイトの使い方</h2>
{cards([
 ("jisseki.html", "実績報告に必要な書類", "7種類の書類について、そろえ方と満たすべき条件をまとめています。"),
 ("tejun.html", "申請マイページの入力手順", "枠と導入内容を選ぶと、あてはまる入力手順のページが開きます。"),
])}
{note("ご利用にあたって", "<p>申請マイページはパソコンでの操作を前提としています。Windows の Microsoft Edge または Google Chrome の最新版をご利用ください。</p>")}
""")

# ---------------------------------------------------------------- 実績報告について
PAGES["jisseki.html"] = ("実績報告に必要な書類", "実績報告で提出する7種類の書類の一覧と、共通の注意点。", f"""
<h1>実績報告に必要な書類</h1>
<p class="lead">実績報告では、「発注 → 契約 → 納品 → 支払い」がすべて完了したことを書類で示します。導入した内容によって必要な書類が変わります。</p>

{phase(1)}

<h2>書類の一覧</h2>
<p>それぞれのページに、そろえ方と満たすべき条件をまとめています。ハードウェア関係の2点は、パソコン・タブレット・POSレジ等を導入した場合のみ必要です。</p>
{cards([
 ("jisseki-seikyusho.html", "請求書（請求明細書）", "弊社が発行します。金額と内訳を確認してください。"),
 ("jisseki-software.html", "ソフトウェアの利用確認", "導入したソフトが使える状態であることを示す画面の記録です。"),
 ("jisseki-shiharai.html", "支払証憑", "振込が完了したことがわかる控えです。"),
 ("jisseki-kouza.html", "補助金の受取口座", "通帳またはネットバンキング画面の記録です。"),
 ("jisseki-hw-nouhin.html", "ハードウェアの納品書", "型番・数量がわかる納品書です。"),
 ("jisseki-hw-shashin.html", "ハードウェアの写真", "現物と設置状況がわかる写真です。"),
 ("jisseki-juugyouin.html", "従業員一覧", "小規模事業者として申請した場合に必要です。"),
])}

<h2>すべての書類に共通する条件</h2>
{ul([
 "文字がはっきり読めること。画面全体が入っており、途中で切れていないこと。",
 "日付の順番が「契約・発注 → 納品 → 請求 → 支払い」になっていること。",
 "会社名・屋号が、交付申請の内容と一致していること。",
 "金額が請求書とすべての書類で一致していること。",
])}

{warn("加工はしないでください", "<p>塗りつぶし・トリミング・文字の追記など、書類に手を加えたものは受理されません。原本をそのまま提出してください。</p>")}

<h2>ファイル形式とファイル名</h2>
{ul([
 "形式は PDF を推奨します（写真は JPEG でも構いません）。",
 "1つの項目に複数枚ある場合は、1つのPDFにまとめてください。",
 "ファイル名は、入力手順のページに書かれている名前に合わせてください。例：<b>1_請求明細書_事業者名</b>",
])}

<p><a class="btn" href="tejun.html">書類がそろったら入力手順へ</a></p>
""")

# ---------------------------------------------------------------- 書類ごとのページ
PAGES["jisseki-seikyusho.html"] = ("請求書（請求明細書）", "請求書（請求明細書）の確認ポイント。", f"""
<h1>請求書（請求明細書）</h1>
<p class="lead">導入したソフトウェア・ハードウェアの内訳と金額を示す書類です。弊社から発行しますので、届いた内容をご確認ください。</p>

<h2>確認していただく点</h2>
{table(["項目", "確認すること"], [
 ("宛名", "交付申請に使った事業者名と同じ表記になっているか"),
 ("発行日", "契約・発注の日以降になっているか"),
 ("品目", "交付決定を受けた製品・型番がもれなく記載されているか"),
 ("数量・単価", "実際に導入した数と一致しているか"),
 ("金額", "交付申請時の金額と一致しているか（税抜・税込の表記も確認）"),
])}

{warn("金額が変わった場合", "<p>交付決定額と請求額が異なる場合は、そのまま提出せず弊社担当までご連絡ください。手続きが必要になることがあります。</p>")}

<h2>提出するもの</h2>
{ul(["弊社が発行した請求書（請求明細書）の PDF を、そのまま添付してください。", "複数枚に分かれている場合は、1つの PDF にまとめてください。"])}
{filebox("1", "1_請求明細書_事業者名", "実績報告の1番目に添付します")}
""")

PAGES["jisseki-software.html"] = ("ソフトウェアの利用確認", "導入したソフトウェアが使える状態であることを示す資料。", f"""
<h1>ソフトウェアの利用確認</h1>
<p class="lead">補助対象のソフトウェアが実際に導入され、使える状態になっていることを示す資料です。ソフトの種類によって、示し方が変わります。</p>

<h2>用意するもの</h2>
{ul([
 "ログイン後の管理画面など、導入先の事業者名（またはアカウント名）が表示されている画面の記録",
 "契約内容がわかる画面（プラン名・契約期間・アカウント数など）",
 "パッケージソフトの場合は、ライセンス証書やライセンスキーが確認できる書類",
])}

<h2>画面を記録するときのポイント</h2>
{ol([
 "ブラウザやアプリの画面全体が入るように、画面ごと撮影（スクリーンショット）します。",
 "事業者名・アカウント名・日付が写るようにします。",
 "複数の画面が必要な場合は、順番どおりに1つの PDF にまとめます。",
])}

{note("うまく用意できないとき", "<p>画面の出し方がわからない場合は、無理に進めず弊社担当までご連絡ください。ソフトごとに適切な画面をご案内します。</p>")}
{filebox("4", "4_ソフトウェア証憑_事業者名", "ファイル名の番号は、導入内容によって変わることがあります")}
""")

PAGES["jisseki-shiharai.html"] = ("支払証憑", "振込が完了したことを示す控えの用意のしかた。", f"""
<h1>支払証憑</h1>
<p class="lead">請求金額の支払いが完了したことを示す資料です。支払いは<b>銀行振込</b>で行ってください。</p>

{warn("現金払い・手形は使えません", "<p>支払いの事実が確認できないため、現金や手形での支払いは対象外です。必ず事業用口座からの振込にしてください。</p>")}

<h2>資料に必要な情報</h2>
{ul([
 "振込日（請求書の発行日以降であること）",
 "振込金額（請求書の金額と一致していること）",
 "振込元の口座名義（申請した事業者のもの）",
 "振込先の口座名義（弊社）",
])}

<h2>用意のしかた</h2>
{table(["支払い方法", "提出するもの"], [
 ("窓口・ATM 振込", "振込明細票（利用控え）の原本をスキャンまたは撮影したもの"),
 ("ネットバンキング", "振込完了画面、または取引明細の画面をPDFで保存したもの"),
 ("通帳記帳", "表紙・見開き（口座番号のページ）と、該当の振込が記帳されたページ"),
])}

{note("金額が分かれるとき", "<p>複数回に分けて振り込んだ場合は、すべての控えを1つのPDFにまとめ、合計が請求金額と一致することがわかるようにしてください。</p>")}
{filebox("2", "2_支払証憑_事業者名", "実績報告の2番目に添付します")}
""")

PAGES["jisseki-kouza.html"] = ("補助金の受取口座", "補助金が振り込まれる口座の資料と、名義の確認方法。", f"""
<h1>補助金の受取口座</h1>
<p class="lead">補助金の振込先となる口座の情報です。名義が1文字でも違うと振込ができないため、事前の確認をお願いします。</p>

{warn("口座名義は必ず事前に確認を", "<p>金融機関に登録されている名義と<b>完全に一致</b>している必要があります。スペースの有無、濁点・半濁点、法人格の略称（カ、ユ、など）の表記に特にご注意ください。ご不明な場合は、口座のある金融機関へお問い合わせください。</p>")}

<h2>用意するもの</h2>
{table(["口座の種類", "提出するもの"], [
 ("通帳がある口座", "通帳の表紙と、見開き1ページ目（金融機関名・支店名・口座番号・名義が見えるページ）"),
 ("ネット銀行など通帳がない口座", "口座情報が表示された画面（金融機関名・支店名・口座番号・名義がわかるもの）"),
])}

<h2>確認していただく点</h2>
{ul([
 "申請した事業者の口座であること（代表者個人の口座は原則使えません）",
 "金融機関名・支店名・口座種別・口座番号・名義（カナ）がすべて読み取れること",
 "画面や通帳が途中で切れていないこと",
])}
{filebox("7", "7_口座情報_事業者名", "ファイル名の番号は、導入内容によって変わることがあります")}
""")

PAGES["jisseki-hw-nouhin.html"] = ("ハードウェアの納品書", "パソコン・POSレジ等を導入した場合の納品書。", f"""
<h1>ハードウェアの納品書</h1>
<p class="lead">パソコン・タブレット・POSレジなどを導入した場合に必要です。何を何台納品したかを示します。</p>

<h2>記載されている必要がある項目</h2>
{ul([
 "納品日（契約・発注の日以降であること）",
 "納品先の事業者名",
 "製品名・型番",
 "数量",
])}

{note("メーカーの出荷伝票しかない場合", "<p>型番と数量が確認できれば差し支えありません。判断に迷う場合は弊社担当へご連絡ください。</p>")}

<h2>提出のしかた</h2>
{ul([
 "パソコン等とPOSレジ等の両方を導入した場合も、納品書は1つのPDFにまとめて、それぞれの欄に同じファイルを添付します。",
 "枚数が多い場合も、順番を整えて1つのPDFにしてください。",
])}
{filebox("5", "5_ハードウェア導入情報（納品書）_事業者名", "納品書の欄に添付します")}
""")

PAGES["jisseki-hw-shashin.html"] = ("ハードウェアの写真", "導入した機器の現物写真の撮り方。", f"""
<h1>ハードウェアの写真</h1>
<p class="lead">導入した機器が実際に納品され、事業所で使われていることを示す写真です。</p>

<h2>撮影する写真</h2>
{table(["撮るもの", "ポイント"], [
 ("機器の全体", "機器の形がはっきりわかるように、正面から撮ります。"),
 ("型番・製造番号のラベル", "本体の裏面や側面にあるシールを、文字が読める距離で撮ります。"),
 ("設置状況", "事業所内に設置され、使える状態になっていることがわかるように撮ります。"),
])}

<h2>撮影のコツ</h2>
{ul([
 "明るい場所で、手ぶれとピンボケに注意して撮ります。",
 "複数台ある場合は、台数がわかるようにすべて撮影します。",
 "撮影した写真は、1つのPDFにまとめて添付します。",
])}

{warn("段ボールに入ったままの写真は使えません", "<p>開梱前の写真や、床に置いたままの写真では設置が確認できません。設置後の状態を撮影してください。</p>")}
{filebox("6", "6_ハードウェア導入情報（現物写真）_事業者名", "現物写真の欄に添付します")}
""")

PAGES["jisseki-juugyouin.html"] = ("従業員一覧", "小規模事業者として申請した場合に必要な従業員一覧。", f"""
<h1>従業員一覧</h1>
<p class="lead">小規模事業者として申請した場合に、従業員数の要件を満たしていることを示す資料です。</p>

<h2>記載する内容</h2>
{ul([
 "常時使用する従業員の氏名（または番号などの識別）",
 "雇用形態（正社員・パート・アルバイトなど）",
 "人数の合計",
])}

{note("常時使用する従業員の考え方", "<p>会社の代表者・役員、および日雇いや契約期間が限られた方などは、原則として人数に含めません。数え方に迷う場合は弊社担当へご相談ください。</p>")}

<h2>提出のしかた</h2>
{ul([
 "書式の指定は特にありません。Excel などで作成し、PDFにして添付してください。",
 "賃金台帳や労働者名簿の写しでも差し支えありません。",
 "従業員がいない場合は、その旨を記載した一覧（0名）を提出してください。",
])}
{filebox("3", "3_従業員一覧_事業者名", "小規模事業者として申請した場合のみ")}
""")

# ---------------------------------------------------------------- 手順トップ（チューザー）
PAGES["tejun.html"] = ("申請マイページの入力手順", "枠と導入内容にあわせた入力手順の選び方。", f"""
<h1>申請マイページの入力手順</h1>
<p class="lead">入力する画面は、申請した枠と導入した内容によって変わります。下の3つを選ぶと、あてはまる手順のページが開きます。</p>

{phase(1)}

<form class="chooser" id="chooser">
  <fieldset>
    <legend>申請した枠</legend>
    <div class="opts">
      <label><input type="radio" name="waku" value="inv" checked><span>インボイス枠</span></label>
      <label><input type="radio" name="waku" value="tsujo"><span>通常枠</span></label>
    </div>
  </fieldset>
  <fieldset data-inv>
    <legend>事業者の区分</legend>
    <div class="opts">
      <label><input type="radio" name="kubun" value="chusho"><span>中小企業</span></label>
      <label><input type="radio" name="kubun" value="shokibo"><span>小規模事業者</span></label>
    </div>
  </fieldset>
  <fieldset data-inv>
    <legend>パソコン・タブレット等の導入</legend>
    <div class="opts">
      <label><input type="radio" name="pc" value="1"><span>あり</span></label>
      <label><input type="radio" name="pc" value="0"><span>なし</span></label>
    </div>
  </fieldset>
  <fieldset data-inv>
    <legend>POSレジ等の導入</legend>
    <div class="opts">
      <label><input type="radio" name="pos" value="1"><span>あり</span></label>
      <label><input type="radio" name="pos" value="0"><span>なし</span></label>
    </div>
  </fieldset>
  <div class="chooser__out" id="chooser-result" hidden>
    <p>選んだ内容にあてはまる手順はこちらです。</p>
    <a class="btn" id="chooser-link" href="#">手順を開く</a>
  </div>
</form>

{note("区分がわからないとき", "<p>交付決定通知書に記載された枠と、申請時に選んだ事業者区分をご確認ください。判断がつかない場合は弊社担当までお問い合わせください。</p>")}

<h2>一覧から選ぶ</h2>
{cards([(h, t, "") for h, t in NAV[2][2]])}
""")

# ---------------------------------------------------------------- 事務局への提出
PAGES["tejun-teishutsu.html"] = ("事務局への提出", "弊社の確認後に行う、最後の提出操作。", f"""
<h1>事務局への提出</h1>
<p class="lead">弊社での確認が終わったあと、貴社の申請マイページから事務局へ提出します。ここまで行って実績報告が完了します。</p>

{phase(3)}

{warn("この操作を行わないと提出されません", "<p>①の送信だけでは、実績報告は事務局に届いていません。弊社からご案内が届いたら、必ずこの操作を行ってください。</p>")}

{steps([
 ("申請マイページにログインする", f'<p><a class="btn" href="{MYPAGE}" target="_blank" rel="noopener">申請マイページを開く</a></p>'
  + note("推奨環境", "<p>Windows の Microsoft Edge または Google Chrome の最新版でご利用ください。</p>")),
 ("実績報告の画面を開く", ol(["「申請者メニュー」をクリックする", "「実績報告情報詳細」をクリックする"])),
 ("内容を確認する", "<p>添付したファイルと入力内容が、画面に正しく反映されているかを上から順に確認します。</p>"
  + ul(["ファイルが開けるか（別のファイルを添付していないか）", "口座情報の入力に誤りがないか", "金額が請求書と一致しているか"])),
 ("事務局へ提出する", "<p>画面の一番下にあるボタンを押して提出します。</p>" + nextbtn("事務局に提出")
  + note("提出後について", "<p>提出後は内容を変更できません。事務局から差戻しの連絡があった場合は、その指示にしたがって修正し、あらためて提出してください。</p>")),
 ("完了", "<p>提出が完了すると、画面のステータスが提出済みに変わります。以降は事務局による確定検査を待ちます。</p>"),
])}
""")

# ---------------------------------------------------------------- 入力手順ページ（枠別）
def build_tejun(kubun, pc, pos):
    """kubun: 'chusho' | 'shokibo' | 'tsujo'"""
    tsujo = (kubun == "tsujo")
    shokibo = (kubun == "shokibo")
    hw = (pc or pos) and not tsujo

    # 添付ファイルの通し番号（納品書・現物写真はPC欄／POS欄で同じ番号を使います）
    n = 0
    def nxt():
        nonlocal n
        n += 1
        return str(n)
    no_seikyu = nxt()
    no_shiharai = nxt()
    no_juugyouin = nxt() if shokibo else None
    no_software = nxt()
    no_nouhin = nxt() if hw else None
    no_shashin = nxt() if hw else None
    no_kouza = nxt()

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

    st = []
    st.append(("申請マイページにログインする",
        f'<p><a class="btn" href="{MYPAGE}" target="_blank" rel="noopener">申請マイページを開く</a></p>'
        + note("推奨環境", "<p>Windows の Microsoft Edge または Google Chrome の最新版でご利用ください。</p>")
        + ol(["ログイン画面で、紫色の「GビズIDでログイン」を押す",
              "GビズIDのアカウントとパスワードを入力する",
              "画面の案内にしたがって二要素認証を行う",
              "ログイン後、「申請者メニュー」→「実績報告情報編集」へ進む"])))

    st.append(("説明画面を確認する",
        ol(["画面内の研修動画のリンクをクリックする",
            "動画を最後まで視聴したら、ブラウザの「戻る」で説明画面に戻る",
            "「動画を視聴して内容を理解しました」のチェックを入れる"]) + nextbtn()))

    st.append(("請求書を添付する",
        filebox(no_seikyu, f"{no_seikyu}_請求明細書_事業者名") + nextbtn()))

    st.append(("支払方法を選択する",
        '<ul class="choices"><li class="pick">銀行振込</li><li>クレジットカード払い</li></ul>' + nextbtn()))

    st.append(("支払証憑を添付する",
        filebox(no_shiharai, f"{no_shiharai}_支払証憑_事業者名") + nextbtn()))

    if shokibo:
        st.append(("その他資料を添付する",
            "<p>従業員一覧を添付します。</p>"
            + filebox(no_juugyouin, f"{no_juugyouin}_従業員一覧_事業者名") + nextbtn()))
    else:
        st.append(("その他資料を確認する",
            "<p>添付が必要な資料はありません。画面の内容を確認して、そのまま次へ進みます。</p>" + nextbtn()))

    st.append(("ソフトウェア証憑を添付する",
        filebox(no_software, f"{no_software}_ソフトウェア証憑_事業者名") + nextbtn()))

    if not tsujo:
        for label, flag in (("パソコン・タブレット等", pc), ("POSレジ等", pos)):
            if flag:
                body = (f"<p>{label}の導入ありを選び、次の2点を添付します。</p>"
                        + '<ul class="choices"><li class="pick">はい</li><li>いいえ</li></ul>'
                        + filebox(no_nouhin, f"{no_nouhin}_ハードウェア導入情報（納品書）_事業者名", "納品書の欄")
                        + filebox(no_shashin, f"{no_shashin}_ハードウェア導入情報（現物写真）_事業者名", "現物写真の欄")
                        + nextbtn())
            else:
                body = (f"<p>{label}の導入はないため、「いいえ」を選びます。添付は不要です。</p>"
                        + '<ul class="choices"><li>はい</li><li class="pick">いいえ</li></ul>'
                        + nextbtn())
            st.append((f"ハードウェア導入情報（{label}）", body))

    st.append(("口座情報を添付する",
        filebox(no_kouza, f"{no_kouza}_口座情報_事業者名") + nextbtn()))

    st.append(("口座情報を入力する",
        "<p>添付したPDFを開き、そこに書かれている内容を画面の項目へ入力します。</p>"
        + warn("口座名義は事前に確認を", "<p>金融機関に登録されている名義と<b>完全に一致</b>している必要があります。スペース・濁点・半濁点にご注意ください。</p>")
        + table(["項目", "入力のしかた"], [
            ("金融機関名", "画面を下にスクロールし、紫色の「検索」ボタンをクリック → 全角カタカナで入力 → 入力欄の外をクリック →「検索」→ 候補から選択<br><small>文字を入力している間は「検索」ボタンを押せません。</small>"),
            ("支店名", "金融機関名と同じ手順で検索して選択します。"),
            ("口座種別・口座番号", "通帳または口座情報の画面のとおりに入力します。"),
            ("口座名義（カナ）", "金融機関の登録どおりに入力します。"),
        ]) + nextbtn()))

    st.append(("実績報告の入力を完了する",
        "<p>入力確認画面で内容を確認し、画面の一番下のボタンを押します。</p>" + nextbtn("実績報告入力完了")
        + note("ここで①は完了です", "<p>入力内容が弊社に引き継がれます。弊社での確認が終わりましたら、③「<a href=\"tejun-teishutsu.html\">事務局への提出</a>」の操作をご案内します。</p>")))

    body = f"""
<h1>{e(title)}</h1>
<p class="lead">申請マイページでの操作手順です。画面の表示にあわせて、上から順に進めてください。</p>
<div class="tag-row">{"".join(tags)}</div>

{phase(1)}

{note("進める前に", '<p>添付するファイルは、先にすべて手元にそろえておくとスムーズです。<a href="jisseki.html">必要な書類はこちら</a>。</p>')}

{steps(st)}
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
