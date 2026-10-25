import json, sys, os
ep = sys.argv[1]
d = json.load(open("episodes.json", encoding="utf-8"))
e = next(x for x in d["episodes"] if x["id"] == ep)
repo = os.environ.get("GITHUB_REPOSITORY", "")
left = sum(1 for x in d["episodes"] if x.get("status") == "uploaded")
print(f"## 오늘 게시 후보: {e['no']}편 / 전체 {len(d['episodes'])}편 (남은 편 {left})\n")
print(f"**제목**: {e['title']}\n")
print(f"**길이**: {e['duration']}  ·  **비공개 미리보기**: {e.get('youtube_url','')}\n")
print(f"![thumbnail](https://github.com/{repo}/raw/main/thumbnails/{ep}.jpg)\n")
print("**설명**\n\n```\n" + e["description"] + "\n```\n")
print("✅ 승인: 위쪽 *Review deployments* → `youtube-publish` 체크 → **Approve and deploy**\n")
print("⏭ 오늘 건너뛰기: **Reject** (다음날 같은 편이 다시 올라옵니다)")
