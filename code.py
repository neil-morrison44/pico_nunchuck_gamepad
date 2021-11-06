import time
import board
import busio
import usb_hid
from gamepad import Gamepad

FREQ_MOD = 3

i2c = busio.I2C(board.GP17, board.GP16, frequency=10000)

while not i2c.try_lock():
    pass
gamepadDevice = [dev for dev in usb_hid.devices if dev.usage is 0x5][0]
gp = Gamepad(gamepadDevice)
time.sleep(0.02)

# https://circuitpython.readthedocs.io/projects/hid/en/latest/examples.html#simple-gamepad


buttons = [False for i in range(0, 16)]
data = bytearray(7)

i2c.writeto(0x52, bytes([0x40, 0x00]))
time.sleep(0.01)

ZERO_BYTES = bytes([0x00])


def setButton(index, pressed):
    if ((not buttons[index]) and pressed):
        # print(index, "press")
        gp.press_buttons([index + 1])
    elif(buttons[index] and not pressed):
        # print(index, "unpress")
        gp.release_buttons([index + 1])
    buttons[index] = pressed


while True:
    i2c.writeto(0x52, ZERO_BYTES)
    time.sleep(0.01)
    i2c.readfrom_into(0x52, data)

    dataA = 0x17 + (0x17 ^ data[4])
    dataB = 0x17 + (0x17 ^ data[5])

    setButton(0, not (dataB & ~0b11111110))  # UP
    setButton(1, not (dataB & ~0b11111101))  # LEFT
    setButton(2, not (dataA & ~0b10111111))  # DOWN
    setButton(3, not (dataA & ~0b01111111))  # RIGHT
    setButton(4, not (dataA & ~0b11011111))  # L
    setButton(5, not (dataA & ~0b11111101))  # R
    setButton(6, not (dataB & ~0b11101111))  # A
    setButton(7, not (dataB & ~0b10111111))  # B
    setButton(8, not (dataB & ~0b11011111))  # Y
    setButton(9, not (dataB & ~0b11110111))  # X
    setButton(10, not (dataA & ~0b11101111))  # SELECT
    setButton(11, not (dataA & ~0b11111011))  # START

    gp.send()
