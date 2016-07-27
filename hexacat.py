from websocket import RobotWebSocketServer
from hardware import LEDDisplay, ServoDriver

server = RobotWebSocketServer("10.0.0.1", 8080)
server.start()



# # Add scalable time in between steps to control speed
# # Add scalable angles for steering
#
# 1  4
# 2  5
# 3  6
# ----------
# upper,lower
# 0,1  6,7
# 2,3  8,9
# 4,5  10,11

# LOWER LEG
def liftup(legs):
    for leg in legs:
        leg.moveLower(lowerMoveAngle)

def setdown(legs):
    for leg in legs:
        leg.moveLower(0)

# UPPER LEG
def forward(legs):
    for leg in legs:
        leg.moveUpper(upperMoveAngle)

def backward(legs):
    for leg in legs:
        leg.moveUpper(-upperMoveAngle)

# BOTH LEGS
def setdefault():
    # for channel in range(0, 16, 2):
    #     servoDriver.set_pwm(channel, 0, 450)
    # for channel in range(1, 16, 2):
    #     servoDriver.set_pwm(channel, 0, 600)
    for leg in [leg1,leg2,leg3,leg4,leg5,leg6]:
        leg.moveLower(0)
        leg.moveUpper(0)

def walkCycle(cycles):
    setdefault()
    time.sleep(5)

    for x in range(cycles):
        liftup([leg1, leg3, leg5])
        forward([leg1, leg3, leg5])
        time.sleep(.1)
        backward([leg2, leg4, leg6])
        # time.sleep(.2)
        setdown([leg1, leg3, leg5])
        time.sleep(.2)

        liftup([leg2, leg4, leg6])
        forward([leg2, leg4, leg6])
        time.sleep(.1)
        backward([leg1, leg3, leg5])
        # time.sleep(.2)
        setdown([leg2, leg4, leg6])
        time.sleep(.2)

    time.sleep(1)
    setdefault()


# MAIN
servoDriver = ServoDriver(busnum=1)
# ledDisplay = LEDDisplay(busnum=2)
# ledDisplay.draw(Faces.a)

def testlooppwm():
    while True:
        t = input("upper width, lower width: ")
        for channel in range(0,16,2):
            servoDriver.set_pwm(channel, 0, t[0])
        for channel in range(1,16,2):
            servoDriver.set_pwm(channel, 0, t[1])

def testloopangles():
    while True:
        t = input("upper angle, lower angle: ")
        # for channel in range(0,16,2):
        #     servoDriver.move(channel, t[0])
        # for channel in range(1,16,2):
        #     servoDriver.move(channel, t[1])
        for leg in [leg1,leg2,leg3,leg4,leg5,leg6]:
            leg.moveUpper(t[0])
            leg.moveLower(t[1])

lowerMoveAngle = 25
upperMoveAngle = 20
leg1 = Leg(1)
leg2 = Leg(2)
leg3 = Leg(3, lowerOffset=-8)
leg4 = Leg(4, lowerOffset=-7)
leg5 = Leg(5, lowerOffset=-5)
leg6 = Leg(6)

try:
    walkCycle(20)
except KeyboardInterrupt:
    setdefault()
    # ledDisplay.shutOff()
    try:
        testlooppwm()
    except KeyboardInterrupt:
        try:
            testloopangles()
        except:
            raise
