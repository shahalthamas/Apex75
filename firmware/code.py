# AI-GENERATED FIRMWARE — untested on physical hardware.
# Target: CircuitPython on Raspberry Pi Pico 2 W (RP2350).
# Review the provisional keymap and pin mapping before flashing.

import board
import keypad
import rotaryio
import usb_hid

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode as K


# Pin nets verified against production/netlist.ipc:
# ROW1..ROW6 -> Pico GPIO2..GPIO7
# COLUMN1..COLUMN15 -> Pico GPIO8..GPIO22
# REA / REB -> Pico GPIO26 / GPIO27
MATRIX_ROWS = (
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
)

MATRIX_COLUMNS = (
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15,
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19,
    board.GP20,
    board.GP21,
    board.GP22,
)

ENCODER_A = board.GP26
ENCODER_B = board.GP27


# Entries are ordered by physical ROW1..ROW6, then COLUMN1..COLUMN15.
# Empty matrix locations are None. The key legends are a provisional ANSI-style
# layout inferred from the switch positions; review them against the intended
# keycap layout before use. No custom Fn layer is implemented yet.
KEYMAP = (
    # ROW1: Esc and F1-F12
    (
        K.ESCAPE, K.F1, K.F2, K.F3, K.F4, K.F5, K.F6, K.F7, K.F8,
        K.F9, K.F10, K.F11, K.F12, None, None,
    ),
    # ROW2: number row, Backspace, Delete
    (
        K.GRAVE_ACCENT, K.ONE, K.TWO, K.THREE, K.FOUR, K.FIVE, K.SIX,
        K.SEVEN, K.EIGHT, K.NINE, K.ZERO, K.MINUS, K.EQUALS,
        K.BACKSPACE, K.DELETE,
    ),
    # ROW3: tab row and right-side navigation
    (
        K.TAB, K.Q, K.W, K.E, K.R, K.T, K.Y, K.U, K.I, K.O, K.P,
        K.LEFT_BRACKET, K.RIGHT_BRACKET, K.BACKSLASH, K.INSERT,
    ),
    # ROW4: home row; column 14 is unpopulated on the PCB
    (
        K.CAPS_LOCK, K.A, K.S, K.D, K.F, K.G, K.H, K.J, K.K, K.L,
        K.SEMICOLON, K.QUOTE, K.ENTER, None, K.HOME,
    ),
    # ROW5: shift row and arrow/navigation keys
    (
        K.LEFT_SHIFT, None, K.Z, K.X, K.C, K.V, K.B, K.N, K.M,
        K.COMMA, K.PERIOD, K.FORWARD_SLASH, K.RIGHT_SHIFT,
        K.UP_ARROW, K.END,
    ),
    # ROW6: bottom row. The wide spacebar switch is at column 7.
    (
        K.LEFT_CONTROL, K.LEFT_GUI, K.LEFT_ALT, None, None, None,
        K.SPACE, None, None, K.RIGHT_ALT, K.RIGHT_GUI, K.APPLICATION,
        K.LEFT_ARROW, K.DOWN_ARROW, K.RIGHT_ARROW,
    ),
)

assert len(KEYMAP) == 6
assert all(len(row) == 15 for row in KEYMAP)

keyboard = Keyboard(usb_hid.devices)
consumer = ConsumerControl(usb_hid.devices)

# On RP2350, CircuitPython documents swapping the scanner axes and using
# columns_to_anodes=True when the diode direction would otherwise require
# pull-downs. In this swapped scanner, scanner columns are physical ROW pins,
# which are on the diode anodes in this PCB design.
matrix = keypad.KeyMatrix(
    row_pins=MATRIX_COLUMNS,
    column_pins=MATRIX_ROWS,
    columns_to_anodes=True,
    interval=0.02,
    max_events=128,
    debounce_threshold=2,
)

encoder = rotaryio.IncrementalEncoder(ENCODER_A, ENCODER_B, divisor=4)
last_encoder_position = encoder.position

while True:
    event = matrix.events.get()
    if event is not None:
        # The scanner's row axis is the 15 physical columns; its column axis
        # is the 6 physical rows. Convert the event back to ROW/COLUMN order.
        physical_column = event.key_number // len(MATRIX_ROWS)
        physical_row = event.key_number % len(MATRIX_ROWS)
        keycode = KEYMAP[physical_row][physical_column]

        if keycode is not None:
            if event.pressed:
                keyboard.press(keycode)
            else:
                keyboard.release(keycode)

    position = encoder.position
    while position > last_encoder_position:
        consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        last_encoder_position += 1
    while position < last_encoder_position:
        consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        last_encoder_position -= 1
