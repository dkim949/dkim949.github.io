# 버전과 릴리즈

`main`은 GitHub Pages가 자동으로 공개하는 branch입니다. 기능 변경은 짧게 유지하는 feature branch에서 만들고 PR의 검사와 화면을 확인한 뒤 합칩니다. 기존 Pages의 `main` / root 설정을 유지합니다.

## 변경 기록

- `CHANGELOG.md`: 사용자에게 보이는 변화와 검증 내용을 기록합니다.
- `VERSION`: 이 source의 version. 현재는 `0.1.0`입니다.
- `vMAJOR.MINOR.PATCH` tag / GitHub Release: 사이트 배포를 확인한 commit에 붙입니다.
- 작은 기능은 MINOR, 수정은 PATCH. 글이나 기록 추가는 보통 일반 commit만 남깁니다.

## 공개 순서

1. feature branch에서 구현하고 로컬 build 및 note tests를 실행합니다.
2. PR의 Site checks와 실제 desktop/mobile 화면을 확인합니다.
3. `main`에 합치면 기존 Pages workflow가 사이트를 갱신합니다.
4. 공개 URL과 Pages build 성공을 확인한 뒤 changelog의 version과 날짜로 release를 만듭니다.

태그가 배포를 실행하지는 않습니다. 문제가 생기면 해당 변경을 되돌리는 새 commit을 main에 반영합니다. Git history를 강제로 다시 쓰지 않습니다.

## 유지하기 위한 결정

- 기존 Jekyll 3.10과 Pages를 유지해 새 framework, Node dependency, hosting 계정을 추가하지 않았습니다.
- Jekyll 3에서는 `render_with_liquid: false`가 작동하지 않습니다. 게시 도구는 Liquid 시작 토큰을 거절합니다.
- `_notes`는 `published: true`를 명시해야 공개됩니다. 목록, RSS, sitemap에서도 공개 여부와 날짜를 검사합니다.
- Jekyll 3는 `published: "false"`도 truthy로 취급합니다. 공통 layout에도 정확한 boolean true 검사를 두어 잘못된 metadata의 본문과 SEO 내용이 출력되지 않게 합니다.
- `.local/`은 Git과 build 모두에서 제외합니다. 공개 repository에 commit한 내용은 사이트에 보이지 않아도 공개입니다.
- 미래 날짜는 다음 build에서 반영될 수 있습니다. 예약 시각에 build를 실행하는 scheduler는 없습니다.
- 옛 글의 작성일은 추측하지 않습니다. 실제 기록이 없을 때는 정직한 빈 상태를 보여줍니다.
- 외부 메모는 한 파일씩 선택하며 원본을 바꾸지 않습니다. 전체 vault 동기화는 아직 구현하지 않았습니다.

이 항목들은 구현 전후 critique에서 확인한 유지보수와 게시 경계에 대한 결정입니다.
