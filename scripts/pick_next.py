"""다음 게시할 편을 고른다. 이미 오늘 게시했으면 건너뛴다."""
import json, os, sys, datetime
forced = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
eps = json.load(open("episodes.json", encoding="utf-8"))["episodes"]
today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()
pick = ""
if forced:
    pick = next((e["id"] for e in eps if e["id"] == forced or str(e["no"]) == forced), "")
elif not any((e.get("published_at") or "").startswith(today) for e in eps):
    pick = next((e["id"] for e in eps if e.get("status") == "uploaded"), "")
print(f"pick={pick or '(없음)'}")
with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"ep={pick}\n")
