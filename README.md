# Un toit pour moi: photo gallery

A dark, cinematic photo gallery (slider and grid views) that links to the association's HelloAsso page. Comes with a password-protected admin page where photos are dragged and dropped in. Hosted for free on Cloudflare Pages, built from this private GitHub repo.

- `public/index.html` is the gallery. It reads `public/content/photos.json`. The first photo is the backdrop of the title slide.
- `public/admin/` is the admin page: password, drag and drop, reorder, captions, delete, **Publier**.
- `functions/api/` is the small server code behind the admin, run by Cloudflare. It checks the password and turns each publish into one commit on this repo, which Cloudflare then redeploys (1–2 min).
- Photos are resized in the browser to 2000 px WebP (about 50–400 KB each) before upload.

HelloAsso links are hard-coded in `public/index.html`:
- the campaign: https://www.helloasso.com/associations/un-toit-pour-moi/formulaires/1
- the association: https://www.helloasso.com/associations/un-toit-pour-moi

## One-time setup (about 10 min)

### 1. GitHub token, so the admin can save photos
GitHub → Settings → Developer settings → **Fine-grained personal access tokens** → Generate new token:
- Repository access: **Only select repositories → untoitpourmoi**
- Permissions: **Contents → Read and write**
- Expiration: the longest offered. Write the expiry date down: when it passes, publishing stops until you make a new token.

### 2. Cloudflare Pages
1. Create a free account at https://dash.cloudflare.com.
2. **Workers & Pages → Create → Pages → Connect to Git**, then authorise GitHub for **untoitpourmoi** only.
3. Build settings:
   - Framework preset: **None**
   - Build command: *(leave empty)*
   - Build output directory: `public`
4. **Environment variables**, all as type **Secret** (Encrypt) where offered:
   | Name | Value |
   |---|---|
   | `ADMIN_PASSWORD` | a long passphrase, e.g. 4–5 random words |
   | `GITHUB_TOKEN` | the token from step 1 |
   | `GITHUB_REPO` | `dufourau/untoitpourmoi` |
5. Click **Save and Deploy**. The site goes live at `https://untoitpourmoi.pages.dev`, or a close variant if that name is taken.

If you change a variable later, redeploy (Deployments → ⋯ → Retry deployment) for it to apply.

## For the person adding photos
1. Open **`https://<site>/admin`**.
2. Type the password.
3. Drag photos into the box, or click it to choose them. Add a caption if you want one. Drag the thumbnails to change the order; the first one is the background of the home page. Use ✕ to remove a photo.
4. Click **Publier**. The site updates within 1–2 minutes.

Only publish photos of people who have signed an image-rights consent form (signed by their legal guardian where needed).

## Custom domain (optional, about €10 a year)
`untoitpourmoi.fr` is already registered (since 2020, through Scaleway/o2switch). It currently forwards to an empty `1toitpourmoi.fr` page. Either find its owner or pick another name, for example `un-toit-pour-moi.fr`, which looked free in Oct 2026. Then go to Cloudflare Pages → the project → **Custom domains → Set up a domain** and follow its DNS instructions.

## Local test
```bash
npx wrangler pages dev public --binding ADMIN_PASSWORD=test --binding GITHUB_REPO=dufourau/untoitpourmoi --binding GITHUB_BRANCH=some-test-branch --binding GITHUB_TOKEN=<token>
```
`GITHUB_BRANCH` (default `main`) lets a test publish to a throwaway branch.
