"""Draws the profile README art in the portfolio's style.

Every image comes in a dark and a light version (GitHub picks one with
prefers-color-scheme). Fonts are subset per image and embedded, so the
SVGs need nothing from the network.

    pip install fonttools brotli
    python art/build.py
"""
import base64, io, os
from html import escape
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets')
FONTS = {'serif': os.path.join(HERE, 'fonts', 'cinzel-latin.woff2'),
         'sans': os.path.join(HERE, 'fonts', 'nunito-sans-latin.woff2')}
FAMILY = {'serif': 'Cinzel', 'sans': 'Nunito Sans'}

THEMES = {
    'dark': dict(bg='#070b18', bg2='#0b1022', surface='#0e1426', line='rgba(216,182,110,.22)',
                 line2='rgba(216,182,110,.45)', text='#e7e3d7', muted='#aeb1c2', title='#f7f1e1',
                 gold='#d8b66e', gold_hi='#f0dfaf', gold_lo='#a07f3e', star='#f3ead2',
                 acc=dict(anemo='#7fd3c0', dendro='#add06a', electro='#bf9cf5', hydro='#6cc0f0',
                          cryo='#ade0ec', geo='#ebbd5c', pyro='#f29a72', gold='#d8b66e')),
    'light': dict(bg='#f6f0e3', bg2='#efe7d6', surface='#fffcf5', line='rgba(138,100,32,.22)',
                  line2='rgba(138,100,32,.45)', text='#1d2232', muted='#454d66', title='#141826',
                  gold='#8a6420', gold_hi='#6e4d12', gold_lo='#c09a4c', star='#c28f34',
                  acc=dict(anemo='#0e6a4e', dendro='#465f0e', electro='#6340b5', hydro='#145b8b',
                           cryo='#195f72', geo='#764f00', pyro='#963a17', gold='#8a6420')),
}

_metrics = {}


def width(text, kind, size, bold=False):
    """Rough advance width, used for layout (wrapping, pill sizes)."""
    if kind not in _metrics:
        f = TTFont(FONTS[kind])
        _metrics[kind] = (f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    cmap, hmtx, upm = _metrics[kind]
    w = sum(hmtx[cmap[ord(c)]][0] if ord(c) in cmap else upm * .55 for c in text)
    return w / upm * size * (1.06 if bold else 1)


def font_face(kind, chars):
    f = TTFont(FONTS[kind])
    opts = Options(); opts.flavor = 'woff2'; opts.layout_features = ['kern', 'liga', 'lnum']
    s = Subsetter(options=opts); s.populate(text=''.join(sorted(set(chars + ' '))))
    s.subset(f)
    buf = io.BytesIO(); f.flavor = 'woff2'; f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f"@font-face{{font-family:'{FAMILY[kind]}';src:url(data:font/woff2;base64,{b64}) format('woff2');"
            f"font-weight:200 1000}}")


class SVG:
    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.parts, self.css, self.chars = [], [], {'serif': '', 'sans': ''}

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, kind='sans', size=16, fill='#fff', weight=400, anchor='start', ls=0, extra=''):
        self.chars[kind] += s
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAMILY[kind]}" font-size="{size}" '
                 f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>'
                 f'{escape(s)}</text>')

    def save(self, name):
        faces = ''.join(font_face(k, c) for k, c in self.chars.items() if c)
        out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.label)}">'
               f'<title>{escape(self.label)}</title><style>{faces}{"".join(self.css)}'
               f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>'
               + ''.join(self.parts) + '</svg>')
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
            fh.write(out)


def stars(svg, t, n, seed, area, twinkle=True, r=(0.6, 1.6)):
    import random
    rnd = random.Random(seed)
    x0, y0, x1, y1 = area
    for i in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        rad = rnd.uniform(*r); op = rnd.uniform(.25, .9)
        cls = f' class="tw{i % 3}"' if twinkle else ''
        svg.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}" fill="{t["star"]}" opacity="{op:.2f}"{cls} '
                f'style="animation-delay:-{rnd.uniform(0, 6):.1f}s"/>')
    if twinkle:
        svg.css.append('.tw0{animation:tw 4s ease-in-out infinite}.tw1{animation:tw 6s ease-in-out infinite}'
                       '.tw2{animation:tw 9s ease-in-out infinite}@keyframes tw{50%{opacity:.08}}')


