# 한 문장 기록하기

제목, 요약, 이미지, 교훈 없이 한 문장으로 끝내도 됩니다. 아래 문장은 사용법을 위한 예시입니다. CLI에는 Python 3.9 이상이 필요하며 추가 package는 없습니다.

저장소 root에서 실행합니다.

```sh
python3 scripts/note.py new '오늘은 작은 아이디어를 하나 시험했다.'
```

출력되는 `.local/notes/note-….md`가 비공개 draft입니다. 편집기로 내용을 바꿀 수 있습니다. 공개하기로 정한 draft의 **출력 경로를 그대로** 다음 명령에 전달합니다.

```sh
python3 scripts/note.py publish .local/notes/note-실제파일이름.md
```

`publish`는 `_notes/`에 공개용 Markdown를 만들며 원본 draft를 남깁니다. 이 명령은 Git commit, push, 원격 배포를 실행하지 않습니다. 파일이 생겼다고 온라인에 올라간 것은 아닙니다. 실제 사이트 반영은 별도의 Git/배포 단계입니다.

제목이 필요할 때만 `new '본문' --title '선택 제목'`을 사용합니다. 이미 쓴 단일 Markdown에서 draft를 만들려면 `new --file '/선택한/파일.md'`를 사용합니다. 폴더나 vault를 검색하지 않습니다.

## Obsidian 메모 한 개 가져오기

공개할 메모의 앞부분에 아래와 같이 명시하고, 정확히 그 파일만 선택합니다.

```markdown
---
public: true
---
이전에는 X라고 생각했지만, 직접 해보니 Y가 더 맞았다.
```

```sh
python3 scripts/note.py import '/선택한/메모.md'
```

`import`는 정확한 `public: true`가 없으면 중단합니다. 원본은 수정하지 않습니다. `publish`는 이 CLI로 만든 draft에만 사용할 수 있습니다. `new --file`은 공개 허용 여부와 상관없이 비공개 draft를 만들 수 있으며, 공개하려면 다시 `publish`를 직접 실행해야 합니다.

원본 frontmatter에서는 `date`, `title`, `public`만 읽습니다. 공개 파일에는 정규화한 UTC `date`, 선택적 `title`, `published: true`, `render_with_liquid: false`만 씁니다. 원본 경로·태그·그 외 metadata는 복사하지 않습니다. 본문은 직접 확인한 그대로 가져오므로 공개하기 어려운 내용은 먼저 제거합니다.

`date`가 없으면 가져온 시각을 기록합니다. 원래 작성일이나 과거 공개일을 추정하지 않습니다. `date: 2026-10-18`은 해당 날짜 00:00 UTC로 해석하고, timestamp에는 `Z` 또는 `+02:00` 같은 UTC offset이 필요합니다.

## 지원 범위

이 CLI는 범용 YAML parser가 아닙니다. 맨 위 `---` 사이의 top-level `date`, `title`, `public` 한 줄만 읽습니다. 날짜와 제목은 단순 한 줄 문자열, YAML single quote, JSON 방식 double quote를 지원합니다. `public`은 따옴표나 주석 없는 소문자 `true`만 허용합니다. 여러 줄 title/date, YAML anchor, tag, 중복된 허용 key는 거절합니다. 나머지 metadata는 통째로 버립니다.

첫 버전은 일반 Markdown 텍스트와 `https://`, `http://`, `mailto:`, `#` 링크만 지원합니다. 이미지, `[[wikilink]]`, 상대 파일 링크, 로컬 파일 경로, raw HTML, Obsidian comment, `{: ...}` 형태의 Kramdown attribute list는 게시할 때 명시적 오류를 냅니다. 첨부파일을 자동으로 찾거나 공개하지 않습니다. 이 제한은 code block 안에도 적용됩니다.

현재 Jekyll 3에서는 `render_with_liquid: false`가 보호 기능으로 작동하지 않으므로, `{{`와 `{%`가 있는 제목·본문은 게시를 거절합니다. `_notes/`를 직접 편집할 때도 이 토큰을 넣지 않습니다.

## 수정과 중복

한 source 파일은 절대 경로에서 계산한 ID를 사용하므로 같은 경로를 다시 가져와도 새 공개 기록을 만들지 않습니다. ID에는 원본 경로 문자열이 들어가지 않습니다. 파일을 옮기거나 이름을 바꾸면 별도 source로 인식하므로, 기존 공개본이 있다면 다시 import하지 않습니다. `new '문장'`은 실행할 때마다 별개의 draft를 만듭니다.

이미 파일이 있으면 모든 명령이 오류로 끝나며 덮어쓰지 않습니다. 이미 공개한 내용을 수정할 때는 해당 `_notes/파일.md`를 편집기로 직접 수정하고, 이후 별도의 Git/배포 단계를 진행합니다. 단순 문장 교정이면 같은 파일을 고치고, 생각이 바뀐 자취를 남기려면 `new`로 새 기록을 작성합니다. draft를 바꾼 뒤 `publish`를 다시 실행해도 기존 공개본은 바뀌지 않습니다.

수동 편집 시 `published`는 반드시 따옴표 없는 boolean `true` 또는 `false`로 씁니다. `published: "false"`처럼 문자열로 쓰면 Jekyll 3가 공개 대상으로 해석합니다.

검증은 실제 vault나 공개 기록을 건드리지 않는 임시 디렉터리에서 실행합니다.

```sh
python3 -B -m unittest discover -s tests -p 'test_note.py'
```
