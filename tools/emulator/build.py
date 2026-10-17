#!/usr/bin/env python3
"""Baut rollerball/spielen.html: eine einzelne HTML-Datei mit Atari-Emulator
(Sfotty Pie), freien Altirra-ROMs und dem tokenisierten Rollerball-II-Programm.

Aufruf: python3 tools/emulator/build.py [--ohne-rahmen ZIELDATEI]
"""
import base64
import html
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = ROOT / "tools" / "emulator"
VENDOR = HERE / "vendor"


def b64(path):
    return base64.b64encode(path.read_bytes()).decode()


def build():
    page = (HERE / "page.html").read_text(encoding="utf-8")
    bundle = (VENDOR / "sfotty-pie-a8.min.js").read_text(encoding="utf-8")
    listing = (ROOT / "rollerball" / "rollerball2.txt").read_text(encoding="utf-8")
    for key, value in {
        "__LISTING__": html.escape(listing.rstrip()),
        "__OS_ROM__": b64(VENDOR / "altirraos-xl.rom"),
        "__BASIC_ROM__": b64(VENDOR / "altirra-basic.rom"),
        "__PROGRAM__": b64(ROOT / "rollerball" / "ROLLER.BAS"),
        "__A8_BUNDLE__": bundle,
    }.items():
        assert key in page, key
        page = page.replace(key, value)
    return page


def main():
    page = build()
    full = ('<!doctype html>\n<html lang="de">\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + page.replace("* { box-sizing: border-box; }", "* { box-sizing: border-box; }\nhtml, body { margin: 0; }", 1)
            + "</html>\n")
    out = ROOT / "rollerball" / "spielen.html"
    out.write_text(full, encoding="utf-8")
    print(f"geschrieben: {out.relative_to(ROOT)} ({len(full) // 1024} KB)")
    if len(sys.argv) == 3 and sys.argv[1] == "--ohne-rahmen":
        pathlib.Path(sys.argv[2]).write_text(page, encoding="utf-8")
        print(f"geschrieben: {sys.argv[2]}")


if __name__ == "__main__":
    main()
