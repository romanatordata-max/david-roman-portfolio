#!/usr/bin/env python3
"""Build index.html from games.json.

To add a game: add an entry to "games" in games.json, put its banner image in
assets/, then run `python3 build.py` and commit index.html alongside the change.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "games.json").read_text(encoding="utf-8"))
site = data["site"]

CSS = """
:root {
  --bg: #fbf7f1;
  --surface: #ffffff;
  --ink: #1d1820;
  --body-ink: #3b3440;
  --muted: #6f6776;
  --line: #e7dfd4;
  --violet-bg: #0f0426;
  --violet-panel: #1a1030;
  --violet-line: #2e1f52;
  --cream: #fff3d4;
  --cream-muted: #c9bfd9;
  --gold: #d9a52e;
  --display: "Bricolage Grotesque", "Helvetica Neue", Arial, sans-serif;
  --body: "Figtree", system-ui, -apple-system, "Segoe UI", sans-serif;
  color-scheme: light;
}
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--bg); color: var(--ink); }
body { font-family: var(--body); font-size: 17px; line-height: 1.6; color: var(--body-ink); }
main { max-width: 1040px; margin: 0 auto; padding: 48px 20px 40px; }
a { color: inherit; }
:focus-visible { outline: 3px solid var(--gold); outline-offset: 3px; border-radius: 4px; }
strong { color: var(--ink); font-weight: 700; }

header { display: grid; gap: 14px; }
header h1 {
  font-family: var(--display);
  font-weight: 800;
  font-size: clamp(2.6rem, 7vw, 4.4rem);
  line-height: 1;
  margin: 0;
  color: var(--ink);
  text-wrap: balance;
}
header h1 .accent { color: #e8452c; }
header p { margin: 0; max-width: 60ch; font-size: 1.1rem; color: var(--body-ink); }

h2.section {
  font-family: var(--display);
  font-weight: 800;
  font-size: clamp(1.6rem, 4vw, 2.2rem);
  line-height: 1.1;
  margin: 0;
  color: var(--ink);
}

.games { display: grid; gap: 28px; margin-top: 44px; grid-template-columns: 1fr; }
@media (min-width: 820px) { .games { grid-template-columns: 1fr 1fr; } }

.card {
  background: var(--surface);
  border: 6px solid var(--accent);
  border-radius: 18px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-width: 0;
  box-shadow: 0 0 0 4px rgba(var(--glow), 0.12), 0 0 36px rgba(var(--glow), 0.32), 0 12px 32px rgba(29, 24, 32, 0.08);
}
.card.dark {
  background: var(--card-bg);
  color: var(--cream-muted);
  box-shadow: 0 0 0 4px rgba(var(--glow), 0.12), 0 0 36px rgba(var(--glow), 0.35), 0 16px 40px rgba(15, 4, 38, 0.5);
}
.card.dark .body { background: var(--panel-bg); }
.card.dark strong { color: var(--cream); }
.card.dark h2 { color: var(--cream); }
.card.dark .facts dd { color: var(--cream); }
.card.dark .facts { border-top-color: var(--violet-line); }
.card.dark .facts dt { color: var(--cream-muted); }

.art {
  margin: 14px 14px 0;
  background: var(--accent-soft);
  aspect-ratio: 1200 / 630;
  overflow: hidden;
  border-radius: 12px;
}
.card.dark .art { background: var(--art-bg); }
.art img { display: block; width: 100%; height: 100%; object-fit: cover; }

.body { padding: 26px 26px 24px; display: flex; flex-direction: column; gap: 14px; flex: 1; }
.status {
  align-self: flex-start;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent-text);
  background: var(--accent-soft);
  border-radius: 999px;
  padding: 5px 12px;
}
.card h2 { font-family: var(--display); font-weight: 800; font-size: 2.1rem; line-height: 1.05; margin: 0; color: var(--ink); }
.hook { margin: 0; font-size: 1.12rem; font-weight: 700; color: var(--accent-text); line-height: 1.35; }
.card p { margin: 0; }

.points { list-style: none; padding: 0; margin: 2px 0 0; display: grid; gap: 8px; }
.points li { position: relative; padding-left: 22px; }
.points li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.55em;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--accent);
}

.facts {
  list-style: none;
  padding: 16px 0 0;
  margin: 4px 0 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 18px;
  border-top: 1px solid var(--line);
  font-size: 0.95rem;
}
.facts dt { color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; }
.facts dd { margin: 2px 0 0; color: var(--ink); font-weight: 700; }

