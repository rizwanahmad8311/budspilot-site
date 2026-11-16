#!/usr/bin/env python3
"""Builds the BudsPilot site (static HTML in the repo root, served by GitHub Pages).

    python3 build.py

Edit the content below, run this, commit the generated .html files.
privacy.html: copy brand/privacy-policy.html from the app repo over privacy.html, then run this;
the policy sections and date are kept and wrapped in the site's header and footer.
To move the site to another address (for example budspilot.com) change SITE and rebuild.
"""
import html, json, pathlib, re, datetime

SITE = 'https://rizwanahmad8311.github.io/budspilot-site/'
EMAIL = 'budspilot@gmail.com'
EARLY = ('mailto:' + EMAIL + '?subject=BudsPilot%20early%20access'
         '&body=Please%20let%20me%20know%20when%20BudsPilot%20is%20on%20Google%20Play.%20My%20earbuds%3A%20')
ROOT = pathlib.Path(__file__).resolve().parent
TODAY = datetime.date.today().isoformat()

ICONS = {
    'battery': '<rect x="2" y="7" width="16" height="10" rx="2.5"/><path d="M22 11v2M6 11v2M10 11v2"/>',
    'eq': '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
    'tap': '<path d="M9 11V6a2 2 0 1 1 4 0v5"/><path d="M13 11V9a2 2 0 1 1 4 0v3a2 2 0 1 1 4 0v3a7 7 0 0 1-7 7h-1a7 7 0 0 1-6-3.5L4.5 15a2 2 0 0 1 3.4-2L9 14.5"/>',
    'ear': '<path d="M6 8.5a6.5 6.5 0 1 1 13 0c0 6-6 6-6 10a3.5 3.5 0 1 1-7 0"/><path d="M15 8.5a2.5 2.5 0 0 0-5 0v1a2 2 0 1 1 0 4"/>',
    'find': '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    'tool': '<path d="M14.7 6.3a4 4 0 0 0 5 5l-9.4 9.4a2.1 2.1 0 0 1-3-3z"/><path d="M14.7 6.3 18 3"/>',
    'play': '<path d="M5 3.5v17a1 1 0 0 0 1.5.9l14-8.5a1 1 0 0 0 0-1.8l-14-8.5A1 1 0 0 0 5 3.5z" fill="currentColor" stroke="none"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3 7 9 6 9-6"/>',
}

def icon(name, size=24):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

NAV = [('index.html#features', 'Features'), ('supported-earbuds.html', 'Supported earbuds'),
       ('index.html#faq', 'FAQ'), ('privacy.html', 'Privacy')]

FEATURES = [  # slug, short name, one-line, icon, tint
    ('earbuds-battery-level.html', 'Earbuds battery level', 'Left, right and case battery, widget, alerts and time left.', 'battery', ''),
    ('earbuds-equalizer.html', 'Equalizer & bass booster', '10-band EQ, presets, bass boost and left / right volume.', 'eq', 'p'),
    ('earbuds-tap-controls.html', 'Tap controls & noise cancelling', 'Remap taps, switch ANC and gaming mode on supported buds.', 'tap', 'b'),
    ('live-listen.html', 'Live Listen', 'Hear the room through your earbuds with a volume boost.', 'ear', 'y'),
    ('find-my-earbuds.html', 'Find my earbuds', 'Play a loud sound on the left, right or both buds.', 'find', 'g'),
    ('earbuds-test-and-tools.html', 'Left / right test & tools', 'Left right check, water eject, speaker cleaner, codec.', 'tool', 'b'),
]

def cta_buttons(second=('index.html#features', 'See all features')):
    return (f'<div class="cta"><a class="btn" href="{EARLY}">{icon("play", 18)} Coming soon to Google Play</a>'
            f'<a class="btn ghost" href="{second[0]}">{second[1]}</a></div>')

def band(title='Give your earbuds the app they never had'):
    return f'''<section id="get"><div class="wrap"><div class="band rv">
<img src="icon.png" width="84" height="84" alt="BudsPilot app icon" loading="lazy">
<h2>{title}</h2>
<p>BudsPilot is coming soon to Google Play for Android 9 and newer. Free, no account, no ads. Send us an email and we will tell you the day it is live.</p>
<div class="cta"><a class="btn" href="{EARLY}">{icon("mail", 18)} Get early access</a><a class="btn ghost" href="supported-earbuds.html">Check your earbuds</a></div>
</div></div></section>'''

def faq_html(items):
    return '<div class="faq">' + ''.join(
        f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'

def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))

def faq_ld(items):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': strip_tags(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}}
        for q, a in items]}

APP_LD = {
    '@type': 'MobileApplication', '@id': SITE + '#app', 'name': 'BudsPilot',
    'alternateName': 'BudsPilot: Earbud Battery & EQ',
    'description': 'Android app for Bluetooth earbuds without a companion app: battery level for each earbud and the case, '
                   '10-band equalizer, bass booster, tap controls, noise cancelling, find my earbuds and Live Listen.',
    'operatingSystem': 'Android 9.0 and up', 'applicationCategory': 'MusicApplication',
    'applicationSubCategory': 'Earbuds controller', 'softwareVersion': '1.2.0',
    'url': SITE, 'image': SITE + 'icon.png', 'screenshot': SITE + 'assets/img/01-battery.webp',
    'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
    'featureList': ['Earbuds battery level for left, right and case', 'Battery widget and low battery alerts',
                    '10-band equalizer and bass booster', 'Left and right volume balance', 'Customizable tap controls',
                    'Noise cancelling and transparency mode', 'Gaming mode', 'Find my earbuds', 'Live Listen sound amplifier',
                    'Left / right earbud test', 'Water eject and speaker cleaner'],
    'author': {'@id': SITE + '#org'},
}
ORG_LD = {'@type': 'Organization', '@id': SITE + '#org', 'name': 'BudsPilot', 'url': SITE,
          'logo': SITE + 'icon.png', 'email': EMAIL}

