"""
Builds the SVG images used by README.md.

Edit the content below, then run:  python3 build.py
Every image switches between light and dark to match the viewer's system theme.

GitHub shows SVGs as images, so web fonts can't load inside them: text uses the
system font stack, and widths below are estimated for it.
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"

# ------------------------------------------------------------------
# Content
# ------------------------------------------------------------------
NAME_FIRST, NAME_LAST = "VasanthKumar", "Dhilipkumar"
ROLE = "Generative AI & Business Analytics"
TAGLINE = "I take GenAI projects past the demo and into production."
META = "Ex–Technical Lead, GenAI @ PepsiCo  ·  MSc Business Analytics, University College Cork"
STATUS_CHIP = "OPEN TO ROLES  ·  CORK, IRELAND"

METRICS = [
    ("2.5+", "Years in the AI field", "#6366F1", "#22D3EE"),
    ("12+", "Production deployments", "#8B5CF6", "#D946EF"),
    ("10+", "Business teams served", "#EC4899", "#F97316"),
    ("~40%", "Faster iteration", "#10B981", "#22D3EE"),
]

STACK = [
    ("Generative AI", "#8B5CF6", ["Azure OpenAI", "GPT models", "Multi-LLM orchestration", "AI agents", "Prompt engineering", "Document Q&A"]),
    ("Data & ML", "#22D3EE", ["Python", "Forecasting", "Business analytics", "Dashboards"]),
    ("Web", "#F97316", ["React", "JavaScript", "HTML & CSS", "REST APIs"]),
    ("Cloud & delivery", "#10B981", ["Microsoft Azure", "Production rollout", "Security governance", "ROI evaluation"]),
]

# (file name, title, badge, colour, two description lines, tech pills, graphic)
PROJECTS = [
    ("card-orchestration", "Multi-LLM Orchestration", "PRODUCTION  ·  10+ TEAMS", "#6366F1",
     ["One routing layer that sends each GenAI request to the right model by cost, scale,",
      "resources and data readiness. Reusable prompts cut iteration time by ~40%."],
     ["Azure OpenAI", "Python", "LLM routing", "Prompt templates"], "routing"),
    ("card-roi", "Agent-based ROI Evaluation", "PRODUCTION  ·  WEEKS → HOURS", "#D946EF",
     ["Agents collect and score the inputs a business case needs, so weak GenAI use cases",
      "get turned down before anyone builds them."],
     ["AI agents", "Azure OpenAI", "Python"], "agents"),
    ("card-earlywarn", "EarlyWarn IRL", "MSC DISSERTATION  ·  TEAM OF 5", "#22D3EE",
     ["Forecasts where Ireland's health service will run short of staff, early enough to act.",
      "Built at University College Cork for the MSc in Business Analytics."],
     ["Python", "Forecasting", "Dashboard"], "forecast"),
    ("card-chatbots", "GPT Document Chatbots", "PEPSICO  ·  AZURE OPENAI", "#F59E0B",
     ["PDF Q&A and GAP compliance chatbots on Azure OpenAI, with React frontends for the",
      "internal teams using them."],
     ["Azure OpenAI", "GPT", "React"], "chat"),
]

HEADERS = {
    "hdr-about": "ABOUT ME",
    "hdr-stack": "TECH STACK",
    "hdr-work": "FEATURED WORK",
    "hdr-exp": "EXPERIENCE",
    "hdr-focus": "CURRENT FOCUS",
    "hdr-philosophy": "PHILOSOPHY",
}

# ------------------------------------------------------------------
# Shared styling: light by default, dark when the viewer's system is dark
# ------------------------------------------------------------------
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

BASE_CSS = f"""
  text {{ font-family: {FONT}; }}
  .card {{ fill: #FFFFFF; stroke: #E5E7EB; }}
  .ink {{ fill: #111827; }}
  .muted {{ fill: #4B5563; }}
  .faint {{ stroke: #E5E7EB; }}
  .pill {{ fill: #F3F4F8; }}
  .bg-dot {{ fill: #CBD5E1; }}
  @media (prefers-color-scheme: dark) {{
    .card {{ fill: #0D1117; stroke: #262C36; }}
    .ink {{ fill: #F0F6FC; }}
    .muted {{ fill: #9198A1; }}
    .faint {{ stroke: #262C36; }}
    .pill {{ fill: #161B22; }}
    .bg-dot {{ fill: #30363D; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""


def svg(width, height, body, css="", defs="", label=""):
    role = f'role="img" aria-label="{escape(label)}"' if label else 'aria-hidden="true"'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {role}>
<defs>
<style>{BASE_CSS}{css}</style>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#A855F7"/>
</linearGradient>
{defs}
</defs>
{body}
</svg>
"""


def text_width(s, size, weight_factor=0.56):
    """Rough rendered width of s in the system font."""
    return len(s) * size * weight_factor


def pill(x, y, label, colour, size=12):
    w = text_width(label, size, 0.58) + 24
    return w, (
        f'<g transform="translate({x:.0f},{y})">'
        f'<rect width="{w:.0f}" height="26" rx="13" class="pill" stroke="{colour}" stroke-opacity="0.45"/>'
        f'<text x="{w / 2:.0f}" y="17.5" text-anchor="middle" font-size="{size}" font-weight="600" fill="{colour}">{escape(label)}</text>'
        f"</g>"
    )


# ------------------------------------------------------------------
# Graphics
# ------------------------------------------------------------------
def routing_graphic(cx, cy, scale=1.0, colour="#6366F1"):
    """Requests flow into a router, which sends each one to a different model."""
    s = scale
    models = [(cx + 120 * s, cy - 62 * s), (cx + 120 * s, cy), (cx + 120 * s, cy + 62 * s)]
    sources = [(cx - 130 * s, cy - 40 * s), (cx - 130 * s, cy + 40 * s)]
    out = []
    for i, (mx, my) in enumerate(models):
        out.append(f'<path d="M{cx},{cy} C{cx + 60 * s},{cy} {mx - 60 * s},{my} {mx},{my}" class="faint" stroke-width="2" fill="none"/>')
    for sx, sy in sources:
        out.append(f'<path d="M{sx},{sy} C{sx + 60 * s},{sy} {cx - 60 * s},{cy} {cx},{cy}" class="faint" stroke-width="2" fill="none"/>')
    # packets: in from a source, out to one model
    for i, (mx, my) in enumerate(models):
        sx, sy = sources[i % 2]
        path = (f"M{sx},{sy} C{sx + 60 * s},{sy} {cx - 60 * s},{cy} {cx},{cy} "
                f"C{cx + 60 * s},{cy} {mx - 60 * s},{my} {mx},{my}")
        out.append(
            f'<circle r="{4 * s:.1f}" fill="{colour}" opacity="0"><animateMotion dur="3s" begin="{i}s" repeatCount="indefinite" path="{path}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" dur="3s" begin="{i}s" repeatCount="indefinite"/></circle>'
        )
    for sx, sy in sources:
        out.append(f'<circle cx="{sx}" cy="{sy}" r="{6 * s}" class="pill" stroke="{colour}" stroke-opacity="0.5" stroke-width="1.5"/>')
    for i, (mx, my) in enumerate(models):
        out.append(
            f'<g><rect x="{mx - 4 * s}" y="{my - 14 * s}" width="{52 * s}" height="{28 * s}" rx="{8 * s}" class="pill" stroke="{colour}" stroke-opacity="0.6" stroke-width="1.5"/>'
            f'<text x="{mx + 22 * s}" y="{my + 4.5 * s}" text-anchor="middle" font-size="{12 * s:.0f}" font-weight="700" fill="{colour}">LLM</text>'
            f'<animate attributeName="opacity" values="0.55;1;0.55" dur="3s" begin="{i + 0.9}s" repeatCount="indefinite"/></g>'
        )
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{30 * s}" fill="{colour}" opacity="0.15"><animate attributeName="r" values="{26 * s};{36 * s};{26 * s}" dur="3s" repeatCount="indefinite"/></circle>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{22 * s}" fill="url(#brand)"/>')
    out.append(f'<path d="M{cx - 8 * s},{cy - 7 * s} h{10 * s} l{6 * s},{7 * s} l-{6 * s},{7 * s} h-{10 * s}" stroke="#fff" stroke-width="{2.2 * s}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return "\n".join(out)


def agents_graphic(cx, cy, colour):
    """Three agents feed a score that fills up."""
    nodes = [(cx - 70, cy - 40), (cx - 70, cy + 40), (cx - 110, cy)]
    out = []
    for i, (x, y) in enumerate(nodes):
        out.append(f'<line x1="{x}" y1="{y}" x2="{cx + 10}" y2="{cy}" class="faint" stroke-width="2" stroke-dasharray="4 5"><animate attributeName="stroke-dashoffset" from="18" to="0" dur="1.2s" repeatCount="indefinite"/></line>')
    for i, (x, y) in enumerate(nodes):
        out.append(
            f'<circle cx="{x}" cy="{y}" r="13" class="pill" stroke="{colour}" stroke-width="1.5">'
            f'<animate attributeName="stroke-opacity" values="0.3;1;0.3" dur="2.4s" begin="{i * 0.8}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{x}" cy="{y - 3}" r="3.5" fill="{colour}"/><path d="M{x - 6},{y + 7} a6,5 0 0 1 12,0" fill="{colour}"/>'
        )
    bx, by = cx + 10, cy - 34
    out.append(f'<rect x="{bx}" y="{by}" width="92" height="68" rx="12" class="pill" stroke="{colour}" stroke-opacity="0.5"/>')
    out.append(f'<text x="{bx + 14}" y="{by + 24}" font-size="11" font-weight="700" letter-spacing="1" class="muted">ROI</text>')
    out.append(f'<rect x="{bx + 14}" y="{by + 38}" width="64" height="8" rx="4" class="bg-dot"/>')
    out.append(f'<rect x="{bx + 14}" y="{by + 38}" width="0" height="8" rx="4" fill="{colour}"><animate attributeName="width" values="0;64;64;0" keyTimes="0;0.6;0.9;1" dur="3.5s" repeatCount="indefinite"/></rect>')
    out.append(f'<path d="M{bx + 68},{by + 20} l5,5 l9,-10" stroke="#10B981" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.55;0.62;0.9;1" dur="3.5s" repeatCount="indefinite"/></path>')
    return "\n".join(out)


def forecast_graphic(cx, cy, colour):
    """History line, a dashed forecast that draws itself, and a warning point."""
    x0, y0, w, h = cx - 110, cy - 50, 220, 100
    out = [f'<line x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}" class="faint" stroke-width="1.5"/>',
           f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + h}" class="faint" stroke-width="1.5"/>']
    # shortage threshold
    out.append(f'<line x1="{x0}" y1="{y0 + 22}" x2="{x0 + w}" y2="{y0 + 22}" stroke="#EF4444" stroke-opacity="0.5" stroke-width="1.5" stroke-dasharray="3 4"/>')
    hist = [(0, 80), (25, 70), (50, 74), (75, 60), (100, 62), (120, 52)]
    fut = [(120, 52), (145, 44), (170, 34), (195, 26), (212, 18)]
    pts = lambda p: " ".join(f"{x0 + x},{y0 + y}" for x, y in p)
    out.append(f'<polyline points="{pts(hist)}" fill="none" stroke="{colour}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
    out.append(f'<polyline points="{pts(fut)}" fill="none" stroke="{colour}" stroke-width="2.5" stroke-dasharray="5 5" stroke-linecap="round" opacity="0.9">'
               f'<animate attributeName="opacity" values="0;0.9;0.9;0" keyTimes="0;0.3;0.9;1" dur="4s" repeatCount="indefinite"/></polyline>')
    ax, ay = x0 + 195, y0 + 26
    out.append(f'<circle cx="{ax}" cy="{ay}" r="5" fill="#EF4444"/>')
    out.append(f'<circle cx="{ax}" cy="{ay}" r="5" fill="none" stroke="#EF4444" stroke-width="2"><animate attributeName="r" values="5;14" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0" dur="1.6s" repeatCount="indefinite"/></circle>')
    return "\n".join(out)


def chat_graphic(cx, cy, colour):
    """A question bubble and an answer bubble with typing dots."""
    out = [
        f'<rect x="{cx - 110}" y="{cy - 52}" width="130" height="40" rx="14" class="pill" stroke="{colour}" stroke-opacity="0.45"/>',
        f'<rect x="{cx - 96}" y="{cy - 38}" width="80" height="6" rx="3" class="bg-dot"/>',
        f'<rect x="{cx - 96}" y="{cy - 26}" width="52" height="6" rx="3" class="bg-dot"/>',
        f'<rect x="{cx - 20}" y="{cy + 4}" width="130" height="44" rx="14" fill="{colour}" fill-opacity="0.15" stroke="{colour}" stroke-opacity="0.6"/>',
    ]
    for i in range(3):
        out.append(f'<circle cx="{cx + 22 + i * 16}" cy="{cy + 26}" r="4.5" fill="{colour}"><animate attributeName="opacity" values="0.25;1;0.25" dur="1.2s" begin="{i * 0.2}s" repeatCount="indefinite"/></circle>')
    # document icon
    dx, dy = cx - 150, cy + 4
    out.append(f'<path d="M{dx},{dy} h22 l10,10 v30 h-32 z" class="pill" stroke="{colour}" stroke-width="1.5" stroke-linejoin="round"/>')
    out.append(f'<text x="{dx + 16}" y="{dy + 32}" text-anchor="middle" font-size="9" font-weight="800" fill="{colour}">PDF</text>')
    return "\n".join(out)


GRAPHICS = {"routing": routing_graphic, "agents": agents_graphic, "forecast": forecast_graphic, "chat": chat_graphic}


# ------------------------------------------------------------------
# Images
# ------------------------------------------------------------------
def hero():
    chip_w = text_width(STATUS_CHIP, 11, 0.66) + 44
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.3" class="bg-dot"/>' for x in range(820, 1180, 24) for y in range(28, 300, 24)
    )
    body = f"""
<rect x="1" y="1" width="1198" height="298" rx="22" class="card" stroke-width="1.5"/>
<g opacity="0.7">{dots}</g>
<circle cx="1000" cy="150" r="150" fill="#6366F1" opacity="0.10" filter="url(#blur)"><animate attributeName="opacity" values="0.06;0.16;0.06" dur="8s" repeatCount="indefinite"/></circle>

<g transform="translate(48,44)">
  <rect width="{chip_w:.0f}" height="28" rx="14" fill="#10B981" fill-opacity="0.10" stroke="#10B981" stroke-opacity="0.4"/>
  <circle cx="16" cy="14" r="4" fill="#10B981"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="28" y="18.5" font-size="11" font-weight="700" letter-spacing="1.4" fill="#10B981">{escape(STATUS_CHIP)}</text>
</g>

<text x="46" y="128" font-size="54" font-weight="800" letter-spacing="-1.5" class="ink">{escape(NAME_FIRST)} <tspan fill="url(#brand)">{escape(NAME_LAST)}</tspan></text>
<text x="48" y="170" font-size="22" font-weight="500" class="muted">{escape(ROLE)}</text>
<text x="48" y="218" font-size="17" font-weight="600" class="ink">{escape(TAGLINE)}</text>
<text x="48" y="252" font-size="14" font-weight="500" class="muted">{escape(META)}</text>

{routing_graphic(985, 150, 1.05)}
"""
    defs = '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>'
    return svg(1200, 300, body, defs=defs, label=f"{NAME_FIRST} {NAME_LAST}. {ROLE}. {TAGLINE}")


def metrics():
    w, gap = 282, 24
    cards, defs = [], []
    for i, (num, label, c1, c2) in enumerate(METRICS):
        x = i * (w + gap)
        defs.append(f'<linearGradient id="m{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{c1}"/><stop offset="100%" stop-color="{c2}"/></linearGradient>')
        cards.append(f"""
<g transform="translate({x + 1},1)">
  <rect width="{w - 2}" height="106" rx="16" class="card" stroke-width="1.5"/>
  <rect width="{w - 2}" height="106" rx="16" fill="none" stroke="url(#m{i})" stroke-width="1.5" opacity="0.2">
    <animate attributeName="opacity" values="0.15;0.6;0.15" dur="4s" begin="{i * 0.6}s" repeatCount="indefinite"/>
  </rect>
  <rect x="24" y="0" width="44" height="3" rx="1.5" fill="url(#m{i})"/>
  <text x="24" y="58" font-size="40" font-weight="800" letter-spacing="-1" fill="url(#m{i})">{escape(num)}</text>
  <text x="24" y="84" font-size="14" font-weight="500" class="muted">{escape(label)}</text>
</g>""")
    alt = "Highlights: " + ", ".join(f"{n} {l.lower()}" for n, l, *_ in METRICS)
    return svg(1200, 108, "".join(cards), defs="".join(defs), label=alt)


def header(title):
    css = """
  .bar { transform-box: fill-box; transform-origin: left; animation: grow 3s ease-in-out infinite; }
  @keyframes grow { 0%, 100% { transform: scaleX(0.55); } 50% { transform: scaleX(1); } }
"""
    body = f"""
<text x="0" y="28" font-size="19" font-weight="800" letter-spacing="3" class="ink">{escape(title)}</text>
<rect class="bar" x="0" y="40" width="80" height="3" rx="1.5" fill="url(#brand)"/>
"""
    return svg(1200, 48, body, css=css, label=title.title())


def divider():
    body = """
<line x1="0" y1="12" x2="1200" y2="12" stroke="url(#fade)" stroke-width="1.5"/>
<circle cx="200" cy="12" r="3" fill="#A855F7"><animate attributeName="cx" values="200;1000;200" dur="8s" repeatCount="indefinite"/></circle>
"""
    defs = """<linearGradient id="fade" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1200" y2="0">
  <stop offset="0%" stop-color="#6366F1" stop-opacity="0"/><stop offset="50%" stop-color="#8B5CF6" stop-opacity="0.6"/><stop offset="100%" stop-color="#6366F1" stop-opacity="0"/>
</linearGradient>"""
    return svg(1200, 24, body, defs=defs)


def stack():
    rows, y = [], 34
    for label, colour, items in STACK:
        x, line = 250, []
        for item in items:
            w, g = pill(x, y - 18, item, colour)
            if x + w > 1160:
                x, y = 250, y + 38
                w, g = pill(x, y - 18, item, colour)
            line.append(g)
            x += w + 10
        rows.append(
            f'<circle cx="46" cy="{y - 5}" r="5" fill="{colour}"/>'
            f'<text x="62" y="{y}" font-size="15" font-weight="700" class="ink">{escape(label)}</text>' + "".join(line)
        )
        y += 54
    h = y - 20
    body = f'<rect x="1" y="1" width="1198" height="{h - 2}" rx="18" class="card" stroke-width="1.5"/>' + "".join(
        f'<g transform="translate(0,6)">{r}</g>' for r in rows
    )
    alt = "Tech stack. " + " ".join(f"{l}: {', '.join(i)}." for l, _, i in STACK)
    return svg(1200, h, body, label=alt)


def project_card(title, badge, colour, desc, pills, graphic):
    badge_w = text_width(badge, 11, 0.68) + 36
    pill_svg, x = [], 0
    for p in pills:
        w, g = pill(x, 0, p, colour)
        pill_svg.append(g)
        x += w + 8
    body = f"""
<rect x="1" y="1" width="1198" height="196" rx="18" class="card" stroke-width="1.5"/>
<rect x="1" y="24" width="4" height="150" rx="2" fill="{colour}"/>
<g transform="translate(40,26)">
  <rect width="{badge_w:.0f}" height="24" rx="12" fill="{colour}" fill-opacity="0.12" stroke="{colour}" stroke-opacity="0.4"/>
  <circle cx="14" cy="12" r="3.5" fill="{colour}"><animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/></circle>
  <text x="25" y="16" font-size="11" font-weight="700" letter-spacing="1.2" fill="{colour}">{escape(badge)}</text>
</g>
<text x="40" y="84" font-size="26" font-weight="800" letter-spacing="-0.5" class="ink">{escape(title)}</text>
<text x="40" y="114" font-size="16" class="muted">{escape(desc[0])}</text>
<text x="40" y="137" font-size="16" class="muted">{escape(desc[1])}</text>
<g transform="translate(40,152)">{''.join(pill_svg)}</g>
<g>{GRAPHICS[graphic](985, 100, *([1.0, colour] if graphic == 'routing' else [colour]))}</g>
"""
    return svg(1200, 198, body, label=f"{title}: {badge.title()}. {' '.join(desc)}")


def main():
    OUT.mkdir(exist_ok=True)
    files = {"hero.svg": hero(), "metrics.svg": metrics(), "divider.svg": divider(), "stack.svg": stack()}
    files |= {f"{name}.svg": header(t) for name, t in HEADERS.items()}
    files |= {f"{f}.svg": project_card(t, b, c, d, p, g) for f, t, b, c, d, p, g in PROJECTS}
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"Wrote {len(files)} images to {OUT}")


if __name__ == "__main__":
    main()
