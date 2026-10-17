#!/usr/bin/env python3
"""Lädt den Scan von Computer Kontakt Nr. 20 (6-7/86) von archive.org und
schneidet einzelne Seiten heraus: als PDF und als Bilder.

Aufruf: python3 tools/scan_seiten.py [--von 76] [--bis 78]

Ergebnis in scans/:
  ComputerKontakt_20.pdf              kompletter Scan (wird nur einmal geladen)
  ck20_seiten_076-078.pdf             nur die gewünschten Seiten
  seiten/ck20_s076.png                Seite aus dem PDF gerendert
  seiten/ck20_s076_hq.jpg             Seite aus den Original-Scans (volle Auflösung)

Die Seitennummern sind PDF-Seiten (1 = Titelseite). Im Heft gedruckte
Seitenzahlen können um ein paar Seiten davon abweichen.
"""
import argparse
import io
import pathlib
import subprocess
import urllib.request
import zipfile

ITEM = "https://archive.org/download/computerkontakt-magazine-20/"
PDF_NAME = "ComputerKontakt_20.pdf"
JP2_ZIP = "ComputerKontakt_20_jp2.zip"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "scans"


def download(name, target=None):
    print(f"Lade {ITEM + name} ...")
    req = urllib.request.Request(ITEM + name, headers={"User-Agent": "scan-seiten/1.0"})
    with urllib.request.urlopen(req) as r:
        data = r.read()
    if target:
        target.write_bytes(data)
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--von", type=int, default=76)
    ap.add_argument("--bis", type=int, default=78)
    ap.add_argument("--ohne-hq", action="store_true", help="keine Original-Scans laden (spart 29 MB Download)")
    a = ap.parse_args()
    seiten = range(a.von, a.bis + 1)

    (OUT / "seiten").mkdir(parents=True, exist_ok=True)
    pdf = OUT / PDF_NAME
    if not pdf.exists():
        download(PDF_NAME, pdf)

    # 1. Seiten als eigenes PDF
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(str(pdf))
    print(f"Scan hat {len(reader.pages)} Seiten")
    writer = PdfWriter()
    for s in seiten:
        writer.add_page(reader.pages[s - 1])
    teil = OUT / f"ck20_seiten_{a.von:03d}-{a.bis:03d}.pdf"
    with open(teil, "wb") as f:
        writer.write(f)
    print(f"geschrieben: {teil.relative_to(ROOT)}")

    # 2. Seiten aus dem PDF als PNG rendern (braucht pdftoppm aus poppler-utils)
    for s in seiten:
        base = OUT / "seiten" / f"ck20_s{s:03d}"
        subprocess.run(["pdftoppm", "-r", "200", "-png", "-singlefile", "-f", str(s), "-l", str(s), str(pdf), str(base)], check=True)
        print(f"geschrieben: {base.relative_to(ROOT)}.png")

    # 3. Dieselben Seiten aus den Original-Scans in voller Auflösung
    if not a.ohne_hq:
        from PIL import Image
        z = zipfile.ZipFile(io.BytesIO(download(JP2_ZIP)))
        bilder = sorted(n for n in z.namelist() if n.lower().endswith(".jp2"))
        print(f"Original-Scans: {len(bilder)} Seiten")
        for s in seiten:
            if s - 1 >= len(bilder):
                continue
            img = Image.open(io.BytesIO(z.read(bilder[s - 1]))).convert("RGB")
            ziel = OUT / "seiten" / f"ck20_s{s:03d}_hq.jpg"
            img.save(ziel, quality=88)
            print(f"geschrieben: {ziel.relative_to(ROOT)} ({img.width}x{img.height}, aus {bilder[s - 1]})")


if __name__ == "__main__":
    main()
