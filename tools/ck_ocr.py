#!/usr/bin/env python3
"""Lädt Metadaten und OCR-Volltexte aller Computer-Kontakt-Hefte von archive.org.

Aufruf: python3 tools/ck_ocr.py

Ergebnis in data/computerkontakt/:
  hefte.json        je Heft: archive.org-Kennung, Titel, Datum, Dateinamen von PDF, Bilder-Zip und OCR
  <kennung>.txt     OCR-Volltext (djvu.txt), Grundlage für die Inhaltsverzeichnisse in index.html
"""
import json
import pathlib
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "computerkontakt"
UA = {"User-Agent": "ck-ocr/1.0"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    q = urllib.parse.urlencode({
        "q": 'identifier:computerkontakt* OR title:"computer kontakt"',
        "fl[]": "identifier", "rows": "500", "output": "json",
    })
    ids = sorted(d["identifier"] for d in json.loads(get("https://archive.org/advancedsearch.php?" + q))["response"]["docs"])
    print(len(ids), "Treffer:", ids)
    hefte = []
    for ident in ids:
        meta = json.loads(get(f"https://archive.org/metadata/{ident}"))
        md, files = meta.get("metadata", {}), meta.get("files", [])
        names = [f["name"] for f in files]
        pick = lambda pred: next((n for n in names if pred(n)), None)
        heft = {
            "id": ident,
            "title": md.get("title"),
            "date": md.get("date"),
            "pdf": pick(lambda n: n.lower().endswith(".pdf") and "_text" not in n.lower()),
            "zip": pick(lambda n: n.lower().endswith("_jp2.zip")) or pick(lambda n: n.lower().endswith(".zip")),
            "ocr": pick(lambda n: n.endswith("_djvu.txt")),
            "sizes": {f["name"]: f.get("size") for f in files if f["name"].lower().endswith((".pdf", ".zip"))},
        }
        hefte.append(heft)
        if heft["ocr"]:
            try:
                (OUT / f"{ident}.txt").write_bytes(get(f"https://archive.org/download/{ident}/{urllib.parse.quote(heft['ocr'])}"))
            except Exception as e:  # einzelne fehlende OCR-Texte nicht fatal
                print("OCR fehlt:", ident, e)
        print(ident, heft["title"], heft["date"], heft["pdf"], heft["zip"])
    (OUT / "hefte.json").write_text(json.dumps(hefte, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
