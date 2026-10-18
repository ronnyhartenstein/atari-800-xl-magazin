#!/usr/bin/env python3
"""Holt die Inhaltsverzeichnis-Seiten der Computer-Kontakt-Hefte in guter Qualität.

Der OCR-Text von archive.org ist für die Inhaltsseiten kaum brauchbar. Dieses
Script lädt deshalb je Heft das Zip mit den Original-Scans, erkennt die ersten
Seiten selbst mit Tesseract (deutsch) und speichert die Seite(n), auf denen
„Inhalt“ steht, als Bild und Text.

Aufruf: python3 tools/ck_inhalt.py [kennung ...]

Ergebnis in data/computerkontakt/inhalt/:
  <kennung>_sNN.jpg   Inhaltsseite (PDF-Seite NN), 1600 Pixel breit
  <kennung>_sNN.txt   Tesseract-Text dieser Seite
"""
import io
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "computerkontakt"
OUT = DATA / "inhalt"
UA = {"User-Agent": "ck-inhalt/1.0"}
ERSTE_SEITEN = 10


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r:
        return r.read()


def ocr(img):
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        img.save(f.name)
        return subprocess.run(["tesseract", f.name, "-", "-l", "deu", "--psm", "3"],
                              capture_output=True, text=True).stdout


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hefte = json.loads((DATA / "hefte.json").read_text())
    wahl = set(sys.argv[1:])
    for h in hefte:
        if not h.get("zip") or (wahl and h["id"] not in wahl):
            continue
        size = int(h.get("sizes", {}).get(h["zip"], 0) or 0)
        if size > 120_000_000:
            print("übersprungen (zu groß):", h["id"]); continue
        print("Lade", h["id"], h["zip"], size // 1_000_000, "MB", flush=True)
        try:
            z = zipfile.ZipFile(io.BytesIO(get(f"https://archive.org/download/{h['id']}/{urllib.parse.quote(h['zip'])}")))
        except Exception as e:
            print("Fehler:", h["id"], e); continue
        names = sorted(n for n in z.namelist() if n.lower().endswith((".jp2", ".jpg", ".png", ".tif")))
        treffer = []
        for i, n in enumerate(names[:ERSTE_SEITEN]):
            img = Image.open(io.BytesIO(z.read(n))).convert("L")
            text = ocr(img)
            score = len(re.findall(r"inhalt", text, re.I))
            if score:
                treffer.append((i + 1, img, text))
        if not treffer:   # nichts gefunden: Seiten 3 und 4 als Ersatz
            treffer = [(i + 1, Image.open(io.BytesIO(z.read(names[i]))).convert("L"), "") for i in (2, 3) if i < len(names)]
        for s, img, text in treffer[:3]:
            w = 1600
            img = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
            img.save(OUT / f"{h['id']}_s{s:02d}.jpg", quality=78)
            (OUT / f"{h['id']}_s{s:02d}.txt").write_text(text)
            print("  Inhaltsseite", s, flush=True)


if __name__ == "__main__":
    main()
