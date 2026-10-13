# Recording the vendor app on Windows (Wireshark + USBPcap)

Goal: see exactly what the official app sends, to decode macros, any reload/reset command and confirm the light format.

## Part 1: install and try the vendor app
1. Back up first: open the web app in Chrome, **Connect keyboard**, **More tools → Download backup**. Close the tab.
2. Run `MKESPN-K808___.20250610.exe` (if SmartScreen warns: **More info → Run anyway**) and install.
3. Open **Gaming Keyboard** with the keypad plugged in.
4. Change key `5` to **B**, click the green ✓, then press `5` in Notepad **without unplugging**. Does it type `b`? (Tells us whether the vendor app can apply changes without a replug.)

## Part 2: record
1. Install Wireshark from https://www.wireshark.org/download.html and tick **Install USBPcap**. Restart the PC.
2. Open Wireshark. On the start screen, press keys on the keypad and watch which **USBPcapN** graph moves. Double-click it to start recording.
3. In the vendor app do, with ~5 seconds between each, and **write down the order**:
   1. key `5` → **B**, ✓
   2. key `5` → **5**, ✓
   3. Light mode → **Constant**, ✓
   4. a simple macro (e.g. types `ab`) on key `0`, ✓
   5. **Reset** (if there is one), ✓
4. Stop (red ■), **File → Save As** `k808-capture.pcapng`.
5. Share the file and your list of actions.

Close the vendor app afterwards; don't run it at the same time as the web app.
