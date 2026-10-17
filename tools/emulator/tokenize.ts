import fs from "node:fs";
import { Atari } from "./src/machine.ts";
import { ReadOptions } from "@sfotty-pie/sfotty";
import { paletteFor } from "./src/palette.ts";
import { frameToPng } from "./src/screenshot.ts";
import { NTSC_CYCLES_PER_FRAME } from "./src/timing-constants.ts";
const FW = "../../apps/a8-web/library/firmware/";
const [out, pasteFile, basOut] = process.argv.slice(2);
const m = new Atari({ xl: true, os: new Uint8Array(fs.readFileSync(FW + "AltirraOS XL-XE.rom")), basic: new Uint8Array(fs.readFileSync(FW + "Altirra BASIC.rom")) });
const rd = (a: number) => m.mmu.read(a, ReadOptions.PEEK);
const w = (a: number) => rd(a) | (rd(a + 1) << 8);
let f = 0;
const frames = (n: number) => { for (let i = 0; i < n; i++) { for (let c = 0; c < NTSC_CYCLES_PER_FRAME; c++) m.cycle(); f++; } };
frames(150);
m.paste(fs.readFileSync(pasteFile!, "utf8"));
// wait until the statement table stops growing
let last = -1, stable = 0;
while (stable < 10) { frames(60); const s = w(0x8c); if (s === last) stable++; else { stable = 0; last = s; } }
console.log("paste done at frame", f, "seconds", (f / 60).toFixed(1));
fs.writeFileSync(`${out}/10-entered.png`, frameToPng(m.frame, paletteFor("ntsc")));
const lomem = w(0x80);
const ptrs = [0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c].map((z) => w(z) - lomem);
const starp = ptrs[6]!;
const hdr = new Uint8Array(14);
ptrs.forEach((p, i) => { hdr[i * 2] = p & 255; hdr[i * 2 + 1] = p >> 8; });
const body = new Uint8Array(starp - 256);
for (let i = 0; i < body.length; i++) body[i] = rd(lomem + 256 + i);
fs.writeFileSync(basOut!, Buffer.concat([hdr, body]));
console.log("lomem", lomem.toString(16), "ptrs", ptrs, "bytes", 14 + body.length);
// count lines in statement table
let p = lomem + ptrs[4]!, n = 0, lastLine = 0;
while (true) { const ln = w(p); if (ln >= 32768) break; n++; lastLine = ln; p += rd(p + 2); }
console.log("lines", n, "last", lastLine);
