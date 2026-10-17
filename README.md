# Atari 800 XL Magazin – getippte Texte

Sammlung abgetippter Texte und Listings aus Zeitschriften rund um den Atari 800 XL.

> ⚠️ Platzhalter: Diese README ist noch ein Dummy und wird später ausgebaut.

## Inhaltsverzeichnisse ATARImagazin 1987

[`index.html`](index.html) listet die Inhaltsverzeichnisse aller sechs Hefte des ATARImagazins (Verlag Rätz-Eberle) von 1987, mit Suchfeld und Filtern (nur Listings, nur XL/XE, Spieletests). Die Datei läuft ohne Build direkt im Browser, auch auf dem Handy: einfach öffnen.

Grundlage sind die OCR-Volltexte der Scans auf archive.org bzw. Atarimania; unsichere Einträge sind markiert. Das Heft erschien erst ab Januar 1987, für 1986 gibt es keine Ausgaben.

## Rollerball

- [`rollerball/`](rollerball/index.html): das Rollerball-Listing aus dem Chat, lauffähig im Browser über einen kleinen Atari-BASIC-Interpreter. Achtung, das Listing ist sehr wahrscheinlich eine KI-Nachbildung und nicht der Originalcode aus dem Heft.
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
