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


# ───────────────────────── banner ─────────────────────────
def banner(t, mode):
    W, H = 1280, 400
    s = SVG(W, H, 'Mukul Rayana. AI/ML Engineer: agentic AI, LLMOps, and reinforcement learning for game AI.')
    s.add(f'<defs><radialGradient id="glow" cx="50%" cy="46%" r="60%"><stop offset="0" stop-color="{t["gold"]}" stop-opacity=".16"/>'
          f'<stop offset="1" stop-color="{t["gold"]}" stop-opacity="0"/></radialGradient>'
          f'<linearGradient id="bgg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["bg2"]}"/><stop offset="1" stop-color="{t["bg"]}"/></linearGradient>'
          f'<linearGradient id="goldtx" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["gold_lo"]}"/>'
          f'<stop offset=".45" stop-color="{t["gold_hi"]}"/><stop offset=".55" stop-color="{"#fff7dd" if mode == "dark" else "#d2a24a"}"/>'
          f'<stop offset="1" stop-color="{t["gold"]}"/></linearGradient></defs>')
    s.add(f'<rect width="{W}" height="{H}" rx="22" fill="url(#bgg)"/><rect width="{W}" height="{H}" rx="22" fill="url(#glow)"/>')
    stars(s, t, 90, 7, (12, 12, W - 12, H - 12))
    rune(s, t, W / 2, 180, .52)
    # shooting star
    s.add(f'<g class="shoot"><path d="M0 0h-120" stroke="{t["gold_hi"]}" stroke-width="1.6" stroke-linecap="round" opacity=".8"/></g>')
    s.css.append('.shoot{transform:translate(1050px,40px) rotate(160deg);opacity:0;animation:shoot 11s ease-in 3s infinite}'
                 '@keyframes shoot{0%{opacity:0;transform:translate(1050px,40px) rotate(160deg)}3%{opacity:1}'
                 '10%{opacity:0;transform:translate(820px,125px) rotate(160deg)}100%{opacity:0;transform:translate(820px,125px) rotate(160deg)}}')
    s.text(W / 2, 92, 'AI / ML ENGINEER', size=17, fill=t['gold'], weight=800, anchor='middle', ls=6)
    # name: MUKUL in title ink, RAYANA in gold
    size = 84
    w1, w2, gap = width('MUKUL', 'serif', size, True), width('RAYANA', 'serif', size, True), 26
    x0 = W / 2 - (w1 + gap + w2) / 2
    s.text(x0, 205, 'MUKUL', 'serif', size, t['title'], 700, ls=2)
    s.text(x0 + w1 + gap, 205, 'RAYANA', 'serif', size, 'url(#goldtx)', 700, ls=2)
    # divider with diamond
    s.add(f'<path d="M{W / 2 - 170} 238h150M{W / 2 + 20} 238h150" stroke="{t["gold"]}" stroke-opacity=".6"/>'
          f'<path d="M{W / 2} 232l6 6-6 6-6-6z" fill="{t["gold"]}"/>')
    s.text(W / 2, 282, 'Agentic AI  ·  LLMOps  ·  RAG  ·  Reinforcement Learning for Game AI', size=23,
           fill=t['text'], weight=600, anchor='middle')
    s.text(W / 2, 320, 'M.S. Applied Machine Learning, University of Maryland  ·  Open to work', size=18,
           fill=t['muted'], anchor='middle')
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
    W, H = 1280, 64
    s = SVG(W, H, label)
    tw = width(label.upper(), 'serif', 30, True) + len(label) * 2.5
    s.add(f'<path d="M4 34l6-6 6 6-6 6z" fill="{t["gold"]}"/>')
    s.text(28, 45, label.upper(), 'serif', 30, t['title'], 700, ls=2.5)
    s.add(f'<path d="M{40 + tw} 34H{W - 4}" stroke="{t["gold"]}" stroke-opacity=".45"/>')
    s.save(f'title-{name}-{mode}.svg')


# ───────────────────────── highlights ─────────────────────────
HIGHLIGHTS = [
    ('1st place', 'UMD Smith Agentic AI Challenge 2026', 'PharmaChain, an 8-agent LangGraph system for pharma cold-chain risk', '$4K prize · Team Synapse'),
    ('3× faster', 'Production QA inference at BeeBox Studios', 'P95 latency 185 → 62 ms after ONNX export and INT8 quantization', 'AI Research Intern'),
    ('IEEE', 'Published at IDCIoT 2024', 'Voice-driven panoramic VR generation: speech to 360° scenes', 'Peer-reviewed paper'),
    ('3 live demos', 'Agents and RAG you can try right now', 'Hosted on Vercel and Hugging Face Spaces', 'PharmaChain · RECON · Irminsul'),
]


