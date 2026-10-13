# Project history

How the K808 Configurator was built (October 2026), and what was learned along the way.

## 1. Studying the vendor software
- The driver `MKESPN-K808___.20250610.exe` is an Inno Setup installer. Unpacked (not run) it contains `Gaming Keyboard.exe` (32-bit MFC app) plus INI configs and skin images.
- The app talks plain **USB HID** (no custom driver): `HidD_SetFeature` / `HidD_GetFeature` on the vendor interface (usage page `0xFF01`), feature report ID `7`.
- Disassembly gave the device IDs (VID `0x30FA` "Instant", PID `0x2350`), the packet layout (`07 18 cmd idx addrLo addrHi data len`) and the read/write sequences.

## 2. First contact through the browser (WebHID)
- A read-only page confirmed the interfaces on the real keypad (0x000C, 0xFF00, 0xFF01 with feature report 7, 0x0001).
- First reads returned `07 07 07...`: Chrome includes the report ID at index 0. Fixed; the keypad then returned its own VID/PID from address `0x0000`.
- A memory dump (`0x0000-0x03FF`) revealed two key tables (`0x0020`, `0x0128`, one byte per key every 8 bytes), light settings near `0x00E0`, and macro data at `0x0240-0x031F`.

## 3. First write
- Key 11 was changed to `f` with cmd 3 / 9 / 1. After a replug the `.` key typed `f`. Writing works and persists.
- Side effect: the keypad stops typing after a write until it is replugged.

## 4. Hosting
- Deployed as a static Cloudflare Worker with Workers Builds from GitHub `main`. The git commit is shown in the page title.

## 5. Chasing the freeze and the "lost" saves
- Found the vendor's full write session in the exe: a begin packet `07 09 41 00`, block writes, and a finish pair `0x11` + `0`. Added them; keys still froze until replug.
- Found the keypad drops off USB during writes; the page now reconnects automatically.
- Saves then seemed to be lost after a replug. The real cause, found from a debug report: the keypad has **two key tables** and bit 7 of the settings byte at `0x00E0` (vendor name **KEYSMODE**) chooses between them. The keypad had switched to the keypad table `0x0020` while the page edited `0x0128`.
- Fix: read KEYSMODE on connect, edit the active table and write both by default. Confirmed on hardware: a key changed to `a` worked after a replug.

## 6. The vendor-style app
- New main page laid out like the vendor app: Button / Light / Macro tabs, keyboard picture with knob Roll- / Roll+, key dialog (Default, Disable, Media, Keyboard keys...), Configurations with •••, green ✓ / red ✗.
- Light settings decoded from the vendor code: 7 colors as 4-bit RGB nibbles at `0x00E1-0x00EE`; mode/speed/brightness/direction/symmetry/color select at `0x00F8-0x00FB`. Decoding the real dump gave exactly the vendor default colors.
- After saving, a popup guides the replug and re-checks the keys.

## 7. Open questions
- No reload/reset command exists in the vendor app; a replug seems unavoidable.
- What switches KEYSMODE on the keypad itself (a hidden key combination?).
- Macro format and how a key is assigned a macro.
- Media and knob codes need testing.
- Next step: record the vendor app on Windows with Wireshark ([guide](WINDOWS_CAPTURE.md)).

## Commit log
See `git log` for every change; each one is also shown in the app header when deployed.
