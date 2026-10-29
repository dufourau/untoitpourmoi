// Every /api/* call must carry "Authorization: Bearer <ADMIN_PASSWORD>".
export async function onRequest({ request, env, next }) {
  if (!env.ADMIN_PASSWORD || !env.GITHUB_TOKEN || !env.GITHUB_REPO) {
    return json({ error: "Site mal configuré : ADMIN_PASSWORD, GITHUB_TOKEN et GITHUB_REPO sont requis." }, 500);
  }
  const given = (request.headers.get("Authorization") || "").replace(/^Bearer /, "");
  if (!(await sameText(given, env.ADMIN_PASSWORD))) {
    await new Promise(r => setTimeout(r, 800));   // slows down password guessing
    return json({ error: "Mot de passe incorrect." }, 401);
  }
  try {
    return await next();
  } catch (err) {
    return json({ error: String(err.message || err) }, 502);
  }
}

// Compare hashes rather than the strings so the check takes the same time whatever the input.
async function sameText(a, b) {
  const enc = new TextEncoder();
  const [ha, hb] = await Promise.all([a, b].map(s => crypto.subtle.digest("SHA-256", enc.encode(s))));
  const x = new Uint8Array(ha), y = new Uint8Array(hb);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } });
}
