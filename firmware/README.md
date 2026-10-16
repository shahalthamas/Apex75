# Apex 75 firmware

**AI-generated firmware. Hardware testing has not been done.**

`code.py` is a CircuitPython USB keyboard starting point for a Raspberry Pi Pico 2 W. It scans the six-by-fifteen switch matrix and uses the encoder to send volume up/down consumer-control reports.

## Install

1. Install a CircuitPython build for Raspberry Pi Pico 2 W.
2. Copy `adafruit_hid` from the Adafruit CircuitPython library bundle to `CIRCUITPY/lib/adafruit_hid`.
3. Copy `code.py` to the root of the `CIRCUITPY` drive.
4. Verify every key position and the encoder with a keyboard tester before relying on it.

## Hardware mapping

The row and column nets and Pico pad assignments were read from `production/netlist.ipc`:

| Net | Pico GPIO |
| --- | --- |
| ROW1–ROW6 | GP2–GP7 |
| COLUMN1–COLUMN15 | GP8–GP22 |
| REA, REB | GP26, GP27 |

The production netlist connects encoder A/B only. The encoder's push contact is unconnected. The `KEYMAP` in `code.py` is a provisional ANSI-style mapping based on switch positions, and needs review against the intended keycap layout. No Fn layer or VIA support is implemented.

The PCB diode anodes are on the switch/row side and their cathodes face the column side. The scanner swaps its row and column arrays and uses `columns_to_anodes=True` for the RP2350 workaround described in the [CircuitPython keypad documentation](https://docs.circuitpython.org/en/10.3.1/shared-bindings/keypad/index.html).

## Credit

The source in this folder was generated with AI at the project author's request. It uses CircuitPython's built-in `keypad` and `rotaryio` modules and Adafruit's separately installed `adafruit_hid` library.
