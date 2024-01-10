import time

from machine import Pin, SoftI2C

# Define I2C bus
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))

# TCN75A address, 0x48(72)
TCN75A_ADDR = 0x48
TCN75A_ADDR2 = 0x49

print(i2c.scan())

time.sleep(1)


while True:
    # Read data back from 0x00(0), 2 bytes
    # temp MSB, temp LSB
    data = i2c.readfrom_mem(TCN75A_ADDR, 0x00, 2)
    data2 = i2c.readfrom_mem(TCN75A_ADDR2, 0x00, 2)

    # Convert the data to 13-bits
    temp = ((data[0] << 8) | (data[1] & 0xFF)) / 128
    temp2 = ((data2[0] << 8) | (data2[1] & 0xFF)) / 128

    # Output data to console
    print("Temperature in Celsius is : %.4f C, %.2f C" % (temp, temp2))

    # Wait for a second before reading the data again
    time.sleep(0.1)
