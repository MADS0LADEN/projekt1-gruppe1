import time

from machine import Pin, SoftI2C

# Define I2C bus
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))

# TCN75A addresses
TCN75A_ADDR = 0x48
TCN75A_ADDR2 = 0x49

CONFIG_REG_ADDR = 0x01
CONFIG_VALUE = 0x60

i2c.writeto_mem(TCN75A_ADDR, CONFIG_REG_ADDR, bytearray([CONFIG_VALUE]))
i2c.writeto_mem(TCN75A_ADDR2, CONFIG_REG_ADDR, bytearray([CONFIG_VALUE]))

while True:
    # Read data from TCN75A_ADDR
    data = i2c.readfrom_mem(TCN75A_ADDR, 0x00, 2)
    temp = ((data[0] << 8) | (data[1] & 0xFF)) / 128

    # Read data from TCN75A_ADDR2
    data2 = i2c.readfrom_mem(TCN75A_ADDR2, 0x00, 2)
    temp2 = ((data2[0] << 8) | (data2[1] & 0xFF)) / 128

    # print(data, data2)

    # Output data to console
    print(
        ("Temperature in Celsius is: %.2f C, %.2f C" % (temp, temp2)), abs(temp - temp2)
    )

    # Wait for 1 seconds before reading the data again
    time.sleep(1)