.actions { margin-top: auto; padding-top: 8px; display: flex; flex-wrap: wrap; gap: 12px; }
.btn {
  display: inline-block;
  font-weight: 700;
  text-decoration: none;
  padding: 13px 22px;
  border-radius: 12px;
  background: var(--btn-bg);
  color: var(--btn-text);
  box-shadow: 0 6px 16px -6px rgba(var(--glow), 0.6);
}
.btn:hover { filter: brightness(1.07); }

/* Work with me / licensing */
.work {
  margin-top: 64px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 30px 28px;
  display: grid;
  gap: 16px;
  box-shadow: 0 1px 2px rgba(29, 24, 32, 0.05), 0 12px 32px rgba(29, 24, 32, 0.06);
}
.work p { max-width: 62ch; }
.work .points li::before { background: var(--ink); }
.work .btn { background: var(--ink); color: #ffffff; box-shadow: 0 6px 16px -6px rgba(29, 24, 32, 0.5); }
.fit { display: grid; gap: 16px; grid-template-columns: 1fr; }
@media (min-width: 720px) { .fit { grid-template-columns: 1fr 1fr; } }
.fit-card { border-radius: 14px; padding: 18px 20px; background: var(--bg); border-top: 4px solid var(--accent); }
.fit-card h3 { font-family: var(--display); font-weight: 800; font-size: 1.2rem; margin: 0 0 10px; color: var(--ink); }

footer {
  margin-top: 56px;
  padding-top: 22px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 0.95rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 10px;
}
footer a { color: var(--ink); font-weight: 700; }

@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
"""


def esc(text):
    """Escape plain text. Fields marked as HTML in games.json are inserted as-is."""
    return html.escape(text, quote=True)


def card(game):
    classes = "card dark" if game["dark"] else "card"
    style = (
        f"--card-bg:{game.get('cardBg', '#0f0426')};--panel-bg:{game.get('panelBg', '#1a1030')};"
        f"--art-bg:{game.get('artBg', '#0f0426')};"
        f"--accent:{game['accent']};--accent-text:{game['accentText']};"
        f"--accent-soft:{game['accentSoft']};--glow:{game['glow']};"
        f"--btn-bg:{game['button']['background']};--btn-text:{game['button']['text']};"
    )
    points = "\n".join(f"          <li>{p}</li>" for p in game["points"])
    facts = "\n".join(
        f"          <div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in game["facts"]
    )
    return f"""    <article class="{classes}" data-game="{esc(game['id'])}" style="{style}">
      <figure class="art">
        <img src="{esc(game['banner'])}" alt="{esc(game['bannerAlt'])}">
      </figure>
      <div class="body">
        <span class="status">{esc(game['status'])}</span>
        <h2>{esc(game['name'])}</h2>
        <p class="hook">{game['hook']}</p>
        <p>{game['body']}</p>
        <ul class="points">
{points}
        </ul>
        <dl class="facts">
{facts}
        </dl>
        <div class="actions">
          <a class="btn" href="{esc(game['cta']['url'])}">{esc(game['cta']['label'])}</a>
        </div>
      </div>
    </article>
"""


def fit_card(game):
    style = f"--accent:{game['accent']};"
    items = "\n".join(f"          <li>{esc(i)}</li>" for i in game["suits"]["items"])
    return f"""      <div class="fit-card" style="{style}">
        <h3>{game['suits']['title']}</h3>
        <ul class="points">
{items}
        </ul>
      </div>
"""


def build():
    h = site["heading"]
    lic = site["licensing"]
    foot = site["footer"]
    cards = "\n".join(card(g) for g in data["games"])
    fits = "".join(fit_card(g) for g in data["games"])
    subject = html.escape(lic["emailSubject"]).replace(" ", "%20")

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(site['title'])}</title>
<meta name="description" content="{esc(site['description'])}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<main>
  <header>
    <h1>{esc(h['lead'])} <span class="accent">{esc(h['accent'])}</span> {esc(h['tail'])}</h1>
    <p>{site['intro']}</p>
  </header>

  <section class="games" aria-label="Games">

{cards}
  </section>

  <section class="work" aria-labelledby="work-title">
    <h2 class="section" id="work-title">{esc(lic['title'])}</h2>
    <p>{lic['intro']}</p>
    <div class="fit">
{fits}    </div>
    <p>{lic['closing']}</p>
    <div class="actions">
      <a class="btn" href="mailto:{esc(lic['email'])}?subject={subject}">{esc(lic['buttonLabel'])}</a>
    </div>
  </section>

  <footer>
    <span>Portfolio by <a href="{esc(foot['linkedin'])}">{esc(foot['name'])}</a></span>
    <span>{esc(foot['note'])}</span>
  </footer>
</main>
</body>
</html>
"""


if __name__ == "__main__":
    (ROOT / "index.html").write_text(build(), encoding="utf-8")
    print("Wrote index.html")
