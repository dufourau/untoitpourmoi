# Un toit pour moi: photo gallery

A dark, cinematic photo gallery (slider and grid views) that links to the association's HelloAsso page. A password-protected admin page lets someone drag and drop photos in. It's all free on GitHub Pages: no server and no other account.

- Site: https://dufourau.github.io/untoitpourmoi/
- Admin: https://dufourau.github.io/untoitpourmoi/admin/

## How it works
- `docs/` is what GitHub Pages serves.
- `docs/index.html` is the one-page site: hero, "Qui sommes-nous", the garden slider, the "Notre histoire" timeline, a before/after comparison and a last call to donate. The HelloAsso links (the campaign `formulaires/1` and the association page) are hard-coded at the top of its script.
- Its content comes from three files in `docs/content/`:
  - `photos.json`: the garden renders (artist's views). The first one is also the hero background, and the first four close the timeline as "Demain".
  - `timeline.json`: `{src, caption, w, h, date}`, where `date` is `YYYY-MM` or empty for "Aujourd'hui". The site groups photos by month, in date order.
  - `compare.json`: `[{before, after, caption, beforeLabel, afterLabel}]`, where `before` is a photo of a spot today and `after` the render of the same spot, both cropped to 4:3 around the same view. Each pair is a side-by-side slide at the end of the garden slider; when it comes into view, the render sweeps over today's photo on the right.
- The timeline picture is drawn with WebGL as a "3D photo": each photo has a depth map in `docs/images/depth/` (same file name), made with the Depth Anything V2 small model (ONNX). The camera drifts with parallax, and the next photo grows from the nearest objects to the background. A photo added from the admin page has no depth map yet, so it moves flat; without WebGL, or with reduced motion, plain cross-fades are used.
- The admin page edits `photos.json` (tab "Le jardin"), `compare.json` (tab "Avant / après": two pictures per pair), `timeline.json` (tab "Notre histoire") and `goal.json` (tab "Cagnotte": amount collected and goal, typed in by hand from HelloAsso). Uploads are resized in the browser (garden 2000 px, pairs 1400 px, story 1600 px on the longest side); previews have each slider's shape (16:9, 4:3, 3:2), and a red note flags a small (blurry) or upright (cropped) picture. ↻ replaces a picture and keeps its caption and place.
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
3. Choose the tab: **Le jardin** (images of the future garden), **Avant / après** (pairs: today's photo and the project image, from the same spot), **Notre histoire** (dated photos of the construction and of today) or **Cagnotte** (the amount collected, copied from HelloAsso).
4. Drag photos into the box, or click it to choose them. Add a caption if you want one. In **Le jardin**, drag the thumbnails to change the order; the first one is the background of the home page. In **Notre histoire**, set the month of each photo, or leave it empty for "Aujourd'hui". Use ✕ to remove a photo.
5. Click **Publier**. The site updates within 1–2 minutes.

Only publish photos of people who have signed an image-rights consent form (signed by their legal guardian where needed).

## Custom domain (optional, about €10 a year)
`untoitpourmoi.fr` is already registered (since 2020, through Scaleway/o2switch). It currently forwards to an empty `1toitpourmoi.fr` page. Either find its owner or pick another name, for example `un-toit-pour-moi.fr`, which looked free in Oct 2026. Then:
1. Set the DNS: `A` records for `@` pointing to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, plus a `CNAME` for `www` pointing to `dufourau.github.io`.
2. In GitHub repo **Settings → Pages → Custom domain**, enter the domain and tick **Enforce HTTPS**.

## Testing
Serve `docs/` locally with `python serve.py` (http://localhost:8811/, never cached by the browser). Open `admin/?branch=<test-branch>` so publishes go to a throwaway branch instead of `main`.

## Flyer, email and QR code (`flyer/`)
`python -E flyer/make_flyer.py [--url https://new-domain/]` rebuilds everything in `flyer/out/`:
the A5 flyer (`flyer.pdf`, `flyer.png`), the house-shaped QR code (`qr_maison.svg/.png`), the invitation
email (`email.html`: open it in a browser, select all, copy, paste into a new mail) and `messages.txt`
(subject line, plain-text mail, short messages). It checks that each QR scans. The email's pictures are
served from `docs/flyer/`, so push the site after rebuilding. When the domain is bought: rerun with `--url`.
