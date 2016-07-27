from websocket import RobotWebSocketServer
from hardware import LEDDisplay, ServoDriver, Faces, Leg, walkCycle

print("Starting WebSocket server...")
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

try:
    print("walking")
    walkCycle(20)
except KeyboardInterrupt:
    setdefault()
    ledDisplay.shutOff()
