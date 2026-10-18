# Warm editorial notebook

넓은 여백과 ASCII 기하학 위에 따뜻한 종이색, serif 제목, coral 디테일을 얹는다. 사용자 제공 [원본 분석 문서](studio/references/DESIGN-claude.md)의 시각 요소를 개인 기록장에 맞게 적용했다.

## 레퍼런스의 역할

| 자료 | 적용하는 요소 |
| --- | --- |
| Moon | 넓은 여백, 간결한 글 목록 |
| Tessel | 단순한 기하학 도형 |
| Son Daven | ASCII 질감과 monospace 보조 정보 |
| DESIGN-claude.md | cream·coral 색, serif/sans 대비, 어두운 코드 표면 |

현재 섹션 순서는 소개와 ASCII → 작은 기록 → 기존 프로젝트 → footer다. 메뉴와 콘텐츠 배치는 유지한다. 제품 소개용 pricing, 후기, 문의 form, 큰 CTA는 이 사이트의 목적에 맞지 않아 추가하지 않는다.

## Tokens

| 용도 | 값 |
| --- | --- |
| Canvas | `#faf9f5` |
| 제목 | `#141413` |
| 본문 | `#3d3d3a` |
| 보조 텍스트 | `#6c6a64` |
| 구분선 | `#e6dfd8` |
| ASCII·장식 coral | `#cc785c` |
| 링크·선택·focus coral | `#a9583e` |
| 부드러운 표면 | `#f5f0e8` |
| 코드 배경 / 글자 | `#181715` / `#faf9f5` |

원본의 밝은 coral은 작은 본문 링크에 대비가 부족하여 더 짙은 active 색을 사용한다. source 문서의 모든 component를 강제로 가져오지 않는다.

## Typography and spacing

- 제목: Noto Serif KR 400, serif fallback. 원본에 언급된 유료 font 파일을 복제하지 않는다.
- 본문: 기존 Pretendard. ASCII와 날짜: 기존 IBM Plex Mono.
- hero 제목: desktop 최대 46px, mobile 28px, 좁은 mobile 25px.
- 현재 container·grid·breakpoint 유지. hero 여백은 desktop 88px, tablet 64px, mobile 52px.
- 본문은 밝은 canvas, 코드만 어두운 charcoal로 읽기 구분을 준다.
- 새 animation이나 icon library를 추가하지 않는다. 기존 focus와 reduced-motion 동작을 유지한다.

## Files

`assets/css/notebook.css`가 구조를, `assets/css/editorial.css`가 색·font·간격·표면을 담당한다. theme CSS를 제거하면 기존 olive 스타일로 돌아갈 수 있다. `_includes/head.html`에서 web font와 theme CSS를 연결한다.

## Review decisions

1. 원본은 Claude 마케팅 사이트의 분석 문서이므로 brand logo, 제품 component, license font 지시를 그대로 적용하지 않는다.
2. 문서에 쓰인 'navy'라는 표현보다 실제 token `#181715`에 맞춰 따뜻한 charcoal로 해석한다.
3. 재료와 미확정 도안은 공개 사이트 밖에 둔다. 이전 repo는 `.git`까지 로컬 archive에 이동해 복구 가능성을 보존한다.
4. 전체 구조 변경보다 작은 theme layer를 선택했다. 기존 주소·기록 도구의 회귀 위험을 줄이고 취향 비교를 쉽게 하기 위해서다.