def page(path, title, desc, body, ld=None, crumbs=None, og_type='website'):
    url = SITE + ('' if path == 'index.html' else path)
    graph = [ORG_LD] + (ld or [])
    if crumbs:
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + ('' if p == 'index.html' else p)}
            for i, (p, n) in enumerate([('index.html', 'BudsPilot')] + crumbs)]})
    ld_json = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    cur = ' aria-current="page"'
    nav = ''.join(f'<a href="{h}"{cur if h == path else ""}>{t}</a>' for h, t in NAV)
    feats = ''.join(f'<li><a href="{f[0]}">{f[1]}</a></li>' for f in FEATURES)
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#101113">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="BudsPilot">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/PlusJakartaSans-ExtraBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/Inter-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<noscript><style>.rv{{opacity:1;transform:none}}</style></noscript>
<script type="application/ld+json">{ld_json}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="index.html"><img src="icon.png" width="34" height="34" alt="">BudsPilot</a>
<button class="menu" aria-label="Menu" aria-expanded="false" aria-controls="nav"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn sm" href="index.html#get">Get the app</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
<div class="fgrid">
<div><a class="brand" href="index.html"><img src="icon.png" width="34" height="34" alt="">BudsPilot</a>
<p class="about">The earbuds app for Android that works with the Bluetooth earbuds you already own, including budget TWS buds that never came with an app.</p></div>
<div><h4>Features</h4><ul>{feats}</ul></div>
<div><h4>BudsPilot</h4><ul><li><a href="supported-earbuds.html">Supported earbuds</a></li><li><a href="index.html#faq">FAQ</a></li><li><a href="privacy.html">Privacy policy</a></li></ul></div>
<div><h4>Contact</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{EARLY}">Get early access</a></li></ul></div>
</div>
<div class="legal"><span>© {datetime.date.today().year} BudsPilot. Android is a trademark of Google LLC. AirPods and Beats are trademarks of Apple Inc. Other brand names belong to their owners; BudsPilot is not affiliated with any earbud maker.</span></div>
</div></footer>
<script src="assets/app.js" defer></script>
</body>
</html>
'''
    (ROOT / path).write_text(out)
    return path

def shot(name, alt, tone, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="assets/img/{name}.webp" width="640" height="1101" alt="{alt}" {load}>'

# ---------------------------------------------------------------- home
HOME_FAQ = [
    ('What is BudsPilot?',
     'BudsPilot is an Android app for Bluetooth earbuds that came without a companion app. It shows the battery level of each earbud and the charging case, adds a 10-band equalizer and bass booster, lets you change tap controls on supported buds, and helps you find lost earbuds.'),
    ('Does BudsPilot work with my earbuds?',
     'The equalizer, bass booster, left and right volume, find my earbuds, left / right test and cleaning tools work with any Bluetooth earbuds, earphones or headphones on Android 9 and newer. Per-bud battery, tap controls, noise cancelling and gaming mode depend on the chip inside your buds. See <a href="supported-earbuds.html">supported earbuds</a>.'),
    ('How do I check my earbuds battery level on Android?',
     'Connect your earbuds, open BudsPilot and the Buds tab shows the left earbud, right earbud and case battery on buds that report them. You can also add the battery widget to your home screen and turn on low battery alerts at 20% and 10%.'),
    ('Can I change the tap controls on earbuds that have no app?',
     'Yes, on buds with a supported chip. BudsPilot can remap single tap, double tap, triple tap and long press on each side to actions such as play / pause, next track, volume up or the voice assistant. The settings are saved inside the buds, so they also work on your laptop and other phones.'),
    ('Is there an equalizer for Bluetooth earbuds on Android?',
     'BudsPilot includes a 10-band equalizer with Bass, Vocal, Treble, Rock, Pop, Classical and Jazz presets, plus a bass booster. It applies to everything you play on those earbuds, and each pair keeps its own sound settings.'),
    ('Can BudsPilot show AirPods battery on Android?',
     'Yes. BudsPilot shows left, right and case battery for AirPods and Beats on an Android phone.'),
    ('Is BudsPilot free? Does it have ads?',
     'BudsPilot is free, has no ads and needs no account. Your settings stay on your phone. The app sends anonymous usage statistics and crash reports to help us improve it, and you can turn that off in Settings. Details are in the <a href="privacy.html">privacy policy</a>.'),
    ('Is there an iPhone version?',
     'No. BudsPilot is Android only, because iOS does not allow apps to apply system-wide sound effects or to talk to earbuds in the way BudsPilot needs.'),
]

def build_home():
    cards = ''.join(
        f'<a class="card rv" href="{s}"><div class="ico {t}">{icon(i, 26)}</div><h3>{n}</h3><p>{d}</p><span class="more">Learn more →</span></a>'
        for s, n, d, i, t in FEATURES)
    strip_items = ['Bluetooth earbuds', 'TWS earphones', 'Wireless headphones', 'Budget buds with no app',
                   'AirPods and Beats battery', 'Android 9 and newer', 'No account', 'No ads']
    strip = ''.join(f'<li>{s}</li>' for s in strip_items * 2)
    body = f'''<section class="hero"><div class="wrap">
