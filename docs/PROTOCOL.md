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