def rune(svg, t, cx, cy, s, spin=True):
    """The portfolio's hero rune, scaled to radius s*300."""
    k = s
    g1, g2 = t['gold'], t['acc']['anemo']
    svg.add(f'<defs><linearGradient id="rg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{g1}"/>'
            f'<stop offset="1" stop-color="{g2}"/></linearGradient><linearGradient id="rg2" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{g2}"/><stop offset="1" stop-color="{t["acc"]["electro"]}"/></linearGradient></defs>')
    svg.add(f'<g transform="translate({cx - 300 * k:.1f} {cy - 300 * k:.1f}) scale({k})" fill="none" opacity=".55">'
            f'<g class="spin"><circle cx="300" cy="300" r="280" stroke="url(#rg1)" stroke-dasharray="8 16"/>'
            f'<circle cx="300" cy="300" r="258" stroke="url(#rg1)" stroke-width=".5" opacity=".6"/>'
            f'<polygon points="300,30 332,268 570,300 332,332 300,570 268,332 30,300 268,268" stroke="url(#rg2)" stroke-width=".9"/></g>'
            f'<g class="spinr"><circle cx="300" cy="300" r="178" stroke="url(#rg2)" stroke-dasharray="4 20"/>'
            f'<circle cx="300" cy="300" r="158" stroke="url(#rg1)" stroke-width=".5" stroke-dasharray="2 10"/>'
            f'<polygon points="300,132 378,258 378,342 300,468 222,342 222,258" stroke="url(#rg1)" stroke-width=".9"/></g>'
            f'<g stroke="url(#rg1)" opacity=".7"><path d="M300 22v22M300 556v22M22 300h22M556 300h22M88 88l14 14M498 102l14-14M88 512l14-14M512 512l-14-14"/></g></g>')
    if spin:
        svg.css.append('.spin,.spinr{transform-origin:300px 300px;transform-box:view-box}'
                       '.spin{animation:spin 120s linear infinite}.spinr{animation:spin 80s linear infinite reverse}'
                       '@keyframes spin{to{transform:rotate(360deg)}}')


def panel(svg, t, x, y, w, h, accent=None, r=16):
    a = accent or t['gold']
    svg.add(f'<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="{r}" fill="{t["surface"]}" stroke="{t["line2"]}" stroke-width="1.5"/>')
    # gold diamond filigree, as on the site's panels
    for (dx, dy) in ((x + 28, y), (x + w - 28, y + h)):
        svg.add(f'<path d="M{dx} {dy - 4}l4 4-4 4-4-4z" fill="{a}"/>')


def wrap(text, kind, size, maxw, bold=False):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t_ = (cur + ' ' + w_).strip()
        if width(t_, kind, size, bold) > maxw and cur:
            lines.append(cur); cur = w_
        else:
            cur = t_
    return lines + [cur]