<div>
<span class="pill"><i></i>For Android · works with the buds you already own</span>
<h1>The earbuds app your <span class="accent">Bluetooth earbuds</span> never came with</h1>
<p class="lede">See the battery level of each earbud and the case, tune the sound with a 10-band equalizer, change tap controls and find lost earbuds. One app for wireless earbuds that shipped without one.</p>
{cta_buttons()}
<ul class="ticks"><li>Free</li><li>No account</li><li>No ads</li><li>Android 9+</li></ul>
</div>
<div class="phone">{shot('01-battery', 'BudsPilot showing left, right and case earbuds battery level on Android', 'dark', True)}</div>
</div></section>

<div class="strip" aria-hidden="true"><ul>{strip}</ul></div>

<section id="features"><div class="wrap">
<div class="head rv"><span class="eyebrow">Features</span><h2>Everything a good earbuds app should do</h2>
<p>Most budget TWS earbuds ship with no app at all. BudsPilot adds the controls you get with expensive buds: battery, equalizer, touch controls and more.</p></div>
<div class="bento">{cards}</div>
</div></section>

<section style="padding-top:0"><div class="wrap">
<div class="show dark rv"><div class="copy"><span class="eyebrow">Earbuds battery</span><h2>Know the battery of every bud</h2>
<p>Stop guessing which earbud is about to die. BudsPilot shows the left earbud, right earbud and charging case on one screen.</p>
<ul class="list"><li>Battery widget for your home screen</li><li>Popup when you open the case or your buds connect</li><li>Low battery alerts at 20% and 10% for each side</li><li>Battery time left, learned from how your buds drain</li></ul>
<a class="link" href="earbuds-battery-level.html">More about earbuds battery level →</a></div>
<div class="mock" role="img" aria-label="Illustration: earbuds battery widget with left 90%, right 85% and case 70%, a low battery alert and a time left estimate">
<div class="w"><b>AirBuds Pro</b>
<div class="row"><span>Left</span><div class="bar"><i style="width:90%"></i></div><span>90%</span></div>
<div class="row"><span>Right</span><div class="bar"><i style="width:85%"></i></div><span>85%</span></div>
<div class="row"><span>Case</span><div class="bar"><i style="width:70%"></i></div><span>70%</span></div></div>
<div class="toast"><img src="icon.png" width="36" height="36" alt="" loading="lazy"><div>Right earbud at 20%<small>Low battery alert</small></div></div>
<div class="toast"><img src="icon.png" width="36" height="36" alt="" loading="lazy"><div>About 4 h 10 min left<small>Battery time left</small></div></div>
</div></div>

<div class="show light flip rv"><div class="copy"><span class="eyebrow">Equalizer</span><h2>Tune your sound, not just the volume</h2>
<p>A real 10-band equalizer for Bluetooth earbuds, with a bass booster and separate left and right volume up to 150%.</p>
<ul class="list"><li>Presets: Bass, Vocal, Treble, Rock, Pop, Classical, Jazz</li><li>Hearing test that tunes the EQ to each ear</li><li>Saved per pair and applied when they connect</li></ul>
<a class="link" href="earbuds-equalizer.html">More about the earbuds equalizer →</a></div>
<div class="shot">{shot('04-sound', '10-band equalizer for earbuds with presets and bass boost', 'light')}</div></div>

<div class="show dark rv"><div class="copy"><span class="eyebrow">Tap controls</span><h2>Remap every tap</h2>
<p>On buds with a supported chip, choose what single tap, double tap, triple tap and long press do on each side.</p>
<ul class="list"><li>Play / pause, next and previous track, volume up and down</li><li>Noise cancelling (ANC) and transparency mode</li><li>Gaming mode for low latency audio</li><li>Saved inside the buds, so it works on every device</li></ul>
<a class="link" href="earbuds-tap-controls.html">More about earbuds tap controls →</a></div>
<div class="shot">{shot('03-taps', 'Customize earbuds touch controls: single, double, triple tap and long press', 'dark')}</div></div>

<div class="show light flip rv"><div class="copy"><span class="eyebrow">Find my earbuds</span><h2>Lost a bud? Make it chirp</h2>
<p>Play a loud sound on the left bud, the right bud or both to find earbuds hiding in the sofa, a bag or a jacket pocket.</p>
<ul class="list"><li>Pick the side you lost</li><li>Your media volume is restored afterwards</li><li>Works with any connected Bluetooth earbuds</li></ul>
<a class="link" href="find-my-earbuds.html">More about find my earbuds →</a></div>
<div class="shot">{shot('06-find', 'Find my earbuds screen playing a loud sound on left, right or both', 'light')}</div></div>
</div></section>

