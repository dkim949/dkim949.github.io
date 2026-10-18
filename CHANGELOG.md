# Changelog

사이트 기능과 디자인의 의미 있는 변경을 기록합니다. 짧은 기록이나 글을 추가할 때마다 version을 올리지는 않습니다.

## Unreleased

- Obsidian·프롬프트·현재 대화를 짧은 기록으로 작성하는 project-local `write-site-note` skill 추가.
- AGENTS.md·CLAUDE.md에서 같은 작성 기준 연결. 비공개 draft, 공개용 source, 실제 배포 상태 구분.
- Agent skill 디렉터리를 Pages build 제외 목록과 output 검사에 명시.

## 0.2.0 — 2026-10-18

- 현재 구조와 ASCII 도형을 유지하면서 cream·coral·serif theme 적용.
- 한글 serif 제목, 기존 sans 본문, 어두운 코드 블록. 작은 링크는 대비를 위해 짙은 coral 사용.
- 준비 폴더를 `studio/`로 통합하고 이전 두 도안과 새 theme 비교 화면 제공.
- 사용자 제공 디자인 원문을 `studio/references/DESIGN-claude.md`로 이동.
- 프로젝트의 목적·독자·방문 행동·디자인 기준을 AGENTS.md, DESIGN.md, studio/brief.md에 정리.
- 이전 Astro repository와 이관 snapshot은 `.local/archive/`에 Git 이력과 함께 보관. 로컬 전용이며 원격에 올리지 않음.
- studio와 디자인 문서를 공개 build에서 제외하고 기존 output 검사에 추가.

검증: Jekyll build, 14 HTML 페이지의 내부 링크·asset·XML·공개 제외 검사, desktop·390px·320px 화면, 본문·보조 글씨·링크·코드 색상 대비, 팀 critique.

## 0.1.0 — 2026-10-18

- 넓은 여백, 한 가지 olive 색, ASCII 도형을 사용하는 개인 기록장 화면.
- 기존 프로젝트 5개와 글 4개의 `.html` 주소 유지, Berlin 프로필 반영.
- 제목 없는 짧은 Markdown 기록, 개별 permalink, RSS와 sitemap.
- 로컬 비공개 draft와 선택한 Obsidian 메모 한 개의 명시적 공개 도구.
- 공개 기본값은 false. 샘플 기록을 실제 활동처럼 게시하지 않음.
- 기존 글의 시리즈 링크와 미완성 chart 문구 정리.
- 사이트에서 운영 alert screenshot 제외. 원본 source와 Git 이력은 유지.
- Pages build 및 게시 도구 검사 CI, branch/PR/release 절차 문서화.

검증: Python tests 12개, Jekyll 3.10 build, HTML 페이지 14개의 내부 링크·asset·XML 검사, 공개 경계 integration build, desktop·390px·320px 화면 검사.

릴리즈 tag: `v0.1.0`. 실제 배포 상태는 GitHub Pages workflow에서 확인합니다.
