# K808 protocol notes (from static analysis of `Gaming Keyboard.exe`, build 2025-06-10)

Status: **unverified against real hardware.** Found by reading the vendor app's code, not by sniffing traffic.

## Device
- Primary: VID `0x30FA`, PID `0x2350` (30FA = "Instant" in the USB-IF list; matches the app copyright).
- The app also accepts a second pair stored as VID `0x2130`, PID `0x30FA` (probably a firmware/bootloader variant or a vendor typo).
- Talks over plain USB HID (`HID.DLL`, `SETUPAPI`); no custom driver.

## Interfaces
The app enumerates HID devices and picks vendor-defined collections:
- Usage page `0xFF00`, usage `1` -> opened read-only (likely input/status).
- Usage page `0xFF01`, usage `1` -> opened write; **this is the one that receives the feature reports below.**

## Feature report (report ID `0x07`)
Sent with `HidD_SetFeature`, read with `HidD_GetFeature`. Buffer length = `FeatureReportByteLength` from the device caps.

Observed layout (byte 0 = report ID):

| byte | meaning |
|------|---------|
| 0 | `0x07` report ID |
| 1 | `0x18` constant |
| 2 | command: `3` = write byte, `5` = read request, `1` = end/commit (`07 18 01 00 ...`), `9` = block write/commit (`07 18 09 00 ...`) |
| 3 | running index within the transfer |
| 4 | address low byte |
| 5 | address high byte |
| 6 | data byte (write) |
| 7 | length-related byte: `len-1` or `len+0x5f` depending on a global mode flag (meaning not yet understood) |

Typical write: loop `cmd=3` per byte, then `cmd=1`/`cmd=9` to commit, sleeping between steps (1-10 ms).
Typical read: `cmd=5` request, then `GetFeature` with first byte `7`; the answer byte is at index 1 of the returned buffer.

## Config files shipped with the app
- `config/KBconfig.ini`: key matrix as USB HID usage codes (30-39 = digits 1-0, 40 = Enter, 53 = backtick, 255 = unused).
- `config/config.ini`, `reset_config.ini`: RGB effect settings.
- `skins/*/defMacro.dat`, `macroGrp.ini`: macro storage.

## Open questions
- Exact meaning of byte 7 and the global mode flag at `0x63dda8`.
- Address map: where key matrix, RGB and macros live in keyboard memory.
- Best confirmed by a USBPcap capture of the official app.

## Verified on hardware (read path, 2026-10-11)
- WebHID `receiveFeatureReport(7)` returns the report ID at index 0; payload byte is index 1.
- Read of n bytes at addr: n x `cmd3` (zero staging), `cmd0` (load addr), n x `cmd5` + GetFeature, `cmd1` (end). Length byte = n-1 works.
- Device answers in 8-byte blocks; step addresses by 8.
- Memory map seen (0x0000-0x03ff):
  - `0x0000`: `b4 01 b4 | 50 23 (PID) | fa 30 (VID) | 4b` device info.
  - `0x0020 + 8*k`: key k (14 keys), HID usage code, e.g. `59 5a 5b 5c 5d 58 61 60 5f 5e 62 63 f4 e9` (keypad codes).
  - `0x0128 + 8*k`: second table `1e 52 20 21 22 28 26 4f 51 50 27 35 f4 e9` (differs from KBconfig.ini default: arrows on keys 1,7,8,9).
  - `0x0100-0x011f`: settings/LED nibbles (unknown).
  - `0x01d8-0x023f`: repeating `07 00 40 02 00` (unknown).
  - `0x0240-0x031f`: macro data (HID codes incl. `e0` LCtrl + `04/06/16/19`, i.e. Ctrl+A/C/S/V style).

## Profiles / layers (findings from the vendor app files, not verified on hardware)
- The vendor app keeps up to 5 profiles ("Config1".."Config5", names GAME / Normal / Profile4 / Profile5, `CurConfig`) in its PC-side `config/config.ini`. Switching profile in the app rewrites the keyboard; there is no sign of an on-keyboard profile switch.
- Special-function codes the app can assign to a key (skin_main.ini): Vol-, Vol+, Previous, Next, Player, Mail, WWW Forward/Stop/Back/Refresh/Search/Favourite, Mute, My Computer, Stop, Calculator, Web Browser, Full-key Lock, LED mode/color/speed/brightness/on-off, Roll Up/Down (knob). **No profile/layer switch function is listed.**
- `KBconfig.ini` has 8 rows x 20 columns (`N_M`); on the device each key owns an 8-byte slot (`0x20+8k` and `0x128+8k`), so byte j of a slot is probably row j. Only row 0 is used by default (rest 0xff). What selects the other rows is unknown.
- Free-looking memory: `0x0320-0x03f7` (all 0xff). Could hold stored profile copies, but nothing on the keyboard would switch to them by itself.

## Write session (found in vendor function 0x40fd80)
Vendor full write: `07 09 41 00 00 00 00 00` (begin, then Sleep 200 ms) -> optional erase loop (only if a mode flag is set: `07 18 81 00 lo hi 00 60` per 0x20 bytes, Sleep 100 ms, then `07 18 00 00 00 00 00 60`) -> GetFeature(7) -> data blocks written 8 bytes at a time (cmd 3 stage, cmd 9 commit, cmd 1 end) -> **finish: `07 18 11 00 00 00 00 00`, Sleep 10 ms, `07 18 00 00 00 00 00 00`**.
Our page never sent the finish pair, and the keyboard stopped typing after writes (until replug). The page now sends it after every write session (`finishWrite()`); there is also an "Unfreeze keyboard" button. Not yet verified on hardware.
