import time
import board
import busio

FREQ_MOD = 3

i2c = busio.I2C(board.GP17, board.GP16, frequency=10000)

while not i2c.try_lock():
    pass
print("I'm unlocked!")

time.sleep(0.01)

print([hex(x) for x in i2c.scan()])

time.sleep(0.01)

# device = I2CDevice(i2c, 0x52)
data = bytearray(7)

i2c.writeto(0x52, bytes([0x40, 0x00]))
time.sleep(0.01)

ZERO_BYTES = bytes([0x00])

while True:
    i2c.writeto(0x52, ZERO_BYTES)
    time.sleep(0.01)
    i2c.readfrom_into(0x52, data)
    # i2c.writeto_then_readfrom(0x52, bytes([0x00]), data, out_start=0)
    # print(data)
    # time.sleep(1)

    dataA = 0x17 + (0x17 ^ data[4])
    dataB = 0x17 + (0x17 ^ data[5])

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
    print("---o")
    print(bin(dataA), bin(dataB))
    print("o---")
