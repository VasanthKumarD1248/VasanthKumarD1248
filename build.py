"""
Builds the SVG images used by README.md.

Edit the content below, then run:  python3 build.py
(assets/*.svg is regenerated from scratch each time.)

Design: transparent backgrounds and hairlines so every image sits quietly on GitHub's
page in both light and dark, one indigo accent, and a single slow animation (the
idea → production track in the hero). GitHub can't load web fonts inside SVG images,
so text uses the system font stack and widths below are estimates for it.
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"

# ------------------------------------------------------------------
# Content
# ------------------------------------------------------------------
NAME = "VasanthKumar Dhilipkumar"
KICKER = "GENERATIVE AI  ·  BUSINESS ANALYTICS  ·  CORK, IRELAND"
TAGLINE = "I take GenAI projects past the demo and into production."
STAGES = ["Idea", "Demo", "Pilot", "Production"]
STAGE_NOTE = (1, "where most stop")  # (stage index, note shown above it)

NUMBERS = [
    ("2.5+", "years building with AI"),
    ("12+", "production deployments"),
    ("10+", "business teams served"),
    ("~40%", "faster iteration"),
]

SECTIONS = {
    "s-about": ("01", "ABOUT"),
    "s-work": ("02", "SELECTED WORK"),
    "s-path": ("03", "PATH"),
    "s-toolkit": ("04", "TOOLKIT"),
    "s-now": ("05", "NOW"),
}

# (file, title, one line, stack, outcome, outcome label)
WORK = [
    ("w-orchestration", "Multi-LLM orchestration", "One routing layer that sends each GenAI request to the right model.",
     ["Azure OpenAI", "Python", "LLM routing"], "10+", "business teams"),
    ("w-roi", "Agent-based ROI evaluation", "Agents score each GenAI use case, so weak ones are cut before they're built.",
     ["AI agents", "Azure OpenAI", "Python"], "weeks → hours", "per evaluation"),
    ("w-earlywarn", "EarlyWarn IRL", "Forecasting where Ireland's health service will run short of staff.",
     ["Python", "Forecasting", "Dashboard"], "MSc", "dissertation · team of 5"),
    ("w-chatbots", "GPT document assistants", "PDF Q&A and GAP compliance assistants on Azure OpenAI.",
     ["Azure OpenAI", "GPT", "React"], "2", "internal assistants"),
]

# Timeline rows: (start year, end year, label, place, is_current)
PATH_START, PATH_END, NOW = 2019, 2027, 2026.75
PATH = [
    (2019.6, 2023.4, "BTech Computer Science (Data Science)  ·  VIT", "Vellore, India", False),
    (2023.0, 2025.65, "PepsiCo  ·  Intern → Graduate Engineering Trainee → Technical Lead, GenAI", "India", False),
    (2025.7, NOW, "University College Cork  ·  MSc Business Analytics (2:1) → Teaching Assistant", "Cork, Ireland", True),
]
PATH_MARKS = [(2023.6, 1)]  # small dots on a row: (year, row index), e.g. a role change

TOOLKIT = [
    ("Generative AI", ["Azure OpenAI", "GPT models", "Multi-LLM orchestration", "AI agents", "Prompt engineering", "Document Q&A"]),
    ("Data & ML", ["Python", "Forecasting", "Business analytics", "Dashboards"]),
    ("Web", ["React", "JavaScript", "HTML & CSS", "REST APIs"]),
    ("Delivery", ["Microsoft Azure", "Production rollout", "Security governance", "ROI evaluation"]),
]

# ------------------------------------------------------------------
# Shared styling
# ------------------------------------------------------------------
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
W = 1200

CSS = f"""
  text {{ font-family: {FONT}; }}
  .ink {{ fill: #0F172A; }}
  .muted {{ fill: #64748B; }}
  .accent {{ fill: #6366F1; }}
  .line {{ stroke: #E2E8F0; }}
  .line-strong {{ stroke: #CBD5E1; }}
  .dot {{ fill: #CBD5E1; }}
  .past {{ fill: #94A3B8; }}
  .live {{ fill: #10B981; }}
  @media (prefers-color-scheme: dark) {{
    .ink {{ fill: #E6EDF3; }}
    .muted {{ fill: #8B949E; }}
    .accent {{ fill: #8B93FF; }}
    .line {{ stroke: #30363D; }}
    .line-strong {{ stroke: #484F58; }}
    .dot {{ fill: #484F58; }}
    .past {{ fill: #6E7681; }}
    .live {{ fill: #3FB950; }}
  }}
"""


def svg(height, body, label=""):
    role = f'role="img" aria-label="{escape(label)}"' if label else 'aria-hidden="true"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" {role}>\n'
            f"<style>{CSS}</style>\n{body}\n</svg>\n")


def width(s, size, factor=0.54, spacing=0.0):
    """Rough rendered width of s in the system font."""
    return len(s) * (size * factor + spacing)


# ------------------------------------------------------------------
# Images
# ------------------------------------------------------------------
def hero():
    y_track, x0, x1 = 236, 8, W - 8
    dur = 9  # seconds for one pass; the dot then rests at Production
    travel = 0.55  # share of the loop spent moving
    xs = [x0 + (x1 - x0) * i / (len(STAGES) - 1) for i in range(len(STAGES))]

    parts = [
        f'<text x="2" y="34" font-size="12" font-weight="600" letter-spacing="2.4" class="muted">{escape(KICKER)}</text>',
        f'<g transform="translate({W - 128},22)"><circle cx="6" cy="7" r="4" class="live">'
        f'<animate attributeName="opacity" values="1;0.35;1" dur="3s" repeatCount="indefinite"/></circle>'
        f'<text x="18" y="12" font-size="13" font-weight="500" class="muted">Open to roles</text></g>',
        f'<text x="0" y="112" font-size="62" font-weight="700" letter-spacing="-1.8" class="ink">{escape(NAME)}</text>',
        f'<text x="2" y="156" font-size="21" class="muted">{escape(TAGLINE)}</text>',
        # track
        f'<line x1="{x0}" y1="{y_track}" x2="{x1}" y2="{y_track}" class="line-strong" stroke-width="1.5"/>',
        f'<rect x="{x0}" y="{y_track - 1}" width="0" height="2" rx="1" class="accent">'
        f'<animate attributeName="width" values="0;{x1 - x0};{x1 - x0}" keyTimes="0;{travel};1" dur="{dur}s" '
        f'calcMode="spline" keySplines="0.45 0 0.25 1;0 0 1 1" repeatCount="indefinite"/></rect>',
    ]
    for i, (x, stage) in enumerate(zip(xs, STAGES)):
        last = i == len(STAGES) - 1
        anchor = "start" if i == 0 else "end" if last else "middle"
        parts.append(f'<circle cx="{x}" cy="{y_track}" r="5" class="dot"/>')
        # the stage lights up as the dot reaches it (approximate: spline easing)
        f = travel * i / (len(STAGES) - 1)
        on = f"{max(f - 0.001, 0):.3f}"
        parts.append(
            f'<circle cx="{x}" cy="{y_track}" r="5" class="accent" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{on};{f:.3f};1" dur="{dur}s" repeatCount="indefinite"/></circle>'
        )
        cls, weight = ("accent", 700) if last else ("muted", 500)
        parts.append(f'<text x="{x}" y="{y_track + 30}" text-anchor="{anchor}" font-size="12" font-weight="{weight}" '
                     f'letter-spacing="2" class="{cls}">{stage.upper()}</text>')
    i, note = STAGE_NOTE
    parts.append(f'<text x="{xs[i]}" y="{y_track - 16}" text-anchor="middle" font-size="13" font-style="italic" class="muted">{escape(note)}</text>')
    parts.append(f'<line x1="{xs[i]}" y1="{y_track - 11}" x2="{xs[i]}" y2="{y_track - 6}" class="line-strong" stroke-width="1.5"/>')
    # a soft halo at Production once the dot arrives
    parts.append(
        f'<circle cx="{x1}" cy="{y_track}" r="5" fill="none" stroke="#6366F1" stroke-width="1.5" opacity="0">'
        f'<animate attributeName="r" values="5;5;16;16" keyTimes="0;{travel};{travel + 0.2};1" dur="{dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;0;0.6;0;0" keyTimes="0;{travel};{travel + 0.02};{travel + 0.2};1" dur="{dur}s" repeatCount="indefinite"/></circle>'
    )
    return svg(290, "\n".join(parts), label=f"{NAME}. {TAGLINE}")


def numbers():
    col = W / len(NUMBERS)
    parts = [f'<line x1="0" y1="1" x2="{W}" y2="1" class="line" stroke-width="1.5"/>',
             f'<line x1="0" y1="103" x2="{W}" y2="103" class="line" stroke-width="1.5"/>']
    for i, (num, label) in enumerate(NUMBERS):
        x = i * col + (0 if i == 0 else 28)
        if i:
            parts.append(f'<line x1="{i * col:.0f}" y1="24" x2="{i * col:.0f}" y2="80" class="line" stroke-width="1.5"/>')
        parts.append(f'<text x="{x:.0f}" y="58" font-size="36" font-weight="600" letter-spacing="-1" class="ink">{escape(num)}</text>')
        parts.append(f'<text x="{x:.0f}" y="82" font-size="14" class="muted">{escape(label)}</text>')
    return svg(104, "\n".join(parts), label="; ".join(f"{n} {l}" for n, l in NUMBERS))


def section(num, title):
    title_x = 34
    end = title_x + width(title, 13, 0.62, 3) + 18
    body = (f'<text x="0" y="26" font-size="13" font-weight="600" class="accent">{num}</text>'
            f'<text x="{title_x}" y="26" font-size="13" font-weight="700" letter-spacing="3" class="ink">{escape(title)}</text>'
            f'<line x1="{end:.0f}" y1="21.5" x2="{W}" y2="21.5" class="line" stroke-width="1.5"/>')
    return svg(40, body, label=title.title())


def work_row(title, line, stack, outcome, outcome_label):
    body = f"""
<text x="0" y="40" font-size="23" font-weight="600" letter-spacing="-0.3" class="ink">{escape(title)}<tspan class="muted" font-weight="400" dx="10">↗</tspan></text>
<text x="0" y="70" font-size="16" class="muted">{escape(line)}</text>
<text x="0" y="100" font-size="11.5" font-weight="600" letter-spacing="1.8" class="muted">{escape("  ·  ".join(s.upper() for s in stack))}</text>
<text x="{W}" y="50" text-anchor="end" font-size="30" font-weight="600" letter-spacing="-0.8" class="accent">{escape(outcome)}</text>
<text x="{W}" y="76" text-anchor="end" font-size="13" class="muted">{escape(outcome_label)}</text>
<line x1="0" y1="123" x2="{W}" y2="123" class="line" stroke-width="1.5"/>
"""
    return svg(124, body, label=f"{title}: {line} Outcome: {outcome} {outcome_label}.")


def path():
    left, right = 20, W - 20
    x = lambda year: left + (right - left) * (year - PATH_START) / (PATH_END - PATH_START)
    axis_y, row_gap, top = 214, 60, 56
    parts = [f'<line x1="{left}" y1="{axis_y}" x2="{right}" y2="{axis_y}" class="line-strong" stroke-width="1.5"/>']
    for year in range(PATH_START, PATH_END + 1):
        parts.append(f'<line x1="{x(year):.0f}" y1="{axis_y}" x2="{x(year):.0f}" y2="{axis_y + 6}" class="line-strong" stroke-width="1.5"/>')
        parts.append(f'<text x="{x(year):.0f}" y="{axis_y + 24}" text-anchor="middle" font-size="12" class="muted">{year}</text>')

    for i, (start, end, label, place, current) in enumerate(PATH):
        y = top + i * row_gap
        x0, x1 = x(start), x(end)
        cls = "accent" if current else "past"
        parts.append(f'<rect x="{x0:.0f}" y="{y}" width="{x1 - x0:.0f}" height="6" rx="3" class="{cls}"/>')
        # labels sit above the bar, aligned to whichever end keeps them on the canvas
        text_w = width(label, 14, 0.52)
        anchor, tx = ("start", x0) if x0 + text_w < right else ("end", x1 - 16)
        parts.append(f'<text x="{tx:.0f}" y="{y - 12}" text-anchor="{anchor}" font-size="14" font-weight="500" class="ink">{escape(label)}</text>')
        place_x, place_anchor = (x0 - 12, "end") if anchor == "start" and x0 > 140 else (x1 + 12, "start") if anchor == "start" else (x0 - 12, "end")
        parts.append(f'<text x="{place_x:.0f}" y="{y + 6}" text-anchor="{place_anchor}" font-size="12" font-style="italic" class="muted">{escape(place)}</text>')
    for year, row in PATH_MARKS:
        parts.append(f'<circle cx="{x(year):.0f}" cy="{top + row * row_gap + 3}" r="4.5" class="ink"/>')

    # "now" marker
    nx = x(NOW)
    parts.append(f'<line x1="{nx:.0f}" y1="24" x2="{nx:.0f}" y2="{axis_y}" stroke="#6366F1" stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="3 4"/>')
    parts.append(f'<text x="{nx:.0f}" y="16" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2" class="accent">NOW</text>')
    parts.append(f'<circle cx="{nx:.0f}" cy="{top + (len(PATH) - 1) * row_gap + 3}" r="5" class="accent">'
                 f'<animate attributeName="opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite"/></circle>')
    alt = "Path: " + "; ".join(f"{l} ({p})" for _, _, l, p, _ in PATH)
    return svg(250, "\n".join(parts), label=alt)


def toolkit():
    col = W / len(TOOLKIT)
    rows = max(len(items) for _, items in TOOLKIT)
    h = 44 + rows * 28 + 8
    parts = []
    for i, (label, items) in enumerate(TOOLKIT):
        x = i * col + (0 if i == 0 else 28)
        if i:
            parts.append(f'<line x1="{i * col:.0f}" y1="4" x2="{i * col:.0f}" y2="{h - 8}" class="line" stroke-width="1.5"/>')
        parts.append(f'<text x="{x:.0f}" y="18" font-size="11.5" font-weight="700" letter-spacing="2.2" class="accent">{escape(label.upper())}</text>')
        for j, item in enumerate(items):
            parts.append(f'<text x="{x:.0f}" y="{52 + j * 28}" font-size="16" class="ink">{escape(item)}</text>')
    alt = "Toolkit. " + " ".join(f"{l}: {', '.join(i)}." for l, i in TOOLKIT)
    return svg(h, "\n".join(parts), label=alt)


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    files = {"hero.svg": hero(), "numbers.svg": numbers(), "path.svg": path(), "toolkit.svg": toolkit()}
    files |= {f"{name}.svg": section(n, t) for name, (n, t) in SECTIONS.items()}
    files |= {f"{f}.svg": work_row(*rest) for f, *rest in WORK}
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"Wrote {len(files)} images to {OUT}")


if __name__ == "__main__":
    main()
