import machine
import time

GAMEPAD_ADDR = 0x52

FREQ_MOD = 3

# Create I2C object
i2c = machine.I2C(0, scl=machine.Pin(
    17), sda=machine.Pin(16), freq=int(100000 * FREQ_MOD))

# writeToNunchuck(0x40, 0x00)
i2c.writeto_mem(GAMEPAD_ADDR, 0x40, b'\x00')
time.sleep(0.05)
# writeToNunchuck(0xA400FB, 0xFB)


def reconnect():
    i2c.writeto_mem(GAMEPAD_ADDR, 0x40, b'\x00')
    time.sleep(0.05 / FREQ_MOD)


while True:
    i2c.writeto(GAMEPAD_ADDR, b'\x00')
    time.sleep(0.05 / FREQ_MOD)
    data = i2c.readfrom(GAMEPAD_ADDR, 6)
    # print(data[1])

    if (data[1] == 255):
        reconnect()
    else:
        dataA = 0x17 + (0x17 ^ data[4])
        dataB = 0x17 + (0x17 ^ data[5])
        # print(bin(dataA), bin(dataB))

        if not (dataB & ~0b11111110):
            print("UP")
        if not (dataB & ~0b11111101):
            print("LEFT")
        if not (dataA & ~0b10111111):
            print("DOWN")
        if not (dataA & ~0b01111111):
            print("RIGHT")
        if not (dataA & ~0b11011111):
            print("L")
        if not (dataA & ~0b11111101):
            print("R")
        if not (dataB & ~0b11101111):
            print("A")
        if not (dataB & ~0b10111111):
            print("B")
        if not (dataB & ~0b11011111):
            print("Y")
        if not (dataB & ~0b11110111):
            print("X")
        if not (dataA & ~0b11101111):
            print("SELECT")
        if not (dataA & ~0b11111011):
            print("START")
    # time.sleep(0.05)
