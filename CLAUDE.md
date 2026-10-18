# Repository guide

## Purpose

A minimal personal notebook hosted at https://dkim949.github.io using Jekyll 3.10 and GitHub Pages. The main branch is the live publication source.

Read AGENTS.md and DESIGN.md for the current project brief and visual decisions. This repository is the only active workspace; studio/ contains the old preparation project, and .local/archive/ preserves the previous Astro repository.

## Writing records

When the user asks to turn an Obsidian note, prompt, or conversation into a site record, read and follow [.agents/skills/write-site-note/SKILL.md](.agents/skills/write-site-note/SKILL.md). Claude Code also discovers it through `.claude/skills/write-site-note`, a relative symlink to the same skill. Keep editorial rules in that single source. Use the existing note tool and distinguish a private draft, a public source file, and a verified live publication.

## Structure

- `index.md` and `_layouts/home.html`: short notes and selected archived projects.
- `_notes/`: explicit public notes; defaults in `_config.yml` set published to false.
- `.local/notes/`: private drafts; never stage or publish this directory.
- `works/`, `blog/`: archived content; preserve existing .html URLs.
- `_data/`: lists of archived projects and articles.
- `_layouts/`, `_includes/`, `assets/css/notebook.css`: structural visual system; `assets/css/editorial.css` applies the current theme.
- `scripts/note.py`: explicit one-file publishing, with no vault scanning.
- `docs/writing.md`, `docs/releases.md`: writing and release workflows.
- `_sass/`, `assets/css/style.scss`, `plainwhite.gemspec`: legacy theme sources, not the active layout stylesheet.

## Verification

Follow README for the project-local Ruby environment. Run Python tests, Jekyll build, and scripts/check_site.py against _site. Verify desktop and mobile layout after visual changes.

Do not invent dates for old content or create example posts that look like the author's real activity. Jekyll 3 does not honor render_with_liquid: false; keep the note tool's Liquid checks. Public source commits are public even when a page is not rendered.

Update VERSION and CHANGELOG.md for meaningful site changes. Do not add AI attribution to commits.
