#!/usr/bin/env python3
"""Serve only public site artifacts, not authoring documents or design briefs."""
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {"index.html", "en/index.html", "styles.css", "site.js", "appcast.xml", "app-icon-64.png", "app-icon-256.png", "og.png", "en/og.png"}


class PublicHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def allowed(self):
        route = unquote(urlsplit(self.path).path).lstrip("/")
        if not route or route == "en/":
            return True
        if ".." in Path(route).parts:
            return False
        return route in PUBLIC_FILES or (route.startswith("fonts/") and Path(route).suffix == ".woff2")

    def do_GET(self):
        if self.allowed():
            super().do_GET()
        else:
            self.send_error(404)

    def do_HEAD(self):
        if self.allowed():
            super().do_HEAD()
        else:
            self.send_error(404)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8791)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), PublicHandler)
    print(f"Preview: http://127.0.0.1:{args.port}/", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