def highlights(t, mode):
    W, H, gap = 1280, 230, 20
    cw = (W - gap * 3) / 4
    s = SVG(W, H, 'Highlights: 1st place at the UMD Smith Agentic AI Challenge 2026; 3x faster production QA inference at BeeBox Studios; IEEE IDCIoT 2024 publication; 3 live demos.')
    s.add(f'<defs><linearGradient id="foil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["gold_lo"]}"/>'
          f'<stop offset=".5" stop-color="{t["gold_hi"]}"/><stop offset="1" stop-color="{t["gold"]}"/></linearGradient></defs>')
    for i, (v, l, sub, x_) in enumerate(HIGHLIGHTS):
        x = i * (cw + gap)
        panel(s, t, x, 2, cw, H - 4)
        s.text(x + 24, 62, v, 'serif', 34, 'url(#foil)' if i == 0 else t['gold_hi'], 700)
        for j, ln in enumerate(wrap(l, 'sans', 17, cw - 48, True)):
            s.text(x + 24, 98 + j * 22, ln, size=17, fill=t['title'], weight=800)
        for j, ln in enumerate(wrap(sub, 'sans', 15, cw - 48)[:3]):
            s.text(x + 24, 150 + j * 20, ln, size=15, fill=t['muted'])
        s.add(f'<path d="M{x + 24} {H - 36}h{cw - 48}" stroke="{t["line"]}"/>')
        s.text(x + 24, H - 16, x_, size=13.5, fill=t['gold'], weight=800)
    s.save(f'highlights-{mode}.svg')


# ───────────────────────── project cards ─────────────────────────
PROJECTS = [
    dict(slug='pharmachain', acc='anemo', kicker='MULTI-AGENT · 1ST PLACE, $4K', name='PharmaChain',
         sub='AI cargo monitor for pharma cold-chain risk', metric='0.9446', mlabel='XGBoost test ROC-AUC, explained with SHAP',
         minis=[('8', 'LangGraph agents'), ('12–15 s', 'alert → action')], tags=['LangGraph', 'XGBoost', 'SHAP', 'RAG']),
    dict(slug='nemesis', acc='pyro', kicker='REINFORCEMENT LEARNING', name='Nemesis',
         sub='Distributed RL boss AI with real-time LLM narration', metric='+85%', mlabel='longer survival than a scripted FSM boss',
         minis=[('2.6×', 'Ray RLlib, 1 → 8 workers'), ('<2 ms', 'per frame in Unity Sentis')], tags=['PPO', 'Ray RLlib', 'ONNX', 'Unity Sentis']),
    dict(slug='empathrag', acc='hydro', kicker='AI SAFETY', name='EmpathRAG',
         sub='NLI safety guardrail & emotion-conditioned RAG', metric='0.9629', mlabel='crisis recall, DeBERTa NLI guardrail',
         minis=[('1.67M', 'vector FAISS index'), ('0.88', 'emotion alignment (BM25: 0.30)')], tags=['DeBERTa', 'FAISS', 'Captum', 'Mistral 7B']),
    dict(slug='recon', acc='electro', kicker='AGENTIC RESEARCH', name='RECON',
         sub='Multi-agent ML research navigator', metric='52% vs 0%', mlabel='stale ML claims caught vs single-pass RAG',
         minis=[('43.9%', 'top-paper match vs 32.3%'), ('4', 'LangGraph agents')], tags=['LangGraph', 'LLM-as-a-Judge', 'Groq', 'Gradio']),
    dict(slug='irminsul', acc='dendro', kicker='LLMOPS & RAG', name='Irminsul',
         sub='Production LLMOps with a self-healing corpus', metric='0.826', mlabel='semantic similarity, Llama 3.1 8B QLoRA',
         minis=[('6,876', 'Pinecone vectors · 840 docs'), ('Weekly', 'corpus CI on GitHub Actions')], tags=['QLoRA', 'Pinecone', 'FastAPI', 'MLflow']),
    dict(slug='docpilot', acc='cryo', kicker='SECURE DOCUMENT AI', name='DocPilot',
         sub='Secure document intelligence platform', metric='90 ms', mlabel='P95 latency, RoBERTa-squad2 ONNX INT8',
         minis=[('66.0%', 'end-to-end F1'), ('RBAC', 'injection & PII defences')], tags=['BM25 + BGE', 'Reranking', 'ONNX', 'RBAC']),
    dict(slug='eldervale', acc='geo', kicker='GAME DEV · BROWSER CO-OP', name='Eldervale',
         sub='Cozy 3D two-player mystery game', metric='~2 MB', mlabel='to start playing, peer-to-peer co-op over WebRTC',
         minis=[('130', 'automated tests'), ('3', 'endings, solo or co-op')], tags=['Three.js', 'TypeScript', 'WebRTC', 'Vite']),
    dict(slug='vrgen', acc='gold', kicker='GENERATIVE AI · IEEE IDCIOT 2024', name='Panoramic VR Generation',
         sub='Peer-reviewed speech → 360° scene pipeline', metric='2.3×', mlabel='throughput from attention slicing + xFormers',
         minis=[('10 GB', 'VRAM budget'), ('IEEE', 'peer-reviewed')], tags=['Whisper', 'GPT-Neo', 'Stable Diffusion']),
]


