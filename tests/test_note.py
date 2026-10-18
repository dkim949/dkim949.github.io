"""Publication-boundary tests; all note content is synthetic test data."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


module_path = Path(__file__).resolve().parents[1] / "scripts" / "note.py"
spec = importlib.util.spec_from_file_location("note_cli", module_path)
note_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(note_cli)


class NoteCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = (Path(self.temp_dir.name) / "site").resolve()
        self.root.mkdir()
        self.source = Path(self.temp_dir.name) / "external.md"

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        """Run against a temporary repository and capture console output."""
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = note_cli.main(list(args), root=self.root)
        return code, stdout.getvalue().strip(), stderr.getvalue()

    def test_unicode_sentence_stays_private_until_selected(self) -> None:
        code, output, error = self.run_cli("new", "오늘은 한 문장만 남겼다.")
        self.assertEqual((code, error), (0, ""))
        draft = Path(output)
        self.assertEqual(draft.parent, self.root / ".local" / "notes")
        self.assertIn("published: false", draft.read_text())
        self.assertFalse((self.root / "_notes").exists())
        code, output, error = self.run_cli("publish", str(draft))
        self.assertEqual((code, error), (0, ""))
        public = Path(output)
        self.assertEqual(public.name, draft.name)
        self.assertIn("오늘은 한 문장만 남겼다.", public.read_text())
        self.assertIn("published: true", public.read_text())
        self.assertTrue(draft.exists())

    def test_import_requires_exact_opt_in(self) -> None:
        for metadata in ("", "public: false", 'public: "true"', "public: True", "nested:\n  public: true"):
            with self.subTest(metadata=metadata):
                self.source.write_text(f"---\n{metadata}\n---\nA synthetic note.\n")
                code, _, error = self.run_cli("import", str(self.source))
                self.assertEqual(code, 2)
                self.assertIn("public: true", error)
        self.assertFalse((self.root / "_notes").exists())

    def test_import_strips_metadata_and_keeps_safe_title_and_date(self) -> None:
        title = json.dumps('한 줄: "생각"', ensure_ascii=False)
        self.source.write_text(f'---\npublic: true\ndate: 2026-10-18T12:00:00+02:00\ntitle: {title}\nprivate_path: /Users/example/private\nlayout: unsafe\nsecret:\n  value: synthetic-secret\n---\nA short note.\n')
        code, output, error = self.run_cli("import", str(self.source))
        self.assertEqual((code, error), (0, ""))
        content = Path(output).read_text()
        self.assertIn('date: "2026-10-18T10:00:00Z"', content)
        self.assertIn("render_with_liquid: false", content)
        self.assertNotIn("secret", content)
        self.assertNotIn("/Users/", content)
        self.assertNotIn("layout:", content)
        metadata, _ = note_cli._parse_note(content)
        self.assertEqual(metadata["title"], '한 줄: "생각"')

    def test_undated_import_uses_current_time(self) -> None:
        self.source.write_text("---\npublic: true\n---\nA synthetic note.")
        before = datetime.now(timezone.utc).replace(microsecond=0)
        code, output, _ = self.run_cli("import", str(self.source))
        self.assertEqual(code, 0)
        metadata, _ = note_cli._parse_note(Path(output).read_text())
        timestamp = datetime.fromisoformat(metadata["date"].replace("Z", "+00:00"))
        self.assertGreaterEqual(timestamp, before)
        self.assertLessEqual(timestamp, datetime.now(timezone.utc))

    def test_repeat_import_never_overwrites_changed_source(self) -> None:
        self.source.write_text("---\npublic: true\n---\nFirst synthetic thought.")
        code, output, _ = self.run_cli("import", str(self.source))
        self.assertEqual(code, 0)
        original = Path(output).read_text()
        self.source.write_text("---\npublic: true\n---\nChanged synthetic thought.")
        code, _, error = self.run_cli("import", str(self.source))
        self.assertEqual(code, 2)
        self.assertIn("Already exists", error)
        self.assertEqual(Path(output).read_text(), original)
        self.assertEqual(len(list((self.root / "_notes").glob("*.md"))), 1)

    def test_file_draft_and_publish_share_stable_destination(self) -> None:
        self.source.write_text("---\npublic: true\n---\nSynthetic source.")
        code, draft, _ = self.run_cli("new", "--file", str(self.source))
        self.assertEqual(code, 0)
        self.assertEqual(self.run_cli("new", "--file", str(self.source))[0], 2)
        self.assertEqual(self.run_cli("publish", draft)[0], 0)
        self.assertEqual(self.run_cli("publish", draft)[0], 2)
        self.assertEqual(self.run_cli("import", str(self.source))[0], 2)

    def test_external_publish_cannot_bypass_import_opt_in(self) -> None:
        self.source.write_text("A private synthetic note.")
        code, _, error = self.run_cli("publish", str(self.source))
        self.assertEqual(code, 2)
        self.assertIn("use import", error)

    def test_unsupported_markup_and_local_links_stop_publication(self) -> None:
        for body in (
            "[[private note]]",
            "![picture](https://example.com/a.png)",
            "[note](../private.md)",
            "[private](/Users/example/a.md)",
            "[private](file:///tmp/a.md)",
            "[private][x]\n\n[x]: ../a.md",
            "[private][x]\n\n[x]:\n  ../a.md",
            '<a href="/tmp/a.md">file</a>',
            "<vscode://file/tmp/private.md>",
            "{{ site.data.secret }}",
            "{% include secret %}",
            "%%private comment%%",
        ):
            with self.subTest(body=body):
                self.source.write_text(f"---\npublic: true\n---\n{body}")
                self.assertEqual(self.run_cli("import", str(self.source))[0], 2)
        self.assertFalse((self.root / "_notes").exists())

    def test_public_web_links_are_supported(self) -> None:
        self.source.write_text("---\npublic: true\n---\n[Read](https://example.com/a) [Mail](mailto:hello@example.com) [Here](#section)\n\n<https://example.com>")
        self.assertEqual(self.run_cli("import", str(self.source))[0], 0)

    def test_kramdown_attributes_cannot_replace_a_public_link(self) -> None:
        body = '[example](https://example.com){: href="/tmp/private.md"}'
        self.source.write_text(f"---\npublic: true\n---\n{body}")
        code, _, error = self.run_cli("import", str(self.source))
        self.assertEqual(code, 2)
        self.assertIn("Kramdown attribute lists", error)
        code, draft, _ = self.run_cli("new", body)
        self.assertEqual(code, 0)
        self.assertEqual(self.run_cli("publish", draft)[0], 2)
        self.assertFalse((self.root / "_notes").exists())

    def test_title_cannot_inject_frontmatter_or_liquid(self) -> None:
        self.assertEqual(self.run_cli("new", "A synthetic note.", "--title", "a\npublished: true")[0], 2)
        code, draft, _ = self.run_cli("new", "A synthetic note.", "--title", "{{ site.title }}")
        self.assertEqual(code, 0)
        self.assertEqual(self.run_cli("publish", draft)[0], 2)
        self.assertFalse((self.root / "_notes").exists())

    def test_invalid_frontmatter_and_empty_notes_are_rejected(self) -> None:
        for text in (
            "",
            "---\npublic: true",
            "---\npublic: true\npublic: true\n---\nText",
            "---\npublic: true\ntitle: |\n  multiline\n---\nText",
            "---\npublic: true\ndate: invalid\n---\nText",
            "---\npublic: true\ndate: 2026-10-18T12:00:00\n---\nText",
        ):
            with self.subTest(text=text):
                self.source.write_text(text)
                self.assertEqual(self.run_cli("import", str(self.source))[0], 2)
        self.assertFalse((self.root / "_notes").exists())


if __name__ == "__main__":
    unittest.main()