<section style="padding-top:28px"><div class="wrap">
<div class="head rv"><span class="eyebrow">Two modes</span><h2>Useful with every pair. Powerful with supported buds.</h2>
<p>BudsPilot checks your earbuds when they connect and turns on everything they can do.</p></div>
<div class="modes">
<div class="mode rv"><span class="tag">Basic · any Bluetooth earbuds</span><h3>Works with every pair</h3>
<ul class="list"><li>10-band equalizer, bass booster, left / right volume</li><li>Hearing test and personal sound</li><li>Find my earbuds sound</li><li>Left / right test, water eject, speaker cleaner</li><li>Live Listen, connection history, listening time</li></ul></div>
<div class="mode hot rv"><span class="tag">Advanced · supported chips</span><h3>Unlocks the buds themselves</h3>
<ul class="list"><li>Battery for each earbud and the case</li><li>Tap control remapping on each side</li><li>Noise cancelling and transparency mode</li><li>Gaming mode and the buds' built-in EQ</li><li>Rename your buds, see the firmware version</li></ul></div>
</div>
<p class="muted rv" style="text-align:center;margin-top:28px">Not sure which mode you will get? <a href="supported-earbuds.html">See supported earbuds</a>.</p>
</div></section>

<section><div class="wrap">
<div class="head rv"><span class="eyebrow">How it works</span><h2>Set up in under a minute</h2></div>
<div class="steps">
<div class="step rv"><h3>Pair your earbuds</h3><p>Connect your buds in Android's Bluetooth settings as usual. There is nothing new to pair.</p></div>
<div class="step rv"><h3>Open BudsPilot</h3><p>The app detects the connected earbuds and shows what they support. No account, no sign-up.</p></div>
<div class="step rv"><h3>Take control</h3><p>Check the battery, shape the sound, set your taps. Your settings come back every time the buds connect.</p></div>
</div></div></section>

<section style="padding-top:0"><div class="wrap">
<div class="head rv"><span class="eyebrow">More inside</span><h2>Small tools that fix real problems</h2></div>
<ul class="chips rv"><li>Live Listen sound amplifier</li><li>Speak through your buds</li><li>Left / right earbud test</li><li>Fix swapped left and right</li><li>Water eject</li><li>Speaker cleaner tone</li><li>Bluetooth codec info</li><li>Connection history</li><li>Daily listening time</li><li>AirPods battery on Android</li><li>Light and dark mode</li><li>Three styles: Clean, Studio, Pulse</li></ul>
</div></section>

<section id="faq" style="padding-top:28px"><div class="wrap">
<div class="head rv"><span class="eyebrow">FAQ</span><h2>Questions about BudsPilot</h2></div>
{faq_html(HOME_FAQ)}
</div></section>
{band()}'''
    web = {'@type': 'WebSite', '@id': SITE + '#site', 'url': SITE, 'name': 'BudsPilot', 'publisher': {'@id': SITE + '#org'}}
    return page('index.html', 'BudsPilot: Earbuds App for Battery, EQ &amp; Tap Controls',
                'BudsPilot is the Android app for Bluetooth earbuds that came without one: battery level for each bud, '
                '10-band equalizer, tap controls and find my earbuds.',
                body, [web, APP_LD, faq_ld(HOME_FAQ)])

# ---------------------------------------------------------------- feature pages
def article(path, title, desc, crumb, eyebrow, h1, lede, img, img_alt, prose, faq):
    related = ''.join(f'<a href="{s}">{n}<span>{d}</span></a>' for s, n, d, _, _ in FEATURES if s != path)
    media = f'<div class="phone">{shot(img, img_alt, "", True)}</div>' if img else ''
    grid = 'grid' if img else ''
    body = f'''<div class="phead"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">BudsPilot</a> › {crumb}</nav>
<div class="{grid}" style="padding:36px 0 {'0' if img else '20px'}">
<div style="max-width:680px;padding-bottom:40px"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lede">{lede}</p>{cta_buttons(('supported-earbuds.html', 'Check your earbuds'))}</div>
{media}
</div></div></div>
<section style="padding-top:36px"><div class="wrap"><div class="prose">
{prose}
<h2>Questions</h2>
</div>
{faq_html(faq)}
<div class="prose"><h2>More from BudsPilot</h2></div>
<div class="related" style="max-width:980px;margin:20px auto 0">{related}</div>
</div></section>
{band()}'''
    return page(path, title, desc, body, [faq_ld(faq), {'@type': 'WebPage', 'url': SITE + path, 'name': strip_tags(title),
                'description': desc, 'about': {'@id': SITE + '#app'}}], [(path, crumb)])

def build_articles():
    out = []
    out.append(article(
        'earbuds-battery-level.html', 'Earbuds Battery Level on Android: Left, Right &amp; Case | BudsPilot',
        'Check the battery level of each Bluetooth earbud and the charging case on Android. Home screen widget, low battery alerts and time left with BudsPilot.',
        'Earbuds battery level', 'Earbuds battery',
        'See the <span class="accent">battery level</span> of each earbud and the case',
        'Android often shows one battery number for your earbuds, or none. BudsPilot shows the left earbud, the right earbud and the charging case separately, on buds that report them.',
        '01-battery', 'Left, right and case earbuds battery level in the BudsPilot Android app',
        '''<h2>How to check earbuds battery on Android</h2>
