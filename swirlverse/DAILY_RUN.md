# Swirlverse automatic run playbook

Every scheduled run follows this file exactly. The run type comes from the task prompt: `SHORT-A`, `SHORT-B` or `LONG`.
The owner is not watching, so never ask questions. If something blocks the run, skip the upload and notify (step 9).

## Fixed values (validated 2026-11-23)
- Channel: Swirlverse, @theswirlverse, id `UCuUa2n9v57RY3GmgLmSggpQ`, uploads playlist `UUuUa2n9v57RY3GmgLmSggpQ`
- Playlists: Shorts `PLLQeg9yAzaS8` ("Parallel World Shorts 🌀"), Long `PLD1ZRgAZqkno` ("Parallel World Deep Dives 🌀")
- Google Drive archive folder: "Swirlverse Uploads", id `1Feed6O_3r2w7QgPeAGDllh5bl76FClLU` (account iamaliyanrehman@gmail.com)
- Upload repo: `aliyan-rehman/itxmafia-uploads`, branch `main`. Media goes in the repo ROOT as `swirlverse_<id>.mp4` / `swirlverse_<id>_thumb.png`. Raw URL: `https://raw.githubusercontent.com/aliyan-rehman/itxmafia-uploads/main/<file>`
- The repo is shared with the itxMAFIA channel. Never touch files that are not yours (only `swirlverse/` and your own `swirlverse_*` media in the root).
- Zapier YouTube app: selected_api `YouTubeV4CLIAPI` (default connection = Swirlverse). Google Drive: `GoogleDriveCLIAPI`.
- Categories: 27 = Education (default), 28 = Science & Technology, 24 = Entertainment.
- Publishing: `publish_at` does NOT work (not a Partner channel), so the run uploads as **public** at publish time.

## Slots (Asia/Karachi)
- SHORT-A publishes around 17:00 PKT (run starts about 16:00).
- SHORT-B publishes around 22:30 PKT (run starts about 22:00).
- LONG publishes around 20:00 PKT every 2nd day.
- **Skip rule:** before producing, list the last 10 uploads (step 2). If a video of the same kind is already public or scheduled (`publishAt`) within ±3 h of this slot, skip quietly. Two manual Shorts are scheduled for 2026-11-23 and 2026-11-24 at 17:30Z, so SHORT-B skips on those days.
- **Max per day:** 2 Shorts + 1 long. Never upload more, even to catch up after a failure.

## 1. Setup (about 2 min)
```
cd /home/claude/itxmafia-uploads && git pull -q --rebase origin main
bash swirlverse/setup.sh
git config user.name "Swirlverse uploader"; git config user.email "swirlverse-bot@users.noreply.github.com"
```

## 2. Read the channel (always, before choosing anything)
Use Zapier with the exact calls below; inspect_zapier_actions first if a call errors.
- Top videos (28 days): `execute_zapier_read_action(selected_api="YouTubeV4CLIAPI", action="get_report", tool_name="youtube_get_report", params={report_type:"video_top", report_breakdown:"Channel", start_date:<today-28>, end_date:<today>, metrics:["views","estimatedMinutesWatched","averageViewDuration","averageViewPercentage","likes","comments","shares","subscribersGained"], dynamic_properties:{channel:"UCuUa2n9v57RY3GmgLmSggpQ", sort_by:["-views"], max_results:"50"}})`. Note: `sort_by` needs the leading minus.
- Traffic sources: the same call with `report_type:"video_traffic_source_type"`, `metrics:["views","estimatedMinutesWatched"]` and no sort.
- Recent uploads and their status: `execute_zapier_read_action(selected_api="YouTubeV4CLIAPI", action="_zap_raw_request", tool_name="youtube_make_api_get_request", params={url:"https://www.googleapis.com/youtube/v3/playlistItems", querystring:{part:"snippet,status", playlistId:"UUuUa2n9v57RY3GmgLmSggpQ", maxResults:"15"}, method:"GET", fail_on_errors:false})`. For `publishAt` and per-video stats, call `.../youtube/v3/videos` with `part:"status,statistics,contentDetails"` and `id:<comma list>`.
- Then update `swirlverse/STRATEGY.md`:
  - fill the result column for experiments that are now 48 h or older
  - revise the rules of thumb when the numbers clearly disagree

