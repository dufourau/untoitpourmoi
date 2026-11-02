"""Local preview of docs/ that browsers never cache, so a refresh always shows the latest edit.

    python serve.py        then open http://localhost:8811/
"""
import functools, http.server, os

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
http.server.ThreadingHTTPServer(("", 8811), functools.partial(NoCache, directory=docs)).serve_forever()