<ol><li>Connect your earbuds to your phone over Bluetooth.</li><li>Open BudsPilot. The <strong>Buds</strong> tab lists your connected pair.</li><li>Read the left, right and case percentages. A lightning mark shows what is charging.</li></ol>
<h2>What you get</h2>
<ul><li><strong>Left, right and case battery</strong> at a glance, on buds that report each level.</li>
<li><strong>Earbuds battery widget</strong> for your home screen, so you do not have to open the app.</li>
<li><strong>Battery popup</strong> when you open the case or when your buds connect.</li>
<li><strong>Low battery alerts</strong> at 20% and 10% for each side, before one earbud cuts out mid-call.</li>
<li><strong>Battery time left</strong>: an estimate that BudsPilot learns from how fast your own earbuds drain.</li>
<li><strong>Listening time</strong>: how long you use your earbuds each day.</li></ul>
<h2>AirPods and Beats battery on Android</h2>
<p>Using AirPods or Beats with an Android phone? BudsPilot shows their left, right and case battery too, so you get the same view you would have on an iPhone.</p>
<div class="note">Per-bud battery depends on what your earbuds broadcast. Some budget buds report only a single level or none at all. The equalizer, volume controls and tools still work on every pair.</div>''',
        [('Why does Android show only one battery percentage for my earbuds?', 'Android reads a single battery value from most Bluetooth earbuds. Many buds also broadcast separate levels for the left bud, right bud and case, which BudsPilot reads on supported buds and shows side by side.'),
         ('Is there a battery widget for Bluetooth earbuds?', 'Yes. BudsPilot includes an earbuds battery widget for the Android home screen.'),
         ('Can I get a warning before my earbuds die?', 'Yes. Turn on low battery alerts and BudsPilot notifies you at 20% and 10% for each side.'),
         ('How accurate is battery time left?', 'It is an estimate. BudsPilot learns how fast your earbuds drain while you use them, so it gets better after a few listening sessions.')]))

    out.append(article(
        'earbuds-equalizer.html', 'Equalizer for Bluetooth Earbuds on Android: 10-Band EQ | BudsPilot',
        'A 10-band equalizer and bass booster for Bluetooth earbuds on Android, with presets, left / right volume balance and a hearing test. Saved per pair.',
        'Equalizer & bass booster', 'Earbuds equalizer',
        'A 10-band <span class="accent">equalizer</span> for your Bluetooth earbuds',
        'Budget earbuds often sound thin, boomy or harsh, and have no app to fix it. BudsPilot adds an equalizer, a bass booster and left / right volume to any pair.',
        '', '',
        '''<h2>Shape the sound of any earbuds</h2>
<ul><li><strong>10-band equalizer</strong> from 31 Hz to 16 kHz for precise control over bass, mids and treble.</li>
<li><strong>EQ presets</strong>: Flat, Bass, Vocal, Treble, Rock, Pop, Classical and Jazz.</li>
<li><strong>Bass booster</strong> for deeper low end on small drivers.</li>
<li><strong>Left and right volume</strong>, separately, up to 150%. A volume booster and balance control in one, useful if one ear hears less or one bud plays quieter.</li>
<li><strong>Applies to everything you play</strong> on those earbuds: music, video and games.</li>
<li><strong>Saved per pair</strong>: each set of earbuds keeps its own sound and gets it back automatically on connect.</li></ul>
<h2>Hearing test and personal sound</h2>
<p>A short tone test for each ear lets BudsPilot tune the equalizer to how you hear, so quiet frequencies are lifted for you and not for everyone.</p>
<div class="note">The hearing test is a sound personalisation feature. It is not a medical or diagnostic test.</div>
<h2>How to set the equalizer</h2>
<ol><li>Connect your earbuds and open the <strong>Sound</strong> tab.</li><li>Switch sound on, then pick a preset or drag the ten bands.</li><li>Adjust bass boost and left / right volume to taste. Your settings are saved for that pair.</li></ol>
<h2>The buds' built-in EQ</h2>
<p>On buds with a supported chip, BudsPilot can also change the equalizer stored inside the earbuds themselves, so the sound follows them to your laptop or another phone. See <a href="earbuds-tap-controls.html">advanced controls</a>.</p>''',
        [('Does the equalizer work with any Bluetooth earbuds?', 'Yes. The 10-band equalizer, bass booster and left / right volume work with any Bluetooth earbuds, earphones or headphones on Android 9 and newer.'),
         ('Does the EQ work with Spotify, YouTube and other apps?', 'The equalizer is applied to what you play on those earbuds, whichever app the sound comes from.'),
         ('Can I make one earbud louder than the other?', 'Yes. Left and right volume are separate and go up to 150%, so you can balance a quiet bud or compensate for an ear that hears less.'),
         ('Will my settings be lost when I switch earbuds?', 'No. BudsPilot saves a sound profile for each pair and applies it when that pair connects.')]))

    out.append(article(
        'earbuds-tap-controls.html', 'Change Earbuds Tap Controls, ANC &amp; Gaming Mode | BudsPilot',
        'Customize touch controls on earbuds without an app: remap single, double and triple tap and long press, switch noise cancelling and gaming mode.',
        'Tap controls & noise cancelling', 'Advanced controls',
        'Change the <span class="accent">tap controls</span> on earbuds that have no app',
        'Double tap skips a track when you wanted volume? On buds with a supported chip, BudsPilot lets you decide what every tap does, and switch noise cancelling and gaming mode.',
        '03-taps', 'Earbuds tap controls screen: remap single tap, double tap, triple tap and long press',
        '''<h2>Customize earbuds touch controls</h2>
