#!/usr/bin/env python3
"""Check a built site for broken local links and unintended source publication."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as element_tree


class LinkParser(HTMLParser):
    """Collect local link and resource targets from rendered HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Collect URL attributes, ignoring empty values."""
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.targets.append(value)


def check_site(site: Path) -> list[str]:
    """Validate generated pages and return actionable errors.

    Args:
        site: Jekyll output directory.

    Returns:
        Missing routes, broken links, or excluded source files found in output.
    """
    errors: list[str] = []
    required = ["index.html", "about/index.html", "works/index.html", "blog/index.html", "404.html"]
    source = Path(__file__).resolve().parent.parent
    required += [str(item.relative_to(source).with_suffix(".html")) for directory in ("works", "blog") for item in (source / directory).glob("*.md")]
    for name in required:
        if not (site / name).is_file():
            errors.append(f"Missing route: {name}")
    for name in (".local", "vendor", "scripts", "tests", "docs", "README.md", "CLAUDE.md", "marketing_AB.csv", "marketing_AB.ipynb", "assets/images/anomaly_detection2.png"):
        if (site / name).exists():
            errors.append(f"Excluded source in build: {name}")
    for page in site.rglob("*.html"):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        page_url = "https://dkim949.github.io/" + page.relative_to(site).as_posix()
        for link in parser.targets:
            url = urlsplit(urljoin(page_url, link))
            if url.scheme not in {"http", "https"} or url.netloc != "dkim949.github.io":
                continue
            target = site / unquote(url.path).lstrip("/")
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{page.relative_to(site)}: missing {link}")
    for name in ("feed.xml", "sitemap.xml"):
        try:
            element_tree.parse(site / name)
        except (OSError, element_tree.ParseError) as error:
            errors.append(f"Invalid {name}: {error}")
    return errors


def main() -> int:
    """Report output validation and return a process exit code."""
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    errors = check_site(site)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Site checks passed: {len(list(site.rglob('*.html')))} HTML pages, local links, excluded files, RSS and sitemap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
