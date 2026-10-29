import { github } from "./_github.js";
import { json } from "./_middleware.js";

// POST /api/blob, body = one image as base64 text. Returns its blob sha, used later by /api/photos.
// Images go up one by one so each request stays small.
export async function onRequestPost({ request, env }) {
  const base64 = (await request.text()).trim();
  if (!/^[A-Za-z0-9+/=]+$/.test(base64)) return json({ error: "Image invalide." }, 400);
  if (base64.length > 14_000_000) return json({ error: "Image trop lourde (10 Mo max)." }, 413);
  const blob = await github(env).createBlob(base64);
  return json({ sha: blob.sha });
}