<p>Many popular budget earbuds are built on the same Bluetooth chip family. When BudsPilot recognises it, the <strong>Advanced controls</strong> screen appears and you can remap each gesture on each side:</p>
<ul><li><strong>Gestures</strong>: single tap, double tap, triple tap and long press, for the left and the right bud.</li>
<li><strong>Actions</strong>: play / pause, next track, previous track, volume up, volume down, answer call, hang up, call back, voice assistant, switch noise control, switch gaming mode, or nothing.</li></ul>
<p>The new layout is saved inside the earbuds, so it keeps working on your laptop, tablet and other phones without the app.</p>
<h2>Noise cancelling and transparency mode</h2>
<p>If your buds have active noise cancelling, switch between <strong>Off</strong>, <strong>ANC</strong> and <strong>Transparency</strong> from the app. It only appears on buds that have noise cancelling microphones.</p>
<h2>Gaming mode</h2>
<p>Gaming mode lowers the sound delay for games and videos. It may use a little more battery.</p>
<h2>Rename your buds and more</h2>
<ul><li>Give your earbuds a new Bluetooth name.</li><li>Change the buds' built-in EQ preset.</li><li>Check the firmware version.</li></ul>
<h2>Start Live Listen with a tap</h2>
<p>You can also set a tap on your earbuds to start <a href="live-listen.html">Live Listen</a> or a recording, even with the phone screen off. Other taps keep controlling your music.</p>
<div class="note">Tap remapping, noise control and gaming mode need buds with a supported chip. If yours are not supported yet, every other BudsPilot feature still works. <a href="supported-earbuds.html">Check supported earbuds</a>.</div>''',
        [('Can I change touch controls on earbuds without an app?', 'On earbuds with a supported chip, yes. BudsPilot remaps single tap, double tap, triple tap and long press on each bud.'),
         ('Can I add volume control to my earbuds taps?', 'Yes, on supported buds. Assign volume up and volume down to any gesture, for example triple tap on the right and left bud.'),
         ('Do the new tap controls work on other devices?', 'Yes. The settings are stored inside the earbuds, so they work with a laptop, tablet or another phone.'),
         ('How do I know if my earbuds are supported?', 'Connect them and open BudsPilot. If the buds show an Advanced badge, tap controls and the other advanced settings are available.')]))

    out.append(article(
        'find-my-earbuds.html', 'Find My Earbuds on Android: Play a Sound on Lost Buds | BudsPilot',
        'Lost an earbud nearby? BudsPilot plays a loud sound on the left, right or both Bluetooth earbuds so you can find them. Works with any connected pair.',
        'Find my earbuds', 'Find my earbuds',
        '<span class="accent">Find lost earbuds</span> by making them chirp',
        'One bud slipped between the cushions again. If it is still connected to your phone, BudsPilot can play a loud chirp on it until you track it down.',
        '', '',
        '''<h2>How to find a lost earbud</h2>
<ol><li>Open BudsPilot and tap <strong>Find my buds</strong>.</li><li>Choose <strong>Left</strong>, <strong>Right</strong> or <strong>Both</strong>.</li><li>Tap play and follow the sound.</li></ol>
<div class="note">The chirp plays at full volume. Take the buds out of your ears first. Your media volume is restored when it stops.</div>
<h2>Good to know</h2>
<ul><li><strong>Works with any Bluetooth earbuds</strong> that are connected to your phone.</li>
<li><strong>The bud must be in range and switched on.</strong> Earbuds have no GPS, so a bud that is out of Bluetooth range, out of battery or shut inside its case cannot play a sound.</li>
<li><strong>Connection history</strong> shows when your buds last connected and disconnected, which helps you work out when you last had them.</li></ul>''',
        [('Can I find an earbud that is in its case?', 'Usually not. Most earbuds switch off and disconnect when the case is closed, so they cannot play a sound.'),
         ('Can I find earbuds that are far away or offline?', 'No. BudsPilot plays a sound over Bluetooth, so the earbud has to be switched on and within range of your phone. The connection history shows when they were last connected.'),
         ('Does find my earbuds work with any brand?', 'Yes. It works with any Bluetooth earbuds that are currently connected to your Android phone.')]))

    out.append(article(
        'live-listen.html', 'Live Listen for Android: Sound Amplifier for Earbuds | BudsPilot',
        'Live Listen on Android: hear the room through your own earbuds using your phone microphone, with volume boost and noise reduction. Part of BudsPilot.',
        'Live Listen', 'Live Listen',
        '<span class="accent">Live Listen</span> for Android: hear the room through your earbuds',
        'Put your phone near the TV, the speaker at a lecture or the person across the table, and hear it more clearly in your own earbuds.',
        '', '',
        '''<h2>A sound amplifier for your own ears</h2>
