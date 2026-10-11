#!/usr/bin/env python3
"""Command-line tool for the K808 macro keyboard (VID 0x30FA, PID 0x2350).

Same protocol as the web page (see docs/PROTOCOL.md). Runs on your own PC.
  pip install hidapi
  python tools/k808.py info
  python tools/k808.py dump                 # hex dump 0x0000-0x03ff
  python tools/k808.py backup my.json       # save full dump
  python tools/k808.py keys                 # show key table @0x0128
  python tools/k808.py set 11 0x09          # key# 11 -> HID usage 0x09 ('f'), auto-backup first
  python tools/k808.py restore my.json      # restore key table from a backup
After any write: unplug the keyboard for 5 seconds and plug it back in.
Not tested on hardware by its author: try read-only commands first.
"""
import json, sys, time
import hid

VID, PID = 0x30FA, 0x2350
TABLE = 0x128
NKEYS = 12


def open_dev():
    for d in hid.enumerate(VID, PID):
        if d["usage_page"] == 0xFF01:
            h = hid.device()
            h.open_path(d["path"])
            return h
    sys.exit("K808 vendor interface (usage page 0xFF01) not found. Is it plugged in and the official app closed?")


def pkt(cmd, idx, lo, hi, data, last):
    return bytes([7, 0x18, cmd, idx, lo, hi, data, last])  # report ID 7 + 7 data bytes


def send(h, b):
    if h.send_feature_report(b) < 0:
        sys.exit("send_feature_report failed: " + str(h.error()))


def read_block(h, addr, n=8):
    lo, hi = addr & 0xFF, (addr >> 8) & 0xFF
    for i in range(n):
        send(h, pkt(3, i, lo, hi, 0, (n - 1) & 0xFF))
    time.sleep(0.001)
    send(h, pkt(0, 0, lo, hi, 0, 0))
    time.sleep(0.001)
    out = []
    for i in range(n):
        send(h, pkt(5, i, lo, hi, 0, (n - 1) & 0xFF))
        time.sleep(0.001)
        r = h.get_feature_report(7, 8)
        out.append(r[1])
    time.sleep(0.001)
    send(h, pkt(1, 0, 0, 0, 0, 0))
    return out


def write_byte(h, addr, val):
    lo, hi = addr & 0xFF, (addr >> 8) & 0xFF
    send(h, pkt(3, 0, lo, hi, val, 0))
    time.sleep(0.002)
    send(h, pkt(9, 0, lo, hi, 0, 0))
    time.sleep(0.010)
    send(h, pkt(1, 0, lo, hi, 0, 0))
    time.sleep(0.010)
    return read_block(h, addr, 1)[0]


def dump(h, start=0, end=0x3FF):
    data = []
    for a in range(start, end + 1, 8):
        data += read_block(h, a, 8)
    return data


def cmd_info(h):
    b = read_block(h, 0, 8)
    print("block 0x0000:", " ".join(f"{x:02x}" for x in b))
    print("PID in memory: 0x%04x  VID in memory: 0x%04x" % (b[3] | b[4] << 8, b[5] | b[6] << 8))


def cmd_dump(h):
    d = dump(h)
    for a in range(0, len(d), 8):
        print(f"0x{a:04x}: " + " ".join(f"{x:02x}" for x in d[a:a + 8]))


def cmd_backup(h, path):
    d = dump(h)
    with open(path, "w") as f:
        json.dump({"vid": VID, "pid": PID, "start": 0, "hex": bytes(d).hex()}, f)
    print("saved", path)


def cmd_keys(h):
    for k in range(NKEYS):
        print(f"key {k:2d}: 0x{read_block(h, TABLE + k * 8, 1)[0]:02x}")


def cmd_set(h, key, code):
    if not 0 <= key < NKEYS:
        sys.exit("key must be 0-11")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    cmd_backup(h, f"k808-backup-{stamp}.json")
    before = read_block(h, TABLE + key * 8, 1)[0]
    after = write_byte(h, TABLE + key * 8, code)
    print(f"key {key}: 0x{before:02x} -> 0x{code:02x}, read back 0x{after:02x}", "OK" if after == code else "MISMATCH")
    print("Now unplug the keyboard for 5 seconds and plug it back in.")


def cmd_restore(h, path):
    with open(path) as f:
        data = bytes.fromhex(json.load(f)["hex"])
    for k in range(NKEYS):
        a = TABLE + k * 8
        now = read_block(h, a, 1)[0]
        if now != data[a]:
            print(f"key {k}: 0x{now:02x} -> 0x{data[a]:02x} (read back 0x{write_byte(h, a, data[a]):02x})")
    print("Done. Unplug and replug the keyboard.")


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    h = open_dev()
    c = argv[1]
    if c == "info": cmd_info(h)
    elif c == "dump": cmd_dump(h)
    elif c == "backup": cmd_backup(h, argv[2])
    elif c == "keys": cmd_keys(h)
    elif c == "set": cmd_set(h, int(argv[2], 0), int(argv[3], 0))
    elif c == "restore": cmd_restore(h, argv[2])
    else: sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
