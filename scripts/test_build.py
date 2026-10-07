"""python3 -m unittest scripts/test_build.py : the hub builds, stays closed without a Kit form, opens with one."""
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import build  # noqa: E402

APPS = json.loads((build.ROOT / "apps.json").read_text())


class BuildTest(unittest.TestCase):
    def render(self, kit):
        real = Path.read_text
        fake = lambda p, *a, **k: json.dumps({"kit": kit}) if p.name == "config.json" else real(p, *a, **k)
        with mock.patch.object(Path, "read_text", fake):
            return build.build()

    def test_closed_without_form_id(self):
        page = self.render({"form_id": "", "tags": {}})
        self.assertIn("Signups open soon", page)
        self.assertNotIn("app.kit.com", page)
        self.assertEqual(page.count('name="tags[]"'), len(APPS))
        self.assertIn('<button type="button" disabled>', page)  # only the button waits for Kit

    def test_open_with_form_id_and_tags(self):
        page = self.render({"form_id": "123", "tags": {"pinfiles": "999"}})
        self.assertIn('action="https://app.kit.com/forms/123/subscriptions" method="post"', page)
        self.assertIn('value="999" data-app="pinfiles"', page)
        self.assertIn('name="email_address"', page)

    def test_relative_assets_only(self):
        page = self.render({"form_id": "", "tags": {}})
        self.assertNotIn('href="/', page)
        self.assertNotIn('src="/', page)


if __name__ == "__main__":
    unittest.main()