<p>Live Listen plays your phone's microphone on your earbuds or headphones in real time.</p>
<ul><li><strong>Volume boost</strong> to bring quiet voices and sounds up.</li>
<li><strong>Noise reduction</strong>, optional, to cut steady background noise.</li>
<li><strong>Speak</strong>: the other way round. Talk through your earbuds' microphone and your voice plays on the phone's speaker, with noise reduction and automatic anti-whistle.</li>
<li><strong>Tap to start</strong>: set a tap on your earbuds to start Live Listen or a recording, even with the screen off.</li>
<li><strong>Record</strong> only when you tap Record. Recordings stay on your phone; you can play, share or delete them.</li></ul>
<h2>How to use Live Listen</h2>
<ol><li>Connect your earbuds and open <strong>Live Listen</strong> in BudsPilot.</li><li>Tap <strong>Start</strong> and allow the microphone.</li><li>Place the phone near the sound you want to hear and set the boost.</li></ol>
<h2>Clear about the microphone</h2>
<p>Live Listen starts only when you tap Start, or a bud tap that you chose. Android's microphone indicator shows the whole time it is on. Nothing the microphone hears is uploaded.</p>
<div class="note">Live Listen is a convenience feature for hearing your surroundings through your own earbuds. It is not a hearing aid or a medical device.</div>''',
        [('Does Android have Live Listen like the iPhone?', 'BudsPilot adds a Live Listen feature to Android: your phone microphone is played on your earbuds or headphones with an optional volume boost and noise reduction.'),
         ('Does Live Listen work with any earbuds?', 'Yes. It works with any Bluetooth earbuds or headphones connected to your Android phone.'),
         ('Is the sound recorded?', 'Only if you tap Record, or a bud tap you set to Record. Recordings are kept in the app on your phone and are never uploaded.'),
         ('Is there a delay?', 'Bluetooth audio always adds a small delay. It is short enough for listening to speech, a TV or a lecture.')]))

    out.append(article(
        'earbuds-test-and-tools.html', 'Left Right Earbud Test, Water Eject &amp; Speaker Cleaner | BudsPilot',
        'Test left and right earbuds, fix swapped sides, eject water and clean muffled earbud speakers with sound. Free tools in the BudsPilot Android app.',
        'Left / right test & tools', 'Test & tools',
        '<span class="accent">Left / right earbud test</span>, water eject and speaker cleaner',
        'Is one earbud quieter? Are left and right swapped? Did your buds get wet? BudsPilot has a quick test and a set of cleaning tones for exactly that.',
        '05-check', 'Left right earbud test in the BudsPilot app',
        '''<h2>Left / right earbud test</h2>
<p>Two quick tests, about a minute in total. First you say which side each tone plays on, then whether you hear five tones in each ear.</p>
<ul><li>Checks that <strong>each ear plays on the correct side</strong>.</li><li>Checks that <strong>both buds sound the same</strong>.</li><li><strong>Fixes buds that swap left and right</strong>: if the test finds the sides reversed, BudsPilot can swap them back for that pair.</li></ul>
<h2>Water eject for earbuds</h2>
<p>Caught in the rain or dropped a bud in the sink? Water eject plays a low pulsing tone for 30 seconds that vibrates water out of the speaker grille.</p>
<ol><li>Take the buds out of your ears.</li><li>Hold them with the speaker mesh facing down.</li><li>Tap <strong>Start</strong>. Your volume is restored afterwards.</li></ol>
<h2>Speaker cleaner for dust</h2>
<p>A dust cleaning tone helps loosen fine dust from a muffled earbud speaker. For wax or packed dirt you will still need a soft dry brush.</p>
<h2>Bluetooth codec and connection history</h2>
<ul><li><strong>Codec</strong>: see which Bluetooth codec your earbuds are using.</li><li><strong>Connection history</strong>: when your buds connected and disconnected, useful for spotting drop-outs.</li></ul>
<div class="note">Sound can only move water and loose dust. It cannot repair earbuds that are damaged by liquid.</div>''',
        [('How do I test if my left and right earbuds are working?', 'Open Left / right check in BudsPilot. It plays tones on each side and asks what you hear, which takes about a minute.'),
         ('My earbuds have left and right swapped. Can I fix it?', 'Yes. If the left / right test finds that the sides are reversed, BudsPilot can swap the channels for that pair.'),
         ('How do I get water out of my earbuds?', 'Take the buds out of your ears, hold them with the mesh facing down and run Eject water in BudsPilot. A low pulsing tone pushes water out of the speaker.'),
         ('One earbud is quieter than the other. What can I do?', 'Run the dust cleaning tone and clean the mesh, then use the separate left and right volume in the Sound tab to balance them.')]))
    return out

def build_supported():
    faq = [('Do Audionic earbuds have an app?', 'Many Audionic earbuds ship without a companion app. BudsPilot works with them: every pair gets the equalizer, volume controls and tools, and pairs with a supported chip also get per-bud battery and tap controls.'),
           ('Do Ronin earbuds work with BudsPilot?', 'Yes. Ronin earbuds, like any Bluetooth earbuds, get the equalizer, bass booster, left / right volume, find my earbuds and tools. Advanced controls depend on the chip inside the model you have.'),
           ('How do I know which features my earbuds get?', 'Connect them and open BudsPilot. Buds with an Advanced badge have per-bud battery, tap controls and the other advanced settings. All other buds run in Basic mode.'),
           ('My earbuds are not supported. Can you add them?', f'Write to <a href="mailto:{EMAIL}">{EMAIL}</a> with the brand and model and we will look at adding support.')]
    body = f'''<div class="phead"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">BudsPilot</a> › Supported earbuds</nav>
