from __future__ import division
from Adafruit_LED_Backpack.Matrix8x8 import Matrix8x8
from Adafruit_PCA9685 import PCA9685
import time


class ServoDriver(PCA9685):

    def __init__(self, **kwargs):
        super(ServoDriver, self).__init__(**kwargs)
        self.frequency = 100  # Hz
        self.set_pwm_freq(self.frequency)
        self.min_angle = 0
        self.max_angle = 128
        self.min_pulse_length = 200  # Out of 4096 (length of cycle)
        self.max_pulse_length = 1000  # Out of 4096 (length of cycle)

    def move(self, channel, angle):
        t = int(self.max_pulse_length - (angle / self.max_angle)
                * (self.max_pulse_length - self.min_pulse_length))
        self.set_pwm(channel, 0, t)


class LEDDisplay(Matrix8x8):

    def __init__(self, **kwargs):
        super(LEDDisplay, self).__init__(**kwargs)
        self.begin()

    def draw(self, image):
        self.clear()
        for y in range(8):
            for x in range(8):
                self.set_pixel(x, y, image[7-x][7-y])
        self.write_display()

    def shutOff(self):
        self.clear()
        self.write_display()


class Faces:
    a = [
        [0,0,0,0,0,0,0,0],
        [0,1,1,0,0,1,1,0],
        [0,1,1,0,0,1,1,0],
        [0,1,1,0,0,1,1,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0]]

    b = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,1,0],
        [0,1,1,0,0,1,1,0],
        [0,0,0,0,0,0,0,0],
        [1,0,0,1,1,0,0,1],
        [0,0,1,1,1,1,0,0],
        [1,0,0,0,0,0,0,1]]


class Leg:

    def __init__(self, id, upperOffset=0, lowerOffset=0):
        self.id = id
        if self.id in [1,2,6]:
            self.left = True
            self.right = False
        elif self.id in [3,4,5]:
            self.left = False
            self.right = True
        self.lowerOffset = lowerOffset
        self.upperOffset = upperOffset
        self.lowerChannel = (self.id - 1) * 2 + 1
        self.upperChannel = (self.id - 1) * 2
        self.lowerRestAngle = 45 + 20
        self.upperRestAngle = 70
        self.backLowerOffset = 50

    def moveLower(self, angle):
        if self.left:
            servoDriver.move(self.lowerChannel, self.lowerRestAngle + angle + self.lowerOffset)
        elif self.right:
            servoDriver.move(self.lowerChannel, servoDriver.max_angle - (self.lowerRestAngle + angle + self.lowerOffset))

    def moveUpper(self, angle):
        if self.left and self.id != 6 or self.id == 3:
            if self.id == 3:
                servoDriver.move(self.upperChannel, self.upperRestAngle + angle + self.backLowerOffset + self.upperOffset)
            else:
                servoDriver.move(self.upperChannel, self.upperRestAngle + angle + self.upperOffset)
        elif self.right and self.id != 3 or self.id == 6:
            if self.id == 6:
                servoDriver.move(self.upperChannel, servoDriver.max_angle - (self.upperRestAngle + angle + self.backLowerOffset + self.upperOffset) + 45)
            else:
                servoDriver.move(self.upperChannel, servoDriver.max_angle - (self.upperRestAngle + angle + self.upperOffset) + 45)
