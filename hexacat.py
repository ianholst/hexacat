from websocket import RobotWebSocketServer
from hardware import LEDDisplay, ServoDriver, Faces, Leg
import threading

server = RobotWebSocketServer("10.0.0.1", 8080)
threading.Thread(target=server.start()).start()

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

# MAIN
print("Starting hardware...")
servoDriver = ServoDriver(busnum=1)
ledDisplay = LEDDisplay(busnum=2)
ledDisplay.draw(Faces.a)

leg1 = Leg(1)
leg2 = Leg(2)
leg3 = Leg(3, lowerOffset=-8)
leg4 = Leg(4, lowerOffset=-7)
leg5 = Leg(5, lowerOffset=-5)
leg6 = Leg(6)

upperMoveAngle = 20
lowerMoveAngle = 25

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
        time.sleep(.2)
        setdown([leg1, leg3, leg5])
        time.sleep(.2)

        liftup([leg2, leg4, leg6])
        forward([leg2, leg4, leg6])
        time.sleep(.1)
        backward([leg1, leg3, leg5])
        time.sleep(.2)
        setdown([leg2, leg4, leg6])
        time.sleep(.2)

    time.sleep(1)
    setdefault()



try:
    print("walking")
    walkCycle(20)
except KeyboardInterrupt:
    setdefault()
    ledDisplay.shutOff()