<div style="padding:36px 0 20px;max-width:760px"><span class="eyebrow">Compatibility</span>
<h1>Earbuds that work with <span class="accent">BudsPilot</span></h1>
<p class="lede">Short answer: any Bluetooth earbuds, earphones or headphones that connect to an Android 9+ phone. How much BudsPilot can do depends on the chip inside them.</p>
{cta_buttons(('index.html#features', 'See all features'))}</div></div></div>
<section style="padding-top:36px"><div class="wrap">
<div class="modes">
<div class="mode rv"><span class="tag">Basic · any Bluetooth earbuds</span><h3>Every pair gets</h3>
<ul class="list"><li><a href="earbuds-equalizer.html">10-band equalizer</a> and bass booster</li><li>Left and right volume up to 150%</li><li>Hearing test and personal sound</li><li><a href="find-my-earbuds.html">Find my earbuds</a> sound</li><li><a href="earbuds-test-and-tools.html">Left / right test</a>, water eject, speaker cleaner</li><li><a href="live-listen.html">Live Listen</a></li><li>Codec, connection history and listening time</li></ul></div>
<div class="mode hot rv"><span class="tag">Advanced · supported chips</span><h3>Supported buds also get</h3>
<ul class="list"><li><a href="earbuds-battery-level.html">Battery for each earbud and the case</a></li><li><a href="earbuds-tap-controls.html">Tap control remapping</a></li><li>Noise cancelling and transparency mode, on buds that have them</li><li>Gaming mode</li><li>The buds' built-in EQ</li><li>Rename and firmware version</li></ul></div>
</div>
<div class="prose">
<h2>Budget TWS earbuds without an app</h2>
<p>BudsPilot was built for earbuds that ship with no companion app, such as many models from <strong>Audionic</strong>, <strong>Ronin</strong> and other budget TWS brands. A large share of these buds use the same Bluetooth chip family, and on those BudsPilot unlocks the advanced controls.</p>
<p>Two models of the same brand can use different chips, so one may get Advanced mode and another Basic. The app tells you as soon as your buds connect.</p>
<h2>AirPods and Beats on Android</h2>
<p>BudsPilot shows left, right and case battery for <strong>AirPods</strong> and <strong>Beats</strong> on an Android phone, together with the equalizer and tools that work with every pair.</p>
<h2>Bluetooth headphones and earphones</h2>
<p>Over-ear headphones, neckbands and single earphones work in Basic mode: equalizer, bass booster, volume balance, Live Listen and the tools.</p>
<h2>What you need</h2>
<ul><li>An Android phone or tablet with <strong>Android 9 or newer</strong>.</li><li>Earbuds that are already paired in Android's Bluetooth settings.</li></ul>
<div class="note">BudsPilot is an independent app. It is not made by or affiliated with any earbud brand named on this page.</div>
<h2>Questions</h2>
</div>
{faq_html(faq)}
</div></section>
{band('Try BudsPilot with your earbuds')}'''
    return page('supported-earbuds.html', 'Supported Earbuds: Audionic, Ronin, AirPods &amp; More | BudsPilot',
                'Which earbuds work with BudsPilot? Any Bluetooth earbuds on Android get the equalizer and tools; supported chips add per-bud battery and tap controls.',
                body, [faq_ld(faq)], [('supported-earbuds.html', 'Supported earbuds')])

def build_privacy():
    src = (ROOT / 'privacy.html').read_text()
    updated = re.search(r'Last updated ([^·<]+?)\s*·', src).group(1)
    sections = re.findall(r'<section><h2>.*?</h2><p>.*?</p></section>', src, re.S)
    assert sections, 'no policy sections found in privacy.html'
    body = f'''<div class="phead"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">BudsPilot</a> › Privacy policy</nav>
<div style="padding:36px 0 8px;max-width:760px"><h1>BudsPilot privacy policy</h1>
<p class="meta lede">Last updated {updated} · Contact: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div></div>
<div class="wrap"><div class="prose policy">
''' + '\n'.join('  ' + s for s in sections) + '\n</div></div>'
    return page('privacy.html', 'Privacy Policy | BudsPilot',
                'Privacy policy for BudsPilot, the Android app for earbuds without a companion app.',
                body, None, [('privacy.html', 'Privacy policy')])

def build_404():
    body = f'''<section style="text-align:center;padding:120px 0"><div class="wrap"><span class="eyebrow">404</span>
<h1>This page wandered off, like a lost earbud</h1><p class="lede" style="margin:22px auto 30px">The page you are looking for is not here.</p>
<div class="cta" style="justify-content:center"><a class="btn" href="{SITE}">Back to BudsPilot</a></div></div></section>'''
    p = page('404.html', 'Page not found | BudsPilot', 'Page not found.', body)
    f = ROOT / p
    # 404 can be served from any depth: absolute asset and link URLs, and keep it out of the index
    s = f.read_text().replace('content="index, follow, max-image-preview:large"', 'content="noindex"')
    s = re.sub(r'(href|src)="(?!https?:|mailto:|#)([^"]+)"', lambda m: f'{m.group(1)}="{SITE}{m.group(2)}"', s)
    f.write_text(s)

pages = [build_home()] + build_articles() + [build_supported(), build_privacy()]
build_404()

(ROOT / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{SITE}{"" if p == "index.html" else p}</loc><lastmod>{TODAY}</lastmod>'
            f'<priority>{"1.0" if p == "index.html" else "0.3" if p == "privacy.html" else "0.8"}</priority></url>\n' for p in pages) +
    '</urlset>\n')
(ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
(ROOT / 'site.webmanifest').write_text(json.dumps({
    'name': 'BudsPilot', 'short_name': 'BudsPilot', 'start_url': './', 'display': 'browser',
    'background_color': '#101113', 'theme_color': '#101113',
    'icons': [{'src': 'icon.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=2) + '\n')
print('built', len(pages) + 1, 'pages')
