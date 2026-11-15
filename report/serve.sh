#!/bin/sh
# Serve the repo root and open /report/ (the page reads ../data/*.json, so it needs a web server).
cd "$(dirname "$0")/.." && echo "open http://localhost:8000/report/" && exec python3 -m http.server 8000
