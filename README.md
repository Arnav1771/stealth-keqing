# Stealth Keqing

One page listing every app, with one signup: pick the apps you care about and get an email when
they ship something. Live at https://arnav1771.github.io/stealth-keqing/

- **Add or change an app:** edit `apps.json` (slug, name, status `live` / `beta` / `soon`, url, one line).
- **Link from an app:** `https://arnav1771.github.io/stealth-keqing/?app=<slug>` preselects it
  (`?app=pinfiles,fahh` for several).
- **Turn on signups (once):** create a free [Kit](https://kit.com) account, one form, and one tag per
  app slug. Put the form id and tag ids in `config.json` (public values, not secrets) and push.
  Until then the page says signups open soon. Turn on double opt-in in the Kit form settings, and set a postal address in Kit (every email must carry one).
- **Send an update:** write a broadcast in Kit and filter by the app's tag.

Build and test locally: `python3 -m unittest scripts/test_build.py && python3 scripts/build.py`
(writes `site/`). Pushing to `main` deploys `site/` to the `gh-pages` branch.