## 3. Choose
**Read `swirlverse/FORMATS.md` first.** The channel makes any curiosity video that fits it: WHAT IF, WHY, IS IT TRUE?, VS, MIND HACK or IMAGINE.
- Every topic must pass that file's research gate (true, wanted, fresh, score ≥ 19/25) before you write a line.
- Mix the formats across the week, so no more than 2 of the same format in a row unless the data clearly says it wins.
- For non-portal formats use `K.cold_open`, `K.verdict` and `K.versus` from shortkit.
- First check `swirlverse/ready/` for a finished video of this run's kind (listed in history.json "ready"). If one exists, use it: run QA again (step 6) and go to step 7.
- Otherwise pick a NEW topic using STRATEGY.md:
  - about 70% proven categories, about 30% experiments
  - never a topic or close variant from history.json within 60 days
- **Originality:**
  - 100% original story with our cast only: Nova, Kiko, baby Kiko, Mom, Dad, Grandpa, the mouse
  - no copyrighted characters, brands, logos, real people, song lyrics or movie references
  - no fear or shock content
  - family-friendly; made_for_kids stays false
- **Facts:**
  - check every number and claim with WebSearch, with at least 2 independent reliable sources (government, university, encyclopedia, peer-reviewed or major science outlet)
  - put the facts and sources in the episode docstring, and the key facts in the description
  - if a fact can't be confirmed, cut it or pick another topic
- **Format:**
  - for WHAT IF and IMAGINE: "In our world, … But in this parallel world, …" (portal at the cut). Other formats are explained in FORMATS.md
  - Nova = George voice, Kiko = second voice
  - end with a 2-option poll and "Comment below. A new parallel world, every day."

## 4. Write the episode
- **Short:** copy `swirlverse/episodes/ep13_ice_sinks.py` to `swirlverse/episodes/<id>.py`.
  - Script: 8–11 lines, 25–45 s total.
  - Shots: use the kit (`K.hook`, `K.arrive`, `K.twoshot`, `K.kcu`, `K.ncu`, `K.stat`, `K.compare`, `K.words`, `K.custom`, `K.end`). Add 2–4 custom drawings for the topic's key image.
  - Change the camera or shot every 1.5–4 s. Keep the twist visible in the first 2 s after the portal.
  - Thumbnail: `thumbnail(c, K)` with thumbkit (huge text, big character, hero object, arrow/burst).
- **Long:** copy `swirlverse/episodes/long03_nobody_could_lie.py` to a new file.
  - 2:15–3:30, 6–7 chapters, each ≥ 10 s. "In our world" is ch2–3, the portal/parallel world is ch4.
  - `META.description` must contain `{CHAPTERS}`.
  - Reuse longkit sets and props (room, board, street, office, brain, mouse, people icons, etc.). See examples/ for more scenes.
- Set `META` title, description (with `#shorts` for Shorts), tags (≤ 15, ≤ 450 characters total), topic and category.

## 5. Build
```
cd /home/claude/itxmafia-uploads/swirlverse/engine
python3 build_short.py ../episodes/<id>.py stills     # look at /tmp/swirl/<id>/stills/*.png and fix framing, overlaps, empty shots
python3 build_short.py ../episodes/<id>.py all        # mp4 + thumb + meta.json in /tmp/swirl/<id>/
# long: python3 build_long.py ../episodes/<id>.py stills / all   (render takes about 25 min; run it in the background and poll)
```
- Look at the stills and the thumbnail with the Read tool before rendering. Fix anything that is:
  - cut-off faces or characters overlapping text
  - text over faces
  - black gaps, or an empty or confusing frame

## 6. Quality gate (must pass)
```
python3 engine/qa.py /tmp/swirl/<id>/<id>.mp4 /tmp/swirl/<id>/<id>_thumb.png /tmp/swirl/<id>/meta.json short|long
```
- QA checks:
  - duration (Short 15–59.5 s, long 2–5 min) and resolution
  - loudness −16..−12 LUFS and true peak
  - black or frozen frames, and silence gaps
  - thumbnail < 2 MB
  - title, description and tag limits, `#shorts`, made_for_kids
