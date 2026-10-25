# 생성형 AI로 PPT 만들기 — 매일 10분 시리즈 자동 게시

매일 아침 08:00(KST)에 GitHub Actions가 **다음 편을 골라 승인 요청**을 보냅니다.
편집이 끝난 영상은 미리 **비공개로 YouTube 재생목록에 업로드**되어 있고, 승인(Approve)하면 그 편이 **공개로 전환**되며, `episodes.json`에 게시 기록이 남습니다.

```
[매일 08:00 cron] → prepare(다음 편 선택·미리보기) → ⏸ 승인 대기(youtube-publish 환경)
                                                     ├─ Approve → publish(zernio→YouTube) → episodes.json 갱신
                                                     └─ Reject  → 오늘 건너뜀(다음날 같은 편 재요청)
```

## 클론해야 하나요?
**아니요.** 이 저장소를 GitHub에 한 번 올려 두면 Actions가 GitHub 서버에서 매일 돕니다. PC가 꺼져 있어도 됩니다.
제목·순서를 고치고 싶으면 GitHub 웹에서 `episodes.json`을 바로 편집하면 됩니다.

## 구성
| 경로 | 역할 |
|---|---|
| `.github/workflows/daily-episode.yml` | 매일 스케줄 + 수동 실행(편 번호 지정 가능) |
| `episodes.json` | 편 목록·제목·설명·태그·상태(`ready`/`published`) |
| `thumbnails/epXX.jpg` | 썸네일 (1280×720) |
| YouTube 재생목록 `PLfvfRjza5HL0` | 비공개로 미리 올라간 편들 (영상 파일은 GitHub에 없음) |
| `tools/upload_private.py` | 새 편을 비공개 업로드할 때 쓰는 도구 |
| `scripts/` | 다음 편 선택 · 미리보기 · 게시 |

## 1회 설정 (약 5분)
1. **Secrets** (Settings → Secrets and variables → Actions → *New repository secret*)
   - `ZERNIO_API_KEY` : 기존 `.env.txt` 의 값
2. **승인 게이트** (Settings → Environments → *New environment* → 이름 `youtube-publish`)
   - **Required reviewers** 체크 → 본인 계정 추가 → Save
   - (선택) *Deployment branches* 를 `main` 으로 제한
3. **Variables** (선택): `YT_VISIBILITY` (기본 `public`, 시험 시 `unlisted`)
4. GitHub 모바일 앱 알림을 켜 두면 "Review pending deployment" 알림에서 바로 승인할 수 있습니다.

## 매일 하는 일
알림 → Actions 실행 화면의 요약(제목·썸네일·설명) 확인 → **Review deployments → Approve and deploy**.

## 수동 실행
Actions → `daily-episode` → *Run workflow* → `episode` 칸에 번호(예: `5`) 입력 시 해당 편을 바로 승인 요청.
같은 날 이미 게시했으면 스케줄 실행은 자동으로 건너뜁니다.

## 주의
- zernio로 이미 게시된 글은 API로 삭제되지 않습니다. 잘못 올라간 편은 YouTube Studio에서 직접 정리하세요.
- 게시는 `Idempotency-Key`(편별 고정)로 24시간 내 재시도 시 중복 업로드를 막습니다.
