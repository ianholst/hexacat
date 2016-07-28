from hardware import LEDDisplay, ServoDriver, Faces, Leg
import threading
import subprocess
import time
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
        ledDisplay.draw(Faces.b)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            threading.Thread(target=handleMessage, args=(payload.decode("utf8"), self)).start()
        # echo back message verbatim
        # self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed for reason: " + str(reason))


# class RobotServerFactory(WebSocketServerFactory):

def startWebSocketServer(address, port):
    print("Starting WebSocket server...")
    factory = WebSocketServerFactory()
    factory.protocol = RobotServerProtocol
    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, address, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
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
        print("walk")
        liftup([leg1, leg3, leg5])
        forward([leg1, leg3, leg5])
        time.sleep(.1)
        backward([leg2, leg4, leg6])
        time.sleep(.2)
        setdown([leg1, leg3, leg5])
        time.sleep(.2)
        print("walk1")
        if HALT: break
        print("walk2")
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
    print(msg)
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
        subprocess.call("shutdown now", shell=True)

    elif msg == "BATTERY":
        batteryOutput = subprocess.check_output("./battery.sh", shell=True)
        lineIndex = batteryOutput.find("Battery gauge")
        percentage = batteryOutput[lineIndex+len("Battery gauge")+3:]
        server.sendMessage(("BATTERY:" + percentage).encode('utf8'))

# MAIN


def main():
    global HALTservoDriver, ledDisplay, leg1, leg2, leg3, leg4, leg5, leg6, upperMoveAngle, lowerMoveAngle
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
        # threading.Thread(target=startWebSocketServer, args=("10.0.0.1", 8080)).start()

        print("Ready for input")
        ledDisplay.draw(Faces.a)

    except KeyboardInterrupt:
        setdefault()
        ledDisplay.shutOff()
        raise

threading.Thread(target=main).start()
startWebSocketServer("10.0.0.1", 8080)
