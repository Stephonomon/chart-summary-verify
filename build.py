"""Step 4: inject results.json + the chart into template.html.
  index.html     standalone page for GitHub Pages
  artifact.html  the same page without the document wrapper, for publishing as a claude.ai artifact"""
import json
from data import SOURCES, PATIENT, TODAY

d = json.load(open("results.json"))
d["sources"], d["patient"], d["today"] = SOURCES, PATIENT, TODAY
page = open("template.html").read().replace("/*DATA*/null", json.dumps(d, separators=(",", ":")).replace("</", "<\\/"))
open("artifact.html", "w").write(page)
open("index.html", "w").write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + page.replace("<style>", "</head>\n<body>\n<style>", 1) + "\n</body>\n</html>\n")
print(f"index.html {len(page)/1024:.0f} KB")
