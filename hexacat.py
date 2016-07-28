from hardware import LEDDisplay, ServoDriver, Faces, Leg
import threading
import subprocess
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
try:
    import asyncio
except ImportError:
    import trollius as asyncio



class RobotServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: " + request.peer)
        # TODO: flash face

    def onOpen(self):
        print("WebSocket connection open.")
        # TODO: face smile
        ledDisplay.draw(Faces.a)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            handleMessage(payload.decode("utf8"), self)
        # echo back message verbatim
        # self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed for reason: " + str(reason))


# class RobotServerFactory(WebSocketServerFactory):

factory = WebSocketServerFactory()
factory.protocol = RobotServerProtocol
loop = asyncio.get_event_loop()

def startWebSocketServer(address, port):
    global server
    print("Starting WebSocket server...")
    server = loop.run_until_complete(loop.create_server(factory, address, port))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()




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
    for leg in [leg1,leg2,leg3,leg4,leg5,leg6]:
        leg.moveLower(0)
        leg.moveUpper(0)

def walkCycle():
    global HALT
    HALT = False
    setdefault()

    while not HALT:
        liftup([leg1, leg3, leg5])
        forward([leg1, leg3, leg5])
        time.sleep(.1)
        backward([leg2, leg4, leg6])
        time.sleep(.2)
        setdown([leg1, leg3, leg5])
        time.sleep(.2)

        if HALT: break

        liftup([leg2, leg4, leg6])
        forward([leg2, leg4, leg6])
        time.sleep(.1)
        backward([leg1, leg3, leg5])
        time.sleep(.2)
        setdown([leg2, leg4, leg6])
        time.sleep(.2)

        if HALT: break

    setdefault()

def handleMessage(msg, server):
    global HALT
    if msg == "FORWARD":
        walkCycle()

    elif msg == "BACKWARD":
        pass
    elif msg == "ROTATELEFT":
        pass
    elif msg == "ROTATERIGHT":
        pass
    elif msg == "STOP":
        HALT = True

    elif msg.startswith("FACE"):
        faceID = int(msg[5:])

    elif msg == "SHUTDOWN":
        subprocess.call("shutdown now")

    elif msg == "BATTERY":
        batteryOutput = subprocess.check_output("./battery.sh")
        lineIndex = batteryOutput.find("Battery gauge")
        percentage = batteryOutput[lineIndex+len("Battery gauge")+3:]
        server.sendMessage(percentage.encode('utf8'))

# MAIN
try:
    print("Starting hardware...")
    servoDriver = ServoDriver(busnum=1)
    ledDisplay = LEDDisplay(busnum=2)
    ledDisplay.shutOff()

    leg1 = Leg(1, servoDriver)
    leg2 = Leg(2, servoDriver)
    leg3 = Leg(3, servoDriver, lowerOffset=-8)
    leg4 = Leg(4, servoDriver, lowerOffset=-7)
    leg5 = Leg(5, servoDriver, lowerOffset=-5)
    leg6 = Leg(6, servoDriver)

    upperMoveAngle = 20
    lowerMoveAngle = 25

    setdefault()
    HALT = True
    threading.Thread(target=startWebSocketServer, args=("10.0.0.1", 8080)).start()
    print("Ready for input")

except KeyboardInterrupt:
    setdefault()
    ledDisplay.shutOff()