def card(t, mode, p):
    W, H = 620, 330
    a = t['acc'][p['acc']]
    s = SVG(W, H, f"{p['name']}: {p['sub']}. {p['metric']} {p['mlabel']}.")
    panel(s, t, 0, 0, W, H, accent=a)
    s.add(f'<rect x="1.5" y="1.5" width="5" height="{H - 3}" rx="2.5" fill="{a}"/>')
    s.text(32, 46, p['kicker'], size=13.5, fill=a, weight=800, ls=2.2)
    s.add(f'<text x="{W - 30}" y="47" font-family="Nunito Sans" font-size="20" fill="{t["gold"]}" text-anchor="end">↗</text>'); s.chars['sans'] += '↗'
    s.text(32, 90, p['name'], 'serif', 31 if len(p['name']) < 16 else 26, t['title'], 700, ls=.5)
    s.text(32, 120, p['sub'], size=16.5, fill=t['muted'])
    s.text(32, 180, p['metric'], 'serif', 40, t['gold_hi'], 700)
    mw = width(p['metric'], 'serif', 40, True) + 46
    for j, ln in enumerate(wrap(p['mlabel'], 'sans', 15, W - mw - 40)[:2]):
        s.text(mw, 166 + j * 19 - (0 if len(wrap(p['mlabel'], 'sans', 15, W - mw - 40)) > 1 else -8), ln, size=15, fill=t['text'])
    # mini stats
    for k, (v, l) in enumerate(p['minis']):
        x = 32 + k * 290
        s.add(f'<path d="M{x} 206h270" stroke="{t["line"]}"/>')
        s.text(x, 234, v, 'serif', 21, t['title'], 700)
        s.text(x + width(v, 'serif', 21, True) + 10, 233, l, size=14, fill=t['muted'])
    # tags
    x = 32
    for tag in p['tags']:
        tw = width(tag, 'sans', 13.5, True) + 26
        s.add(f'<rect x="{x}" y="270" width="{tw:.1f}" height="30" rx="15" fill="none" stroke="{t["line2"]}"/>')
        s.text(x + tw / 2, 290, tag, size=13.5, fill=t['text'], weight=700, anchor='middle')
        x += tw + 8
    s.save(f'card-{p["slug"]}-{mode}.svg')


# ───────────────────────── footer ─────────────────────────
def footer(t, mode):
    W, H = 1280, 120
    s = SVG(W, H, 'Thanks for stopping by.')
    stars(s, t, 30, 3, (0, 10, W, H - 10))
    s.add(f'<path d="M{W / 2 - 260} 52h240M{W / 2 + 20} 52h240" stroke="{t["gold"]}" stroke-opacity=".5"/>'
          f'<path d="M{W / 2} 44l8 8-8 8-8-8z" fill="{t["gold"]}"/>')
    s.text(W / 2, 96, 'Thanks for stopping by  ·  mukulray1603.github.io', size=17, fill=t['muted'], anchor='middle')
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
        banner(t, mode); highlights(t, mode); footer(t, mode)
        for b in BUTTONS: button(t, mode, *b)
        for n, l in TITLES: title(t, mode, n, l)
        for p in PROJECTS: card(t, mode, p)
    print('built', len(os.listdir(OUT)), 'files in', os.path.abspath(OUT))
