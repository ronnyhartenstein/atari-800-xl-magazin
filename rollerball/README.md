# Rollerball II

„Rollerball II“ ist ein Abtipp-Spiel in Atari BASIC von Thomas Tausend. Es erschien in der Zeitschrift **Computer Kontakt 6-7/86** (Heft 20) auf den Seiten 77 bis 79. Genau dieses Listing hat Papa damals auf unserem Atari 800 XL abgetippt.

Dieser Ordner enthält das abgetippte Original und zwei spielbare Fassungen für den Browser:

| | [`spielen.html`](spielen.html): Original im Emulator | [`modern.html`](modern.html): Neuauflage |
|---|---|---|
| Was läuft | das echte BASIC-Programm auf einem emulierten Atari 800 XL | ein Nachbau in JavaScript, ohne Emulator |
| Aussehen | exakt wie damals, weil es das Original ist | wie damals: gleiche PAL-Farben, Rohrteile und Atari-Schrift, aber bildschirmfüllend |
| Spielgefühl | Tempo von Atari BASIC, also gemächlich | flüssige Animationen |
| Steuerung | Pfeiltasten schieben ein Teil ins Loch, Feuer mit Leertaste oder Strg, START mit Enter; auf dem Handy Tasten unter dem Bild | Wischen bewegt das Loch, Doppeltipp startet die Kugel; am Rechner Pfeiltasten und Leertaste |
| Extras | keine | Feldgröße und Schwierigkeit wählbar, Ton, Vollbild, Bestleistung |
| Start | der Atari bootet und baut das Feld auf, etwa 30 Sekunden | sofort |
| Größe | etwa 250 KB, weil Emulator und ROMs eingebettet sind | etwa 30 KB |

Beide sind eigenständige HTML-Dateien: herunterladen oder im Browser öffnen, fertig. Es gibt keine Installation und kein Netz, und beide laufen auch auf dem Handy.

## Das Spiel

Das Spielfeld besteht aus 18 × 11 zufällig verteilten Rohrteilen. Es gibt sieben Sorten: waagrecht, senkrecht, Kreuzung und vier Kurven. Ein Feld ist ein Loch, und ein Nachbarteil lässt sich hineinschieben, so wie bei einem Schiebepuzzle.

Links wartet die Kugel am Eingang, rechts ist irgendwo der Ausgang. Am rechten Rand läuft ein blauer Zeitbalken ab. Mit dem Feuerknopf, oder spätestens wenn die Zeit um ist, rollt die Kugel los und folgt den Rohren.

- **Punkte** gibt es für jedes befahrene Teil: Gerade 100, Kreuzung 70, Kurve 50. Eine Kreuzung zählt bei jeder Durchfahrt.
- **Gewonnen** ist die Runde, wenn die Kugel den Ausgang erreicht. Für jede übrige Zeiteinheit gibt es dann 25 Bonuspunkte.
- **Verloren** ist die Runde, wenn die Kugel ins Loch fällt, gegen den Rand rollt oder in ein Teil ohne passenden Anschluss läuft.

## Variante 1: das Original im Emulator (`spielen.html`)

Hier läuft das abgetippte Programm unverändert auf einem emulierten Atari 800 XL mit PAL-Bild. Nach dem Öffnen bootet der Rechner und lädt das Programm, dann erscheint das Titelbild.

