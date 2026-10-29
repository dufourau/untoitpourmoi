# Un toit pour moi: photo gallery

A dark, cinematic photo gallery (slider and grid views) that links to the association's HelloAsso page. A password-protected admin page lets someone drag and drop photos in. It's all free on GitHub Pages: no server and no other account.

- Site: https://dufourau.github.io/untoitpourmoi/
- Admin: https://dufourau.github.io/untoitpourmoi/admin/

## How it works
- `docs/` is what GitHub Pages serves.
- `docs/index.html` is the gallery. It reads `docs/content/photos.json`, and the first photo is the backdrop of the title slide. The HelloAsso links (the campaign `formulaires/1` and the association page) are hard-coded there.
- `docs/admin/index.html` is the admin page. On login, the password decrypts a GitHub access key stored in `docs/admin/key.json` (AES-GCM, PBKDF2 with 600,000 iterations). The browser then talks to GitHub directly: each **Publier** is one commit, and GitHub Pages redeploys in 1–2 min.
- Photos are resized in the browser to 2000 px WebP (about 50–400 KB) before upload.

The repo is public, so `key.json` is readable by anyone, but encrypted. Security rests on two things:
- **a long admin password.** The setup screen suggests a random 16-character one; keep that or use 5+ random words.
- **a key that can only touch this repo.** At worst, someone who cracked it could change the gallery.

## One-time setup (about 5 min)
1. **Create the GitHub key.** GitHub → Settings → Developer settings → **Fine-grained personal access tokens** → Generate new token:
   - Repository access: **Only select repositories → untoitpourmoi**
   - Permissions → Repository permissions → **Contents: Read and write**
   - Expiration: the longest offered. Write the date down.
2. **Open the admin page** and click **Configurer ou remplacer la clé d'accès**.
3. Paste the key and keep (or change) the suggested password. Click **Enregistrer**. This saves `key.json` encrypted, and you're logged in.
4. Give your friend the address and the password.

When the key expires, publishing fails with "Clé GitHub refusée". Make a new key and repeat steps 2–3. You can keep the same password or choose a new one.

## For the person adding photos
1. Open **https://dufourau.github.io/untoitpourmoi/admin/**.
2. Type the password.
3. Drag photos into the box, or click it to choose them. Add a caption if you want one. Drag the thumbnails to change the order; the first one is the background of the home page. Use ✕ to remove a photo.
4. Click **Publier**. The site updates within 1–2 minutes.

Only publish photos of people who have signed an image-rights consent form (signed by their legal guardian where needed).

## Custom domain (optional, about €10 a year)
`untoitpourmoi.fr` is already registered (since 2020, through Scaleway/o2switch). It currently forwards to an empty `1toitpourmoi.fr` page. Either find its owner or pick another name, for example `un-toit-pour-moi.fr`, which looked free in Oct 2026. Then:
1. Set the DNS: `A` records for `@` pointing to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, plus a `CNAME` for `www` pointing to `dufourau.github.io`.
2. In GitHub repo **Settings → Pages → Custom domain**, enter the domain and tick **Enforce HTTPS**.

## Testing
Serve `docs/` locally (`python -m http.server`). Open `admin/?branch=<test-branch>` so publishes go to a throwaway branch instead of `main`.
