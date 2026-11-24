# Free comment + stats worker: one-time setup (about 10 minutes, $0)

This gives the GitHub Actions worker (`.github/workflows/swirlverse-ops.yml`) its own free access to your channel. It handles comments, replies, playlists, the altered-content setting and stats, so Zapier tasks are only spent on uploads.

1. Open https://console.cloud.google.com and sign in with the Google account that owns Swirlverse. Create a project called **Swirlverse Ops**.
2. Go to **APIs & Services → Library** and enable two APIs:
   - **YouTube Data API v3**
   - **YouTube Analytics API**
3. Go to **Google Auth Platform** (OAuth consent screen) and set it up:
   - **Get started**: user type **External**, app name "Swirlverse Ops", your email.
   - **Audience**: press **Publish app** so it is "In production". In "Testing" the token stops working after 7 days. You don't need Google's verification for your own account.
4. Go to **Clients → Create client** and fill it in:
   - type **Web application**
   - authorised redirect URI: `https://developers.google.com/oauthplayground`

   Then copy the **Client ID** and **Client secret**.
5. Open https://developers.google.com/oauthplayground and get the refresh token:
   1. Click the ⚙️ gear, tick **Use your own OAuth credentials**, and paste the ID and secret.
   2. In the left box "Input your own scopes", paste:
      `https://www.googleapis.com/auth/youtube.force-ssl https://www.googleapis.com/auth/yt-analytics.readonly`
   3. Click **Authorize APIs**, then pick the **Swirlverse** channel when Google asks which account or channel. The screen will say the app isn't verified. Click **Advanced → Go to Swirlverse Ops** and allow it.
   4. Click **Exchange authorization code for tokens**, then copy the **Refresh token**.
6. In GitHub, open `aliyan-rehman/itxmafia-uploads` → **Settings → Secrets and variables → Actions → New repository secret**. Add 3 secrets:
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`
7. Open the **Actions** tab → **swirlverse-ops** → **Run workflow**. A green run that changes `swirlverse/ops/stats.json` means it works.

The secrets stay private even though the repo is public. Never paste them into a file.
Uploading stays on Zapier: videos uploaded through an unaudited Google project are locked to private, and comments are not affected by that rule.
