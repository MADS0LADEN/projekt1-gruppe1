import time

from machine import Pin, SoftI2C

# Define I2C bus
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))

# TCN75A addresses
TCN75A_1 = 0x48
TCN75A_2 = 0x49

# 0.625 resolution
CONFIG_REG_ADDR = 0x01
CONFIG_VALUE = 0x60
i2c.writeto_mem(TCN75A_1, CONFIG_REG_ADDR, bytearray([CONFIG_VALUE]))
i2c.writeto_mem(TCN75A_2, CONFIG_REG_ADDR, bytearray([CONFIG_VALUE]))


class Sensor:
    def read(self):
        try:
            # Read data from TCN75A_ADDR
            data1 = i2c.readfrom_mem(TCN75A_1, 0x00, 2)
            temp1 = ((data1[0] << 8) | (data1[1] & 0xFF)) / 128

            # Read data from TCN75A_ADDR2
            data2 = i2c.readfrom_mem(TCN75A_2, 0x00, 2)
            temp2 = ((data2[0] << 8) | (data2[1] & 0xFF)) / 128
        except OSError:
            return (0, 0)

        return (temp1, temp2)

    def list(self):
        return i2c.scan()

    def diff(self):
        return abs(self.read()[0] - self.read()[1])


class Alarm:
    def __init__(self, sensor):
        self.sensor = sensor

    def check(self, reading1, reading2):
        diff = abs(reading1 - reading2)
        if diff < 1:
            return False
        elif 5 < diff > 1:
            return True
        else:
            return False


if __name__ == "__main__":
    sensor = Sensor()
    alarm = Alarm(sensor)
    while True:
        readings = sensor.read()
        print(alarm.check(readings))
        time.sleep(1)