- **Emulator:** [Sfotty Pie](https://github.com/cyco130/sfotty-pie) (MIT-Lizenz), gebündelt nach [`../tools/emulator/vendor/`](../tools/emulator/vendor/).
- **ROMs:** die freien Nachbauten AltirraOS und Altirra BASIC von Avery Lee. Es steckt also kein Original-ROM von Atari darin.
- **Programm:** [`ROLLER.BAS`](ROLLER.BAS) ist das tokenisierte BASIC-Programm. Es wurde mit [`../tools/emulator/tokenize.ts`](../tools/emulator/tokenize.ts) erzeugt: Das Listing wird im Emulator eingetippt und das Programm danach aus dem Speicher geholt.
- **Neu bauen:** `python3 tools/emulator/build.py` setzt aus [`../tools/emulator/page.html`](../tools/emulator/page.html), dem Emulator, den ROMs und `ROLLER.BAS` die Datei `spielen.html` zusammen.

## Variante 2: die Neuauflage (`modern.html`)

Die Neuauflage spielt sich wie das Original, ist aber in reinem JavaScript auf einem Canvas neu geschrieben.

**Was vom Original stammt:**

- Die Rohrteile sind Pixel für Pixel aus dem umdefinierten Zeichensatz des Listings übernommen, mit grünem Gitter auf ockerfarbenem Grund. Befahrene Rohre färben sich lila.
- Die Farben sind die PAL-Werte der Farbregister, die das Programm setzt.
- Die Schrift ist der Atari-Zeichensatz aus AltirraOS.
- Die Bildschirme sehen aus wie im Original: Titelbild, Punktezeile oben, „> ROLLERBALL II (c) Thomas Tausend <“ unten, „+++ FEHLER! +++“ und „GRATULIERE!“.
- Laufregeln, Punkte, Zeitbalken und Bonus folgen den BASIC-Zeilen 80 bis 175.
- Die Töne sind den `SOUND`-Befehlen nachempfunden.

**Was neu ist:**

- **Startmenü:** Nach dem Titelbild wählt man die Feldgröße (Klein 10 × 7, Mittel 14 × 9, Original 18 × 11) und die Schwierigkeit. Leicht hat 90 Sekunden und eine langsame Kugel, Normal 60 Sekunden, Schwer 35 Sekunden und eine schnelle Kugel. Die Auswahl wird gespeichert.
- **Wischsteuerung:** Finger halten und wischen schiebt das Loch in diese Richtung, und das Nachbarteil rutscht hinein. Wischt man ohne Absetzen weiter, wandert das Loch gleich ein Feld weiter. Ein Doppeltipp startet die Kugel. Nichts verdeckt das Spielfeld.
- **Tastatur:** Pfeiltasten oder WASD bewegen das Loch, Leertaste oder Enter ist Feuer, M schaltet den Ton, F das Vollbild.
- **Vollbild und Querformat:** Das Spielfeld füllt den Bildschirm. Der Vollbild-Knopf erscheint nur, wo der Browser ihn erlaubt; auf dem iPhone genügt es, das Handy quer zu halten.
- **Bestleistung:** Sie wird im Browser gespeichert, getrennt für jede Kombination aus Feldgröße und Schwierigkeit.

**Abweichungen vom Original, mit Absicht:**

- Im Original gibt der Joystick an, in welche Richtung das *Teil* rutscht. In der Neuauflage wandert das *Loch* in Wischrichtung, das fühlt sich auf dem Touchscreen natürlicher an.
- Im Original springt die Kugel von Feldmitte zu Feldmitte. In der Neuauflage rollt sie gleichmäßig.
- Wenn die Kugel im Kreis fährt, hängt das Original endlos fest. Die Neuauflage beendet die Runde nach 800 Feldern.

## Das Listing

- [`rollerball2.txt`](rollerball2.txt) ist das Listing als lesbarer Text, abgetippt vom Scan des Heftes. Grafik- und Steuerzeichen stehen als Platzhalter drin, zum Beispiel `{^A}` für Ctrl-A, `{DOWN}`/`{LEFT}` für Cursortasten und `{INV}…{/INV}` für inverse Zeichen.
- [`ROLLER.LST`](ROLLER.LST) ist dasselbe Listing als ATASCII-Datei für einen echten Atari oder Emulator wie Altirra: `ENTER "D:ROLLER.LST"`, dann `RUN`. Erzeugt mit [`../tools/atascii_lst.py`](../tools/atascii_lst.py).
- Die Scans der Heftseiten liegen unter [`../scans/`](../scans/).

Bei ein paar Stellen war der Scan schwer lesbar: Zeilen 2, 50, 66 (`SOUND 0,N`) und 71 (`POKE 82,0`). In Zeile 154/155 steht im Heft eine Hilfsvariable `MS`. Wer sie als `NS` liest, bekommt eine Endlosschleife beim Punktezählen.

## Rechte

Das Spiel und das Listing stammen von Thomas Tausend und erschienen in Computer Kontakt 6-7/86. Die Rechte liegen beim Autor bzw. Verlag. Sfotty Pie steht unter der MIT-Lizenz ([`../tools/emulator/vendor/LICENSE-sfotty-pie.txt`](../tools/emulator/vendor/LICENSE-sfotty-pie.txt)). AltirraOS und Altirra BASIC sind von Avery Lee frei weitergebbar.
