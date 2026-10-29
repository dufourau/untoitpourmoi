import { github, PHOTOS_PATH } from "./_github.js";
import { json } from "./_middleware.js";

const SRC = /^images\/[A-Za-z0-9_-]+\.(webp|jpe?g|png)$/;

// GET /api/photos: the gallery as it is on the branch right now (not the deployed copy,
// which can lag a minute behind).
export async function onRequestGet({ env }) {
  const { headSha, photos } = await github(env).readPhotos();
  return json({ headSha, photos });
}

// POST /api/photos, body { headSha, photos: [{ src, caption, w, h, blob? }] }
// The list is the full new gallery in order. Entries with "blob" are new images uploaded through
// /api/blob; images in the old list but not the new one are deleted. One commit for everything.
export async function onRequestPost({ request, env }) {
  const gh = github(env);
  const body = await request.json();
  const current = await gh.readPhotos();
  if (body.headSha && body.headSha !== current.headSha) {
    return json({ error: "La galerie a été modifiée ailleurs entre-temps. Rechargez la page." }, 409);
  }

  const photos = [];
  const entries = [];
  for (const p of body.photos || []) {
    if (!SRC.test(p.src || "")) return json({ error: `Nom de fichier invalide : ${p.src}` }, 400);
    if (p.blob) {
      if (!/^[0-9a-f]{40}$/.test(p.blob)) return json({ error: "Identifiant d'image invalide." }, 400);
      entries.push({ path: `public/${p.src}`, sha: p.blob });
    }
    photos.push({
      src: p.src,
      caption: String(p.caption || "").slice(0, 200),
      ...(p.w && p.h ? { w: Math.round(p.w), h: Math.round(p.h) } : {}),
    });
  }

  const kept = new Set(photos.map(p => p.src));
  for (const old of current.photos) {
    if (!kept.has(old.src) && SRC.test(old.src)) entries.push({ path: `public/${old.src}`, sha: null });
  }
  entries.push({ path: PHOTOS_PATH, content: JSON.stringify(photos, null, 2) + "\n" });

  const added = entries.filter(e => e.sha).length;
  const removed = entries.filter(e => e.sha === null).length;
  const message = `Galerie : ${photos.length} photos` +
    (added ? `, ${added} ajoutée(s)` : "") + (removed ? `, ${removed} supprimée(s)` : "");
  const headSha = await gh.commit(current.headSha, entries, message);
  return json({ headSha, photos });
}