- Then **open the `_sheet.png` contact sheet with Read** and confirm it looks right.
- If QA fails: fix and rebuild at most 2 times. If it still fails, go to step 9 (skip and notify).

## 7. Upload (public, at publish time)
1. Copy the media to the repo root as `swirlverse_<id>.mp4` and `swirlverse_<id>_thumb.png`, then `git add` those 2 files plus `swirlverse/` changes, commit, and `git -c push.negotiate=true push origin HEAD:main`. On a reject: `git pull --rebase` and retry once. Wait about 20 s, then check the raw URLs answer HTTP 200 with `curl -sI`.
2. `execute_zapier_write_action(selected_api="YouTubeV4CLIAPI", action="upload_video", tool_name="youtube_upload_video", params={title, description, tags:[...], video:<raw mp4 url>, thumbnail:<raw png url>, privacy_status:"public", category_id:"27", made_for_kids:false, notify_subscribers:true, default_language:"en", default_audio_language:"en"})`. Save the returned `id`.
3. Add to playlist: `execute_zapier_write_action(selected_api="YouTubeV4CLIAPI", action="add_video_to_playlist", tool_name="youtube_add_video_to_playlist", params={video_id:<id>, playlist_id:"PLLQeg9yAzaS8" (short) or "PLD1ZRgAZqkno" (long)})`.
4. Altered-content setting (our videos are clearly animated, so "No"): `execute_zapier_write_action(selected_api="YouTubeV4CLIAPI", action="_zap_raw_request", tool_name="youtube_make_api_mutating_request", params={url:"https://www.googleapis.com/youtube/v3/videos", querystring:{part:"status"}, method:"PUT", headers:{"Content-Type":"application/json"}, body:"{\"id\":\"<id>\",\"status\":{\"privacyStatus\":\"public\",\"license\":\"youtube\",\"embeddable\":true,\"publicStatsViewable\":true,\"selfDeclaredMadeForKids\":false,\"containsSyntheticMedia\":false}}", fail_on_errors:false})`.
5. If the upload response shows no custom thumbnail, call `upload_video_thumbnail` (tool_name `youtube_update_video_thumbnail`) with the raw png url.
6. Archive to Drive, twice (mp4 and png): `execute_zapier_write_action(selected_api="GoogleDriveCLIAPI", action="file", tool_name="google_drive_upload_file", params={file:<raw url>, folder:"1Feed6O_3r2w7QgPeAGDllh5bl76FClLU", new_name:"<YYYY-MM-DD> <id> <short title>"})`. Leave the extension off the name; Drive adds it.
7. Delete the 2 media files from the repo root (`git rm`), and from `swirlverse/ready/` if they came from there. Commit and push.

## 8. Record
- Append the video to `swirlverse/history.json` "videos" (date, kind, video_id, title, topic, category, style, thumb, experiment). Remove it from "ready" if it was there.
- Append a row to the STRATEGY.md experiment log: what this video tests.
- Commit and push (`swirlverse/` only).

## 9. Notify the owner (always, success or skip)
- **Success:** use PushNotification if available, or SendUserMessage. One short summary:
  - "✅ Swirlverse <slot>: '<title>' is live — https://youtu.be/<id>"
  - plus 1 line of channel stats (views or subs from step 2) and what was tested
- **Skip or failure:** "⚠️ Swirlverse <slot> skipped: <reason in one line>". Don't upload anything partial. Leave a finished video in `swirlverse/ready/` if only the upload failed.
- Never post anything to other places.

## Never
- Upload more than the daily limit, or upload without passing QA and the visual check.
- Use copyrighted or real-person content, misleading thumbnails (the thumbnail must show something that really happens in the video), or unverified facts.
- Delete or change other files in the repo, or other videos and playlists on the channel.
- Set "altered content" to Yes (our content is clearly animated), or made_for_kids to true.
