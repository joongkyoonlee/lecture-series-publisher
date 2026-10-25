"""zernio API 로 YouTube 에 업로드·게시하고 episodes.json 을 갱신한다."""
import json, os, sys, datetime, uuid, urllib.request

API = "https://zernio.com/api/v1"
KEY = os.environ["ZERNIO_API_KEY"]
ACC = os.environ["ZERNIO_YOUTUBE_ACCOUNT_ID"]


def call(method, path, body=None, headers=None):
    h = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    h.update(headers or {})
    req = urllib.request.Request(API + path, method=method, headers=h,
                                 data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.loads(r.read() or b"{}")


def upload(path, ctype):
    pre = call("POST", "/media/presign", {"filename": os.path.basename(path),
                                          "contentType": ctype, "size": os.path.getsize(path)})
    with open(path, "rb") as f:
        req = urllib.request.Request(pre["uploadUrl"], method="PUT", data=f,
                                     headers={"Content-Type": ctype,
                                              "Content-Length": str(os.path.getsize(path))})
        urllib.request.urlopen(req, timeout=1800).read()
    return pre["publicUrl"]


ep = sys.argv[1]
db = json.load(open("episodes.json", encoding="utf-8"))
e = next(x for x in db["episodes"] if x["id"] == ep)

video_url = upload(f"dist/{ep}.mp4", "video/mp4")
thumb_url = upload(f"thumbnails/{ep}.jpg", "image/jpeg")
yt = {"title": e["title"][:100], "visibility": os.environ.get("YT_VISIBILITY", "public"),
      "madeForKids": False, "categoryId": "27"}
if os.environ.get("YT_PLAYLIST_ID"):
    yt["playlistId"] = os.environ["YT_PLAYLIST_ID"]

res = call("POST", "/posts", {
    "content": e["description"],
    "mediaItems": [{"type": "video", "url": video_url, "thumbnail": thumb_url}],
    "platforms": [{"platform": "youtube", "accountId": ACC, "platformSpecificData": yt}],
    "tags": e.get("tags", []),
    "publishNow": True,
}, headers={"Idempotency-Key": f"{os.environ.get('GITHUB_REPOSITORY','')}-{ep}-{uuid.uuid5(uuid.NAMESPACE_URL, ep)}"})
post = res.get("post", res)
print(json.dumps(post, ensure_ascii=False)[:1500])

e["status"] = "uploaded"
e["uploaded_at"] = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
e["zernio_post_id"] = post.get("_id") or post.get("id")
for p in post.get("platforms", []):
    if p.get("platformPostUrl"):
        e["youtube_url"] = p["platformPostUrl"]
json.dump(db, open("episodes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("youtube:", e.get("youtube_url"))
