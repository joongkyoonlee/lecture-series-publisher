"""승인된 편을 비공개 → 공개로 전환한다 (zernio update-metadata)."""
import json, os, sys, datetime, urllib.request
API = "https://zernio.com/api/v1"
ep = sys.argv[1]
db = json.load(open("episodes.json", encoding="utf-8"))
e = next(x for x in db["episodes"] if x["id"] == ep)
body = {"platform": "youtube", "privacyStatus": os.environ.get("YT_VISIBILITY") or "public"}
req = urllib.request.Request(f"{API}/posts/{e['zernio_post_id']}/update-metadata", method="POST",
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {os.environ['ZERNIO_API_KEY'].strip()}", "Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as r:
    print(r.status, r.read()[:500])
e["status"] = "published"
e["published_at"] = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
json.dump(db, open("episodes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("공개 전환:", e.get("youtube_url"))
