#!/usr/bin/env python3
"""Wandelt ein Listing mit lesbaren Platzhaltern in eine ATASCII-Datei (.LST) um,
die man am Atari oder im Emulator mit ENTER "D:ROLLER.LST" laden kann.

Platzhalter: {^A}..{^Z} = CTRL-Grafikzeichen, {DOWN}/{UP}/{LEFT}/{RIGHT} = Cursor,
{INV}...{/INV} = inverse Zeichen (Bit 7 gesetzt, gilt nicht für Cursorzeichen).

Aufruf: python3 tools/atascii_lst.py rollerball/rollerball2.txt rollerball/ROLLER.LST
"""
import re
import sys

CURSOR = {"UP": 28, "DOWN": 29, "LEFT": 30, "RIGHT": 31}
TOKEN = re.compile(r"\{(\^[A-Z]|UP|DOWN|LEFT|RIGHT|INV|/INV)\}")


def convert_line(line):
    out, inv, pos = bytearray(), False, 0
    for m in TOKEN.finditer(line):
        for ch in line[pos:m.start()]:
            out.append(ord(ch) | (128 if inv else 0))
        t = m.group(1)
        if t == "INV":
            inv = True
        elif t == "/INV":
            inv = False
        elif t in CURSOR:
            out.append(CURSOR[t])
        else:
            out.append((ord(t[1]) - 64) | (128 if inv else 0))
        pos = m.end()
    for ch in line[pos:]:
        out.append(ord(ch) | (128 if inv else 0))
    return bytes(out)


def main(src, dst):
    lines = [l.rstrip("\n") for l in open(src, encoding="utf-8") if l.strip()]
    with open(dst, "wb") as f:
        for l in lines:
            f.write(convert_line(l) + b"\x9b")  # 155 = ATASCII-Zeilenende
    print(f"{len(lines)} Zeilen nach {dst} geschrieben")


if __name__ == "__main__":
    main(*sys.argv[1:3])
