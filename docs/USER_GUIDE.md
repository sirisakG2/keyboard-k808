# K808 Configurator: user guide

## What you need
- The K808 keypad plugged into USB.
- **Chrome or Edge** on a computer (Windows, macOS, Linux, ChromeOS). Not Firefox/Safari, not phones.
- Close the vendor app (*Gaming Keyboard*) if it is running.

Open https://keyboard-k808.sirisak-anotai.workers.dev. The version (git commit) is shown next to "K808" and in the tab title; hard refresh (Ctrl+Shift+R / Cmd+Shift+R) to get the newest.

## 1. Connect
1. Click **Connect keyboard** (top right).
2. Pick **USB Keyboard** in the browser popup and click **Connect**.
3. The keys load onto the picture. The chip **Key mode 0/1** shows which key table the keypad is using.

## 2. Change a key
1. Click a key on the picture (or **Roll- / Roll+** for the knob).
2. In the popup pick a category on the left:
   - **Keyboard keys**: Common (Enter, Space, Esc...), Arrows, Letters, Numbers, F keys, Symbols, Keypad, Modifiers. Use the search box.
   - **Media**: Play/Pause, Vol+/-, Mute, Next... (not tested yet)
   - **Default**: factory function of that key.
   - **Disable**: key does nothing (not tested yet).
3. Click **OK** (top of the popup). The key gets a yellow dot.
4. Change more keys if you like, then press the green **✓** at the bottom to save.
5. The page asks you to **unplug the keypad, wait 3 seconds, plug it back in**. Then click **"It's plugged back in - check my keys"**. (Chrome may show the picker again; pick the keypad.)
6. The page confirms the keys are stored. Your new keys work now.

The red **✗** undoes unsaved changes.

## 3. Configurations (profiles)
At the bottom, **Configurations** works like the vendor app:
- **••• → New configuration from current keys**: save the keys on screen under a name.
- Pick a configuration in the dropdown: its keys load onto the picture. Press **✓** to write them to the keypad (then replug).
- **••• → Save / Rename / Delete / Export all to file / Import from file**.
Configurations live in your browser. Export them to a file to keep them safe or move them to another computer. `(before last save)` is created automatically before every save as an undo.

## 4. Light (experimental)
Open the **Light** tab: Mode, Brightness, Speed, Colors (one color or cycle through ticked colors), Symmetry, Direction. Click **Save light to keyboard**. Not tested on a real keypad yet: please report what happens.

## 5. More tools (below the keyboard)
- **Download a backup file**: on by default for the first save of each visit. Restore with **Restore keys from a backup file**.
- **Save keys to both key modes**: on by default (recommended).
- **Save method**: *Simple* (default, proven) or *Vendor-style*.
- **Unfreeze keyboard**, **Find what freezes the keyboard**: diagnostics.
- **Advanced page** (key test, calibration) and **Developer tools** (memory dump, raw commands).
- **Copy debug report** (top bar): copies version, keys and log; paste it when asking for help.

## Troubleshooting
| Problem | Fix |
|---|---|
| No keypad in the popup | Use Chrome/Edge; plug the keypad directly (no hub); close the vendor app. |
| Saved but the key didn't change | Unplug and replug the keypad. Check the **Key mode** chip; keep "save to both modes" ticked. |
| Keys stop typing after saving | Expected until you replug. |
| Popup stays open after replug | Click "It's plugged back in - check my keys". |
| `.` key types § or ` on a Mac | That is the backtick code on a non-US layout; assign another key. |
| Something looks wrong | Click **Copy debug report** and send it. |
