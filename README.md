# K808 Configurator

A web app to configure the **MKESPN K808** 12-key macro keypad (USB VID `0x30FA`, PID `0x2350`) from the browser, without the vendor's Windows-only software. It is a clean-room re-creation: the USB protocol was worked out by reading the vendor app (`MKESPN-K808___.20250610.exe`) and testing on a real keypad.

**Live app:** https://keyboard-k808.sirisak-anotai.workers.dev
(Chrome or Edge on a desktop computer: the app uses WebHID, which Firefox and Safari don't support.)

## What works

| Feature | Status |
|---|---|
| Read the keypad's keys | Works (tested on hardware) |
| Change any of the 12 keys to a keyboard key | Works (tested). The keypad needs an **unplug/replug** after saving before it uses the new keys. |
| Two key modes (KEYSMODE) | Detected automatically; keys are saved to both tables by default |
| Knob Roll- / Roll+ | Editable, not tested yet |
| Media keys (Play/Pause, Vol+/-, Mute, ...) | Codes taken from the vendor app, not tested yet |
| Configurations (profiles) | Works; stored in the browser, export/import as a file |
| Light (mode, colors, brightness, speed, direction, symmetry) | Decoded from the vendor app; matches the real memory; saving not tested yet |
| Macros | Not done (format partly decoded) |
| Apply without replug | Not possible so far: the vendor app has no reload command either |

## Documents

- [User guide](docs/USER_GUIDE.md): how to use the app, step by step
- [Protocol notes](docs/PROTOCOL.md): USB commands, memory map, light and key formats
- [Project history](docs/HISTORY.md): how the project got here, what was learned
- [Windows capture guide](docs/WINDOWS_CAPTURE.md): record the vendor app with Wireshark to decode the rest

## Repository layout

| Path | What it is |
|---|---|
| `web/index.html` | Main app, laid out like the vendor app (Button / Light / Macro, Configurations, save) |
| `web/advanced.html` | Older editor with key test and calibration |
| `web/dev.html` | Developer tools: raw read, memory dump, single-byte write, freeze lab |
| `tools/k808.py` | Command-line tool (Python + `hidapi`): info, dump, backup, keys, set, restore |
| `docs/` | Documentation |
| `scripts/version.js` | Build step: writes `web/version.js` with the git commit shown in the page title |
| `wrangler.jsonc`, `package.json` | Cloudflare Workers (static assets) config |

## Deploying

The site is a static Cloudflare Worker connected with **Workers Builds** to this repo's `main` branch:

- Build command: `npm run build` (creates `web/version.js`)
- Deploy command: `npm run deploy:ci`

Every push to `main` redeploys automatically. Local preview: `npm install && npm run build && npx wrangler dev`.

## Command-line tool

```
pip install hidapi
python3 tools/k808.py info      # read-only
python3 tools/k808.py keys      # read-only
python3 tools/k808.py set 11 0x09   # key 11 -> 'f' (backs up first)
```

Note: the CLI edits table `0x0128` (key mode 1) only; the web app handles both key modes.

## Disclaimer

Not affiliated with MKESPN / Dongguan ShiXingSheng. Writing to the keypad is at your own risk; the app downloads a backup before the first write.
