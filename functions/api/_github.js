// Small GitHub REST helper. Everything the admin publishes becomes one commit on GITHUB_BRANCH,
// and Cloudflare Pages redeploys the site from that commit.
export const PHOTOS_PATH = "public/content/photos.json";

export function github(env) {
  const repo = env.GITHUB_REPO;
  const branch = env.GITHUB_BRANCH || "main";

  async function api(path, init = {}) {
    const res = await fetch(`https://api.github.com/repos/${repo}${path}`, {
      ...init,
      headers: {
        "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
        "Accept": "application/vnd.github+json",
        "User-Agent": "untoitpourmoi-admin",
        ...(init.body ? { "Content-Type": "application/json" } : {}),
      },
    });
    if (!res.ok) throw new Error(`GitHub ${res.status} sur ${path} : ${(await res.text()).slice(0, 200)}`);
    return res.json();
  }

  return {
    api,
    branch,

    async readPhotos() {
      const ref = await api(`/git/ref/heads/${branch}`);
      const file = await api(`/contents/${PHOTOS_PATH}?ref=${ref.object.sha}`);
      const text = new TextDecoder().decode(Uint8Array.from(atob(file.content.replace(/\n/g, "")), c => c.charCodeAt(0)));
      return { headSha: ref.object.sha, photos: JSON.parse(text) };
    },

    createBlob(base64) {
      return api("/git/blobs", { method: "POST", body: JSON.stringify({ content: base64, encoding: "base64" }) });
    },

    // entries: [{ path, sha }] to add (sha of an uploaded blob), [{ path, sha: null }] to delete,
    // [{ path, content }] for a text file.
    async commit(parentSha, entries, message) {
      const parent = await api(`/git/commits/${parentSha}`);
      const tree = await api("/git/trees", {
        method: "POST",
        body: JSON.stringify({
          base_tree: parent.tree.sha,
          tree: entries.map(e => ({ path: e.path, mode: "100644", type: "blob",
                                    ...(e.content !== undefined ? { content: e.content } : { sha: e.sha }) })),
        }),
      });
      const commit = await api("/git/commits", {
        method: "POST",
        body: JSON.stringify({ message, tree: tree.sha, parents: [parentSha] }),
      });
      // Not forced: if someone else published in between, GitHub refuses and the admin retries.
      await api(`/git/refs/heads/${branch}`, { method: "PATCH", body: JSON.stringify({ sha: commit.sha }) });
      return commit.sha;
    },
  };
}
