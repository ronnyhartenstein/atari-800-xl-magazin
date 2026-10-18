# Atari 800 XL Magazin – getippte Texte

Sammlung abgetippter Texte und Listings aus Zeitschriften rund um den Atari 800 XL.

> ⚠️ Platzhalter: Diese README ist noch ein Dummy und wird später ausgebaut.

## Inhaltsverzeichnisse ATARImagazin 1987 und Computer Kontakt 1984–1988

[`index.html`](index.html) listet die Inhaltsverzeichnisse aller sechs Hefte des ATARImagazins (Verlag Rätz-Eberle) von 1987, mit Suchfeld und Filtern (nur Listings, nur XL/XE, Spieletests). Die Datei läuft ohne Build direkt im Browser, auch auf dem Handy: einfach öffnen.

Grundlage sind die OCR-Volltexte der Scans auf archive.org bzw. Atarimania; unsichere Einträge sind markiert. Das Heft erschien erst ab Januar 1987, für 1986 gibt es keine Ausgaben.

Dazu kommen alle 30 Hefte der Zeitschrift **Computer Kontakt** (Nr. 1, 5/84, bis Nr. 30, 2-3/88), mit Filter nach Zeitschrift und je Heft Links zum Scan auf archive.org, zum kleinen PDF und zum Zip mit den Seitenbildern in voller Auflösung. Die Einträge sind von den gedruckten Inhaltsseiten abgeschrieben und liegen in [`data/computerkontakt/inhalt.json`](data/computerkontakt/inhalt.json); [`tools/ck_index.py`](tools/ck_index.py) schreibt sie in `index.html`. Die Inhaltsseiten lassen sich mit den von Hand startbaren Actions „Computer-Kontakt-OCR laden“ ([`tools/ck_ocr.py`](tools/ck_ocr.py)) und „Computer-Kontakt-Inhaltsseiten“ ([`tools/ck_inhalt.py`](tools/ck_inhalt.py)) neu aus den Scans holen.

## Rollerball

Ausführliche Erklärung der beiden spielbaren Varianten in [`rollerball/README.md`](rollerball/README.md).

- [`rollerball/rollerball2.txt`](rollerball/rollerball2.txt): das Original-Listing „Rollerball II“ von Thomas Tausend (Computer Kontakt 6-7/86, S. 77–79), abgetippt vom Scan. Grafik- und Cursorzeichen stehen als Platzhalter wie `{^A}` oder `{DOWN}` drin.
- [`rollerball/ROLLER.LST`](rollerball/ROLLER.LST): dasselbe Listing als ATASCII-Datei, im Emulator (z. B. Altirra) per `ENTER "D:ROLLER.LST"` laden und mit `RUN` starten. Erzeugt mit [`tools/atascii_lst.py`](tools/atascii_lst.py).
- [`rollerball/spielen.html`](rollerball/spielen.html): **Rollerball II spielen.** Ein emulierter Atari 800 XL im Browser ([Sfotty Pie](https://github.com/cyco130/sfotty-pie), MIT) mit den freien AltirraOS- und Altirra-BASIC-ROMs, der das Original-Programm lädt. Eine einzige Datei, einfach öffnen. Gebaut mit [`tools/emulator/build.py`](tools/emulator/build.py) aus [`rollerball/ROLLER.BAS`](rollerball/ROLLER.BAS) (das tokenisierte Programm, erzeugt mit `tools/emulator/tokenize.ts`).
- [`rollerball/modern.html`](rollerball/modern.html): **Rollerball II als Neuauflage im Original-Look.** Eigenständige HTML-Datei in reinem JavaScript, ohne Emulator. Spielfeld bildschirmfüllend mit den PAL-Farben, Rohrteilen und dem Atari-Zeichensatz (aus dem freien AltirraOS), Regeln und Punkte wie im Listing. Beim Start wählt man Feldgröße (10×7, 14×9 oder Original 18×11) und Schwierigkeit (Zeit und Kugeltempo). Gesteuert wird per Wischen (das Loch wandert in Wischrichtung), ein Doppeltipp startet die Kugel; am Rechner gehen Pfeiltasten und Leertaste. Dazu Vollbild, Ton und Bestleistung je Einstellung.
- [`tools/scan_seiten.py`](tools/scan_seiten.py): lädt den Scan von Computer Kontakt 6-7/86 von archive.org und schneidet Seiten heraus (Standard: 76 bis 78), als PDF und als Bilder in voller Auflösung. Läuft automatisch als GitHub Action und legt das Ergebnis unter `scans/` ab.

## Inhalt (geplant)

- Abgetippte BASIC- und Maschinensprache-Listings
- Artikel und Begleittexte aus den Heften
- Hinweise zu Ausgabe, Seite und Quelle

## Struktur (Vorschlag)

```
magazin/
  ausgabe-JJJJ-MM/
    listing-name.bas
    artikel.md
```

## Hinweis

Die Rechte an den Originaltexten liegen bei den jeweiligen Verlagen und Autoren.
