# 작업 폴더 통합 — 2026-10-18

앞으로 **`~/git/dkim949.github.io/` 하나**에서 작업한다. remote repository와 hosting은 그대로다.

| 이전 위치 | 현재 위치 | 용도 |
| --- | --- | --- |
| `~/git/dkim949.github.io/` | 동일 | 사이트 코드·콘텐츠·Git·배포 |
| `~/git/personal/personal-site/` | `studio/` | 도안·레퍼런스·현재 brief |
| `~/git/personal-website/` | `.local/archive/personal-website-astro/` | 이전 Astro 시도 전체, `.git` 포함 |
| `~/git/DESIGN-claude.md` | `studio/references/DESIGN-claude.md` | 다운로드한 원문, 내용 보존 |
| 이전 준비 폴더의 `migration/` | `.local/archive/migration-2026-10-18/` | 이관 당시 원본 snapshot |

기존 폴더를 그대로 rename/move하여 같은 inode인지 확인했다. 파일 내용을 재구성하거나 Git 이력을 합치지 않았다. 원본 도안 두 개와 다운로드 문서는 checksum도 확인했다. 실제 기록·프로필의 유지보수는 운영 source에서만 한다.

`studio/`는 Pages build에서 제외한다. `.local/archive/`는 Git에도 포함하지 않는 이 컴퓨터의 로컬 보관소다. 이 archive는 원격 backup이 아니다. 로컬 이동 기록은 `.local/archive/consolidation-2026-10-18.json`에 있다. 이전 폴더의 README·brief도 같은 archive에 보존했다.

## 복구

이전 Astro 작업을 다시 이어가려면 `.local/archive/personal-website-astro/`를 원하는 새 경로로 이동하면 된다. `.git`, dependency, source 모두 보존되어 있다. 현재 사이트를 바꾸는 작업은 이 archive에서 하지 않는다.

이전 도안 URL은 port 8767을 그대로 사용하며 서버의 root를 `studio/design/`으로 갱신했다. 실제 사이트의 로컬 build는 `_site/`, 미리보기는 port 8768이다.
