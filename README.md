# Un toit pour moi: photo and donation site

A one-page static site: hero photo, project story, photo gallery with a lightbox, and the HelloAsso donation form embedded. Hosted for free on GitHub Pages. Edited through a free admin UI ([Pages CMS](https://pagescms.org)), with no code involved.

- `index.html` is the page. It reads all its text and photos from `content/site.json`.
- `images/` holds the uploaded photos.
- `.pages.yml` defines the admin form: which fields exist and where photos go.
- `admin/` redirects `<site>/admin` to the Pages CMS login.

## How editing works
1. Your friend opens `<site>/admin` (or https://app.pagescms.org) and logs in.
2. She opens the **untoitpourmoi** repo and then **Le site**. She drags photos into "Photos de la galerie", adds captions, and clicks **Save**.
3. The save is a commit to the repo. GitHub Pages republishes the site within 1–2 minutes.

### Giving her access
- **Easiest:** in Pages CMS, open the repo, go to **Settings → Collaborators**, and invite her email. She logs in with a link sent by email, so she doesn't need a GitHub account.
- **Or:** she creates a free GitHub account, and you add her under GitHub repo **Settings → Collaborators**.

## Photos
Phone photos are often 4–8 MB each. Before uploading, run them through https://squoosh.app (WebP or JPEG, about 1600 px wide), or the site will be slow on mobile.

Only publish photos of people who have signed an image-rights consent form (signed by their legal guardian where needed).

## Custom domain (optional, about €10 a year)
`untoitpourmoi.fr` was already registered in Oct 2026 (since 2020, through Scaleway/o2switch). Either find its owner or pick a free alternative such as `un-toit-pour-moi.fr`. Then:
1. Buy the domain from a registrar such as OVH, Gandi or Infomaniak.
2. Set the DNS: `A` records for `@` pointing to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, plus a `CNAME` for `www` pointing to `dufourau.github.io`.
3. In GitHub repo **Settings → Pages → Custom domain**, enter the domain and tick **Enforce HTTPS**.

## Local preview
```bash
python -m http.server 8000
```
Then open http://localhost:8000.
