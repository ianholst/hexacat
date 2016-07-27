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

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: " + str(len(payload)) + " bytes")
        else:
            print("Text message received: " + payload.decode("utf8"))
        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed for reason: " + str(reason))


class RobotWebSocketServer(object):

    def __init__(self, address, port):
        self.factory = WebSocketServerFactory()
        self.factory.protocol = RobotServerProtocol
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.run_until_complete(self.loop.create_server(self.factory, address, port))

    def start(self):
        try:
            self.loop.run_forever()
        finally:
            self.server.close()
            self.loop.close()
