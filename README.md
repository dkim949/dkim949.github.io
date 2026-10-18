# Dongin Kim — personal notebook

[공개 사이트](https://dkim949.github.io/) · [기록하는 방법](docs/writing.md) · [릴리즈](docs/releases.md) · [변경 이력](CHANGELOG.md)

한 문장도 자연스럽게 남길 수 있는 개인 기록장입니다. Jekyll 3.10과 기존 GitHub Pages를 사용합니다.

## 시작하기

Python 3.9 이상에서 추가 package 없이 draft를 만듭니다. 아래 문장은 사용법 예시입니다.

```sh
python3 scripts/note.py new '오늘은 작은 아이디어를 하나 시험했다.'
```

명령이 출력한 파일을 확인하고 `publish`하면 공개용 `_notes/` 파일이 생깁니다. 온라인 반영은 별도 Git/Pages 배포 과정입니다. [Obsidian 메모 한 개 가져오기](docs/writing.md)도 지원합니다.

## 구조

- `_notes/`: 공개를 명시한 짧은 기록. 실제 첫 게시 때 생성됩니다.
- `.local/notes/`: 비공개 draft. Git과 build에서 제외합니다.
- `works/`, `blog/`: 기존 프로젝트 5개와 글 4개. 기존 URL을 유지합니다.
- `_data/`: 프로젝트와 글 목록.
- `_layouts/`, `_includes/`, `assets/css/notebook.css`: 화면과 ASCII 도형.
- `about.md`: 프로필.
- `scripts/`, `tests/`, `docs/`: 게시 도구, 검사, 사용법. 사이트에는 포함하지 않습니다.

## 로컬 확인

Ruby와 Jekyll이 설치된 환경에서:

```sh
python3 -B -m unittest discover -s tests
JEKYLL_NO_BUNDLER_REQUIRE=true jekyll build --strict_front_matter
python3 -B scripts/check_site.py _site
python3 -m http.server 8768 --bind 127.0.0.1 --directory _site
```

이 작업 환경에서는 승인받아 gem을 `vendor/gems/`에 설치했습니다. 해당 환경에서:

```sh
export GEM_HOME="$PWD/vendor/gems"
export GEM_PATH="$GEM_HOME"
export PATH="/opt/homebrew/Library/Homebrew/vendor/portable-ruby/3.4.8/bin:$GEM_HOME/bin:$PATH"
JEKYLL_NO_BUNDLER_REQUIRE=true ruby vendor/gems/bin/jekyll build --strict_front_matter
```

`vendor/`는 commit하거나 배포하지 않습니다. CI는 GitHub 공식 `actions/jekyll-build-pages`로 Pages 환경에서 빌드합니다. 기존 gemspec은 theme 배포용 legacy 파일이며 새 화면은 해당 theme의 CSS를 사용하지 않습니다.

## 디자인 출처

Moon의 여백과 정돈된 목록, Tessel의 단순한 도형, Son Daven의 ASCII 질감을 참고했습니다. 레이아웃과 ASCII 도형은 이 사이트용으로 작성했으며 유료 template 코드나 asset은 사용하지 않았습니다. 이전 도안은 별도 `personal-site` 준비 폴더에 보관합니다.
