# Paste this whole file into a Pipedream "Python" code step (see SETUP.md, part B).
# Then connect your YouTube (Swirlverse) account in the step and set SECRET below.
# It downloads the video from GitHub, uploads it to YouTube (resumable, 8 MB chunks),
# sets the thumbnail, and answers the GitHub worker with the new video id.
import requests

SECRET = "PASTE_THE_SAME_RANDOM_TEXT_YOU_SAVE_AS_PD_SECRET"
CHUNK = 8 * 1024 * 1024  # multiple of 256 KB


def handler(pd: "pipedream"):
    ev = pd.steps["trigger"]["event"]
    body = ev.get("body") or {}
    if body.get("secret") != SECRET:
        pd.respond({"status": 403, "body": {"error": "bad secret"}})
        return
    tok = pd.inputs["youtube_data_api"]["$auth"]["oauth_access_token"]
    H = {"Authorization": "Bearer " + tok}

    meta = {
        "snippet": {"title": body["title"], "description": body.get("description", ""),
                    "tags": body.get("tags", []), "categoryId": str(body.get("category_id", "27")),
                    "defaultLanguage": "en", "defaultAudioLanguage": "en"},
        "status": {"privacyStatus": body.get("privacy", "public"), "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": False, "embeddable": True, "publicStatsViewable": True},
    }
    size = int(requests.head(body["video_url"], allow_redirects=True, timeout=30).headers["Content-Length"])
    r = requests.post("https://www.googleapis.com/upload/youtube/v3/videos",
                      params={"uploadType": "resumable", "part": "snippet,status", "notifySubscribers": "true"},
                      headers={**H, "Content-Type": "application/json; charset=UTF-8",
                               "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)},
                      json=meta, timeout=60)
    r.raise_for_status()
    session = r.headers["Location"]

    start, video = 0, None
    with requests.get(body["video_url"], stream=True, timeout=120) as dl:
        dl.raise_for_status()
        buf = b""
        for part in dl.iter_content(1024 * 1024):
            buf += part
            while len(buf) >= CHUNK or (buf and start + len(buf) == size):
                piece, buf = buf[:CHUNK], buf[CHUNK:]
                end = start + len(piece) - 1
                u = requests.put(session, data=piece, timeout=300,
                                 headers={**H, "Content-Range": f"bytes {start}-{end}/{size}"})
                if u.status_code in (200, 201):
                    video = u.json()
                elif u.status_code != 308:
                    pd.respond({"status": 502, "body": {"error": u.text[:300]}})
                    return
                start = end + 1
    if not video:
        pd.respond({"status": 502, "body": {"error": "upload did not finish"}})
        return

    vid, thumb = video["id"], "skipped"
    if body.get("thumb_url"):
        png = requests.get(body["thumb_url"], timeout=60).content
        t = requests.post("https://www.googleapis.com/upload/youtube/v3/thumbnails/set",
                          params={"videoId": vid, "uploadType": "media"},
                          headers={**H, "Content-Type": "image/png"}, data=png, timeout=120)
        thumb = "ok" if t.ok else t.text[:200]
    pd.respond({"status": 200, "body": {"video_id": vid,
                                        "privacy": video.get("status", {}).get("privacyStatus"),
                                        "upload_status": video.get("status", {}).get("uploadStatus"),
                                        "thumbnail": thumb}})
