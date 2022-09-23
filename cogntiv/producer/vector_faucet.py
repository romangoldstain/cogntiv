import threading


class VectorFaucet:

    def __init__(self, vector_factory, bus):
        self.vector_factory = vector_factory
        self.bus = bus
        self.running = False

    def start(self):
        if self.running:
            return
        
        self.running = True
        th = threading.Thread(target=self._streamout, daemon=True, args=())
        th.start()
        return th

    def stop(self):
        self.running = False

    def _streamout(self):
        while self.running:
            vector = self.vector_factory.create()
            self.bus.put(vector)
