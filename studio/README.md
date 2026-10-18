# 디자인 작업실

이 폴더는 **`dkim949.github.io` repository 안의 디자인 자료실**이다. 사이트 코드, 콘텐츠, 기록 도구는 바로 위 repository root에서 관리한다. 이전 `personal-site` 폴더의 자료를 이곳으로 이동했다.

- [현재 방향](brief.md)
- [현재 디자인 기준](../DESIGN.md)
- [시안 비교](design/compare.html): 기존 두 도안과 새 theme
- [레퍼런스 메모](references/notes.md)
- [사용자가 받은 디자인 원본](references/DESIGN-claude.md)
- `references/images/`: 앞으로 모을 도안 캡처
- `references/guides/`: 작업 방법을 설명하는 캡처. 로컬 전용

기존 두 도안의 날짜·기록은 가상 예시다. 새 theme 미리보기는 실제 사이트의 build snapshot이다. 도안은 공개 게시물이 아니며 이 폴더 전체를 Pages build에서 제외한다.

repository root에서 미리보기를 실행한다.

```sh
python3 -m http.server 8767 --bind 127.0.0.1 --directory studio/design
```

이전 이관 snapshot과 오래된 Astro repo는 `.local/archive/`에 보관한다. 상세 위치와 복구 방법은 [폴더 정리 기록](../docs/workspace.md)을 참고한다.
