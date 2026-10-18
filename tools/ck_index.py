#!/usr/bin/env python3
"""Schreibt die Computer-Kontakt-Inhaltsverzeichnisse in index.html.

Quelle: data/computerkontakt/inhalt.json (abgeschrieben von den gedruckten
Inhaltsseiten) und data/computerkontakt/hefte.json (archive.org-Dateien).
Ersetzt in index.html den Block zwischen // CK-DATEN-START und // CK-DATEN-ENDE.

Aufruf: python3 tools/ck_index.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "computerkontakt"
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]
# Bessere Scans desselben Hefts als eigene archive.org-Einträge
ALT = {3: "computer-kontakt-8-9-84-august-september", 8: "ck198502"}


def monate(ausgabe):
    m = re.fullmatch(r"(\d+)/(\d\d)-(\d+)/(\d\d)", ausgabe or "")   # über den Jahreswechsel, z. B. 12/86-1/87
    if m:
        return f"{MONATE[int(m[1]) - 1]} {1900 + int(m[2])}/{MONATE[int(m[3]) - 1]} {1900 + int(m[4])}"
    m = re.fullmatch(r"(\d+)(?:-(\d+))?/(\d\d)", ausgabe or "")
    if not m:
        return ausgabe or ""
    a, b, j = int(m[1]), m[2] and int(m[2]), 1900 + int(m[3])
    return f"{MONATE[a - 1]}/{MONATE[b - 1]} {j}" if b else f"{MONATE[a - 1]} {j}"


def main():
    hefte = {h["id"]: h for h in json.loads((DATA / "hefte.json").read_text())}
    out = []
    for heft in json.loads((DATA / "inhalt.json").read_text()):
        ident = f"computerkontakt-magazine-{heft['nr']:02d}"
        h = hefte[ident]
        size = lambda n: int(h["sizes"].get(n) or 0) if n else 0
        o = {"mag": "ck", "nr": str(heft["nr"]), "monate": f"{heft['ausgabe']} · {monate(heft['ausgabe'])}", "id": ident,
             "pdf": h["pdf"], "pdfB": size(h["pdf"]), "zip": h["zip"], "zipB": size(h["zip"]),
             "e": [[r, t, s] + ([f] if f else []) for r, t, s, f in heft["e"]]}
        if heft["nr"] in ALT:
            o["alt"] = ALT[heft["nr"]]
        out.append(o)
    js = "const CK = [\n" + ",\n".join("  " + json.dumps(o, ensure_ascii=False) for o in out) + "\n];"
    p = ROOT / "index.html"
    s = p.read_text()
    s = re.sub(r"(// CK-DATEN-START\n).*?(\n// CK-DATEN-ENDE)", lambda m: m[1] + js + m[2], s, flags=re.S)
    p.write_text(s)
    print(len(out), "Hefte,", sum(len(o["e"]) for o in out), "Einträge")


if __name__ == "__main__":
    main()
