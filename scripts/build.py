"""Build the Stealth Keqing hub into site/ from apps.json + config.json (stdlib only).

The page is complete static HTML, so the signup works with JavaScript off. hub.js only adds
?app=<slug> preselection.
"""
import datetime
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
HUB = "https://arnav1771.github.io/stealth-keqing/"
STATUS = {"live": "Out now", "beta": "In beta", "soon": "Coming soon"}


def human(day):
    d = datetime.date.fromisoformat(day)
    return f"{d.day} {d:%b %Y}"


def feed(apps):
    """Atom feed of every app's news, newest first: follow updates without giving anyone an email."""
    e = html.escape
    items = sorted(((n["date"], i, a, n) for a in apps for i, n in enumerate(a.get("news", []))),
                   key=lambda t: (t[0], -t[1]), reverse=True)
    newest = items[0][0] if items else "2026-10-01"
    entries = "".join(
        f'<entry><title>{e(a["name"])}: {e(n["text"])}</title>'
        f'<link href="{e(a["url"] or HUB + "#" + a["slug"])}"/>'
        f'<id>tag:arnav1771.github.io,{day}:{e(a["slug"])}-{i}</id>'
        f'<updated>{day}T00:00:00Z</updated><summary>{e(n["text"])}</summary></entry>'
        for day, i, a, n in items)
    return ('<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">'
            f'<title>Stealth Keqing updates</title><link href="{HUB}"/><link rel="self" href="{HUB}feed.xml"/>'
            f'<id>{HUB}</id><updated>{newest}T00:00:00Z</updated><author><name>Stealth Keqing</name></author>'
            f'{entries}</feed>\n')


def build():
    apps = json.loads((ROOT / "apps.json").read_text())
    kit = json.loads((ROOT / "config.json").read_text())["kit"]
    form_id, tags = kit.get("form_id", "").strip(), kit.get("tags", {})
    open_ = bool(form_id)
    e = html.escape

    toggles = "\n".join(
        f'<label class="pick"><input type="checkbox" name="tags[]" value="{e(tags.get(a["slug"], a["slug"]))}" '
        f'data-app="{e(a["slug"])}"><span>{e(a["name"])}</span></label>'
        for a in apps)
    def row(a):
        name = f'<a href="{e(a["url"])}">{e(a["name"])}</a>' if a["url"] else e(a["name"])
        new = a.get("news", [])
        latest = (f'<p class="new"><time datetime="{e(new[0]["date"])}">{human(new[0]["date"])}</time> '
                  f'{e(new[0]["text"])}</p>') if new else ""
        return (f'<li class="app" id="{e(a["slug"])}"><span class="state state-{e(a["status"])}">{STATUS[a["status"]]}</span>'
                f'<h3>{name}</h3><p>{e(a["line"])}</p>{latest}</li>')

    rows = "\n".join(row(a) for a in apps)
    action = f"https://app.kit.com/forms/{e(form_id)}/subscriptions" if open_ else ""
    submit = ('<button type="submit">Sign me up</button>' if open_ else
              '<button type="button" disabled>Signups open soon</button>')
    note = ("You'll get one email to confirm. After that, a short note when something you picked ships. "
            "Unsubscribe from any email in one click." if open_ else
            'The list isn\'t open yet. Follow the <a href="feed.xml">updates feed</a> in any reader until it is.')

    page = TEMPLATE.format(toggles=toggles, rows=rows, action=action, submit=submit, note=note,
                           method="post" if open_ else "get", count=len(apps))
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(page)
    (OUT / "feed.xml").write_text(feed(apps))
    for f in ("style.css", "hub.js"):
        shutil.copy(ROOT / f, OUT / f)
    (OUT / ".nojekyll").write_text("")
    return page


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Stealth Keqing</title>
<meta name="description" content="Small, local-first tools for developers. Pick the ones you care about and hear when they ship.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=Atkinson+Hyperlegible:wght@400;700&display=swap">
<link rel="stylesheet" href="style.css">
<link rel="alternate" type="application/atom+xml" title="Stealth Keqing updates" href="feed.xml">
</head>
<body>
<header class="top"><span class="mark" aria-hidden="true"></span><span>Stealth Keqing</span><a href="https://github.com/Arnav1771">GitHub</a></header>
<main>
<form class="ask" action="{action}" method="{method}">
  <h1>Tell me when
    <span class="picks">{toggles}</span>
    ship something new.</h1>
  <p class="send"><label for="email">Send it to</label>
    <input id="email" name="email_address" type="email" required autocomplete="email" placeholder="you@example.com">
    {submit}</p>
  <p class="fine">{note} At most one email a month per app you pick. No account needed, and every app runs on your own machine.</p>
  <p class="fine">Your email and the apps you picked are stored with Kit, the newsletter service. Reply to any email to have them deleted.</p>
</form>
<section class="log" aria-labelledby="log-h">
  <h2 id="log-h">Everything I make</h2>
  <p class="fine">Newest change under each one. <a href="feed.xml">Follow every update by feed</a>, no email needed.</p>
  <ul>{rows}</ul>
</section>
</main>
<footer><p>Made by Arnav, published as Stealth Keqing. Every tool runs on your own machine.</p></footer>
<script src="hub.js"></script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
    print("built", OUT / "index.html")