def constellation(svg, t, pts, cls, delay):
    """Stars joined by a line that draws itself, holds, then fades."""
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    svg.add(f'<path d="{d}" fill="none" stroke="{t["gold"]}" stroke-width="1" stroke-opacity=".55" pathLength="100" '
            f'class="draw" style="animation-delay:{delay}s"/>')
    for x, y in pts:
        svg.add(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{t["gold_hi"]}"/>')
    svg.css.append('.draw{stroke-dasharray:100;stroke-dashoffset:100;animation:draw 12s ease-in-out infinite}'
                   '@keyframes draw{0%{stroke-dashoffset:100;opacity:1}35%{stroke-dashoffset:0}80%{stroke-dashoffset:0;opacity:1}'
                   '100%{stroke-dashoffset:0;opacity:0}}')


# ───────────────────────── banner ─────────────────────────
def banner(t, mode):
    W, H = 880, 330
    s = SVG(W, H, 'Mukul Rayana. AI/ML Engineer: agentic AI, LLMOps, RAG and reinforcement learning for game AI.')
    s.add(f'<defs><radialGradient id="glow" cx="50%" cy="44%" r="60%"><stop offset="0" stop-color="{t["gold"]}" stop-opacity=".16"/>'
          f'<stop offset="1" stop-color="{t["gold"]}" stop-opacity="0"/></radialGradient>'
          f'<linearGradient id="bgg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["bg2"]}"/><stop offset="1" stop-color="{t["bg"]}"/></linearGradient>'
          f'<linearGradient id="goldtx" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["gold"]}"/>'
          f'<stop offset=".40" stop-color="{t["gold"]}"/><stop offset=".5" stop-color="{"#fff7dd" if mode == "dark" else "#e0b45a"}"/>'
          f'<stop offset=".60" stop-color="{t["gold"]}"/>'
          f'<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;1 0" keyTimes="0;.4;1" dur="7s" repeatCount="indefinite"/>'
          f'<stop offset="1" stop-color="{t["gold"]}"/></linearGradient></defs>')
    s.add(f'<rect width="{W}" height="{H}" rx="18" fill="url(#bgg)"/><rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/>')
    stars(s, t, 70, 7, (10, 10, W - 10, H - 10))
    rune(s, t, W / 2, 150, .44)
    constellation(s, t, [(40, 270), (85, 228), (140, 240), (172, 190), (228, 168), (205, 118)], 'c1', 0)
    constellation(s, t, [(840, 70), (792, 108), (740, 94), (702, 140), (660, 128), (682, 210)], 'c2', 6)
    s.add(f'<g transform="translate({W / 2} 150)"><g class="orbit"><circle cx="128" cy="0" r="3" fill="{t["gold_hi"]}"/>'
          f'<circle cx="128" cy="0" r="8" fill="{t["gold_hi"]}" opacity=".18"/></g></g>')
    s.css.append('.orbit{animation:spin 26s linear infinite}')
    s.add(f'<g class="shoot"><path d="M0 0h-90" stroke="{t["gold_hi"]}" stroke-width="1.5" stroke-linecap="round" opacity=".8"/></g>')
    s.css.append('.shoot{opacity:0;animation:shoot 11s ease-in 3s infinite}'
                 '@keyframes shoot{0%{opacity:0;transform:translate(760px,30px) rotate(160deg)}3%{opacity:1}'
                 '10%{opacity:0;transform:translate(590px,95px) rotate(160deg)}100%{opacity:0;transform:translate(590px,95px) rotate(160deg)}}')
    s.text(W / 2, 74, 'AI / ML ENGINEER', size=15, fill=t['gold'], weight=800, anchor='middle', ls=5)
    size = 66
    w1, w2, gap = width('MUKUL', 'serif', size, True), width('RAYANA', 'serif', size, True), 20
    x0 = W / 2 - (w1 + gap + w2) / 2
    s.text(x0, 168, 'MUKUL', 'serif', size, t['title'], 700, ls=1.5)
    s.text(x0 + w1 + gap, 168, 'RAYANA', 'serif', size, 'url(#goldtx)', 700, ls=1.5)
    s.add(f'<path d="M{W / 2 - 140} 196h124M{W / 2 + 16} 196h124" stroke="{t["gold"]}" stroke-opacity=".6"/>'
          f'<path d="M{W / 2} 191l5 5-5 5-5-5z" fill="{t["gold"]}"/>')
    for i, line in enumerate(['Agentic AI & multi-agent systems', 'LLMOps, RAG & fine-tuning in production',
                              'Reinforcement learning for game AI']):
        s.text(W / 2, 238, line, size=22, fill=t['text'], weight=700, anchor='middle',
               extra=f'class="cyc" style="animation-delay:{i * 4}s"')
    s.css.append('.cyc{opacity:0;transform-box:fill-box;transform-origin:center;animation:cyc 12s ease-in-out infinite}'
                 '@keyframes cyc{0%{opacity:0;transform:translateY(10px)}6%,29%{opacity:1;transform:none}'
                 '35%,100%{opacity:0;transform:translateY(-8px)}}'
                 '@media (prefers-reduced-motion:reduce){.cyc{opacity:0}.cyc:first-of-type{opacity:1}}')
    s.text(W / 2, 276, 'M.S. Applied Machine Learning, University of Maryland', size=16.5, fill=t['muted'], anchor='middle')
    s.save(f'banner-{mode}.svg')

# ───────────────────────── buttons ─────────────────────────
ICONS = {
    'globe': '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    'doc': '<path d="M6 2.5h8l4.5 4.5v14.5H6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M14 2.5V7h4.5M9 12h7M9 16h7" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    'linkedin': '<path fill="currentColor" d="M20.4 20.5h-3.6v-5.6c0-1.3 0-3-1.8-3-1.9 0-2.1 1.4-2.1 2.9v5.7H9.4V9h3.4v1.6c.5-.9 1.6-1.9 3.4-1.9 3.6 0 4.3 2.4 4.3 5.5v6.3zM5.3 7.4a2.1 2.1 0 1 1 0-4.1 2.1 2.1 0 0 1 0 4.1zm1.8 13.1H3.6V9h3.5v11.5zM22.2 0H1.8C.8 0 0 .8 0 1.7v20.6c0 .9.8 1.7 1.8 1.7h20.4c1 0 1.8-.8 1.8-1.7V1.7C24 .8 23.2 0 22.2 0z"/>',
    'hf': '<circle cx="12" cy="10.5" r="8.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="9" cy="9" r="1.25" fill="currentColor"/><circle cx="15" cy="9" r="1.25" fill="currentColor"/><path d="M8.4 12.6c.9 1.7 2.2 2.5 3.6 2.5s2.7-.8 3.6-2.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><ellipse cx="5.2" cy="19.2" rx="2.6" ry="1.9" fill="currentColor"/><ellipse cx="18.8" cy="19.2" rx="2.6" ry="1.9" fill="currentColor"/>',
    'mail': '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    'play': '<circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M10 8.3v7.4l6-3.7z" fill="currentColor"/>',
}


def button(t, mode, name, label, icon, primary=False):
    size = 17
    tw = width(label, 'sans', size, True)
    W, H = int(tw + 78), 50
    s = SVG(W, H, label)
    if primary:
        s.add(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{"#f0dfaf" if mode == "dark" else "#c79b48"}"/>'
              f'<stop offset="1" stop-color="{"#c99a4c" if mode == "dark" else "#8a6420"}"/></linearGradient></defs>')
        s.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="{H / 2 - .5}" fill="url(#bg)"/>')
        ink = '#1a1305' if mode == 'dark' else '#fffaf0'
    else:
        s.add(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="{H / 2 - .75}" fill="{t["surface"]}" stroke="{t["line2"]}" stroke-width="1.5"/>')
        ink = t['gold_hi']
    s.add(f'<g transform="translate(22 13)" color="{ink}" style="color:{ink}"><svg width="24" height="24" viewBox="0 0 24 24">{ICONS[icon]}</svg></g>')
    s.text(56, 31.5, label, size=size, fill=ink, weight=800)
    s.save(f'btn-{name}-{mode}.svg')


# ───────────────────────── section titles ─────────────────────────
def title(t, mode, name, label):
    W, H = 880, 56
    s = SVG(W, H, label)
    tw = width(label.upper(), 'serif', 25, True) + len(label) * 2
    s.add(f'<path d="M3 30l6-6 6 6-6 6z" fill="{t["gold"]}"/>')
    s.text(25, 39, label.upper(), 'serif', 25, t['title'], 700, ls=2)
    s.add(f'<path d="M{34 + tw} 30H{W - 3}" stroke="{t["gold"]}" stroke-opacity=".45"/>')
    s.add(f'<circle cx="{34 + tw}" cy="30" r="2.6" fill="{t["gold_hi"]}" class="run"/>')
    s.css.append(f'.run{{animation:run 9s ease-in-out infinite}}@keyframes run{{0%{{transform:translateX(0);opacity:0}}'
                 f'10%{{opacity:1}}60%{{transform:translateX({W - 40 - tw:.0f}px);opacity:0}}100%{{opacity:0}}}}')
    s.save(f'title-{name}-{mode}.svg')

# ───────────────────────── highlights ─────────────────────────
HIGHLIGHTS = [
    ('1st place', 'UMD Smith Agentic AI Challenge 2026', 'PharmaChain, an 8-agent LangGraph system for pharma cold-chain risk', '$4K prize · Team Synapse'),
    ('3× faster', 'Production QA inference at BeeBox Studios', 'P95 latency 185 → 62 ms after ONNX export and INT8 quantization', 'AI Research Intern'),
    ('IEEE', 'Published at IDCIoT 2024', 'Voice-driven panoramic VR generation: speech to 360° scenes', 'Peer-reviewed paper'),
    ('3 live demos', 'Agents and RAG you can try right now', 'Hosted on Vercel and Hugging Face Spaces', 'PharmaChain · RECON · Irminsul'),
]


def highlights(t, mode):
    W, gap, ch = 880, 16, 172
    cw = (W - gap) / 2
    H = ch * 2 + gap + 4
    s = SVG(W, H, 'Highlights: 1st place at the UMD Smith Agentic AI Challenge 2026; 3x faster production QA inference at BeeBox Studios; IEEE IDCIoT 2024 publication; 3 live demos.')
    s.add(f'<defs><linearGradient id="foil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["gold_lo"]}"/>'
          f'<stop offset=".5" stop-color="{t["gold_hi"]}"/><stop offset="1" stop-color="{t["gold"]}"/></linearGradient></defs>')
    for i, (v, l, sub, x_) in enumerate(HIGHLIGHTS):
        x, y = (i % 2) * (cw + gap), 2 + (i // 2) * (ch + gap)
        panel(s, t, x, y, cw, ch)
        s.add(f'<rect x="{x + .75}" y="{y + .75}" width="{cw - 1.5}" height="{ch - 1.5}" rx="16" fill="none" stroke="{t["gold_hi"]}" '
              f'stroke-width="2" pathLength="1000" class="trail" style="animation-delay:-{i * 2.5}s"/>')
        s.text(x + 26, y + 50, v, 'serif', 32, 'url(#foil)' if i == 0 else t['gold_hi'], 700)
        s.text(x + 26, y + 82, l, size=17.5, fill=t['title'], weight=800)
        for j, ln in enumerate(wrap(sub, 'sans', 15, cw - 52)[:2]):
            s.text(x + 26, y + 108 + j * 20, ln, size=15, fill=t['muted'])
        s.text(x + 26, y + ch - 20, x_, size=14, fill=t['gold'], weight=800)
    s.css.append('.trail{stroke-dasharray:90 910;animation:trail 10s linear infinite;opacity:.85}'
                 '@keyframes trail{to{stroke-dashoffset:-1000}}')
    s.save(f'highlights-{mode}.svg')

# ───────────────────────── project cards ─────────────────────────
PROJECTS = [
    dict(slug='pharmachain', acc='anemo', kicker='MULTI-AGENT · 1ST PLACE, $4K', name='PharmaChain',
         sub='AI cargo monitor for pharma cold-chain risk', metric='12–15 s', mlabel='from alert to an approved plan, vs the usual 6–8 hours',
         minis=[], tags=['LangGraph', 'FastAPI', 'LLM failover', 'Team of 5']),
    dict(slug='nemesis', acc='pyro', kicker='REINFORCEMENT LEARNING', name='Nemesis',
         sub='Distributed RL boss AI with real-time LLM narration', metric='+85%', mlabel='longer survival than a scripted FSM boss',
         minis=[('2.6×', 'Ray RLlib, 1 → 8 workers'), ('<2 ms', 'per frame in Unity Sentis')], tags=['PPO', 'Ray RLlib', 'ONNX', 'Unity Sentis']),
    dict(slug='empathrag', acc='hydro', kicker='AI SAFETY · RESEARCH PROTOTYPE', name='EmpathRAG',
         sub='Safety guardrail for an emotion-aware RAG assistant', metric='0.9629', mlabel='crisis recall on held-out test data (research prototype)',
         minis=[('1.67M', 'vector FAISS index'), ('0.88', 'emotion alignment (BM25: 0.30)')], tags=['DeBERTa', 'FAISS', 'Captum', 'Mistral 7B']),
    dict(slug='recon', acc='electro', kicker='AGENTIC RESEARCH', name='RECON',
         sub='Multi-agent ML research navigator', metric='44% vs 0%', mlabel='of stale claims caught, vs a single-pass RAG baseline',
         minis=[], tags=['LangGraph', 'Critic agent', 'Groq', 'Gradio']),
    dict(slug='irminsul', acc='dendro', kicker='CITED RAG · LLMOPS · LIVE BETA', name='Irminsul',
         sub='Leak-free Genshin assistant that cites every answer', metric='95.8%', mlabel='of the live test set scored, all 19 leak and safety probes handled',
         minis=[('0.946', 'right source in top 8'), ('$0', 'running cost')], tags=['Hybrid search', 'FastAPI', 'ONNX', 'GitHub Actions']),
    dict(slug='docpilot', acc='cryo', kicker='SECURE DOCUMENT AI', name='DocPilot',
         sub='Secure document Q&A service', metric='4× smaller', mlabel='model with ONNX INT8, 2–3× faster per inference on CPU',
         minis=[], tags=['FastAPI', 'Hybrid search', 'RBAC', 'PII redaction']),
    dict(slug='vrgen', acc='gold', kicker='GENERATIVE AI · IEEE IDCIOT 2024', name='Panoramic VR Generation',
         sub='Peer-reviewed speech → 360° scene pipeline', metric='2.3×', mlabel='throughput from attention slicing + xFormers',
         minis=[('10 GB', 'VRAM budget'), ('IEEE', 'peer-reviewed')], tags=['Whisper', 'GPT-Neo', 'Stable Diffusion']),
]


def illo(svg, t, slug, a, cx, cy):
    """A small looping illustration per project, drawn around (cx, cy)."""
    g = lambda body: svg.add(f'<g transform="translate({cx} {cy})" fill="none" stroke="{a}" stroke-width="2" '
                             f'stroke-linecap="round" stroke-linejoin="round">{body}</g>')
    css = svg.css.append
    css('.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 3s ease-in-out infinite}'
        '@keyframes pulse{50%{transform:scale(1.18);opacity:.55}}'
        '.ripple{transform-box:fill-box;transform-origin:center;animation:ripple 3.6s ease-out infinite}'
        '@keyframes ripple{0%{transform:scale(.6);opacity:.9}100%{transform:scale(1.6);opacity:0}}'
        '.rot{animation:spin 14s linear infinite}.rotf{animation:spin 4s linear infinite}'
        '.blink{animation:blink 2.4s ease-in-out infinite}@keyframes blink{50%{opacity:.15}}')
    if slug == 'pharmachain':   # live telemetry trace with a heartbeat spike
        d = 'M-62 0H-30L-22 -14L-12 22L-2 -34L8 16L14 0H62'
        g(f'<rect x="-70" y="-44" width="140" height="88" rx="12" stroke-opacity=".35"/>'
          f'<path d="{d}" stroke-opacity=".25"/><path d="{d}" pathLength="100" class="ecg"/>'
          f'<circle cx="52" cy="-30" r="4" fill="{a}" class="blink"/>')
        css('.ecg{stroke-dasharray:28 72;animation:ecg 2.6s linear infinite}@keyframes ecg{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}')
    elif slug == 'nemesis':     # the boss's eye, watching
        g(f'<circle r="44" stroke-dasharray="6 9" stroke-opacity=".6" class="rot"/>'
          f'<path d="M-40 0Q0 -34 40 0Q0 34 -40 0Z"/><circle r="11" fill="{a}" class="pulse"/>'
          f'<path d="M-52 -40l10 10M52 -40l-10 10M-52 40l10-10M52 40l-10-10" stroke-opacity=".7"/>')
    elif slug == 'empathrag':   # a guardrail shield with care rippling out
        g(f'<circle r="30" class="ripple"/><circle r="30" class="ripple" style="animation-delay:1.8s"/>'
          f'<path d="M0 -36L28 -24V2C28 20 14 32 0 38C-14 32 -28 20 -28 2V-24Z" fill="{t["surface"]}"/>'
          f'<path d="M0 16C-10 8 -15 2 -15 -5A7 7 0 0 1 0 -9A7 7 0 0 1 15 -5C15 2 10 8 0 16Z" fill="{a}" stroke="none"/>')
    elif slug == 'recon':       # radar sweep that finds a stale claim
        svg.add(f'<defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}" stop-opacity="0"/>'
                f'<stop offset="1" stop-color="{a}" stop-opacity=".55"/></linearGradient></defs>')
        g(f'<circle r="44" stroke-opacity=".5"/><circle r="28" stroke-opacity=".35"/><circle r="12" stroke-opacity=".3"/>'
          f'<g class="rotf"><path d="M0 0L44 0A44 44 0 0 0 31 -31Z" fill="url(#sw)" stroke="none"/></g>'
          f'<circle cx="20" cy="-18" r="3.5" fill="{a}" stroke="none" class="blink"/>'
          f'<circle cx="-24" cy="14" r="3.5" fill="{a}" stroke="none" class="blink" style="animation-delay:1.2s"/>')
        css('.rotf{animation-duration:3.2s}')
    elif slug == 'irminsul':    # the world tree, leaves glowing in turn
        leaves = [(-30, -26), (-12, -40), (10, -42), (30, -28), (-36, -6), (36, -8), (0, -24)]
        lv = ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="{a}" stroke="none" class="blink" style="animation-delay:{i * .35:.2f}s"/>'
                     for i, (x, y) in enumerate(leaves))
        g(f'<path d="M0 44V-6M0 16L-22 -2M0 6L22 -10M0 -6L-14 -26M0 -6L14 -30M-22 -2L-34 -8M22 -10L34 -10"/>'
          f'<path d="M-40 44Q-20 36 0 44Q20 36 40 44" stroke-opacity=".6"/>{lv}')
    elif slug == 'docpilot':    # a document scanned under a lock
        g(f'<path d="M-30 -42H14L32 -24V42H-30Z" fill="{t["surface"]}"/><path d="M14 -42V-24H32" />'
          f'<path d="M-18 -16H20M-18 -4H20M-18 8H20M-18 20H8" stroke-opacity=".5"/>'
          f'<path d="M-36 -20H38" stroke-width="3" class="scan"/>'
          f'<rect x="22" y="22" width="22" height="18" rx="4" fill="{a}" stroke="none"/><path d="M27 22V16A6 6 0 0 1 39 16V22"/>')
        css('.scan{animation:scan 2.8s ease-in-out infinite alternate}@keyframes scan{from{transform:translateY(-14px)}to{transform:translateY(46px)}}')
    elif slug == 'eldervale':   # one hums, one weaves: a note flows between two heroes
        g(f'<circle cx="-46" cy="10" r="10" fill="{a}" stroke="none"/><circle cx="46" cy="10" r="10" fill="{t["acc"]["anemo"]}" stroke="none"/>'
          f'<path d="M-34 10C-18 -20 18 40 34 10" stroke-opacity=".3"/><path d="M-34 10C-18 -20 18 40 34 10" pathLength="100" class="flow"/>'
          f'<path d="M-6 -28V-44L6 -47V-31" stroke-width="2.2" class="pulse"/><circle cx="-9" cy="-28" r="4" fill="{a}" stroke="none" class="pulse"/>')
        css('.flow{stroke-dasharray:22 78;animation:ecg 2.4s linear infinite}@keyframes ecg{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}')
    elif slug == 'vrgen':       # a 360° sphere turning
        g(f'<circle r="42"/><ellipse rx="42" ry="14" stroke-opacity=".5"/><ellipse rx="42" ry="30" stroke-opacity=".3"/>'
          f'<ellipse rx="16" ry="42" class="turn"/><ellipse rx="34" ry="42" stroke-opacity=".35" class="turn" style="animation-delay:-2s"/>')
        css('.turn{animation:turn 4s ease-in-out infinite}@keyframes turn{50%{transform:scaleX(-1)}}')


def card(t, mode, p):
    W, H = 430, 286
    a = t['acc'][p['acc']]
    s = SVG(W, H, f"{p['name']}: {p['sub']}. {p['metric']} {p['mlabel']}.")
    panel(s, t, 0, 0, W, H, accent=a)
    s.add(f'<rect x="1.5" y="1.5" width="4.5" height="{H - 3}" rx="2.2" fill="{a}"/>')
    s.add(f'<g transform="translate({W - 72} 72) scale(.74)">'); illo(s, t, p['slug'], a, 0, 0); s.add('</g>')
    s.text(26, 38, p['kicker'], size=12, fill=a, weight=800, ls=1.6)
    nm = 24 if width(p['name'], 'serif', 24, True) < 262 else 19
    s.text(26, 74, p['name'], 'serif', nm, t['title'], 700, ls=.4)
    for j, ln in enumerate(wrap(p['sub'], 'sans', 14.5, 262)[:2]):
        s.text(26, 98 + j * 19, ln, size=14.5, fill=t['muted'])
    s.text(26, 166, p['metric'], 'serif', 34, t['gold_hi'], 700)
    for j, ln in enumerate(wrap(p['mlabel'], 'sans', 14.5, W - 52)[:2]):
        s.text(26, 192 + j * 19, ln, size=14.5, fill=t['text'])
    x = 26
    for tag in p['tags']:
        tw = width(tag, 'sans', 12.5, True) + 22
        if x + tw > W - 20: break
        s.add(f'<rect x="{x}" y="{H - 50}" width="{tw:.1f}" height="28" rx="14" fill="none" stroke="{t["line2"]}"/>')
        s.text(x + tw / 2, H - 31, tag, size=12.5, fill=t['text'], weight=700, anchor='middle')
        x += tw + 7
    s.save(f'card-{p["slug"]}-{mode}.svg')

def now_strip(t, mode):
    W, H = 880, 96
    s = SVG(W, H, 'Now: open to AI/ML Engineer roles. Latest build: Irminsul v1, cited answers. Latest research: human vs AI playtesters.')
    panel(s, t, 0, 0, W, H)
    ok = t['acc']['anemo']
    s.add(f'<circle cx="34" cy="48" r="7" fill="{ok}"/><circle cx="34" cy="48" r="7" fill="none" stroke="{ok}" stroke-width="2" class="ping"/>')
    s.css.append('.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}'
                 '@keyframes ping{from{transform:scale(1);opacity:.9}to{transform:scale(2.8);opacity:0}}')
    items = [('NOW', 'Open to AI/ML roles'), ('LATEST BUILD', 'Irminsul v1, cited answers'), ('LATEST RESEARCH', 'Human vs AI playtesters')]
    colw = (W - 60) / 3
    for i, (k, v) in enumerate(items):
        x = 58 + i * colw
        s.text(x, 40, k, size=12.5, fill=t['gold'], weight=800, ls=2.2)
        s.text(x, 66, v, size=17.5, fill=t['title'], weight=800)
        if i: s.add(f'<path d="M{x - 18} 24V72" stroke="{t["line2"]}"/>')
    s.save(f'now-{mode}.svg')

def _lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def toolkit(t, mode):
    import json
    icons = json.load(open(os.path.join(HERE, 'icons.json')))
    W, cols, tile, gapy = 880, 8, 64, 108
    rows = (len(icons) + cols - 1) // cols
    H = rows * gapy + 8
    s = SVG(W, H, 'Toolkit: ' + ', '.join(i['label'] for i in icons))
    surf = _lum(t['surface'].lstrip('#'))
    cw = W / cols
    for n, ic in enumerate(icons):
        cx, y = cw * (n % cols) + cw / 2, 4 + (n // cols) * gapy
        L = _lum(ic['hex'])
        ratio = (max(L, surf) + .05) / (min(L, surf) + .05)
        col = '#' + ic['hex'] if ratio >= 2.4 else t['title']
        s.add(f'<rect x="{cx - tile / 2}" y="{y}" width="{tile}" height="{tile}" rx="16" fill="{t["surface"]}" '
              f'stroke="{t["line2"]}" stroke-width="1.5"/>')
        s.add(f'<svg x="{cx - 17}" y="{y + 15}" width="34" height="34" viewBox="0 0 24 24"><path fill="{col}" d="{ic["path"]}"/></svg>')
        s.text(cx, y + tile + 24, ic['label'], size=14, fill=t['text'], weight=700, anchor='middle')
    s.save(f'toolkit-{mode}.svg')


# ───────────────────────── footer ─────────────────────────
def footer(t, mode):
    W, H = 880, 110
    s = SVG(W, H, 'Thanks for stopping by.')
    stars(s, t, 26, 3, (0, 10, W, H - 10))
    s.add(f'<path d="M{W / 2 - 200} 46h184M{W / 2 + 16} 46h184" stroke="{t["gold"]}" stroke-opacity=".5"/>'
          f'<path d="M{W / 2} 39l7 7-7 7-7-7z" fill="{t["gold"]}"/>')
    s.text(W / 2, 88, 'Thanks for stopping by  ·  mukulray1603.github.io', size=16, fill=t['muted'], anchor='middle')
    s.save(f'footer-{mode}.svg')

BUTTONS = [('portfolio', 'Portfolio', 'globe', True), ('resume', 'Resumé', 'doc', False),
           ('linkedin', 'LinkedIn', 'linkedin', False), ('hf', 'Hugging Face', 'hf', False),
           ('email', 'Email', 'mail', False),
           ('demo-pharmachain', 'PharmaChain', 'play', False), ('demo-recon', 'RECON', 'play', False),
           ('demo-irminsul', 'Irminsul', 'play', False), ('demo-eldervale', 'Play Eldervale', 'play', False)]
TITLES = [('highlights', 'Highlights'), ('work', 'Featured Work'), ('live', 'Try It Live'),
          ('toolkit', 'Toolkit'), ('journal', 'From the Journal')]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for mode, t in THEMES.items():
        banner(t, mode); highlights(t, mode); footer(t, mode); now_strip(t, mode); toolkit(t, mode)
        for b in BUTTONS: button(t, mode, *b)
        for n, l in TITLES: title(t, mode, n, l)
        for p in PROJECTS: card(t, mode, p)
    print('built', len(os.listdir(OUT)), 'files in', os.path.abspath(OUT))
